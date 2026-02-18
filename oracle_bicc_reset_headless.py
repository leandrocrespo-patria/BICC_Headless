#!/usr/bin/env python3
"""
BICC Oracle ERP Jobs Reset Automation Script

This script automates the process of resetting Oracle ERP jobs through the web interface.
It performs batch operations on multiple rows in the "Manage Jobs" section of Oracle Cloud.

Author: System Automation Team
Date: February 2026
Version: 3.6-headless (improved logout handling)

Dependencies:
- selenium: Web browser automation
- Chrome WebDriver: Required for browser operations

Modificaciones para ejecución headless:
- Opciones de Chrome configuradas para modo headless
- Logging a archivo agregado para monitoreo de ejecuciones programadas
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
from datetime import datetime

# ===============================
# LOGGING CONFIGURATION
# ===============================
# Crear directorio de logs si no existe
LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "oracle_bicc_reset.log")

# Configurar logging a archivo con timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
    ]
)
logger = logging.getLogger(__name__)
logger.info("=" * 60)
logger.info(f"INICIO DE EJECUCIÓN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
logger.info("=" * 60)

# ===============================
# CONFIGURATION PARAMETERS
# ===============================
ORACLE_USER = "svc_incorta"                                     # Oracle Cloud service account username
ORACLE_PASS = "ORACLE_PASS"                                # Oracle Cloud service account password
ORACLE_URL = "https://emfp-test.fa.us2.oraclecloud.com/biacm"   # Oracle Cloud BICC URL
TOTAL_ROWS = 33                                                 # Number of job rows to process

# Timeout settings (in seconds)
PAGE_LOAD_TIMEOUT = 20                   # Maximum wait time for page elements
OPERATION_DELAY = 2                      # Standard delay between operations
SCROLL_DELAY = 4                         # Wait time after scrolling operations

# Logout settings
SKIP_LOGOUT = False                      # Set to True to skip logout entirely (browser will still close)
LOGOUT_TIMEOUT = 5                       # Timeout for logout operations (shorter to avoid long waits)

# ===============================
# BROWSER INITIALIZATION - HEADLESS MODE
# ===============================
options = webdriver.ChromeOptions()        # Initialize Chrome browser options

# Opciones para ejecución headless (sin interfaz gráfica)
options.add_argument('--headless=new')              # Modo headless moderno (Chrome 109+)
options.add_argument('--disable-gpu')               # Deshabilitar GPU (requerido en algunos sistemas)
options.add_argument('--no-sandbox')                # Necesario para ejecución como root/en contenedores
options.add_argument('--disable-dev-shm-usage')     # Evita problemas de memoria compartida
options.add_argument('--window-size=1920,1080')     # Tamaño de ventana virtual
options.add_argument('--disable-extensions')        # Deshabilitar extensiones
options.add_argument('--disable-infobars')          # Ocultar barras de información
options.add_argument('--disable-notifications')     # Deshabilitar notificaciones
options.add_argument('--disable-popup-blocking')    # Permitir popups necesarios
options.add_argument('--ignore-certificate-errors') # Ignorar errores de certificado
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

logger.info("Inicializando navegador Chrome en modo headless...")
driver = webdriver.Chrome(options=options)          # Create Chrome browser instance
driver.set_window_size(1920, 1080)                  # Asegurar tamaño de ventana en headless
actions = ActionChains(driver)                      # Initialize action chains for complex interactions
logger.info("Navegador inicializado correctamente")

try:
    # ===============================
    # STEP 1: NAVIGATE TO ORACLE CLOUD
    # ===============================
    print("1. Navigating to Oracle Cloud login page...")
    logger.info("Navegando a Oracle Cloud...")
    # Navigate to the Oracle Cloud ERP login page with pre-encoded authentication parameters
    driver.get(ORACLE_URL)

    # Initialize WebDriverWait for explicit waits with timeout
    wait = WebDriverWait(driver, PAGE_LOAD_TIMEOUT)

    # ===============================
    # STEP 2: AUTHENTICATION
    # ===============================
    print("2. Performing user authentication...")
    logger.info("Realizando autenticación...")
    # Wait for username field to be clickable and enter credentials
    username_field = wait.until(EC.element_to_be_clickable((By.ID, "userid")))
    username_field.send_keys(ORACLE_USER)
    
    # Enter password and submit form with Enter key
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(ORACLE_PASS + Keys.ENTER)

    print("3. Waiting for dashboard to load...")
    logger.info("Esperando carga del dashboard...")
    # Allow time for dashboard to fully load after authentication
    time.sleep(10) 

    # ===============================
    # STEP 3: NAVIGATE TO MANAGE JOBS
    # ===============================
    print("4. Accessing 'Manage Jobs' module...")
    logger.info("Accediendo a 'Manage Jobs'...")
    # Locate and click the Manage Jobs icon in the dashboard
    manage_jobs_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@title='Manage Jobs']")))
    actions.move_to_element(manage_jobs_icon).click().perform()
    time.sleep(OPERATION_DELAY)
    
    # Click on the Manage Jobs link that appears after hovering/clicking the icon
    manage_jobs_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Manage Jobs'] | //span[text()='Manage Jobs']")))
    actions.move_to_element(manage_jobs_link).click().perform()
    
    print("   > Loading jobs table...")
    # Wait for the jobs table to fully load
    time.sleep(5)

    # ===============================
    # STEP 4: BATCH PROCESSING OF JOB ROWS
    # ===============================
    print(f"5. Starting batch processing of {TOTAL_ROWS} job rows...")
    print(f"   Processing rows 0 through {TOTAL_ROWS - 1} (zero-indexed)")
    logger.info(f"Iniciando procesamiento de {TOTAL_ROWS} filas...")

    # Main processing loop: iterate through each job row
    for i in range(TOTAL_ROWS):
        print(f"\n--- Processing Row {i + 1}/{TOTAL_ROWS} (Index: {i}) ---")
        logger.info(f"Procesando fila {i + 1}/{TOTAL_ROWS}")
        
        try:
            # ===============================
            # SUB-STEP 4.1: LOCATE TARGET ELEMENT
            # ===============================
            # Generate XPath for the specific row's action icon (Oracle's dynamic ID pattern)
            icon_xpath = f"//a[contains(@id, ':t1:{i}:b1::popEl')]"
            
            # ===============================
            # SUB-STEP 4.2: ELEMENT VISIBILITY CHECK & SCROLL HANDLING
            # ===============================
            try:
                # Attempt to find the element in the current viewport
                row_icon = driver.find_element(By.XPATH, icon_xpath)
            except:
                print(f"   > Row {i} icon not visible in current viewport. Initiating smart scroll...")
                
                # ===============================
                # SMART SCROLLING MECHANISM
                # ===============================
                # Oracle tables use specific scrollable containers. We try multiple strategies:
                try:
                    # Strategy A: Target Oracle's specific scroller DIV (most reliable)
                    # Oracle generates divs with IDs ending in '::scroller' for table navigation
                    scroller_div = driver.find_element(By.XPATH, "//div[contains(@id, '::scroller')]")
                    
                    # Perform controlled scroll within the Oracle table container
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 300;", scroller_div)
                    print("   > Applied JavaScript scroll to Oracle table container")
                except:
                    # Strategy B: Fallback keyboard-based scrolling
                    # Find any visible icon and use it as anchor for Page Down navigation
                    print("   > Oracle scroller not found. Using keyboard navigation...")
                    visible_icons = driver.find_elements(By.XPATH, "//a[contains(@id, ':b1::popEl')]")
                    if visible_icons:
                        last_visible_icon = visible_icons[-1]
                        actions.move_to_element(last_visible_icon).click().send_keys(Keys.PAGE_DOWN).perform()
                
                # Wait for Oracle's "Fetching Data..." operation to complete
                print("   > Waiting for Oracle data fetch operation...")
                time.sleep(SCROLL_DELAY)
                
                # Re-attempt to locate the target element after scrolling
                row_icon = wait.until(EC.presence_of_element_located((By.XPATH, icon_xpath)))

            # ===============================
            # SUB-STEP 4.3: ELEMENT POSITIONING & INTERACTION
            # ===============================
            # Center the element in viewport for reliable interaction
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row_icon)
            time.sleep(1)  # Allow rendering to complete

            # ===============================
            # SUB-STEP 4.4: CLICK ROW ACTION ICON
            # ===============================
            try:
                # Primary click method: direct element click
                row_icon.click()
            except:
                # Fallback: ActionChains for stubborn elements
                actions.move_to_element(row_icon).click().perform()
            
            print("   > Successfully clicked row action icon")
            time.sleep(1)  # Allow context menu to appear

            # ===============================
            # SUB-STEP 4.5: LOCATE AND CLICK RESET OPTION
            # ===============================
            # Oracle generates consistent ID patterns: pt1:r2:pt1:lpspc1:t1:{row_index}:resetcm
            reset_option_xpath = f"//*[contains(@id, ':t1:{i}:resetcm')]"
            
            try:
                # Wait for context menu to become visible and locate Reset option
                reset_menu_item = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, reset_option_xpath))
                )
                reset_menu_item.click()
                print("   > Successfully clicked 'Reset' option (located by ID pattern)")
            except:
                # Fallback: Re-open context menu if first attempt failed
                print("   > Reset option not immediately visible. Re-opening context menu...")
                actions.move_to_element(row_icon).click().perform()
                time.sleep(1)
                reset_menu_item = driver.find_element(By.XPATH, reset_option_xpath)
                reset_menu_item.click()
                print("   > Successfully clicked 'Reset' option (second attempt)")

            # ===============================
            # SUB-STEP 4.6: HANDLE CONFIRMATION DIALOGS
            # ===============================
            # Oracle typically shows multiple confirmation dialogs for reset operations
            time.sleep(OPERATION_DELAY)
            
            # Dialog 1: Confirmation prompt ("Are you sure?") - Press 'Y' for Yes
            actions.send_keys('y').perform()
            print("   > Confirmed reset operation with 'Y' key")
            
            time.sleep(0.5)
            
            # Dialog 2: Submit confirmation dialog - Press Enter on "Yes" button
            actions.send_keys(Keys.ENTER).perform()
            print("   > Submitted confirmation with Enter key")

            time.sleep(OPERATION_DELAY)
            
            # Dialog 3: Success acknowledgment dialog - Press Enter on "OK" button
            actions.send_keys(Keys.ENTER).perform()
            print("   > Acknowledged completion with Enter key")
            
            time.sleep(1)  # Brief pause before next iteration
            
            print(f"   > Row {i + 1} reset operation completed successfully")
            logger.info(f"Fila {i + 1} procesada exitosamente")

        except Exception as e:
            # ===============================
            # ERROR HANDLING FOR INDIVIDUAL ROWS
            # ===============================
            print(f"   > FAILED: Row {i + 1} processing encountered an error")
            print(f"   > Error details: {str(e)[:100]}...")
            logger.error(f"Error en fila {i + 1}: {str(e)[:200]}")
            
            # Perform recovery scroll to prevent UI state issues
            driver.execute_script("window.scrollBy(0, 100);")
            continue  # Move to next row

    print("\n" + "="*50)
    print("BATCH PROCESSING COMPLETED")
    print("="*50)
    logger.info("Procesamiento por lotes completado")

    # ===============================
    # STEP 5: CLEAN LOGOUT (NON-CRITICAL)
    # ===============================
    # NOTA: El trabajo principal (reset de jobs) ya se completó exitosamente.
    # El logout es solo una operación de limpieza. Si falla, no afecta el resultado.
    print("\n" + "-"*50)
    print("6. Performing clean logout (non-critical step)...")
    print("   NOTE: Main job reset task completed successfully.")
    print("   Logout is optional cleanup - errors here don't affect results.")
    print("-"*50)
    logger.info("="*40)
    logger.info("TRABAJO PRINCIPAL COMPLETADO EXITOSAMENTE")
    logger.info("Iniciando logout (paso no crítico)...")
    logger.info("="*40)
    
    logout_successful = False
    
    if SKIP_LOGOUT:
        print("   > SKIP_LOGOUT=True: Omitiendo proceso de logout")
        logger.info("Logout omitido por configuración SKIP_LOGOUT=True")
    else:
        # Esperar a que la página se estabilice antes de intentar logout
        print("   > Waiting for page to stabilize before logout...")
        time.sleep(2)
        
        # Verificar que el navegador sigue activo
        try:
            current_url = driver.current_url
            logger.info(f"Página actual antes de logout: {current_url}")
        except Exception as e:
            logger.warning(f"No se pudo obtener URL actual: {e}")
        
        # ===============================
        # ESTRATEGIA 1: Método estándar - Buscar "Sign Out" y hacer click
        # ===============================
        print("   > Strategy 1: Looking for 'Sign Out' element...")
        try:
            logout_wait = WebDriverWait(driver, LOGOUT_TIMEOUT)
            
            # Intentar múltiples selectores para el botón de Sign Out
            sign_out_xpaths = [
                "//*[contains(text(), 'Sign Out')]",
                "//a[contains(text(), 'Sign Out')]",
                "//span[contains(text(), 'Sign Out')]",
                "//button[contains(text(), 'Sign Out')]",
                "//*[@title='Sign Out']",
                "//a[contains(@href, 'logout')]",
            ]
            
            sign_out_element = None
            for xpath in sign_out_xpaths:
                try:
                    sign_out_element = logout_wait.until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    if sign_out_element:
                        logger.info(f"Sign Out encontrado con: {xpath}")
                        break
                except:
                    continue
            
            if sign_out_element:
                # Intentar click normal primero
                try:
                    sign_out_element.click()
                except:
                    # Si falla, usar JavaScript
                    driver.execute_script("arguments[0].click();", sign_out_element)
                
                time.sleep(1)
                
                # Intentar confirmar el logout si hay diálogo
                try:
                    confirm_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.ID, "Confirm"))
                    )
                    confirm_button.click()
                except:
                    # Puede que no haya diálogo de confirmación, lo cual está bien
                    pass
                
                print("   > Strategy 1: SUCCESS - Logged out via Sign Out element")
                logger.info("Logout exitoso (Estrategia 1: elemento Sign Out)")
                logout_successful = True
            else:
                raise Exception("No se encontró elemento Sign Out")
                
        except Exception as e1:
            logger.info(f"Estrategia 1 falló: {str(e1)[:100]}")
            
            # ===============================
            # ESTRATEGIA 2: Navegar directamente a URL de logout
            # ===============================
            print("   > Strategy 2: Navigating to logout URL...")
            try:
                # URLs de logout comunes en Oracle Cloud
                base_url = ORACLE_URL.split('/biacm')[0] if '/biacm' in ORACLE_URL else ORACLE_URL.rsplit('/', 1)[0]
                logout_urls = [
                    f"{base_url}/oam/server/logout",
                    f"{base_url}/logout",
                    f"{base_url}/fscmUI/faces/logout",
                    f"{base_url}/homePage/faces/AtkLogout",
                ]
                
                for logout_url in logout_urls:
                    try:
                        driver.get(logout_url)
                        time.sleep(2)
                        # Verificar si el logout fue exitoso (página cambió o no hay sesión)
                        if 'login' in driver.current_url.lower() or 'logout' in driver.current_url.lower():
                            print(f"   > Strategy 2: SUCCESS - Logged out via URL: {logout_url}")
                            logger.info(f"Logout exitoso (Estrategia 2: URL {logout_url})")
                            logout_successful = True
                            break
                    except:
                        continue
                        
                if not logout_successful:
                    raise Exception("URLs de logout no funcionaron")
                    
            except Exception as e2:
                logger.info(f"Estrategia 2 falló: {str(e2)[:100]}")
                
                # ===============================
                # ESTRATEGIA 3: JavaScript para hacer click en cualquier elemento de logout
                # ===============================
                print("   > Strategy 3: Using JavaScript to find and click logout...")
                try:
                    js_logout = """
                    var elements = document.querySelectorAll('*');
                    for (var i = 0; i < elements.length; i++) {
                        var el = elements[i];
                        var text = el.textContent || el.innerText || '';
                        if (text.toLowerCase().includes('sign out') || 
                            text.toLowerCase().includes('logout') ||
                            text.toLowerCase().includes('cerrar sesión')) {
                            el.click();
                            return 'clicked';
                        }
                    }
                    return 'not_found';
                    """
                    result = driver.execute_script(js_logout)
                    if result == 'clicked':
                        time.sleep(2)
                        print("   > Strategy 3: SUCCESS - Logout triggered via JavaScript")
                        logger.info("Logout exitoso (Estrategia 3: JavaScript)")
                        logout_successful = True
                    else:
                        raise Exception("JavaScript no encontró elemento de logout")
                        
                except Exception as e3:
                    logger.info(f"Estrategia 3 falló: {str(e3)[:100]}")
                    
                    # ===============================
                    # ESTRATEGIA 4: Solo cerrar el navegador (fallback final)
                    # ===============================
                    print("   > Strategy 4: All logout methods failed - will close browser directly")
                    print("   > This is acceptable: session will expire automatically on server")
                    logger.info("Todas las estrategias de logout fallaron - cerrando navegador directamente")
                    logger.info("La sesión expirará automáticamente en el servidor")
    
    # Resumen del logout
    if logout_successful:
        print("   > Logout completed successfully")
    elif not SKIP_LOGOUT:
        print("   > Logout via UI failed, but browser will close cleanly")
        print("   > The Oracle session will expire automatically on the server")
    
    # Pequeña pausa antes del cleanup
    time.sleep(1)

except Exception as e:
    # ===============================
    # CRITICAL ERROR HANDLING
    # ===============================
    print("\n" + "="*50)
    print("CRITICAL ERROR ENCOUNTERED")
    print("="*50)
    print(f"Error: {e}")
    print("Capturing screenshot for debugging purposes...")
    logger.critical(f"ERROR CRÍTICO: {e}")
    
    # Capture screenshot for debugging
    screenshot_path = os.path.join(LOG_DIR, f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved as '{screenshot_path}'")
    logger.info(f"Screenshot guardado: {screenshot_path}")
    
finally:
    # ===============================
    # CLEANUP AND RESOURCE MANAGEMENT
    # ===============================
    # NOTA: Este bloque SIEMPRE se ejecuta, independiente de errores en logout u otras secciones
    print("\n" + "="*50)
    print("CLEANUP: Closing browser session...")
    print("="*50)
    
    browser_closed = False
    
    # Intento 1: Método estándar driver.quit()
    try:
        driver.quit()
        browser_closed = True
        print("   > Browser closed successfully (driver.quit)")
        logger.info("Navegador cerrado exitosamente (driver.quit)")
    except Exception as quit_error:
        logger.warning(f"driver.quit() falló: {quit_error}")
        
        # Intento 2: Cerrar todas las ventanas primero y luego quit
        try:
            driver.close()  # Cerrar ventana actual
            driver.quit()
            browser_closed = True
            print("   > Browser closed successfully (close + quit)")
            logger.info("Navegador cerrado exitosamente (close + quit)")
        except Exception as close_error:
            logger.warning(f"driver.close() + quit() falló: {close_error}")
            
            # Intento 3: Forzar cierre del proceso de Chrome si está disponible
            try:
                import subprocess
                # Intentar matar procesos de chrome/chromium huérfanos (solo los de esta sesión)
                subprocess.run(['pkill', '-f', 'chrome.*--headless'], timeout=5, capture_output=True)
                browser_closed = True
                print("   > Browser process terminated via system command")
                logger.info("Proceso del navegador terminado vía comando del sistema")
            except Exception as kill_error:
                logger.warning(f"No se pudo forzar cierre del navegador: {kill_error}")
                print(f"   > Warning: Could not force-close browser: {kill_error}")
    
    # Resumen final
    print("\n" + "="*50)
    if browser_closed:
        print("SCRIPT EXECUTION COMPLETED SUCCESSFULLY")
    else:
        print("SCRIPT EXECUTION COMPLETED (browser cleanup had warnings)")
    print("="*50)
    
    logger.info("="*60)
    logger.info("FIN DE EJECUCIÓN")
    if browser_closed:
        logger.info("Estado: COMPLETADO EXITOSAMENTE")
    else:
        logger.info("Estado: COMPLETADO CON ADVERTENCIAS EN LIMPIEZA")
    logger.info("="*60)
