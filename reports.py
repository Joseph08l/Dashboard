"""
reports.py — Generador automático de reportes PDF diarios
"""

import os
import sys
from pathlib import Path
from datetime import datetime, date
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))
from database import get_dataframe, init_db

try:
    from fpdf import FPDF
    FPDF_OK = True
except ImportError:
    FPDF_OK = False

REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

VERDE   = (0, 168, 107)
OSCURO  = (15, 23, 42)
GRIS    = (100, 116, 139)
BLANCO  = (255, 255, 255)
CELESTE = (226, 232, 240)

class ReportePDF(FPDF):
    def __init__(self, titulo="Reporte Almacén"):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.titulo = titulo
        self.set_margins(12, 12, 12)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_fill_color(*OSCURO)
        self.rect(0, 0, 297, 18, "F")
        self.set_text_color(*VERDE)
        self.set_font("Helvetica", "B", 13)
        self.set_xy(8, 4)
        self.cell(0, 10, f"INVERSIONES LOS MARACOS SAS - {self.titulo}", ln=False)
        self.set_text_color(*GRIS)
        self.set_font("Helvetica", "", 8)
        self.set_xy(0, 4)
        self.cell(290, 10, datetime.now().strftime("%d/%m/%Y %H:%M"), align="R")
        self.ln(20)

    def footer(self):
        self.set_y(-12)
        self.set_text_color(*GRIS)
        self.set_font("Helvetica", "", 7)
        self.cell(0, 6, f"Página {self.page_no()} | Sistema de Gestión de Almacén 2026", align="C")

    def kpi_row(self, kpis: list[dict]):
        x_start = self.get_x()
        y_start = self.get_y()
        w = (297 - 24) / len(kpis)
        for i, kpi in enumerate(kpis):
            x = 12 + i * w
            self.set_xy(x, y_start)
            self.set_fill_color(26, 34, 53)
            self.rect(x, y_start, w - 2, 22, "F")
            self.set_text_color(*GRIS)
            self.set_font("Helvetica", "", 7)
            self.set_xy(x + 2, y_start + 2)
            self.cell(w - 4, 5, kpi["label"].upper(), align="C")
            self.set_text_color(*VERDE)
            self.set_font("Helvetica", "B", 14)
            self.set_xy(x + 2, y_start + 8)
            self.cell(w - 4, 8, str(kpi["value"]), align="C")
            if kpi.get("sub"):
                self.set_text_color(*GRIS)
                self.set_font("Helvetica", "", 6)
                self.set_xy(x + 2, y_start + 17)
                self.cell(w - 4, 4, kpi["sub"], align="C")
        self.set_xy(12, y_start + 26)

    def table(self, headers: list, rows: list, col_widths: list = None):
        if not rows:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(*GRIS)
            self.cell(0, 8, "Sin datos para mostrar.", ln=True)
            return

        available = 297 - 24
        if not col_widths:
            col_widths = [available / len(headers)] * len(headers)

        # Header
        self.set_fill_color(*VERDE)
        self.set_text_color(*BLANCO)
        self.set_font("Helvetica", "B", 7)
        y = self.get_y()
        for i, h in enumerate(headers):
            self.set_xy(12 + sum(col_widths[:i]), y)
            self.cell(col_widths[i], 7, str(h).upper(), border=0, fill=True, align="C")
        self.ln(7)

        # Rows
        self.set_font("Helvetica", "", 7)
        for ri, row in enumerate(rows):
            if self.get_y() > 185:
                self.add_page()
            fill = ri % 2 == 0
            self.set_fill_color(*CELESTE) if fill else self.set_fill_color(*BLANCO)
            self.set_text_color(*OSCURO)
            y = self.get_y()
            for i, val in enumerate(row):
                self.set_xy(12 + sum(col_widths[:i]), y)
                self.cell(col_widths[i], 6, str(val)[:30], border=0, fill=True, align="L")
            self.ln(6)

