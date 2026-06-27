from dataclasses import dataclass, field
from typing import List

@dataclass
class Insumo:
    tipo: str  # 'material', 'mano_obra', 'equipo'
    codigo: str
    descripcion: str
    unidad: str
    cantidad: float
    precio_unitario: float
    desperdicio: float = 0.0

    @property
    def costo_total(self) -> float:
        return round(self.cantidad * self.precio_unitario * (1 + self.desperdicio), 4)

@dataclass
class APU:
    codigo: str
    descripcion: str
    unidad: str
    insumos: List[Insumo] = field(default_factory=list)
    gastos_generales_pct: float = 0.10
    utilidad_pct: float = 0.10
    impuesto_it_pct: float = 0.03
    impuesto_iva_pct: float = 0.0

    @property
    def materiales(self):
        return [i for i in self.insumos if i.tipo == 'material']

    @property
    def mano_obra(self):
        return [i for i in self.insumos if i.tipo == 'mano_obra']

    @property
    def equipo(self):
        return [i for i in self.insumos if i.tipo == 'equipo']

    @property
    def costo_materiales(self) -> float:
        return round(sum(i.costo_total for i in self.materiales), 4)

    @property
    def costo_mano_obra(self) -> float:
        return round(sum(i.costo_total for i in self.mano_obra), 4)

    @property
    def costo_equipo(self) -> float:
        return round(sum(i.costo_total for i in self.equipo), 4)

    @property
    def costo_directo(self) -> float:
        return round(self.costo_materiales + self.costo_mano_obra + self.costo_equipo, 4)

    @property
    def gastos_generales(self) -> float:
        return round(self.costo_directo * self.gastos_generales_pct, 4)

    @property
    def utilidad(self) -> float:
        return round((self.costo_directo + self.gastos_generales) * self.utilidad_pct, 4)

    @property
    def subtotal(self) -> float:
        return round(self.costo_directo + self.gastos_generales + self.utilidad, 4)

    @property
    def impuesto_it(self) -> float:
        return round(self.subtotal * self.impuesto_it_pct, 4)

    @property
    def impuesto_iva(self) -> float:
        return round(self.subtotal * self.impuesto_iva_pct, 4)

    @property
    def precio_unitario(self) -> float:
        return round(self.subtotal + self.impuesto_it + self.impuesto_iva, 4)

@dataclass
class Actividad:
    codigo: str
    descripcion: str
    unidad: str
    cantidad: float
    apu: APU

    @property
    def precio_total(self) -> float:
        return round(self.cantidad * self.apu.precio_unitario, 4)

@dataclass
class Proyecto:
    nombre: str
    ubicacion: str
    fecha: str
    actividades: List[Actividad] = field(default_factory=list)

    @property
    def total_proyecto(self) -> float:
        return round(sum(a.precio_total for a in self.actividades), 4)
