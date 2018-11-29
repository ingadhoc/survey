##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveyLabel(models.Model):

    _inherit = 'survey.label'

    score = fields.Integer(
        default=0,
    )
    matrix_answer_score_ids = fields.One2many(
        'survey.matrix_answer_score',
        'question_id',
        'Matrix Answer Score',
    )
