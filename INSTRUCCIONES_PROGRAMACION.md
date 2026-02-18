# Instrucciones para Programar Ejecución Automática

## Script: oracle_bicc_reset_headless.py

---

## Cambios Realizados al Script Original

### 1. Modo Headless
Se modificó **únicamente** la sección de inicialización del navegador para ejecutar Chrome sin interfaz gráfica:

```python
options.add_argument('--headless=new')              # Modo headless moderno
options.add_argument('--disable-gpu')               # Requerido en algunos sistemas
options.add_argument('--no-sandbox')                # Para ejecución como root
options.add_argument('--disable-dev-shm-usage')     # Evita problemas de memoria
options.add_argument('--window-size=1920,1080')     # Tamaño de ventana virtual
```

### 2. Logging a Archivo
Se agregó logging con timestamps que escribe a `oracle_bicc_reset.log` en el mismo directorio del script:
- Registra inicio/fin de ejecución
- Registra progreso de cada fila procesada
- Registra errores con detalles
- **Los prints originales se mantienen intactos**

### 3. El Core del Script NO fue Modificado
Todas las acciones de Selenium (XPaths, waits, clicks, scrolls, diálogos) permanecen **exactamente igual** que en el script original.

---

## Ubicación de Logs

| Archivo | Ubicación | Descripción |
|---------|-----------|-------------|
| `oracle_bicc_reset.log` | Mismo directorio del script | Log principal con timestamps |
| `error_YYYYMMDD_HHMMSS.png` | Mismo directorio del script | Screenshots de errores críticos |

---

## Requisitos Previos

### En Windows:
1. **Python 3.8+** instalado
2. **Google Chrome** instalado
3. **ChromeDriver** compatible con la versión de Chrome
   - Descargar de: https://googlechromelabs.github.io/chrome-for-testing/
   - Colocar en el PATH del sistema o en el mismo directorio del script
4. **Dependencias Python:**
   ```bash
   pip install -r requirements.txt
   ```

### En Linux:
1. **Python 3.8+** instalado
2. **Chromium o Google Chrome:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y chromium-browser chromium-chromedriver
   
   # O Google Chrome
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo dpkg -i google-chrome-stable_current_amd64.deb
   sudo apt-get install -f
   ```
3. **ChromeDriver:**
   ```bash
   # Ya incluido con chromium-chromedriver, o:
   sudo apt-get install chromium-chromedriver
   ```
4. **Dependencias Python:**
   ```bash
   pip3 install -r requirements.txt
   ```

---

## Programación en Windows (Task Scheduler)

### Cada 80-90 días (recomendado: cada 85 días)

1. **Abrir Task Scheduler:**
   - Presionar `Win + R`, escribir `taskschd.msc`, Enter

2. **Crear tarea básica:**
   - Click derecho en "Task Scheduler Library" → "Create Basic Task"
   - Nombre: `Oracle BICC Reset`
   - Descripción: `Reset automático de jobs BICC cada 85 días`

3. **Trigger (disparador):**
   - Seleccionar "Monthly"
   - Elegir el día 1 de cada tercer mes (aproximadamente cada 90 días)
   - **O usar trigger personalizado:**
     - "Create Task" (no básica) → Triggers → New
     - "On a schedule" → "Daily"
     - Repeat task every: `85 days`
     - Hora: `02:00:00` (madrugada, menor carga)

4. **Action (acción):**
   - Action: "Start a program"
   - Program/script: `C:\Python3x\python.exe` (ruta completa a Python)
   - Arguments: `C:\ruta\al\script\oracle_bicc_reset_headless.py`
   - Start in: `C:\ruta\al\script\`

5. **Condiciones recomendadas:**
   - ✅ "Run whether user is logged on or not"
   - ✅ "Run with highest privileges"
   - ❌ "Start only if computer is on AC power" (desmarcar)

6. **Settings:**
   - ✅ "Allow task to be run on demand"
   - ✅ "If task fails, restart every: 1 hour"
   - Attempts: 3

### Script BAT alternativo (opcional):
```batch
@echo off
cd /d C:\ruta\al\script
C:\Python3x\python.exe oracle_bicc_reset_headless.py
```

---

## Programación en Linux (Cron)

### Cada 85 días aproximadamente

La forma más práctica es ejecutar mensualmente y controlar internamente, o usar fechas específicas.

#### Opción 1: Ejecutar trimestralmente (cada ~90 días)
```bash
# Editar crontab
crontab -e

