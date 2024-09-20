from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ConsumoInsumos(models.Model):
    _name = 'agro.consumo_insumos'
    _description = 'Consumo de Insumos Agrícolas en Campos'

    campo_id = fields.Many2one('cultivo.campo', string="Campo", required=True)
    fecha_aplicacion = fields.Date(string="Fecha de Aplicación", default=fields.Date.today)
    line_ids = fields.One2many('consumo.insumos.line', 'consumo_insumos_id', string="Líneas de Insumos")
    total_costo = fields.Float(string="Costo Total", compute='_compute_total_costo')
    
    # Relación con stock.picking
    picking_id = fields.Many2one('stock.picking', string="Picking de Inventario", readonly=True)
    
    # Campo para los estados del registro
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado'),
    ], string="Estado", default='draft', required=True)

    @api.depends('line_ids.total_costo')
    def _compute_total_costo(self):
        for record in self:
            record.total_costo = sum(line.total_costo for line in record.line_ids)

    def action_confirm(self):
        """Confirmar el consumo de insumos y generar un picking de inventario."""
        for record in self:
            if record.state == 'draft':
                if not record.line_ids:
                    raise ValidationError("No se puede confirmar un consumo sin líneas de insumos.")
                
                # Crear picking de inventario
                picking = self.env['stock.picking'].create({
                    'partner_id': False,
                    'location_id': self.env.ref('stock.stock_location_stock').id,
                    'location_dest_id': self.campo_id.location_id.id,
                    'picking_type_id': self.env.ref('stock.picking_type_internal').id,  # Tipo de picking interno
                    'move_type': 'direct',
                    'origin': f"Consumo {record.id}",
                })
                record.picking_id = picking.id

                # Crear los movimientos de inventario basados en las líneas de insumos
                record._crear_movimientos_inventario(picking)
                
                # Cambiar estado a "confirmado"
                record.state = 'confirmed'

    def action_cancel(self):
        """Cancelar el consumo de insumos y el picking asociado."""
        for record in self:
            if record.state == 'confirmed':
                # Cancelar el picking asociado
                if record.picking_id:
                    record.picking_id.action_cancel()
                
                # Cambiar estado a "cancelado"
                record.state = 'cancelled'

    def _crear_movimientos_inventario(self, picking):
        """Crear movimientos de inventario asociados a las líneas de insumos."""
        for line in self.line_ids:
            if not self.campo_id.location_id:
                raise ValidationError("El campo de cultivo seleccionado no tiene una ubicación de inventario asociada.")
            
            self.env['stock.move'].create({
                'name': line.insumo_id.name,
                'product_id': line.insumo_id.id,
                'product_uom_qty': line.cantidad_utilizada,
                'product_uom': line.insumo_id.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,  # Salida del almacén principal
                'location_dest_id': self.campo_id.location_id.id,  # Entrada a la ubicación virtual del campo
                'picking_id': picking.id,  # Asociar el movimiento con el picking
                'state': 'confirmed',
            })._action_confirm()._action_done()

    def action_view_stock_moves(self):
        """Abrir los movimientos de inventario asociados a este consumo de insumos."""
        action = self.env["ir.actions.actions"]._for_xml_id("stock.stock_move_action")
        action['domain'] = [('picking_id', '=', self.picking_id.id)]  # Filtrar por picking_id
        action['context'] = dict(self.env.context, create=False)
        return action


class ConsumoInsumosLine(models.Model):
    _name = 'consumo.insumos.line'
    _description = 'Líneas de Consumo de Insumos'

    insumo_id = fields.Many2one('product.product', string="Insumo", required=True)
    cantidad_utilizada = fields.Float(string="Cantidad Utilizada", required=True)
    costo_unitario = fields.Float(string="Costo Unitario", compute='_compute_costo_unitario', store=True)
    total_costo = fields.Float(string="Costo Total", compute='_compute_total_costo')
    consumo_insumos_id = fields.Many2one('agro.consumo_insumos', string="Consumo de Insumos", required=True)

    @api.depends('insumo_id')
    def _compute_costo_unitario(self):
        for line in self:
            line.costo_unitario = line.insumo_id.standard_price if line.insumo_id else 0.0

    @api.depends('cantidad_utilizada', 'costo_unitario')
    def _compute_total_costo(self):
        for line in self:
            line.total_costo = line.cantidad_utilizada * line.costo_unitario

            




