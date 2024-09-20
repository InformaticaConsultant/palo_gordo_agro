from odoo import models, fields

class CultivoState(models.Model):
    _name = 'cultivo.state'
    _description = 'Etapas Personalizadas de Cultivos'
    _order = 'sequence'

    name = fields.Char(string="Estado", required=True)
    description = fields.Text(string="Descripción")
    sequence = fields.Integer(string="Secuencia", default=10)  # Controla el orden de las etapas
