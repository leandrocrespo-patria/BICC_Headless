# BICC Oracle ERP Jobs Reset Automation

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Selenium](https://img.shields.io/badge/selenium-4.0+-green.svg)
![Chrome](https://img.shields.io/badge/chrome-webdriver-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Herramienta de automatización para el reseteo masivo de trabajos (jobs) en Oracle ERP Cloud a través de la interfaz web BICC (Business Intelligence Cloud Connector).

## 📋 Descripción

Este script automatiza el proceso de reseteo de trabajos en Oracle ERP Cloud, específicamente en el módulo "Manage Jobs" de BICC. Utiliza Selenium WebDriver para simular interacciones del usuario y procesar múltiples filas de trabajos de forma batch, optimizado para ejecución en modo headless para entornos de servidor o tareas programadas.

### 🎯 Características Principales

- ✅ **Automatización Web Completa**: Navegación automática, autenticación y procesamiento
- ✅ **Modo Headless**: Ejecución sin interfaz gráfica para servidores y CI/CD
- ✅ **Procesamiento por Lotes**: Manejo de múltiples trabajos (33 filas por defecto)
- ✅ **Logging Detallado**: Registro completo de operaciones con timestamps
- ✅ **Manejo Robusto de Errores**: Recuperación automática y continuidad del procesamiento
- ✅ **Scrolling Inteligente**: Navegación automática en tablas Oracle dinámicas
- ✅ **Cleanup Seguro**: Cierre controlado del navegador y recursos

## 🛠️ Requisitos del Sistema

### Software Requerido
- **Python 3.7+**
- **Google Chrome** (versión actualizada)
- **ChromeDriver** (compatible con la versión de Chrome instalada)

### Dependencias Python
```
selenium>=4.0.0
```

## 📦 Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/leandrocrespo-patria/BICC_Headless.git
cd BICC_Headless
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar ChromeDriver
**Opción A: Instalación Automática (Recomendada)**
```bash
pip install webdriver-manager
```

**Opción B: Instalación Manual**
1. Descargar ChromeDriver desde [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
2. Agregar ChromeDriver al PATH del sistema
3. Verificar instalación: `chromedriver --version`

## ⚙️ Configuración

### Variables de Configuración
Editar las constantes en `oracle_bicc_reset_headless.py`:

```python
# Credenciales de Oracle Cloud
ORACLE_USER = "tu_usuario"           # Usuario del servicio Oracle
ORACLE_PASS = "tu_contraseña"        # Contraseña del servicio
ORACLE_URL = "https://tu-instancia.oraclecloud.com/biacm"  # URL de tu instancia

# Configuración de procesamiento
TOTAL_ROWS = 33                      # Número de filas a procesar
PAGE_LOAD_TIMEOUT = 20               # Timeout para carga de páginas
OPERATION_DELAY = 2                  # Delay entre operaciones
```

### Configuración de Logging
```python
SKIP_LOGOUT = False                  # True para omitir logout
LOGOUT_TIMEOUT = 5                   # Timeout para operaciones de logout
```

## 🚀 Uso

### Ejecución Básica
```bash
python oracle_bicc_reset_headless.py
```

### Ejecución con Logging en Consola
```bash
python oracle_bicc_reset_headless.py 2>&1 | tee execution.log
```

### Ejecución Programada (Cron/Task Scheduler)
```bash
# Linux/Mac - Crontab entry para ejecución diaria a las 2:00 AM
0 2 * * * cd /ruta/al/proyecto && python oracle_bicc_reset_headless.py
```

```batch
# Windows - Task Scheduler
schtasks /create /tn "Oracle BICC Reset" /tr "C:\ruta\al\proyecto\oracle_bicc_reset_headless.py" /sc daily /st 02:00
```

## 📁 Estructura del Proyecto

```
BICC_Headless/
├── 📄 oracle_bicc_reset_headless.py    # Script principal
├── 📄 requirements.txt                 # Dependencias Python
├── 📄 README.md                       # Documentación (este archivo)
├── 📄 INSTRUCCIONES_PROGRAMACION.md   # Documentación técnica
├── 📄 oracle_bicc_reset.log          # Log de ejecuciones
└── 📁 Uploads/                       # Archivos auxiliares
    └── user_message_*.txt
```

## 📊 Proceso de Ejecución

### Flujo de Trabajo
1. **Inicialización**: Configuración del navegador Chrome en modo headless
2. **Autenticación**: Login automático en Oracle Cloud
3. **Navegación**: Acceso al módulo "Manage Jobs" 
4. **Procesamiento**: Iteración sobre las filas de trabajos (0 to TOTAL_ROWS-1)
   - Localización del elemento de acción
   - Scrolling inteligente si es necesario
   - Click en el icono de acciones
   - Selección de "Reset"
   - Confirmación de diálogos
5. **Cleanup**: Logout y cierre seguro del navegador

### Ejemplo de Salida
```
1. Navigating to Oracle Cloud login page...
2. Performing user authentication...
3. Waiting for dashboard to load...
4. Accessing 'Manage Jobs' module...
5. Starting batch processing of 33 job rows...

--- Processing Row 1/33 (Index: 0) ---
   > Successfully clicked row action icon
   > Successfully clicked 'Reset' option
   > Confirmed reset operation with 'Y' key
   > Row 1 reset operation completed successfully

--- Processing Row 2/33 (Index: 1) ---
   ...

BATCH PROCESSING COMPLETED
6. Performing clean logout...
SCRIPT EXECUTION COMPLETED SUCCESSFULLY
```

## 📝 Logging

### Archivo de Log
- **Ubicación**: `oracle_bicc_reset.log` (mismo directorio del script)
- **Formato**: `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`
- **Encoding**: UTF-8

### Ejemplo de Log
```log
2026-02-18 14:30:15 - INFO - ============================================================
2026-02-18 14:30:15 - INFO - INICIO DE EJECUCIÓN - 2026-02-18 14:30:15
2026-02-18 14:30:15 - INFO - ============================================================
2026-02-18 14:30:16 - INFO - Inicializando navegador Chrome en modo headless...
2026-02-18 14:30:17 - INFO - Navegador inicializado correctamente  
2026-02-18 14:30:18 - INFO - Navegando a Oracle Cloud...
2026-02-18 14:30:22 - INFO - Realizando autenticación...
2026-02-18 14:30:35 - INFO - Iniciando procesamiento de 33 filas...
```

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. ChromeDriver no encontrado
```bash
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```
**Solución**: Instalar ChromeDriver o agregarlo al PATH del sistema.

#### 2. Timeout en elementos
```bash
selenium.common.exceptions.TimeoutException: Message: 
```
**Solución**: Incrementar `PAGE_LOAD_TIMEOUT` o verificar selectores XPath.

#### 3. Problemas de autenticación
```bash
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element
```
**Solución**: Verificar credenciales y URL de Oracle Cloud.

#### 4. Errores de scrolling
**Solución**: El script incluye múltiples estrategias de scrolling. Revisar logs para detalles.

### Debug Mode
Para habilitar modo debug (con interfaz gráfica):
```python
# Comentar esta línea en el código:
# options.add_argument('--headless=new')
```

## 🔒 Seguridad

### Mejores Prácticas
- **Nunca hardcodear credenciales** en el código fuente
- Usar variables de entorno para información sensible:
  ```python
  import os
  ORACLE_USER = os.getenv('ORACLE_USER', 'default_user')
  ORACLE_PASS = os.getenv('ORACLE_PASS', 'default_pass')
  ```
- Mantener logs seguros con permisos restrictivos
- Rotar credenciales regularmente

## 📈 Rendimiento

### Métricas Típicas
- **Tiempo por fila**: ~3-5 segundos
- **33 filas completas**: ~2-3 minutos
- **Uso de memoria**: ~100-150 MB (modo headless)

### Optimizaciones
- Modo headless reduce uso de recursos en ~40%
- Timeouts configurables para diferentes entornos de red
- Scrolling inteligente minimiza operaciones DOM

## 🤝 Contribuciones

### Proceso de Contribución
1. Fork del repositorio
2. Crear branch para nueva característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit de cambios (`git commit -am 'Agregar nueva característica'`)
4. Push al branch (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

### Reportar Issues
- Usar el template de issues en GitHub
- Incluir logs relevantes
- Especificar versión de Python, Chrome y ChromeDriver

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

### Contacto
- **Autor**: System Automation Team
- **Email**: [tu-email@empresa.com]
- **Issues**: [GitHub Issues](https://github.com/leandrocrespo-patria/BICC_Headless/issues)

### Documentación Adicional
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [ChromeDriver Documentation](https://chromedriver.chromium.org/getting-started)
- [Oracle Cloud Documentation](https://docs.oracle.com/en/cloud/)

---

**Versión**: 3.6-headless (improved logout handling)  
**Última Actualización**: Febrero 2026  
**Mantenido por**: leandrocrespo-patria