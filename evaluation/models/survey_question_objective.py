##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveyQuestionObjective(models.Model):

    _name = 'survey.question.objective'
    _description = 'Question Objective'

    name = fields.Char(
        required=True,
        translate=True,
    )