def generar_reporte_diario(fecha: str = None) -> str:
    if not FPDF_OK:
        return "ERROR: fpdf2 no instalado"

    init_db()
    hoy = fecha or date.today().isoformat()
    df = get_dataframe({"fecha_desde": hoy, "fecha_hasta": hoy})

    if df.empty:
        df_all = get_dataframe()
    else:
        df_all = df

    pdf = ReportePDF(f"Reporte Diario - {hoy}")
    pdf.add_page()

    # KPIs
    total   = len(df_all)
    entradas = int(df_all[df_all["MOV"]=="ENTRADA"]["CANTIDAD"].sum())
    salidas  = int(df_all[df_all["MOV"]=="SALIDA"]["CANTIDAD"].sum())
    desc     = int(df_all[df_all["MOV"]=="SALIDA DESCUENTO"]["CANTIDAD"].sum())
    articulos = df_all["NOMBRE"].nunique()

    pdf.kpi_row([
        {"label": "Registros Hoy", "value": len(df), "sub": f"de {total} totales"},
        {"label": "Entradas",      "value": f"{entradas:,}", "sub": "unidades"},
        {"label": "Salidas",       "value": f"{salidas:,}", "sub": "unidades"},
        {"label": "S. Descuento",  "value": f"{desc:,}", "sub": "unidades"},
        {"label": "Artículos",     "value": articulos, "sub": "diferentes"},
    ])

    # Movimientos del día
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*VERDE)
    pdf.cell(0, 8, f">> MOVIMIENTOS DEL DIA ({hoy})", ln=True)

    cols_mov = ["FECHA","MOV","NOMBRE","GRUPO_ALMACEN","CANTIDAD","UNIDAD","RESPONSABLE","DESTINO_SALIDA"]
    if not df.empty:
        rows = df[cols_mov].head(40).values.tolist()
        rows = [[str(v)[:28] for v in row] for row in rows]
    else:
        rows = []

    pdf.table(
        headers=["Fecha","Movimiento","Artículo","Grupo","Cant.","Unidad","Responsable","Destino"],
        rows=rows,
        col_widths=[20, 28, 48, 40, 12, 14, 48, 28]
    )

    # Resumen por sección
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*VERDE)
    pdf.cell(0, 8, ">> RESUMEN POR SECCION", ln=True)
    resumen = df_all.groupby("SECCION").agg(
        Registros=("id","count"),
        Cantidad_Total=("CANTIDAD","sum"),
        Artículos=("NOMBRE","nunique")
    ).reset_index().sort_values("Cantidad_Total", ascending=False)

    pdf.table(
        headers=["Sección","Registros","Cantidad Total","Artículos Distintos"],
        rows=resumen.values.tolist(),
        col_widths=[80, 40, 60, 60]
    )

    # Resumen por responsable
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*VERDE)
    pdf.cell(0, 8, ">> ACTIVIDAD POR RESPONSABLE", ln=True)
    resp = df_all.groupby("RESPONSABLE").agg(
        Registros=("id","count"),
        Cantidad=("CANTIDAD","sum")
    ).reset_index().sort_values("Registros", ascending=False).head(15)

    pdf.table(
        headers=["Responsable","Registros","Cantidad Total"],
        rows=resp.values.tolist(),
        col_widths=[120, 60, 60]
    )

    # Guardar
    nombre_pdf = f"reporte_{hoy.replace('-','')}.pdf"
    ruta = REPORTS_DIR / nombre_pdf
    pdf.output(str(ruta))
    return str(ruta)

def generar_reporte_general() -> str:
    if not FPDF_OK:
        return "ERROR: fpdf2 no instalado"

    init_db()
    df = get_dataframe()
    pdf = ReportePDF("Reporte General 2026")
    pdf.add_page()

    total    = len(df)
    entradas = int(df[df["MOV"]=="ENTRADA"]["CANTIDAD"].sum())
    salidas  = int(df[df["MOV"]=="SALIDA"]["CANTIDAD"].sum())
    desc     = int(df[df["MOV"]=="SALIDA DESCUENTO"]["CANTIDAD"].sum())
    ini      = int(df[df["MOV"]=="INVENTARIO INICIAL"]["CANTIDAD"].sum())

    pdf.kpi_row([
        {"label": "Total Registros", "value": f"{total:,}"},
        {"label": "Entradas",        "value": f"{entradas:,}"},
        {"label": "Salidas",         "value": f"{salidas:,}"},
        {"label": "S. Descuento",    "value": f"{desc:,}"},
        {"label": "Inv. Inicial",    "value": f"{ini:,}"},
    ])

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*VERDE)
    pdf.cell(0, 8, ">> RESUMEN POR GRUPO DE ALMACEN", ln=True)
    grp = df.groupby("GRUPO_ALMACEN").agg(
        Registros=("id","count"), Cantidad=("CANTIDAD","sum")
    ).reset_index().sort_values("Registros", ascending=False)
    pdf.table(
        headers=["Grupo Almacén","Registros","Cantidad Total"],
        rows=grp.values.tolist(),
        col_widths=[140, 50, 50]
    )

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*VERDE)
    pdf.cell(0, 8, ">> TOP 20 ARTICULOS MAS MOVIDOS", ln=True)
    arts = df.groupby("NOMBRE").agg(
        Registros=("id","count"), Cantidad=("CANTIDAD","sum"), Unidad=("UNIDAD","first")
    ).reset_index().sort_values("Cantidad", ascending=False).head(20)
    pdf.table(
        headers=["Artículo","Registros","Cantidad","Unidad"],
        rows=arts.values.tolist(),
        col_widths=[120, 40, 50, 30]
    )

    nombre_pdf = f"reporte_general_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    ruta = REPORTS_DIR / nombre_pdf
    pdf.output(str(ruta))
    return str(ruta)


if __name__ == "__main__":
    from database import sync_all
    sync_all()
    ruta = generar_reporte_general()
    print(f"✅ PDF generado: {ruta}")
