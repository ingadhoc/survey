##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api


class SurveyUserInput(models.Model):

    _inherit = 'survey.user_input'

    # TODO: ver si usamos la funcion get_score, el tema es
    #  que hay que poner store=true para poder
    #  usarlo en la vista, habria que ver cuando hay que actualizar los
    # valores
    # 'score': fields.function(_get_score,'Score'),
    score = fields.Integer('Score')
    input_question_score_ids = fields.One2many(
        'survey.user_input_question_score',
        'user_input_id',
        string='Question Scores',
        readonly=True,
    )
    evaluation_type = fields.Selection(
        related='survey_id.evaluation_type',
        readonly=True,
    )

    def compute_score(self):
        question_obj = self.env['survey.question']
        user_input_lines_obj = self.env['survey.user_input_line']
        uiqs_obj = self.env['survey.user_input_question_score']
        for user_input in self:
            computed_score = 0
            questions = question_obj.search(
                [('survey_id', '=', user_input.survey_id.id),
                 ('max_score', '!=', 0)])
            for question in questions:
                user_input_lines = user_input_lines_obj.search(
                    [('question_id', '=', question.id),
                     ('user_input_id', '=', user_input.id)])
                if question.type == 'simple_choice' or question\
                        .score_calc_method == 'direct_sum':
                    question_score = sum(
                        [self.get_answer_score(user_input_line)
                         for user_input_line in user_input_lines])
                elif question.score_calc_method == 'ranges':
                    pre_score = sum(
                        [self.get_answer_score(user_input_line)
                         for user_input_line in user_input_lines])
                    question_score = self.get_ranged_score(
                        question, pre_score)

                computed_score += question_score

                uiqs_ids = uiqs_obj.search(
                    [('question_id', '=', question.id),
                     ('user_input_id', '=', user_input.id)], limit=1)

                # Calculte score_percentage
                score_percentage = question_score * 100.0 / question\
                    .max_score

                if uiqs_ids:
                    uiqs_ids.write(
                        {'score': question_score,
                         'score_percentage': score_percentage})
                else:
                    uiqs_obj.create({
                        'score': question_score,
                        'score_percentage': score_percentage,
                        'question_id': question.id,
                        'user_input_id': user_input.id,
                    })
            if user_input.survey_id.max_score\
                    and user_input.survey_id.max_score != 0:
                computed_score = computed_score * 100.0 / user_input\
                    .survey_id.max_score
            else:
                computed_score = False
            user_input.write({'score': computed_score})
        return True

    # TODO: desde la pregunta, buscar el rango de acuerdo al pre_score
    #  y retornar el score asociado. Sino retornar 0
    def get_ranged_score(self, question, pre_score, context=None):
        question_score_range_obj = self.env.get('survey.question.score.range')
        question_score_range = question_score_range_obj.search(
            [('from', '<=', pre_score),
             ('to', '>=', pre_score),
             ('survey_question_id', '=', question.id)], limit=1)
        if not question_score_range:
            return 0
        else:
            return question_score_range.score

    def get_answer_score(self, user_input_line):
        if user_input_line.question_id.type in [
            'simple_choice', 'multiple_choice'] and\
                user_input_line.value_suggested:
            return user_input_line.value_suggested.score
        elif user_input_line.question_id.type == 'numerical_box':
            return int(user_input_line.value_number)
        elif user_input_line.question_id.type == 'matrix' and\
                user_input_line.value_suggested:
            for given_answer_score in user_input_line.value_suggested_row\
                    .matrix_answer_score_ids:
                if user_input_line.value_suggested.id == given_answer_score\
                        .answer_id.id:
                    return given_answer_score.score
        return 0

    @api.multi
    def write(self, vals):
        write_res = super(SurveyUserInput, self).write(vals)
        # If score in context then score is being writed
        if vals.get('state') == 'done' and 'score' not in vals:
            self.compute_score()
        return write_res
