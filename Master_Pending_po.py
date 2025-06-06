from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import re
from pathlib import Path
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime  # 🔹 Import for timestamp
from selenium.common.exceptions import TimeoutException
import time

# === Setup: download directory ===
download_dir = r"C:\Users\Ariful\Desktop\selenium_download_file\Inventory_report_download"
os.makedirs(download_dir, exist_ok=True)

chrome_options = webdriver.ChromeOptions()
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # 🔹 Run Chrome in headless mode
# chrome_options.add_argument("--disable-gpu")  # Optional: disable GPU usage
# chrome_options.add_argument("--window-size=1920,1080")  # Optional: set window size for full rendering
# chrome_options.add_argument("--no-sandbox")  # Optional: for Linux environments
# chrome_options.add_argument("--disable-dev-shm-usage")  # Optional: prevents crashes on some systems
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

pattern = "Purchase Order (purchase.order)"

def is_file_downloaded():
    return any(Path(download_dir).glob(f"*{pattern}*.xlsx"))


def click_when_clickable(driver, xpath, timeout=10):
    """
    Clicks an element when it becomes clickable.

    Parameters:
        driver: The Selenium WebDriver instance.
        xpath (str): The XPath of the element to click.
        timeout (int): Max seconds to wait for the element. Default is 10.
    """
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

def try_full_export_flow(driver):
    try:
        # Try full flow with "Select All"
        click_when_clickable(driver, "/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/span/a[1]")  # Select All
        time.sleep(2)
        
        click_when_clickable(driver, "/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[2]/button")  # Action
        time.sleep(2)
        
        click_when_clickable(driver, "/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/span[1]")  # Export
        time.sleep(2)
        
        click_when_clickable(driver, "/html/body/div[2]/div[2]/div/div/div/div/main/div/div[2]/div[3]/div/select")  # Template dropdown
        time.sleep(2)
        
        click_when_clickable(driver, "/html/body/div[2]/div[2]/div/div/div/div/main/div/div[2]/div[3]/div/select/option[2]")  # Ariful template
        time.sleep(5)
        
        click_when_clickable(driver, "/html/body/div[2]/div[2]/div/div/div/div/footer/button[1]")  # Final Export
        time.sleep(5)
        
        print("✅ Export completed using Select All flow.")

    except TimeoutException:
        print("⚠️ Select All not available, falling back to export without selection.")

        # Fallback export flow without "Select All"
        try:
            click_when_clickable(driver, "/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[2]/button")  # Action
            time.sleep(2)
            
            click_when_clickable(driver, "/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/span[1]")  # Export
            time.sleep(2)
            
            click_when_clickable(driver, "/html/body/div[2]/div[2]/div/div/div/div/main/div/div[2]/div[3]/div/select")  # Template dropdown
            time.sleep(2)
            
            click_when_clickable(driver, "/html/body/div[2]/div[2]/div/div/div/div/main/div/div[2]/div[3]/div/select/option[2]")  # Ariful template
            time.sleep(5)
            
            click_when_clickable(driver, "/html/body/div[2]/div[2]/div/div/div/div/footer/button[1]")  # Final Export
            time.sleep(5)
            
            print("✅ Export completed using fallback flow.")

        except TimeoutException:
            print("❌ Both export flows failed. Please check element paths or page state.")


def same_work():
    
    # click on Action Button 
    click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[2]/button")
    time.sleep(2)
    # Click on Export button 
    click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/span[1]")
    time.sleep(2)
    # Click on select plate to show my tamplate 
    click_when_clickable(driver, "/html/body/div[2]/div[2]/div/div/div/div/main/div/div[2]/div[3]/div/select")
    time.sleep(2)
    # Click on Ariful tamplate 
    click_when_clickable(driver, "/html/body/div[2]/div[2]/div/div/div/div/main/div/div[2]/div[3]/div/select/option[2]")
    time.sleep(5)
    # Click on Export button
    click_when_clickable(driver,"/html/body/div[2]/div[2]/div/div/div/div/footer/button[1]")
    time.sleep(5)

def element_exists(driver, xpath):
    return len(driver.find_elements(By.XPATH, xpath)) > 0

def are_both_texts_present(driver, text):
    page = driver.page_source.lower()
    return text.lower() in page



