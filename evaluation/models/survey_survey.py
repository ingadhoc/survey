##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveySurvey(models.Model):

    _inherit = 'survey.survey'

    time_allocated = fields.Float()
    is_evaluation = fields.Boolean(
        "Is Evaluation?",
    )
    evaluation_type = fields.Selection(
        [('automatically_evaluated', 'Automatically Evaluated'),
         ('manually_evaluated', 'Manually Evaluated')],
        help="-Automattically Evaluated: you have to set"
        " espected question results and the evaluation will be "
        "evaluated automatically.\n"
        "\n-Manually Evaluated: someone will need to correct"
        " the evaluation and complete with the score.",
        default='automatically_evaluated',
    )
    question_objective_ids = fields.One2many(
        'survey.objective',
        'survey_id',
        string='Questions Objectives',
        copy=True,
    )
    question_level_ids = fields.One2many(
        'survey.level',
        'survey_id',
        string='Questions Levels',
        copy=True,
    )
    question_content_ids = fields.One2many(
        'survey.content',
        'survey_id',
        string='Questions Contents',
        copy=True,
    )
    obj_questions_score = fields.Integer(
        compute='_compute_scores',
        string='Objetives Score',
        help='Score for questions with objetive defined',
        multi='_get_scores',
    )
    non_obj_questions_score = fields.Integer(
        compute='_compute_scores',
        string='Other Questions Score',
        help='Score for questions without objetive defined',
        multi='_get_scores',
    )
    content_questions_score = fields.Integer(
        compute='_compute_scores',
        string='Contents Score',
        help='Score for questions with content defined',
        multi='_get_scores',
    )
    non_content_questions_score = fields.Integer(
        compute='_compute_scores',
        string='Other Questions Score',
        help='Score for questions without content defined',
        multi='_get_scores',
    )
    level_questions_score = fields.Integer(
        compute='_compute_scores',
        string='Levels Score',
        help='Score for questions with level defined',
        multi='_get_scores',
    )
    non_level_questions_score = fields.Integer(
        compute='_compute_scores',
        string='Other Questions Score',
        help='Score for questions without level defined',
        multi='_get_scores',
    )
    max_score = fields.Integer(
        compute='_compute_scores',
        help='Maximum score that can be obtained in this evaluation',
        multi='_get_scores',
    )

    # Metodo por si queremos recalcular todos los score

    def compute_score(self):
        total_user_input_ids = self.env['survey.user_input'].search(
            [('survey_id', 'in', self.ids)], order='id')
        total_user_input_ids.compute_score()
        # return total_user_input_ids

    def _compute_scores(self):
        for survey in self:
            content_questions_score = sum(
                [content.score for content in survey.question_content_ids])
            non_content_questions = self.env['survey.question'].search([(
                'survey_id', '=', survey.id), ('content_id', '=', False)])
            non_content_questions_score = sum(
                [question.max_score for question in non_content_questions])

            obj_questions_score = sum([objective.score
                                       for objective in
                                       survey.question_objective_ids])
            non_obj_questions = self.env['survey.question'].search([(
                'survey_id', '=', survey.id), ('objective_id', '=', False)])
            non_obj_questions_score = sum(
                [question.max_score for question in non_obj_questions])

            level_questions_score = sum([level.score
                                         for level in
                                         survey.question_level_ids])
            non_level_questions = self.env['survey.question'].search(
                [('survey_id', '=', survey.id), ('level_id', '=', False)])
            non_level_questions_score = sum(
                [question.max_score for question in non_level_questions])

            max_score = obj_questions_score + non_obj_questions_score
            survey.update({
                'content_questions_score': content_questions_score,
                'non_content_questions_score': non_content_questions_score,
                'obj_questions_score': obj_questions_score,
                'non_obj_questions_score': non_obj_questions_score,
                'non_level_questions_score': non_level_questions_score,
                'level_questions_score': level_questions_score,
                'max_score': max_score,
            })
