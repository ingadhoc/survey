##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveyQuestionLevel(models.Model):

    _name = 'survey.question.level'
    _description = 'Question Level'

    name = fields.Char(
        required=True,
        translate=True,
    )
