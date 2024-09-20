from odoo import models, fields

class CultivoCultivoState(models.Model):
    _name = 'cultivo.cultivo.state'
    _description = 'Estados de Cultivos'

    name = fields.Char(string="Estado", required=True)
    description = fields.Text(string="Descripción")

