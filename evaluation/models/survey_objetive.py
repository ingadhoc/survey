##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api


class SurveyObjective(models.Model):

    _name = 'survey.objective'
    _description = 'Survey Objective'

    objective_id = fields.Many2one(
        'survey.question.objective',
        string="Objective",
        required=True,
        translate=True,
    )
    score = fields.Integer(
        compute='_compute_score',
        string='Score',
        readonly=True,
    )
    survey_id = fields.Many2one(
        'survey.survey',
        string='Survey',
        required=True,
        ondelete='cascade',
    )
    question_ids = fields.One2many(
        'survey.question',
        compute='_compute_question_ids',
        string='Questions',
    )

    def _compute_score(self):
        for rec in self:
            rec.score = sum(
                [question.max_score for question in rec.question_ids])

    @api.depends('survey_id.page_ids.question_ids.objective_id')
    def _compute_question_ids(self):
        SurveyQuestion = self.env['survey.question']
        for rec in self:
            rec.question_ids = SurveyQuestion.search(
                [('page_id.survey_id', '=', rec.survey_id.id),
                 ('objective_id', '=', rec.objective_id.id)])

    def name_get(self):
        # always return the full hierarchical name
        res = []
        for rec in self:
            name = rec.objective_id.name
            res.append((rec.id, name))
        return res
