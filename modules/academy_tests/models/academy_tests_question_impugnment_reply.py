# -*- coding: utf-8 -*-
""" AcademyTestsQuestionImpugnmentReply

This module contains the academy.tests.question.impugnment.reply Odoo model
which stores all teacher replies for student impugnments, as well as their
attributes and behavior.
"""

from logging import getLogger

from odoo import models, fields

_logger = getLogger(__name__)


class AcademyTestsQuestionImpugnmentReply(models.Model):
    """ Reply to an existin question impugnment
    """

    _name = 'academy.tests.question.impugnment.reply'
    _description = u'Academy tests question impugnment reply'

    _rec_name = 'id'
    _order = 'write_date DESC, create_date DESC'

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Long impugnment description',
        translate=True
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help=('If the active field is set to false, it will allow you to '
              'hide record without removing it')
    )

    impugnment_id = fields.Many2one(
        string='Impugnment',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Choose related impugnment',
        comodel_name='academy.tests.question.impugnment',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    student_id = fields.Many2one(
        string='Student',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose student who impugn this question',
        comodel_name='academy.student',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )
