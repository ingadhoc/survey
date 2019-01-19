##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api


class SurveyContent(models.Model):

    _name = 'survey.content'
    _description = 'Survey Content'

    content_id = fields.Many2one(
        'survey.question.content',
        string="Content",
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
        string='Questions'
    )

    def name_get(self):
        # always return the full hierarchical name
        res = self._complete_name(
            'complete_name')
        return res.items()

    def _complete_name(self, name):
        """ Forms complete name of location from parent location to child location.
        @return: Dictionary of values
        """
        for line in self:
            name = line.content_id.name
            line.name = name

    @api.multi
    def _compute_score(self):
        for rec in self:
            rec.score = sum(
                [question.max_score for question in rec.question_ids])

    @api.depends('survey_id.page_ids.question_ids.content_id')
    def _compute_question_ids(self):
        for rec in self:
            rec.question_ids = rec.env['survey.question'].search(
                [('page_id.survey_id', '=', rec.survey_id.id),
                ('content_id', '=', rec.content_id.id)])
