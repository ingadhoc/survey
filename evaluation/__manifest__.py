##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Academic Evaluations',
    'version': '11.0.1.2.0',
    'author': 'ADHOC SA',
    'category': 'base.module_category_knowledge_management',
    'license': 'AGPL-3',
    'depends': [
            'survey',
    ],
    'data': [
        'views/survey_survey_views.xml',
        'views/survey_content_views.xml',
        'views/survey_level_views.xml',
        'views/survey_matrix_answer_score_views.xml',
        'views/survey_objective_views.xml',
        'views/survey_page_views.xml',
        'views/survey_user_input_views.xml',
        'views/survey_user_input_question_scrore_views.xml',
        'views/survey_question_views.xml',
        'views/survey_question_score_range_views.xml',
        'security/ir.model.access.csv',
        'security/evaluation_security.xml',
    ],
    'website': 'www.adhoc.com.ar',
    'installable': True,
}
