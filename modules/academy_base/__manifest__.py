# -*- coding: utf-8 -*-
{
    'name': "Academy Base",

    'summary': """
        Common information and behavior used by the academy modules""",

    'description': """
        Common information and behavior used by the academy modules
    """,

    'author': "Jorge Soto Garcia",
    'website': "https://github.com/sotogarcia",

    'category': 'Academy',
    'version': '13.0.1.0.0',

    'depends': [
        'base',
        'mail'
    ],

    'data': [
        'data/mail_message_subtype_data.xml',
        'data/res_groups_data.xml',
        'data/ir_sequence_data.xml',
        'data/academy_training_methodology_data.xml',
        'data/academy_training_modality_data.xml',
        'data/academy_application_scope_data.xml',
        'data/academy_knowledge_area_data.xml',
        'data/academy_qualification_level_data.xml',
        'data/academy_professional_family_data.xml',
        'data/academy_training_resource_kind_data.xml',
        'data/academy_professional_field_data.xml',
        'data/academy_professional_sector_data.xml',

        'views/academy_base.xml',

        'views/academy_training_methodology_view.xml',
        'views/academy_application_scope_view.xml',
        'views/academy_knowledge_area_view.xml',
        'views/academy_professional_area_view.xml',
        'views/academy_training_modality_view.xml',
        'views/academy_qualification_level_view.xml',
        'views/academy_professional_category_view.xml',
        'views/academy_professional_family_view.xml',
        'views/academy_professional_qualification_view.xml',
        'views/academy_professional_field_view.xml',
        'views/academy_professional_sector_view.xml',

        'views/academy_training_module_view.xml',
        'views/academy_competency_unit_view.xml',
        'views/academy_training_activity_view.xml',
        'views/academy_training_action_view.xml',

        'views/academy_student_view.xml',
        'views/academy_training_action_enrolment_view.xml',
        'views/academy_training_lesson_view.xml',

        'views/academy_teacher_view.xml',

        'report/academy_base_report_assets.xml',
        'report/academy_training_activity_details_report.xml',

        'views/academy_training_resource_view.xml',
        'views/academy_training_resource_kind_view.xml',

        'wizard/academy_training_session_wizard_view.xml',
        'wizard/academy_training_session_wizard_line_view.xml',

        'security/academy_base.xml',

        'security/academy_training_methodology.xml',
        'security/academy_application_scope.xml',
        'security/academy_knowledge_area.xml',
        'security/academy_professional_area.xml',
        'security/academy_training_modality.xml',
        'security/academy_competency_unit.xml',
        'security/academy_qualification_level.xml',
        'security/academy_professional_category.xml',
        'security/academy_professional_family.xml',
        'security/academy_professional_qualification.xml',
        'security/academy_training_module_tree_readonly.xml',
        'security/academy_professional_field.xml',
        'security/academy_professional_sector.xml',

        'security/academy_training_module.xml',
        'security/academy_training_activity.xml',
        'security/academy_training_action.xml',

        'security/academy_training_action_enrolment.xml',
        'security/academy_training_lesson.xml',

        'security/academy_teacher.xml',
        'security/academy_student.xml',
        'security/academy_training_resource.xml',
        'security/academy_training_resource_file.xml',
        'security/academy_training_resource_kind.xml',

        'security/res_users.xml',
    ],

    'qweb': [

    ],

    'demo': [
        'demo/academy_student_demo.xml',
        'demo/res_partner.xml',
        'demo/res_users.xml',
        'demo/academy_teacher_demo.xml',

        'demo/academy_professional_area.xml',
        'demo/academy_professional_category.xml',
        'demo/academy_professional_qualification.xml',

        'demo/academy_training_module.xml',
        'demo/academy_training_activity.xml',
        'demo/academy_competency_unit.xml',

        'demo/academy_training_action.xml',

        'demo/ir_atachment.xml',
        'demo/academy_training_resource.xml',
        'demo/academy_training_action_enrolment_demo.xml',
        'demo/academy_training_lesson_demo.xml',
    ],

    'js': [
    ],

    'css': [
        'static/src/css/academy_base_view.css',
        'static/src/css/academy_training_activity_details_report.css',
    ],

    "external_dependencies": {
        "python": []
    },

    'license': 'AGPL-3'
}
