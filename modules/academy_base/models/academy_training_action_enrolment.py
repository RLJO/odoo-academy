# -*- coding: utf-8 -*-
""" AcademyTrainingAction

This module contains the academy.action.enrolment Odoo model which stores
all training action attributes and behavior.

"""

from logging import getLogger

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.exceptions import ValidationError


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)


# pylint: disable=locally-disabled, R0903
class AcademyTrainingActionEnrolment(models.Model):
    """ This model stores attributes and behavior relative to the
    enrollment of students in academy training actions
    """

    _name = 'academy.training.action.enrolment'
    _description = u'Academy action enrolment'

    _rec_name = 'code'
    _order = 'code ASC'

    _inherits = {
        'res.partner': 'res_partner_id',
        'academy.training.action': 'training_action_id'
    }

    _inherit = ['mail.thread']


    # pylint: disable=locally-disabled, W0212
    code = fields.Char(
        string='Code',
        required=True,
        readonly=True,
        index=True,
        default=lambda self: self._default_code(),
        help='Enter new code',
        size=12,
        translate=True,
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Enter new description',
        translate=True
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Enables/disables the record'
    )

    res_partner_id = fields.Many2one(
        string='Student',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Choose enroled student',
        comodel_name='res.partner',
        domain=[('is_student', '=', True)],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    training_action_id = fields.Many2one(
        string='Training action',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Choose training action in which the student will be enroled',
        comodel_name='academy.training.action',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    # pylint: disable=locally-disabled, W0212
    training_module_ids = fields.Many2many(
        string='Training modules',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose modules in which the student will be enroled',
        comodel_name='academy.training.module',
        relation='academy_action_enrolment_training_module_rel',
        column1='action_enrolment_id',
        column2='training_module_id',
        domain=[],
        context={},
        limit=None
    )

    # pylint: disable=locally-disabled, W0108
    register = fields.Date(
        string='Sign up',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: fields.Date.context_today(self),
        help='Date in which student has been enroled'
    )

    deregister = fields.Date(
        string='Deregister',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Data in which student has been unsubscribed'
    )

    student_name = fields.Char(
        string='Student name',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Show the name of the related student',
        size=50,
        translate=True,
        compute=lambda self: self._compute_student_name()
    )

    @api.multi
    @api.depends('res_partner_id')
    def _compute_student_name(self):
        for record in self:
            record.student_name = record.res_partner_id.name


    # ---------------------------- ONCHANGE EVENTS ----------------------------

    @api.multi
    @api.onchange('training_action_id')
    def _onchange_training_action_id(self):
        action_set = self.training_action_id
        activity_set = action_set.mapped('training_activity_id')
        competency_set = activity_set.mapped('competency_unit_ids')
        module_set = competency_set.mapped('training_module_id')
        ids = module_set.ids

        self.training_module_ids = module_set

        if module_set:
            domain = {'training_module_ids':  [('id', 'in', ids)]}
            return {'domain': domain}

        return {'domain': {'training_module_ids':  [('id', '=', -1)]}}


    # -------------------------- OVERLOADED METHODS ---------------------------

    @api.one
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        """ Prevents new record of the inherited (_inherits) models will
        be created. It also adds the following sequence value.
        """

        default = dict(default or {})
        default.update({
            'res_partner_id': self.res_partner_id.id,
            'training_action_id': self.training_action_id.id,
            'code': self._default_code()
        })

        rec = super(AcademyTrainingActionEnrolment, self).copy(default)
        return rec


    # -------------------------- PYTHON CONSTRAINTS ---------------------------

    @api.one
    @api.constrains('training_action_id', 'res_partner_id')
    def _check_unique_enrolment(self):

        action_id = self.training_action_id.id or -1
        partner_id = self.res_partner_id.id or -1

        domain = [
            ('training_action_id', '=', action_id),
            ('res_partner_id', '=', partner_id),
            ('deregister', '=', False),
            ('id', '<>', self.id)
        ]
        enroled_set = self.search(domain)

        if enroled_set:
            msg = '{student} already has been enrolled in {action}'
            msg = msg.format(
                student=self.res_partner_id.name,
                action=self.training_action_id.action_name
            )
            raise ValidationError(msg)


    # -------------------------- AUXILIARY METHODS ----------------------------

    @api.model
    def _default_code(self):
        """ Get next value for sequence
        """

        seqxid = 'academy_base.ir_sequence_academy_action_enrolment'
        seqobj = self.env.ref(seqxid)

        result = seqobj.next_by_id()

        return result





