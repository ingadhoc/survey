##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveyMatrixAnswerScore(models.Model):
    _name = 'survey.matrix_answer_score'
    _description = 'Matrix Answer Score'
    _rec_name = 'score'

    score = fields.Integer(
        required=True,
    )
    question_id = fields.Many2one(
        'survey.label',
        'Question',
    )
    answer_id = fields.Many2one(
        'survey.label',
        'Answer',
        required=True,
    )
