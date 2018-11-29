##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveyUserInputQuestionScore(models.Model):
    _name = 'survey.user_input_question_score'
    _description = 'Score of a User Input by Question'
    _rec_name = 'score'

    question_id = fields.Many2one(
        'survey.question',
        'Question',
        ondelete='cascade',
        required=True,
    )
    user_input_id = fields.Many2one(
        'survey.user_input',
        'User Input',
        ondelete='cascade',
        required=True,
        )
    score = fields.Integer(
        required=True,
    )
    score_percentage = fields.Integer(
        'Score %',
        required=True,
    )
