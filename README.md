# 🌿 Sistema de Gestión de Almacén — Inversiones Los Maracos SAS

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/Licencia-Privada-red?style=for-the-badge)

**Sistema empresarial de dashboards automáticos conectado a Excel**  
Dashboard interactivo · Sincronización en tiempo real · Reportes PDF · Correos automáticos

[Ver Demo](#demo) · [Instalación](#instalación-rápida) · [Documentación](#documentación)

</div>

---

## 📋 Descripción

Sistema completo de gestión de almacén para **Inversiones Los Maracos SAS** (Villanueva, Casanare).  
Lee archivos Excel automáticamente, los sincroniza a una base de datos SQLite y presenta dashboards interactivos con actualización en tiempo real.

### ¿Qué hace el sistema?

- 📊 **Dashboard web** con gráficas interactivas, KPIs y filtros múltiples
- 🔄 **Sincronización automática** al detectar cambios en los archivos Excel
- 📄 **Reportes PDF** generados automáticamente cada día
- 📧 **Correos automáticos** con reporte diario a las 8:00 AM
- 🔔 **Alertas** de stock bajo y actividad inusual
- 💾 **Backups diarios** automáticos a las 11:55 PM

---

## 🗂️ Estructura del Proyecto

```
maracos_dashboard/
├── 📄 streamlit_app.py        ← Dashboard web principal
├── 👁️  watcher.py              ← Monitor de archivos Excel en tiempo real
├── ⚙️  scheduler.py            ← Tareas programadas (backup, sync, reportes)
├── 🚀 INICIAR.bat             ← Arrancar en Windows (doble clic)
├── 🚀 iniciar.sh              ← Arrancar en Linux/Mac
├── 📦 requirements.txt        ← Dependencias Python
│
├── app/
│   └── 🗃️  database.py         ← Motor SQLite + lector Excel
│
├── scripts/
│   ├── 📄 reports.py           ← Generador de reportes PDF
│   └── 📧 notificaciones.py    ← Correos automáticos Gmail
│
├── data/                      ← 📁 Carpeta donde van los archivos Excel
├── reports/                   ← 📁 PDFs generados automáticamente
├── backups/                   ← 📁 Backups diarios
└── logs/                      ← 📁 Registros del sistema
```

---

## ⚡ Instalación Rápida

### Requisitos
- Python 3.10 o superior → [descargar](https://www.python.org/downloads/)
- Git → [descargar](https://git-scm.com/downloads)
- Conexión a internet (para instalar dependencias)

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/maracos-dashboard.git
cd maracos-dashboard
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Agregar tu archivo Excel

Copia tu archivo Excel (con hoja **"Base de Datos"**) en la carpeta `/data/`:
```
data/
└── Inventario_Almacén_2026.xlsx
```

### 4. Configurar correo (opcional)

Edita `scripts/notificaciones.py` y agrega tu contraseña de app Gmail:
```python
GMAIL_APP_PASSWORD = "tu clave de 16 caracteres"
```
Ver [Guía completa de configuración Gmail](GUIA_CORREO.md)

### 5. Iniciar el sistema

**Windows:**
```
Doble clic en INICIAR.bat
```

**Linux / Mac:**
```bash
chmod +x iniciar.sh
./iniciar.sh
```

**Manual:**
```bash
streamlit run streamlit_app.py
```

El dashboard abre automáticamente en: **http://localhost:8501**

---

## 📊 Funcionalidades del Dashboard

### KPIs en Tiempo Real
| Indicador | Descripción |
|-----------|-------------|
| Total Registros | Movimientos filtrados |
| Entradas | Unidades ingresadas al almacén |
| Salidas | Unidades despachadas |
| Salida Descuento | Unidades con descuento aplicado |
| Inventario Inicial | Stock de apertura |

### Filtros Disponibles
- 📅 Rango de fechas (desde / hasta)
- 📦 Tipo de movimiento (multi-selección)
- 📂 Sección (Cultivo, Ganadería, Instalaciones...)
- 👤 Responsable
- 🏷️ Grupo de almacén
- 🏠 Destino de salida

### Gráficas Interactivas
- Distribución por tipo de movimiento (doughnut)
- Cantidad por sección (barras)
- Evolución mensual (líneas)
- Top artículos por cantidad (barras horizontales)
- Cantidad por responsable
- Treemap por grupo de almacén
- Distribución por destino (pie)

---

## 🔄 Automatización

### Tareas programadas

| Tarea | Frecuencia |
|-------|------------|
| Sincronizar Excel → SQLite | Cada 5 minutos |
| Reporte PDF diario | 6:00 AM |
| Correo con reporte | 8:00 AM |
| Alertas de stock | Cada hora |
| Backup Excel + DB | 11:55 PM diario |
| Limpieza de logs | Domingos 1:00 AM |

### Detección automática de archivos

El sistema detecta automáticamente:
- ✅ **Nuevo archivo Excel** → sincroniza inmediatamente
- ✅ **Modificación** → resincroniza al guardar
- ✅ **Eliminación** → remueve de la base de datos

---

## 📧 Correos Automáticos

### Reporte Diario (8:00 AM)
Incluye:
- KPIs del día vs acumulado 2026
- Tabla de movimientos del día
- Resumen por sección
- PDF adjunto completo

### Alertas Automáticas
Se envían cuando se detecta:
- ⚠️ Artículos con saldo menor a 5 unidades
- 📦 Movimientos registrados en el día
- 🕐 Artículos sin movimiento en +30 días

---

## 🔗 Vincular con GitHub

### Primera vez (subir el proyecto)

```bash
# 1. Inicializar Git en la carpeta del proyecto
git init

# 2. Crear el .gitignore
echo "data/*.xlsx
*.db
backups/
logs/
reports/
__pycache__/
.installed
*.pyc
.env" > .gitignore

# 3. Agregar todos los archivos
git add .

# 4. Primer commit
git commit -m "🚀 Sistema Almacén Los Maracos - versión inicial"

# 5. Conectar con tu repositorio GitHub
git remote add origin https://github.com/TU-USUARIO/maracos-dashboard.git

# 6. Subir
git push -u origin main
```

### Actualizar después de cambios

```bash
git add .
git commit -m "descripción del cambio"
git push
```

### Descargar en otra computadora

```bash
git clone https://github.com/TU-USUARIO/maracos-dashboard.git
cd maracos-dashboard
pip install -r requirements.txt
# Copiar tus Excel en /data/
# Configurar GMAIL_APP_PASSWORD en scripts/notificaciones.py
./INICIAR.bat
```

---

## 🌐 Publicar en Internet (Streamlit Cloud)

Para acceder al dashboard desde cualquier lugar sin necesidad de tener el PC encendido:

### 1. Subir el proyecto a GitHub (ver arriba)

### 2. Ir a Streamlit Cloud
- Entra a: https://share.streamlit.io
- Inicia sesión con tu cuenta GitHub
- Clic en **"New app"**
- Selecciona tu repositorio `maracos-dashboard`
- En "Main file path" escribe: `streamlit_app.py`
- Clic en **"Deploy"**

### 3. Variables de entorno (para el correo)
En Streamlit Cloud → Settings → Secrets, agrega:
```toml
GMAIL_APP_PASSWORD = "tu clave aqui"
```

### 4. URL pública
Tu dashboard quedará disponible en una URL como:
```
https://maracos-dashboard.streamlit.app
```
Accesible desde cualquier celular, tablet o computador con internet.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| Python 3.10+ | Lenguaje base |
| Streamlit | Dashboard web |
| Plotly | Gráficas interactivas |
| Pandas | Procesamiento de datos |
| OpenPyXL | Lectura de archivos Excel |
| SQLite | Base de datos local |
| Watchdog | Monitor de archivos en tiempo real |
| FPDF2 | Generación de reportes PDF |
| Schedule | Automatización de tareas |
| smtplib | Envío de correos Gmail |

---

## 📞 Soporte

**Empresa:** Inversiones Los Maracos SAS  
**Ubicación:** Villanueva, Casanare, Colombia  
**Correo sistema:** almacen.maracos@gmail.com  
**Reportes a:** invmaracosvillanueva@gmail.com  

---

## 📝 Changelog

### v1.0.0 (Mayo 2026)
- ✅ Dashboard interactivo con 7 filtros y 7 gráficas
- ✅ Sincronización automática Excel → SQLite
- ✅ Monitor de archivos en tiempo real (watchdog)
- ✅ Generador de reportes PDF
- ✅ Correos automáticos con Gmail
- ✅ Alertas de stock bajo
- ✅ Backups diarios automáticos
- ✅ Dashboard HTML standalone (sin servidor)

---

<div align="center">
  Desarrollado para <strong>Inversiones Los Maracos SAS</strong> · Villanueva, Casanare 🌿
</div>
