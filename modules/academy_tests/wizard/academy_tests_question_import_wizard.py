# -*- coding: utf-8 -*-
""" Academy Tests Question Import

This module contains the academy.tests.question.import model
which contains all Import wizzard attributes and behavior.

This model is the a wizard  to import questions from text
"""

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import ValidationError, UserError

from enum import Enum
from collections import Counter
from re import sub as replace, search, MULTILINE, UNICODE, IGNORECASE

from logging import getLogger

_logger = getLogger(__name__)


QUESTION_TEMPLATE = _('''
> Optional comment for question
Optional preamble to the question
![Image title](image name or ID)
1. Question text
a) Answer 1
b) Answer 2
c) Answer 3
x) Right answer
''')

WIZARD_STATES = [
    ('step1', 'Prerequisites'),
    ('step2', 'Content')
]


class Mi(Enum):
    """ Enumerates regex group index un line processing
    """
    ALL = 0
    QUESTION = 1
    ANSWER = 2
    LETTER = 3
    FALSE = 4
    TRUE = 5
    DESCRIPTION = 6
    IMAGE = 7
    TITLE = 8
    URI = 9
    CONTENT = 10


# pylint: disable=locally-disabled, R0903, W0212, E1101
class AcademyTestsQuestionImport(models.TransientModel):
    """ This model is the a wizard  to import questions from text
    """

    _name = 'academy.tests.question.import.wizard'
    _description = u'Academy tests, question import'

    _rec_name = 'id'
    _order = 'id DESC'

    _inherit = ['academy.abstract.owner']

    test_id = fields.Many2one(
        string='Test',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self.default_test_id(),
        help='Choose test to which questions will be append',
        comodel_name='academy.tests.test',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    question_ids = fields.Many2many(
        string='Questions',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Questions has been created',
        comodel_name='academy.tests.question',
        relation='academy_tests_question_import_question_rel',
        column1='question_import_id',
        column2='question_id',
        domain=[],
        context={},
        limit=None
    )

    state = fields.Selection(
        string='State',
        required=False,
        readonly=False,
        index=False,
        default='step1',
        help='Current wizard step',
        selection=WIZARD_STATES
    )

    content = fields.Text(
        string='Content',
        required=True,
        readonly=False,
        index=False,
        default=QUESTION_TEMPLATE,
        help='Text will be processed to create new questions',
        translate=True
    )

    attachment_ids = fields.Many2many(
        string='Attachments',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Attachment has been created',
        comodel_name='ir.attachment',
        relation='academy_tests_question_import_ir_attachment_rel',
        column1='question_import_id',
        column2='attachment_id',
        domain=[
            '|',
            '|',
            ('res_model', '=', 'academy.tests.question'),
            ('res_model', '=', 'academy.tests.question.import.wizard'),
            ('res_model', '=', False)
        ],
        context={
            'search_default_my_documents_filter': 0,
            'search_default_my_own_documents_filter': 1,
            'default_res_model': 'academy.tests.question',
            'default_res_id': 0,
            'default_owner_id': lambda self: self.owner_id.id
        },
        limit=None
    )

    imported_attachment_ids = fields.Many2many(
        string='Imported attachments',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Attachment has been created',
        comodel_name='ir.attachment',
        relation='academy_tests_question_import_imported_ir_attachment_rel',
        column1='question_import_id',
        column2='attachment_id',
        domain=[
            '|',
            '|',
            ('res_model', '=', 'academy.tests.question'),
            ('res_model', '=', 'academy.tests.question.import.wizard'),
            ('res_model', '=', False)
        ],
        context={
            'search_default_my_documents_filter': 0,
            'search_default_my_own_documents_filter': 1,
            'default_res_model': 'academy.tests.question',
            'default_res_id': 0,
            'default_owner_id': lambda self: self.owner_id.id
        },
        limit=None
    )

    topic_id = fields.Many2one(
        string='Topic',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self.default_topic_id(),
        help='Choose topic will be used for new questions',
        comodel_name='academy.tests.topic',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    topic_version_ids = fields.Many2many(
        string='Topic versions',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self.default_topic_version_ids(),
        help='Choose which versions of the topic this question belongs to',
        comodel_name='academy.tests.topic.version',
        relation='academy_tests_question_import_topic_version_rel',
        column1='question_import_id',
        column2='topic_version_id',
        domain=[],
        context={},
        limit=None
    )

    category_ids = fields.Many2many(
        string='Categories',
        required=True,
        readonly=False,
        index=False,
        default=False,
        help='Choose categories will be used for new questions',
        comodel_name='academy.tests.category',
        relation='academy_tests_question_import_category_rel',
        column1='question_import_id',
        column2='category_id',
        domain=[],
        context={},
        limit=None
    )

    type_id = fields.Many2one(
        string='Type',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self.default_type_id(),
        help='Choose type will be used for imported questions',
        comodel_name='academy.tests.question.type',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    level_id = fields.Many2one(
        string='Difficulty',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self.default_level_id(),
        help='Choose level will be used for imported questions',
        comodel_name='academy.tests.level',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    tag_ids = fields.Many2many(
        string='Tags',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Choose tags will be used for imported questions',
        comodel_name='academy.tests.tag',
        relation='academy_tests_question_import_tag_rel',
        column1='question_import_id',
        column2='tag_id',
        domain=[],
        context={},
        limit=None
    )

    autocategorize = fields.Boolean(
        string='Autocategorize',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Check to autoset categories using keywords'
    )

    status = fields.Selection(
        string='Status',
        required=False,
        readonly=False,
        index=False,
        default='ready',
        help='Switch question status',
        selection=[
            ('draft', 'Draft'),
            ('ready', 'Ready')
        ]
    )

    authorship = fields.Boolean(
        string='Authorship',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Check it to indicate that it is your own authorship'
    )

    # ----------------- EVENTS AND AUXILIARY FIELD METHODS --------------------

    def default_test_id(self):
        result_set = self.env['academy.tests.test']

        context = self.env.context or {}
        active_model = context.get('active_model', False)
        active_id = context.get('active_id', False)

        if active_model == 'academy.tests.test' and active_id:
            result_set = self.env[active_model].browse(active_id)

        return result_set

    def default_topic_id(self):
        """ This returns most frecuency used topic id
        """
        return self._most_frecuent('topic_id')

    def default_topic_version_ids(self):
        """ This returns all versions for the chosen topic
        """
        return self.topic_id.last_version()

    def default_type_id(self):
        """ This returns most frecuency used type id
        """
        return self._most_frecuent('type_id')

    def default_level_id(self):
        """ This returns most frecuency used level id
        """
        return self._most_frecuent('level_id')

    @api.onchange('topic_id')
    def _onchange_topid_id(self):
        """ Removes version and categories
        """

        self.topic_version_ids = self.default_topic_version_ids()

    @api.onchange('state')
    def _onchange_state(self):

        # pylint: disable=locally-disabled, E1101
        if self.imported_attachment_ids:
            self._move_imported_attachments()

        if self.state != 'step1' and not (self.topic_id and self.category_ids):
            self.state = 'step1'
            return {
                'warning': {
                    'title': _('Required'),
                    'message': _('Topic and categories are '
                                 'required before continue')
                }
            }

        return False

    # --------------------------- PUBLIC METHODS ------------------------------

    def process_text(self):
        """ Perform job """

        if not (self.topic_id and self.category_ids):
            message = _('Topic and categories are not optional')
            raise ValidationError(message)

        content = self._get_cleared_text()
        groups = self._split_in_line_groups(content)
        value_set = self._build_value_set(groups)

        self._update_attachments()
        self._create_questions(value_set)

        if self.test_id:
            values = {
                'type': 'ir.actions.act_window',
                'res_model': 'academy.tests.test',
                'view_mode': 'form',
                'res_id': self.test_id.id,
                'target': 'main',
                'flags': {
                    'form': {
                        'action_buttons': True, 'options': {'mode': 'edit'}
                    }
                }
            }
        else:
            act_xid = 'academy_tests.action_questions_act_window'
            values = self.env.ref(act_xid).read()[0]
            values['target'] = 'main'

        return values

    # -------------------------------------------------------------------------

    def _update_attachments(self):
        values = {
            'res_model': 'academy.tests.question',
            'res_id': 0,
            'owner_id': self.owner_id.id
        }
        self.attachment_ids.write(values)

    def _get_cleared_text(self):
        """ Perform some operations to obtain a cleared text
            - Replace tabs with spaces en removes extra spaces
            - Replace extra simbols after lists elements
        """
        content = (self.content or '').strip()
        flags = MULTILINE | UNICODE

        # STEP 1: Remove tabs and extra spaces
        content = replace(r'[ \t]+', r' ', content, flags=flags)

        # STEP 2: Remove spaces from both line bounds
        content = replace(r'[ \t]+$', r'', content, flags=flags)
        content = replace(r'^[ \t]+', r'', content, flags=flags)

        # STEP 3: Replace CRLF by LF and remove duplicates
        content = replace(r'[\r\n]', r'\n', content, flags=flags)
        content = replace(r'[\n]{2,}', r'\n\n', content, flags=flags)

        # STEP 2: Update questions and answers numbering formats
        pattern = r'^([0-9]{1,10})[.\-)]+[ \t]+'
        content = replace(pattern, r'\1. ', content, flags=flags)
        pattern = r'^([a-zñA-ZÑ])[.\-)]+[ \t]+'
        content = replace(pattern, r'\1) ', content, flags=flags)

        return content

    @staticmethod
    def _split_in_line_groups(content):
        """ Splits content into lines and then splits these lines into
        groups using empty lines as a delimiter.

        """

        lines = content.splitlines(False)
        groups = []

        group = []
        numlines = len(lines)
        for index in range(0, numlines):
            if lines[index] == '':
                groups.append(group)
                group = []
            elif index == (numlines - 1):
                group.append(lines[index])
                groups.append(group)
            else:
                group.append(lines[index])

        return groups

    @staticmethod
    def _append_line(_in_buffer, line):
        """ Appends new line using previous line break when buffer is not empty
        """
        if _in_buffer:
            _in_buffer = _in_buffer + '\n' + line
        else:
            _in_buffer = line

        return _in_buffer

    @staticmethod
    def safe_cast(val, to_type, default=None):
        """ Performs a safe cast between `val` type to `to_type`
        """

        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default

    def _can_current_user_change_the_owner(self):
        """ If current user is allowed to access to the owner_id field then
        field should be returned by `fields_get` method
        """

        # Check field access in the current wizard
        bret = self.fields_get().get('owner_id', False)

        if bret:
            # Check field access in question model
            question_model = self.env['academy.tests.question']
            bret = question_model.fields_get().get('owner_id', False)

        return bret

    def _process_line_group(self, line_group):
        """ Gets description, image, preamble, statement, and answers
        from a given group of lines
        """

        sequence = 0
        regex = r'((^[0-9]+\. )|(((^[a-wy-z])|(^x))\) )|(^> )|(^\!\[([^]]+)\]\(([^)]+)))?(.+)'  # noqa: E501
        flags = UNICODE | IGNORECASE

        # pylint: disable=locally-disabled, E1101
        catops = [(4, ID, None) for ID in self.category_ids.mapped('id')]
        tagops = [(4, ID, None) for ID in self.tag_ids.mapped('id')]
        verops = [(4, ID, None) for ID in self.topic_version_ids.mapped('id')]

        values = {
            'description': '',
            'preamble': '',
            'name': None,
            'answer_ids': [],
            'ir_attachment_ids': [],
            'topic_id': self.topic_id.id,
            'topic_version_ids': verops,
            'category_ids': catops,
            'type_id': self.type_id.id,
            'tag_ids': tagops,
            'level_id': self.level_id.id
        }

        if self._can_current_user_change_the_owner():
            values['owner_id'] = self.owner_id.id

        for line in line_group:
            found = search(regex, line, flags)
            if found:
                groups = found.groups()

                if groups[Mi.QUESTION.value]:
                    values['name'] = groups[Mi.CONTENT.value]

                elif groups[Mi.ANSWER.value]:
                    sequence = sequence + 1
                    ansvalues = {
                        'name': groups[Mi.CONTENT.value],
                        'is_correct': (groups[Mi.TRUE.value] is not None),
                        'sequence': sequence
                    }
                    values['answer_ids'].append((0, None, ansvalues))

                elif groups[Mi.DESCRIPTION.value]:
                    values['description'] = self._append_line(
                        values['description'], groups[Mi.CONTENT.value])

                elif groups[Mi.IMAGE.value]:
                    ID = self._process_attachment_groups(groups)
                    if ID:
                        self._set_attachment_title(groups, ID)
                        values['ir_attachment_ids'].append((4, ID, None))

                else:
                    values['preamble'] = self._append_line(
                        values['preamble'], groups[Mi.CONTENT.value])

        return values

    def _set_attachment_title(self, groups, ID):
        """ Reads title from markdown line ![title](uri) and set it to the
        attachement with the given ID in related recordset
        """

        attach_record = self.attachment_ids.filtered(
            lambda rec: rec.id == ID)
        attach_record.name = groups[Mi.TITLE.value]

        return attach_record

    def _process_attachment_groups(self, groups):
        uri = groups[Mi.URI.value]
        title = groups[Mi.TITLE.value]
        record = self.env['ir.attachment']

        # STEP 1: Try to find attachment by `id` field
        numericURI = self.safe_cast(uri, int, 0)
        if numericURI:
            record = self.attachment_ids.filtered(
                lambda item: item.id == numericURI)

        # STEP 2: Try to find attachment by `name` field, with (`uri`) or
        # without `title` extension
        if not record:
            uri = groups[Mi.URI.value]

            record = self.attachment_ids.filtered(
                lambda item: self._equal(item.name, uri) or self._equal(item.name, title)) # noqa: 501

        # STEP 3: Raise error if number of found items is not equal to one
        if not record:
            message = _('Invalid attachment URI: ![%s](%s)')
            raise ValidationError(message % (title, uri))
        elif len(record) > 1:
            message = _('Duplicate attachment URI: %s')
            raise ValidationError(message % (title, uri))

        # STEP 4: Return ID
        return record.id

    @staticmethod
    def _equal(str1, str2):
        str1 = (str1 or '').lower()
        str2 = (str2 or '').lower()

        return str1 == str2

    def _build_value_set(self, groups):
        value_set = []
        for group in groups:
            values = self._process_line_group(group)
            value_set.append(values)

        return value_set

    def _create_questions(self, value_set):
        question_obj = self.env['academy.tests.question']
        sequence = 0

        # pylint: disable=locally-disabled, W0703
        try:
            for values in value_set:

                if self.autocategorize:
                    name = values['name']
                    # matches => {topic_id: [categorory_id1, ...]}
                    matches = self.topic_id.search_for_categories(name)
                    ids = matches.get(self.topic_id.id, False)
                    if ids:
                        values['category_ids'] = [(6, False, ids)]

                question_set = question_obj.create(values)

                if self.test_id:
                    sequence = sequence + 1
                    tvalues = {
                        'question_ids': [(0, None, {
                            'test_id': self.test_id.id,
                            'question_id': question_set.id,
                            'sequence': sequence,
                            'authorship': self.authorship
                        })]
                    }
                    self.test_id.write(tvalues)

        except Exception as ex:
            message = _('Some questions could not be created, system says: %s')
            raise UserError(message % ex)

        return False

    def _move_imported_attachments(self):
        """ Appends imported files to list of available attachments and
        removes from list of imported
        """

        _ids = self.imported_attachment_ids.mapped('id')
        self.attachment_ids = [(4, _id, None) for _id in _ids]
        self.imported_attachment_ids = [(5, None, None)]

    def _most_frecuent(self, fname, domain=None):

        uid = self.env.context['uid']
        mode = False
        domain = domain or []

        domain.append(('owner_id', '=', uid))
        order = 'create_date DESC'
        question_obj = self.env['academy.tests.question']
        question_set = question_obj.search(domain, limit=100, order=order)

        if question_set:
            ids = []
            for question_item in question_set:
                target = getattr(question_item, fname)
                ids.extend(target.mapped('id'))

            result = Counter(ids).most_common(1)
            if result:
                mode = result[0][0]

        return mode
