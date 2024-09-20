from odoo import models, fields

class CultivoHistorial(models.Model):
    _name = 'cultivo.historial'
    _description = 'Historial de Siembras en Campos'

    cultivo_id = fields.Many2one('cultivo.cultivo', string="Cultivo", required=True)
    campo_id = fields.Many2one('cultivo.campo', string="Campo", related='cultivo_id.campo_id', readonly=True)
    fecha_siembra = fields.Date(string="Fecha de Siembra", related='cultivo_id.fecha_siembra', readonly=True)
    fecha_cosecha = fields.Date(string="Fecha de Cosecha", related='cultivo_id.fecha_estimada_cosecha', readonly=True)
    rendimiento_real = fields.Float(string="Rendimiento Real (ton/ha)", related='cultivo_id.rendimiento_real', readonly=True)
