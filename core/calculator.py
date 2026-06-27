from .models import Insumo, APU
from typing import List

def crear_insumo(tipo, codigo, descripcion, unidad, cantidad, precio_unitario, desperdicio=0.0) -> Insumo:
    return Insumo(tipo=tipo, codigo=codigo, descripcion=descripcion,
                  unidad=unidad, cantidad=cantidad, precio_unitario=precio_unitario,
                  desperdicio=desperdicio)

def crear_apu(codigo, descripcion, unidad, insumos: List[Insumo],
              gastos_generales_pct=0.10, utilidad_pct=0.10,
              impuesto_it_pct=0.03, impuesto_iva_pct=0.0) -> APU:
    return APU(codigo=codigo, descripcion=descripcion, unidad=unidad,
               insumos=insumos, gastos_generales_pct=gastos_generales_pct,
               utilidad_pct=utilidad_pct, impuesto_it_pct=impuesto_it_pct,
               impuesto_iva_pct=impuesto_iva_pct)

def resumen_apu(apu: APU) -> dict:
    return {
        "codigo": apu.codigo,
        "descripcion": apu.descripcion,
        "unidad": apu.unidad,
        "costo_materiales": apu.costo_materiales,
        "costo_mano_obra": apu.costo_mano_obra,
        "costo_equipo": apu.costo_equipo,
        "costo_directo": apu.costo_directo,
        "gastos_generales": apu.gastos_generales,
        "utilidad": apu.utilidad,
        "subtotal": apu.subtotal,
        "impuesto_it": apu.impuesto_it,
        "impuesto_iva": apu.impuesto_iva,
        "precio_unitario": apu.precio_unitario,
    }
