from odoo import models, fields, api 
from odoo.exceptions import ValidationError

class CultivoCultivo(models.Model):
    _name = 'cultivo.cultivo'
    _description = 'Gestión de Cultivos Agrícolas'

    # Relación con el campo
    campo_id = fields.Many2one('cultivo.campo', string="Campo", required=True)
    
    # Información del cultivo
    cultivo_id = fields.Many2one('product.product', string="Tipo de Cultivo", required=True)
    fecha_siembra = fields.Date(string="Fecha de Siembra", required=True)
    fecha_estimada_cosecha = fields.Date(string="Fecha Estimada de Cosecha")
    
    # Estados dinámicos (relación con la tabla de estados configurables)
    stage_id = fields.Many2one('cultivo.cultivo.state', string="Estado del Cultivo", default=lambda self: self.env.ref('palo_gordo_agro.state_nuevo').id, required=True)

    # Rendimientos
    rendimiento_estimado = fields.Float(string="Rendimiento Estimado (ton/ha)")
    rendimiento_real = fields.Float(string="Rendimiento Real (ton/ha)", readonly=True)

    # Historial de cultivos
    historial_ids = fields.One2many('cultivo.historial', 'cultivo_id', string="Historial de Siembras")
    
    @api.constrains('fecha_siembra', 'fecha_estimada_cosecha')
    def _check_fecha_cosecha(self):
        """Asegura que la fecha estimada de cosecha sea posterior a la fecha de siembra."""
        for record in self:
            if record.fecha_estimada_cosecha and record.fecha_siembra > record.fecha_estimada_cosecha:
                raise ValidationError("La fecha estimada de cosecha debe ser posterior a la fecha de siembra.")

    def action_actualizar_estado(self):
        """
        Permite actualizar el estado del cultivo según su progreso.
        Utiliza la secuencia del estado actual para avanzar al siguiente.
        """
        for record in self:
            next_stage = self.env['cultivo.cultivo.state'].search([('sequence', '>', record.stage_id.sequence)], limit=1)
            if next_stage:
                record.stage_id = next_stage
            if record.stage_id.name == 'Cosechado':
                record._calcular_rendimiento_real()

    def _calcular_rendimiento_real(self):
        """
        Cálculo del rendimiento real basado en datos de cosecha.
        Este valor será ingresado manualmente por el usuario.
        """
        for record in self:
            record.rendimiento_real = record.rendimiento_estimado * 0.95  # Ejemplo simple


