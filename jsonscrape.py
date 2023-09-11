from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import argparse
import json
import time

def scrape(url, endpoint, driver_path):
    # Initialize Selenium WebDriver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    # Load the page
    driver.get(url)
    
    # Give some time for JavaScript to render
    time.sleep(5)  
    
    # Execute JavaScript to fetch JSON from the endpoint
    js_script = f'''
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '{endpoint}', false);
    xhr.send(null);
    return xhr.responseText;
    '''
    json_data = driver.execute_script(js_script)
    
    # Close the driver
    driver.quit()
    
    # Return JSON
    return json_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape JSON data from a given URL and endpoint.")
    parser.add_argument("--url", help="URL to scrape from.", required=True)
    parser.add_argument("--endpoint", help="API endpoint to fetch JSON from.", required=True)
    parser.add_argument("--driver-path", help="Path to the Chrome WebDriver.", default='./chromedriver')
    
    args = parser.parse_args()
    
    scraped_json = scrape(args.url, args.endpoint, args.driver_path)
    
    # Output the scraped JSON
    print(scraped_json)
