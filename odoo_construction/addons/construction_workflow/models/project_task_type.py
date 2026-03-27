from odoo import models


class ProjectTaskType(models.Model):
    """Override project.task.type to add a construction-context form view
    that hides the SMS template field injected by project_sms."""
    _inherit = 'project.task.type'