# Agregar línea (ejecuta día 1 de enero, abril, julio, octubre a las 2:00 AM)
0 2 1 1,4,7,10 * /usr/bin/python3 /ruta/al/script/oracle_bicc_reset_headless.py >> /ruta/al/script/cron_output.log 2>&1
```

#### Opción 2: Usar anacron para ejecución cada N días
```bash
# Instalar anacron si no está
sudo apt-get install anacron

# Editar /etc/anacrontab
sudo nano /etc/anacrontab

# Agregar línea (85 días, delay 5 min, ID único, comando)
85 5 oracle-bicc-reset /usr/bin/python3 /ruta/al/script/oracle_bicc_reset_headless.py
```

#### Opción 3: Cron con script de control
Crear script wrapper `/ruta/al/script/run_bicc_reset.sh`:
```bash
#!/bin/bash
# Ejecutar cada 85 días usando un archivo de marca de tiempo

SCRIPT_DIR="/ruta/al/script"
LAST_RUN_FILE="$SCRIPT_DIR/.last_bicc_run"
DAYS_INTERVAL=85

# Verificar última ejecución
if [ -f "$LAST_RUN_FILE" ]; then
    last_run=$(cat "$LAST_RUN_FILE")
    current_date=$(date +%s)
    days_since=$(( (current_date - last_run) / 86400 ))
    
    if [ $days_since -lt $DAYS_INTERVAL ]; then
        echo "Solo han pasado $days_since días. Se requieren $DAYS_INTERVAL días."
        exit 0
    fi
fi

# Ejecutar script
cd "$SCRIPT_DIR"
/usr/bin/python3 oracle_bicc_reset_headless.py

# Actualizar marca de tiempo
date +%s > "$LAST_RUN_FILE"
```

Luego en crontab, ejecutar diariamente:
```bash
0 2 * * * /ruta/al/script/run_bicc_reset.sh >> /ruta/al/script/cron_wrapper.log 2>&1
```

### Permisos necesarios:
```bash
chmod +x /ruta/al/script/oracle_bicc_reset_headless.py
chmod +x /ruta/al/script/run_bicc_reset.sh
```

---

## Verificación de Ejecución

### Revisar logs:
```bash
# Ver últimas 50 líneas del log
tail -50 oracle_bicc_reset.log

# Buscar errores
grep -i "error\|critical" oracle_bicc_reset.log

# Ver ejecuciones recientes
grep "INICIO DE EJECUCIÓN" oracle_bicc_reset.log
```

### Prueba manual:
```bash
# Ejecutar manualmente para verificar
python3 oracle_bicc_reset_headless.py
```

---

## Troubleshooting

| Problema | Solución |
|----------|----------|
| "ChromeDriver not found" | Verificar que chromedriver está en el PATH |
| "Chrome version mismatch" | Descargar ChromeDriver compatible con versión de Chrome instalada |
| "DevToolsActivePort file doesn't exist" | Agregar `--remote-debugging-port=9222` a las opciones |
| Screenshots en negro | Normal en headless; el script sigue funcionando |
| Timeout en login | Aumentar `PAGE_LOAD_TIMEOUT` o verificar conectividad a Oracle Cloud |

---

## Notas de Seguridad

⚠️ **IMPORTANTE:**
- Las credenciales están en texto plano en el script
- Considerar usar variables de entorno o un archivo de configuración externo:
  ```python
  import os
  ORACLE_USER = os.environ.get('ORACLE_USER', 'default_user')
  ORACLE_PASS = os.environ.get('ORACLE_PASS', '')
  ```
- Restringir permisos del archivo: `chmod 600 oracle_bicc_reset_headless.py`
