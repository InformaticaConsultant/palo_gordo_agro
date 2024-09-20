from odoo import models, fields, api

class CampoCultivo(models.Model):
    _name = 'cultivo.campo'
    _description = 'Campos de Cultivo de Caña de Azúcar'

    name = fields.Char(string="Nombre del Campo", required=True)
    area = fields.Float(string="Área en Hectáreas", required=True)
    tipo_suelo = fields.Selection([('arcilloso', 'Arcilloso'), ('arenoso', 'Arenoso')], string="Tipo de Suelo")
    localizacion = fields.Char(string="Localización")
    rendimiento_historico = fields.Float(string="Rendimiento Histórico (ton/ha)")
    fecha_ultima_siembra = fields.Date(string="Fecha de Última Siembra")
    estado_cultivo = fields.Selection([('preparado', 'Preparado'), ('sembrado', 'Sembrado'), ('cosechado', 'Cosechado')], string="Estado Actual")

    # Campo para asociar la ubicación virtual del inventario al campo
    location_id = fields.Many2one('stock.location', string="Ubicación de Inventario")

    @api.model
    def create(self, vals):
        # Crear el campo de cultivo y luego crear la ubicación virtual
        campo = super(CampoCultivo, self).create(vals)
        campo._crear_ubicacion_virtual()  # Crea la ubicación automáticamente
        return campo

    def _crear_ubicacion_virtual(self):
        # Si la ubicación ya existe, no la creamos de nuevo
        if not self.location_id:
            location = self.env['stock.location'].create({
                'name': f"Campo {self.name}",
                'location_id': self.env.ref('stock.stock_location_locations').id,  # Ubicación padre (general)
                'usage': 'production',  # Tipo de ubicación
            })
            self.location_id = location  # Asignamos la ubicación al campo de cultivo
            self.write({'location_id': location.id})  # Guardamos la ubicación creada
