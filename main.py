import os
import random
import time
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


## ===== PROXY CONFIGURATION ===== ##
PROXY_HOST = os.getenv('PROXY_HOST_')
PROXY_PORT = os.getenv('PROXY_PORT_')
PROXY_USER = os.getenv('PROXY_USER_')
PROXY_PASS = os.getenv('PROXY_PASS_')


# Create a proxy authentication extension
def create_proxy_auth_extension(proxy_host, proxy_port, proxy_user, proxy_pass, scheme='socks5'):
    """Create a Chrome proxy authentication extension"""
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "%s",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
    );
    """ % (scheme, proxy_host, proxy_port, proxy_user, proxy_pass)

    # Create a temporary directory to store extension files
    extension_dir = 'proxy_auth_extension'
    os.makedirs(extension_dir, exist_ok=True)
    
    # Write files
    with open(os.path.join(extension_dir, "manifest.json"), "w") as f:
        f.write(manifest_json)
    with open(os.path.join(extension_dir, "background.js"), "w") as f:
        f.write(background_js)
    
    # Create ZIP file
    extension_path = 'proxy_auth.zip'
    with zipfile.ZipFile(extension_path, 'w') as zp:
        zp.write(os.path.join(extension_dir, "manifest.json"), "manifest.json")
        zp.write(os.path.join(extension_dir, "background.js"), "background.js")
    
    return extension_path

## ===== BROWSER CONFIGURATION ===== ##
def get_driver():
    """Configure and return a Chrome WebDriver with anti-detection measures"""
    
    # Create proxy auth extension
    proxy_extension = create_proxy_auth_extension(
        PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS
    )
    
    # User-Agent rotation
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    ]
    
    # Set up Chrome options
    chrome_options = Options()
    
    # Proxy and extension
    chrome_options.add_extension(proxy_extension)
    
    # Anti-detection settings
    chrome_options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Additional settings
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-notifications')
    
    # Initialize driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Execute CDP commands to prevent detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            window.chrome = {
                runtime: {},
                // etc.
            };
        """
    })
    
    return driver

## ===== SCRAPING FUNCTIONS ===== ##
def human_like_interaction(driver):
    """Simulate human-like behavior"""
    try:
        # Random mouse movements
        actions = ActionChains(driver)
        for _ in range(random.randint(2, 5)):
            x_offset = random.randint(0, 200)
            y_offset = random.randint(0, 200)
            actions.move_by_offset(x_offset, y_offset).perform()
            time.sleep(random.uniform(0.2, 0.5))
        
        # Random scrolling
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(random.randint(1, 3)):
            scroll_amount = random.randint(300, 800)
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(random.uniform(0.5, 1.5))
        
        # Random wait time
        time.sleep(random.uniform(1, 3))
    except Exception:
        pass


def scrape_page(driver, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver.get(url)
            time.sleep(random.uniform(2, 5))
            human_like_interaction(driver)
            
            # Initialize data structure
            results = {
                'airline_info': [],
                'aircraft_info': [],
                'image_urls': []
            }
            
            # Extract airline and aircraft information
            content_blocks = driver.find_elements(By.CSS_SELECTOR, '.ps-v2-results-col-content-primary')
            for block in content_blocks:
                try:
                    # Extract airline information
                    airline_element = block.find_element(By.CSS_SELECTOR, 'div.ps-v2-results-display-detail-no-wrapping:nth-child(1) a')
                    results['airline_info'].append(airline_element.text.strip())
                except:
                    results['airline_info'].append('N/A')
                
                try:
                    # Extract aircraft information
                    aircraft_element = block.find_element(By.CSS_SELECTOR, 'div.ps-v2-results-display-detail-no-wrapping:nth-child(2) a')
                    results['aircraft_info'].append(aircraft_element.text.strip())
                except:
                    results['aircraft_info'].append('N/A')
            
         
            # Extract image URLs using a different approach
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.lazy-load')
            for img in image_elements:
                src = img.get_attribute('src')
                if src and 'airliners.net' in src:
                    results['image_urls'].append(src)


         
            return results
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(5, 15))
            else:
                raise

#save to data to csv
def save_to_csv(data, filename):
    import csv
    """Save scraped data to a CSV file"""
    with open(filename, 'a+', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #writer.writerow(['Airline', 'Aircraft', 'Image URL'])
        for i, (airline, aircraft, url) in enumerate(zip(data['airline_info'], data['aircraft_info'], data['image_urls']), 1):
            writer.writerow([airline, aircraft, url])
def main():
    driver = None
    try:
        driver = get_driver()
        
        # Verify proxy
        print("Testing proxy connection...")
        driver.get("https://ipv4.webshare.io/")
        print("Proxy IP:", driver.find_element(By.TAG_NAME, 'body').text)
        
        # Scrape airliners.net
        for i in range(12, 13):
            url = f"https://www.airliners.net/search?page={i}"
            print(f"Accessing {url}...")
            scraped_data = scrape_page(driver, url)
            

            # Save data to CSV
            #make name update with timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d")
            filename = f"scraped_data_{timestamp}.csv"
            save_to_csv(scraped_data, filename)
     
        
        # Print results
        print("\n=== Scraping Results ===")
        print(f"\nFound {len(scraped_data['image_urls'])} images:")
        for i, url in enumerate(scraped_data['image_urls'][:20], 1):
            print(f"{i}. {url}")
        
        print("\nFound airline information:")
        for i, (airline, aircraft) in enumerate(zip(scraped_data['airline_info'], scraped_data['aircraft_info']), 1):
            print(f"{i}. Airline: {airline} | Aircraft: {aircraft}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if driver:
            driver.save_screenshot('error.png')
            print("Screenshot saved to error.png")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()