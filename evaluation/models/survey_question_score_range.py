##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveyQuestionScoreRange(models.Model):
    _name = 'survey.question.score.range'
    _description = 'Survey Question Score Range'

    survey_from = fields.Integer(
        'From (included)',
        oldname='from',
        required=True,
    )
    to = fields.Integer(
        'To (included)',
        required=True,
    )
    score = fields.Integer(
        'Score',
        required=True,
    )
    survey_question_id = fields.Many2one(
        'survey.question',
        'Question',
    )
