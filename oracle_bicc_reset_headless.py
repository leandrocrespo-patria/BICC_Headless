#!/usr/bin/env python3
"""
BICC Oracle ERP Jobs Reset Automation Script

This script automates the process of resetting Oracle ERP jobs through the web interface.
It performs batch operations on multiple rows in the "Manage Jobs" section of Oracle Cloud.

Author: System Automation Team
Date: February 2026
Version: 3.5-headless

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
ORACLE_PASS = "ORACLE_PASSWORD"                                # Oracle Cloud service account password
ORACLE_URL = "https://emfp-test.fa.us2.oraclecloud.com/biacm"   # Oracle Cloud BICC URL
TOTAL_ROWS = 35                                                 # Number of job rows to process

# Timeout settings (in seconds)
PAGE_LOAD_TIMEOUT = 20                   # Maximum wait time for page elements
OPERATION_DELAY = 2                      # Standard delay between operations
SCROLL_DELAY = 4                         # Wait time after scrolling operations

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
    # STEP 5: CLEAN LOGOUT
    # ===============================
    print("6. Performing clean logout...")
    logger.info("Realizando logout...")
    try:
        # Locate and click the Sign Out button/link
        sign_out_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sign Out')]")))
        driver.execute_script("arguments[0].click();", sign_out_element)
        
        # Confirm logout in the confirmation dialog
        confirm_button = wait.until(EC.element_to_be_clickable((By.ID, "Confirm")))
        confirm_button.click()
        
        print("   > Successfully logged out from Oracle Cloud")
        logger.info("Logout exitoso")
    except Exception as logout_error:
        print(f"   > Logout process failed: {logout_error}")
        logger.warning(f"Error en logout: {logout_error}")
        pass  # Continue with cleanup even if logout fails
    
    time.sleep(5)  # Final wait before cleanup

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
    print("\nPerforming cleanup operations...")
    try:
        driver.quit()  # Properly close browser and free resources
        print("Browser session closed successfully")
        logger.info("Sesión del navegador cerrada")
    except Exception as cleanup_error:
        print(f"Cleanup warning: {cleanup_error}")
        logger.warning(f"Advertencia en limpieza: {cleanup_error}")
    
    print("Script execution completed.")
    logger.info("=" * 60)
    logger.info("FIN DE EJECUCIÓN")
    logger.info("=" * 60)
