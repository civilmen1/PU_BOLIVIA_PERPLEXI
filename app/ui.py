import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.models import Insumo, APU
from core.calculator import resumen_apu

st.set_page_config(page_title="PU Bolivia", page_icon="🏗️", layout="wide")
st.title("🏗️ PU_BOLIVIA_PERPLEXI")
st.subheader("Software de Análisis de Precios Unitarios - APU")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuración APU")
    codigo      = st.text_input("Código APU", value="APU-001")
    descripcion = st.text_input("Descripción", value="Hormigón ciclópeo H-20")
    unidad      = st.text_input("Unidad", value="m3")
    st.markdown("---")
    st.subheader("Indirectos (%)")
    gg_pct  = st.number_input("Gastos Generales %", 0.0, 100.0, 10.0, 0.5) / 100
    ut_pct  = st.number_input("Utilidad %",         0.0, 100.0, 10.0, 0.5) / 100
    it_pct  = st.number_input("Impuesto IT %",      0.0, 100.0,  3.0, 0.5) / 100
    iva_pct = st.number_input("IVA %",              0.0, 100.0,  0.0, 0.5) / 100

tab1, tab2, tab3 = st.tabs(["📋 Insumos", "📊 Resumen APU", "📁 Proyecto"])

with tab1:
    st.subheader("Ingreso de Insumos")
    c1, c2 = st.columns(2)
    with c1:
        tipo   = st.selectbox("Tipo", ["material", "mano_obra", "equipo"])
        cod_i  = st.text_input("Código", value="MAT-001")
        desc_i = st.text_input("Descripción Insumo", value="Cemento Portland IP-40")
    with c2:
        und_i  = st.text_input("Unidad Insumo", value="bolsa")
        cant_i = st.number_input("Cantidad", 0.0, value=1.0, step=0.1)
        prec_i = st.number_input("Precio Unitario (Bs)", 0.0, value=0.0, step=0.5)
        desp_i = st.number_input("Desperdicio %", 0.0, 50.0, 0.0) / 100

    if "insumos" not in st.session_state:
        st.session_state.insumos = []

    b1, b2 = st.columns(2)
    with b1:
        if st.button("➕ Agregar Insumo", use_container_width=True):
            st.session_state.insumos.append({
                "tipo": tipo, "codigo": cod_i, "descripcion": desc_i,
                "unidad": und_i, "cantidad": cant_i,
                "precio_unitario": prec_i, "desperdicio": desp_i
            })
            st.success(f"Insumo agregado: {desc_i}")
    with b2:
        if st.button("🗑️ Limpiar todo", use_container_width=True):
            st.session_state.insumos = []
            st.warning("Lista limpiada.")

    if st.session_state.insumos:
        df = pd.DataFrame(st.session_state.insumos)
        df["costo_total"] = (df["cantidad"] * df["precio_unitario"] * (1 + df["desperdicio"])).round(2)
        st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Resumen del APU")
    if st.session_state.get("insumos"):
        objs = [Insumo(**i) for i in st.session_state.insumos]
        apu  = APU(codigo=codigo, descripcion=descripcion, unidad=unidad,
                   insumos=objs, gastos_generales_pct=gg_pct, utilidad_pct=ut_pct,
                   impuesto_it_pct=it_pct, impuesto_iva_pct=iva_pct)
        r = resumen_apu(apu)
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Costo Directo",  f"Bs {r['costo_directo']:,.2f}")
        c2.metric("📈 Subtotal",        f"Bs {r['subtotal']:,.2f}")
        c3.metric("✅ Precio Unitario", f"Bs {r['precio_unitario']:,.2f}")
        st.markdown("---")
        filas = [
            ("Materiales",                             r["costo_materiales"]),
            ("Mano de Obra",                           r["costo_mano_obra"]),
            ("Equipo",                                 r["costo_equipo"]),
            ("─── Costo Directo",                      r["costo_directo"]),
            (f"Gastos Generales ({gg_pct*100:.1f}%)",  r["gastos_generales"]),
            (f"Utilidad ({ut_pct*100:.1f}%)",          r["utilidad"]),
            ("─── Subtotal",                           r["subtotal"]),
            (f"Impuesto IT ({it_pct*100:.1f}%)",       r["impuesto_it"]),
            (f"IVA ({iva_pct*100:.1f}%)",              r["impuesto_iva"]),
            ("⭐ PRECIO UNITARIO FINAL",               r["precio_unitario"]),
        ]
        st.dataframe(pd.DataFrame(filas, columns=["Rubro","Monto (Bs)"]),
                     use_container_width=True, hide_index=True)
    else:
        st.info("Agrega insumos en la pestaña 'Insumos' para ver el resumen APU.")

with tab3:
    st.subheader("Gestión de Proyecto")
    st.info("Módulo en desarrollo: múltiples APUs, presupuesto general y exportación Excel/PDF.")
    nom  = st.text_input("Nombre del Proyecto", value="PROYECTO APU BOLIVIA")
    ubic = st.text_input("Ubicación", value="Santa Cruz de la Sierra, Bolivia")
    fech = st.text_input("Fecha", value="2026")
    st.success(f"Proyecto: {nom}  |  {ubic}  |  {fech}")
