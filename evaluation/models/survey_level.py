##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api


class SurveyLevel(models.Model):

    _name = 'survey.level'
    _description = 'Survey Level'

    level_id = fields.Many2one(
        'survey.question.level',
        string="Level",
        required=True,
        translate=True,
    )
    score = fields.Integer(
        compute='_compute_score',
        readonly=True,
    )
    survey_id = fields.Many2one(
        'survey.survey',
        string='Survey',
        required=True,
    )
    question_ids = fields.One2many(
        'survey.question',
        compute='_compute_question_ids',
        string='Questions',
    )

    @api.multi
    def _compute_score(self):
        for rec in self:
            rec.score = sum(
                [question.max_score for question in rec.question_ids])

    def name_get(self):
        # always return the full hierarchical name
        res = []
        for rec in self:
            name = rec.level_id.name
            res.append((rec.id, name))
        return res

    @api.depends('survey_id.page_ids.question_ids.level_id')
    def _compute_question_ids(self):
        for rec in self:
            rec.question_ids = rec.env['survey.question'].search(
                [('page_id.survey_id', '=', rec.survey_id.id),
                ('level_id', '=', rec.level_id.id)])
