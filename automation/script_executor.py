"""
Script Executor - Executes JSON automation scripts using Selenium
"""

import json
import os
import time

# Script directory path
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "scripts")


def load_script(script_name):
    """Load a JSON script by name."""
    script_path = os.path.join(SCRIPTS_DIR, f"{script_name}.json")
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script not found: {script_path}")
    
    with open(script_path, "r", encoding="utf-8") as f:
        return json.load(f)


def execute_script(script_name, profile="Default", url=None):
    """
    Execute a JSON automation script.
    
    Args:
        script_name: Name of the script (without .json extension)
        profile: Chrome profile directory name
        url: URL to substitute for {url} placeholder in script
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import sys
    
    # Load credentials for login handling
    from config import MEESHO_EMAIL, MEESHO_PASSWORD
    
    print(f"[ScriptExecutor] Loading script: {script_name}", flush=True)
    script = load_script(script_name)
    
    print(f"[ScriptExecutor] Script: {script.get('name', 'Unnamed')}", flush=True)
    print(f"[ScriptExecutor] Total actions: {len(script.get('actions', []))}", flush=True)
    print(f"[ScriptExecutor] Target URL: {url}", flush=True)
    
    driver = None
    
    try:
        # --- KILL EXISTING CHROME INSTANCES ---
        print("[ScriptExecutor] Closing existing Chrome instances...", flush=True)
        os.system("taskkill /f /im chrome.exe >nul 2>&1")
        time.sleep(3.0)
        
        # --- SETUP CHROME OPTIONS ---
        chrome_options = Options()
        user_data_dir = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        chrome_options.add_argument(f"--profile-directory={profile}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        os.environ['WDM_LOG_LEVEL'] = '0'
        
        # --- LAUNCH BROWSER ---
        print(f"[ScriptExecutor] Launching Chrome with profile: {profile}", flush=True)
        driver = webdriver.Chrome(options=chrome_options)
        
        # Wait for browser to be fully ready
        print("[ScriptExecutor] Browser launched. Waiting for initialization...", flush=True)
        time.sleep(2.0)
        
        wait = WebDriverWait(driver, 30)
        
        # --- EXECUTE ACTIONS ---
        print(f"[ScriptExecutor] Starting action execution...", flush=True)
        for action in script.get("actions", []):
            slno = action.get("slno", "?")
            action_type = action.get("action")
            selector = action.get("selector", "")
            value = action.get("value", "")
            error_msg = action.get("error", f"Error at step {slno}")
            timeout = int(action.get("timeout", 30000)) / 1000  # Convert ms to seconds
            
            # Substitute {url} placeholder
            if value == "{url}" and url:
                value = url
            
            print(f"[Step {slno}] Executing: {action_type}", flush=True)
            
            try:
                if action_type == "goToURL":
                    driver.get(value)
                    
                elif action_type == "wait":
                    wait_ms = int(value)
                    time.sleep(wait_ms / 1000)
                    
                elif action_type == "waitForPageLoad":
                    WebDriverWait(driver, timeout).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )
                    
                elif action_type == "waitUntilVisible":
                    by, locator = _parse_selector(selector)
                    WebDriverWait(driver, timeout).until(
                        EC.visibility_of_element_located((by, locator))
                    )
                    
                elif action_type == "clickElement":
                    by, locator = _parse_selector(selector)
                    element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((by, locator))
                    )
                    driver.execute_script("arguments[0].click();", element)
                    
                elif action_type == "inputText":
                    by, locator = _parse_selector(selector)
                    element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((by, locator))
                    )
                    element.clear()
                    element.send_keys(value)
                    
                elif action_type == "scrollToBottom":
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    
                elif action_type == "scrollIntoView":
                    by, locator = _parse_selector(selector)
                    element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((by, locator))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    
                elif action_type == "checkLoginRequired":
                    _handle_login_if_required(driver, wait, MEESHO_EMAIL, MEESHO_PASSWORD, url)
                    
                else:
                    print(f"[Step {slno}] Unknown action type: {action_type}", flush=True)
                    
                print(f"[Step {slno}] ✓ Completed", flush=True)
                
            except Exception as e:
                print(f"[Step {slno}] ✗ FAILED: {error_msg}", flush=True)
                print(f"[Step {slno}] Exception: {str(e)}", flush=True)
                # Save debug info
                try:
                    with open("debug_script_executor.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print(f"[Step {slno}] Page source saved to debug_script_executor.html", flush=True)
                except:
                    pass
                # Continue to next step instead of failing completely
                continue
        
        print("\n[ScriptExecutor] === AUTOMATION COMPLETE ===", flush=True)
        print("[ScriptExecutor] Browser will remain open for inspection.", flush=True)
        
    except Exception as e:
        print(f"[ScriptExecutor] FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()


def _parse_selector(selector):
    """Parse selector string into Selenium By type and locator."""
    from selenium.webdriver.common.by import By
    
    if selector.startswith("xpath="):
        return By.XPATH, selector[6:]
    elif selector.startswith("css="):
        return By.CSS_SELECTOR, selector[4:]
    elif selector.startswith("id="):
        return By.ID, selector[3:]
    elif selector.startswith("name="):
        return By.NAME, selector[5:]
    elif selector.startswith("class="):
        return By.CLASS_NAME, selector[6:]
    else:
        # Default to XPath for raw selectors
        return By.XPATH, selector


def _handle_login_if_required(driver, wait, email, password, target_url):
    """Check if login is required and handle it."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    
    current_url = driver.current_url.lower()
    print(f"[Login Check] Current URL: {current_url}")
    
    if "login" in current_url or "signin" in current_url or "auth" in current_url:
        print("[Login Check] Login page detected. Attempting login...")
        
        try:
            # Find and fill email
            email_field = wait.until(EC.presence_of_element_located((
                By.XPATH, 
                "//input[@type='email' or @name='email' or contains(@placeholder, 'email') or contains(@placeholder, 'Email')]"
            )))
            email_field.clear()
            email_field.send_keys(email)
            time.sleep(1)
            
            # Find and fill password
            password_field = wait.until(EC.presence_of_element_located((
                By.XPATH,
                "//input[@type='password' or @name='password' or contains(@placeholder, 'password') or contains(@placeholder, 'Password')]"
            )))
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(1)
            
            # Click login button
            login_btn = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign in') or contains(text(), 'Log in')]"
            )))
            driver.execute_script("arguments[0].click();", login_btn)
            
            print("[Login Check] Login submitted. Waiting...")
            time.sleep(5)
            
            # Navigate back to target URL
            if target_url:
                print(f"[Login Check] Navigating to target URL: {target_url}")
                driver.get(target_url)
                wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
                time.sleep(3)
                
        except Exception as e:
            print(f"[Login Check] Auto-login failed: {e}")
            print("[Login Check] Please login manually. Waiting 30 seconds...")
            time.sleep(30)
    else:
        print("[Login Check] No login required.")
