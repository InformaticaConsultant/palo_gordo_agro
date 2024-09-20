from odoo import models, fields

class CultivoState(models.Model):
    _name = 'cultivo.cultivo.state'
    _description = 'Estados Personalizados de Cultivos'

    name = fields.Char(string="Estado", required=True)
    description = fields.Text(string="Descripción")
    sequence = fields.Integer(string="Secuencia", default=1)

