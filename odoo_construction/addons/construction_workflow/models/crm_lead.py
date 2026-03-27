from odoo import models, fields, api
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    site_visit_date = fields.Date(string='Site Visit Scheduled Date')
    site_photos = fields.Many2many('ir.attachment', 'crm_lead_site_photos_rel', 'lead_id', 'attachment_id', string='Site Photos')
    is_quotation_submitted = fields.Boolean(compute='_compute_is_quotation_submitted')

    @api.depends('stage_id')
    def _compute_is_quotation_submitted(self):
        for lead in self:
            lead.is_quotation_submitted = (lead.stage_id.name == 'Quotation Submitted')

    def write(self, vals):
        stage_id = vals.get('stage_id')
        for lead in self:
            new_stage_id = stage_id or lead.stage_id.id
            if new_stage_id:
                stage = self.env['crm.stage'].browse(new_stage_id)
                if stage.name == 'Site Visit Scheduled':
                    new_date = vals.get('site_visit_date') or lead.site_visit_date
                    if not new_date:
                        raise UserError("Please enter date")

        res = super(CrmLead, self).write(vals)
        if 'stage_id' in vals:
            for lead in self:
                if lead.stage_id.is_won:
                    # Check if a project already exists with the same name to prevent duplicates
                    existing_project = self.env['project.project'].search([('name', '=', lead.name)], limit=1)
                    if not existing_project:
                        new_project = self.env['project.project'].create({
                            'name': lead.name,
                            'partner_id': lead.partner_id.id,
                        })
                        
                        # Add specific construction phases to the new project
                        phases = ['Design Phase', 'Approval Phase', 'Construction Phase', 'Finishing Phase']
                        for seq, phase_name in enumerate(phases, start=1):
                            stage = self.env['project.task.type'].search([('name', '=', phase_name)], limit=1)
                            if not stage:
                                stage = self.env['project.task.type'].create({
                                    'name': phase_name,
                                    'sequence': seq * 10,
                                })
                            # Link the stage to the newly created project
                            stage.write({'project_ids': [(4, new_project.id)]})
        return res