def kurram_sir_pending():
    # Clic one down arrow to select apporver list 
    click_when_clickable (driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/button")
    
    # Click on kurram sir pending po
    click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div/div[3]/span[7]/span/span")
    time.sleep(5)
    # Click on panel to shwo bdt and use rfq 
    click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr/th[1]/div/span")
    
    # # click on usd or bdt
    click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[2]/th[1]/div/span")
    
    has_first = False
    has_second = False
    
    if are_both_texts_present(driver,"usd"):
        print("'usd' are present on the page.")
        has_first = True
        
    
    if are_both_texts_present(driver,"bdt"):
        print("'bdt' are present on the page.")
        has_second = True    
    else:
        print("Nothing present")
     
    if has_first and has_second:
        print("✅ Both elements exist – running full export flow.")
        # Click on input/check box 
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[3]/td[1]/div/input")
        # Click on all the checkbox
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/thead/tr/th[1]/div/input")
        time.sleep(2)
        # click on select all
        click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/span/a[1]")
        time.sleep(2)
        same_work()
        

    elif has_first or has_second:
        print("⚠️ Only one element exists – running partial export flow.")
        # Click on input/check box 
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[3]/td[1]/div/input")
        # Click on all the checkbox
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/thead/tr/th[1]/div/input")
        time.sleep(2)
        
        same_work()
        
    
def shahid_sir_pending():
    
    # Clic one down arrow to select apporver list 
    click_when_clickable (driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/button")
    # Click on Shahid sir pending po
    click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div/div[3]/span[13]/span/span")
    time.sleep(5)
    # click on usd or bdt 
    click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr/th[1]/div/span")
    # click on usd or bdt
    time.sleep(2)
    # Click on raw material
    click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[2]/th[1]/div/span")
    
    has_first = False
    has_second = False
    
    if are_both_texts_present(driver,"usd"):
        print("'usd' are present on the page.")
        has_first = True
    if are_both_texts_present(driver,"bdt"):
        print("'bdt' are present on the page.")
        has_second = True    
    else:
        print("Nothing present")
 

     
    if has_first and has_second:
        print("✅ Both elements exist – running full export flow.")
        # Click on input/check box 
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[3]/td[1]/div/input")
        # Click on all the checkbox
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/thead/tr/th[1]/div/input")
        time.sleep(2)
        # click on select all
        click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/span/a[1]")
        time.sleep(2)
        same_work() 
    elif has_first or has_second:
        print("⚠️ Only one element exists – running partial export flow.")
        # Click on input/check box 
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[3]/td[1]/div/input")
        # Click on all the checkbox
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/thead/tr/th[1]/div/input")
        time.sleep(2)
        same_work()
    
        
   
   
def suranjan_sir_pending():
    

     # Clic one down arrow to select apporver list 
    click_when_clickable (driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/button")
    
    # Click on suranjan sir pending po
    click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div/div[3]/span[14]/span/span")
    time.sleep(5)
    # click on usd or bdt
    click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[2]/th[1]/div/span")
    time.sleep(5)
    
    # usd = "/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[2]/th[1]/div/span"
    # bdt = "/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[1]/th[1]/div/span"
    
    has_first = False
    has_second = False
    
    if are_both_texts_present(driver,"usd"):
        print("'usd' are present on the page.")
        has_first = True
        
    
    if are_both_texts_present(driver,"bdt"):
        print("'bdt' are present on the page.")
        has_second = True    
    else:
        print("Nothing present")
     
    if has_first and has_second:
        print("✅ Both elements exist – running full export flow.")
        # Click on input/check box 
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[3]/td[1]/div/input")
        # Click on all the checkbox
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/thead/tr/th[1]/div/input")
        time.sleep(2)
        # click on select all
        click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/span/a[1]")
        time.sleep(2)
        same_work()
        

    elif has_first or has_second:
        print("⚠️ Only one element exists – running partial export flow.")
        # Click on input/check box 
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[3]/td[1]/div/input")
        # Click on all the checkbox
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/thead/tr/th[1]/div/input")
        time.sleep(2)
        
        same_work()
    
    suranjan_sir = False
        
    
    
def monir_sir_pending():

     # Clic one down arrow to select apporver list 
    click_when_clickable (driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/button")
    
    # Click on Monir sir pending po
    click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div/div[3]/span[8]/span/span")
    time.sleep(5)

    click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr/th[1]/div/span")
    time.sleep(5)
    
    has_first = False
    has_second = False
    
    if are_both_texts_present(driver,"usd"):
        print("'usd' are present on the page.")
        has_first = True
        
    
    if are_both_texts_present(driver,"bdt"):
        print("'bdt' are present on the page.")
        has_second = True    
    else:
        print("Nothing present")
     
    if has_first and has_second:
        print("✅ Both elements exist – running full export flow.")
        # Click on input/check box 
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[3]/td[1]/div/input")
        # Click on all the checkbox
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/thead/tr/th[1]/div/input")
        time.sleep(2)
        # click on select all
        click_when_clickable(driver,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/span/a[1]")
        time.sleep(2)
        same_work()
        

    elif has_first or has_second:
        print("⚠️ Only one element exists – running partial export flow.")
        # Click on input/check box 
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[3]/td[1]/div/input")
        # Click on all the checkbox
        click_when_clickable(driver,"/html/body/div[1]/div/div[2]/div[2]/table/thead/tr/th[1]/div/input")
        time.sleep(2)
        
        same_work()
    monir_sir = True


while True:
    try:
        # === Start driver ===
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        wait = WebDriverWait(driver, 20)

        # === Step 1: Log into Odoo ===
        driver.get("https://taps.odoo.com")
        wait.until(EC.presence_of_element_located((By.NAME, "login"))).send_keys("supply.chain3@texzipperbd.com")
        driver.find_element(By.NAME, "password").send_keys("@Shanto@86")
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]").click()
        time.sleep(2)

        # === Step 2: Click user/company switch ===
        time.sleep(2)
        try:
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-backdrop")))
        except:
            pass

        switcher_span = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "div.o_menu_systray div.o_switch_company_menu > button > span"
        )))
        driver.execute_script("arguments[0].scrollIntoView(true);", switcher_span)
        switcher_span.click()
        time.sleep(2)

        # === Step 3: Click 'Zipper' company ===
        target_div = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//div[contains(@class, 'log_into')][span[contains(text(), 'Zipper')]]"
        )))
        driver.execute_script("arguments[0].scrollIntoView(true);", target_div)
        target_div.click()
        time.sleep(2)
        # === Step 4: Navigate to report section ===
        driver.get("https://taps.odoo.com/web#action=529&model=purchase.order&view_type=list&cids=1&menu_id=342")
        wait.until(EC.presence_of_element_located((By.XPATH, "//html")))
        
        shahid_sir_pending()

        # === Step 9: Confirm file downloaded ===
        if is_file_downloaded():
            print("File download complete!")

            # === Step 10: Clean up older files ===
            try:
                files = list(Path(download_dir).glob(f"*{pattern}*.xlsx"))
                if len(files) > 1:
                    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                    for file in files[1:]:
                        file.unlink()
                        print(f"Deleted old file: {file.name}")
                print("File cleanup complete. Only latest report is kept.")
            except Exception as e:
                print(f"Failed during file cleanup: {e}")

            driver.quit()
            break  # Exit loop

        else:
            raise Exception(" File not downloaded. Retrying...")

    except Exception as e:
        print(f"\ Error occurred: {e}\nRetrying in 10 seconds...\n")
        try:
            driver.quit()
        except:
            pass
        time.sleep(5)

# === Step 11: Load latest file and paste to Google Sheet ===
try:
    files = list(Path(download_dir).glob(f"*{pattern}*.xlsx"))
    if not files:
        raise Exception("No matching file found.")

    # Sort and get the latest file
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    latest_file = files[0]
    print(f"Latest file found: {latest_file.name}")

    # Load into DataFrame
    df = pd.read_excel(latest_file)
    print("File loaded into DataFrame.")

    # Setup Google Sheets API
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "smiling-castle-458204-g0-5b5c549533a0.json", scope)
    client = gspread.authorize(creds)

    # Open the sheet and paste the data
    sheet = client.open_by_key("1kD4iCUqEAQsE_CLuv3dFSFNSjD2Hj2dTrE40deGZaK")
    worksheet = sheet.worksheet("Stock_dat")

    # Clear old content (optional)
    worksheet.clear()

    # Paste new data
    set_with_dataframe(worksheet, df)
    print("Data pasted to Google Sheet (Sheet4).")

    # === ✅ Add timestamp to Y2 ===
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.update("W2", [[f"{timestamp}"]])
    print(f"Timestamp written to W2: {timestamp}")

except Exception as e:
    print(f"Error while pasting to Google Sheets: {e}")


