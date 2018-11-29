##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveyQuestionContent(models.Model):

    _name = 'survey.question.content'
    _description = 'Question Content'

    name = fields.Char(
        required=True,
        translate=True,
    )
