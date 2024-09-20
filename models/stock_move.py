from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    # Campo Many2one que relaciona los movimientos con el consumo de insumos
    consumo_insumos_id = fields.Many2one(
        'agro.consumo_insumos', 
        string="Consumo de Insumos", 
        ondelete='cascade',  # Se elimina el movimiento si se elimina el consumo de insumos
        index=True  # Añadir un índice para mejorar el rendimiento
    )