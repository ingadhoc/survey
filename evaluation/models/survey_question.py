##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api


class SurveyQuestion(models.Model):

    _inherit = 'survey.question'

    max_score = fields.Integer(
        compute='_compute_max_score',
        string='Max Score',
        help='Max score an answer of this question can get',
        store=True,
    )

    objective_id = fields.Many2one(
        'survey.question.objective',
        string='Objective',
    )
    level_id = fields.Many2one(
        'survey.question.level',
        string='Level',
    )
    content_id = fields.Many2one(
        'survey.question.content',
        string='Content',
    )

    score_calc_method = fields.Selection(
        [('direct_sum', 'Direct Sum'),
         ('ranges', 'Ranges')],
        string='Score Method',
        help="Choose"
        "-Direct Sum if you want to sum the values "
        " assigned to questions answers."
        "-Ranges if you want to define ranges for correct answers.",
        default='direct_sum',)
    score_ranges_ids = fields.One2many(
        'survey.question.score.range',
        'survey_question_id',
        string='Ranges',
    )
    copy_labels_ids = fields.One2many(
        'survey.label',
        related='labels_ids',
        string='Suggested answers',
        readonly=False,
    )
    is_evaluation = fields.Boolean(
        related='survey_id.is_evaluation',
    )

    @api.depends(
        'score_ranges_ids',
        'score_ranges_ids.score',
        'score_calc_method',
        'copy_labels_ids',
        'copy_labels_ids.score',
        'matrix_subtype',
        'labels_ids_2',
        'labels_ids_2.matrix_answer_score_ids',
        'labels_ids_2.matrix_answer_score_ids.score',
        'type',)
    def _compute_max_score(self):
        # TODO mejorar esto y ver porque se llama
        #  varias veces a esta funcion *hay que cambiarlo tambien
        # en academic_reports que sobreescribimos esta funcion
        max_score = 0
        for question in self:
            if question.type == 'simple_choice':
                scores = [answer.score for answer in question.copy_labels_ids]
                max_score = max(scores if scores else [0])

            elif question.type == 'multiple_choice' and\
                    question.score_calc_method == 'direct_sum':
                max_score = sum(
                    [answer.score for answer in question.copy_labels_ids
                     if answer.score > 0])
            elif question.type == 'multiple_choice' and\
                    question.score_calc_method == 'ranges':
                scores = [score_range.score
                          for score_range in question.score_ranges_ids]
                max_score = max(scores if scores else [0])

            elif question.type == 'numerical_box' and\
                    question.score_calc_method == 'direct_sum':
                max_score = question.validation_max_float_value
            elif question.type == 'numerical_box' and\
                    question.score_calc_method == 'ranges':
                scores = [score_range.score
                          for score_range in question.score_ranges_ids]
                max_score = max(scores if scores else [0])

            elif question.type == 'matrix' and\
                    question.matrix_subtype == 'simple' and \
                    question.score_calc_method == 'direct_sum':
                for matrix_question in question.labels_ids_2:
                    scores = [
                        matrix_score.score
                        for matrix_score in
                        matrix_question.matrix_answer_score_ids]
                    max_score += max(scores if scores else [0])
            elif question.type == 'matrix' and \
                    question.matrix_subtype == 'multiple' and \
                    question.score_calc_method == 'direct_sum':
                for matrix_question in question.labels_ids_2:
                    max_score += sum(
                        [matrix_score.score
                         for matrix_score in
                         matrix_question.matrix_answer_score_ids
                         if matrix_score.score > 0])
            elif question.type == 'matrix' and \
                    question.score_calc_method == 'ranges':
                scores = [score_range.score
                          for score_range in question.score_ranges_ids]
                max_score = max(scores if scores else [0])
            question.max_score = max_score
