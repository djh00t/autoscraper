from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import json
import time


def debug_print(message, debug):
    if debug:
        print(message)


def scrape(url, endpoint, setup=False, debug=False):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Failed to initialize WebDriver: {e}")
        return None

    debug_print("WebDriver initialized.", debug)

    try:
        driver.execute_cdp_cmd("Network.enable", {})
    except Exception as e:
        print(f"Failed to enable Network tracking: {e}")
        return None

    debug_print("Network tracking enabled.", debug)

    intercepted_json = []

    def intercept_response(response):
        url = response["params"]["response"]["url"]
        if endpoint in url:
            intercepted_json.append(response)

    try:
        driver.execute_cdp_cmd(
            "Network.setRequestInterception",
            {"patterns": [{"urlPattern": "*"}]},
        )
    except Exception as e:
        print(f"Failed to set request interception: {e}")
        return None

    debug_print("Request interception set.", debug)

    setup_data = {"cookies": [], "api_calls": []}

    if setup:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            setup_data["cookies"] = driver.get_cookies()
        except Exception as e:
            print(f"Failed to load URL and collect cookies: {e}")

        for response in intercepted_json:
            api_url = response["params"]["response"]["url"]
            if url.split("//")[1].split("/")[0] in api_url:
                setup_data["api_calls"].append(api_url)

        with open("setup_data.json", "w") as f:
            json.dump(setup_data, f)

        print("Setup data saved to 'setup_data.json'")
        return setup_data

    try:
        driver.get(url)
    except Exception as e:
        print(f"Failed to load URL: {e}")
        return None

    debug_print("URL loaded.", debug)

    time.sleep(5)

    driver.quit()

    json_data = []
    for response in intercepted_json:
        try:
            body = response["params"]["response"].get("body", "{}")
            json_data.append(json.loads(body))
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from response: {response}")

    return json_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape JSON data from a given URL and endpoint."
    )
    parser.add_argument("--url", help="URL to scrape from.", required=True)
    parser.add_argument(
        "--endpoint", help="API endpoint to fetch JSON from.", required=True
    )
    parser.add_argument(
        "--setup",
        help="Set up by collecting cookies and API calls.",
        action="store_true",
    )
    parser.add_argument(
        "--debug", help="Enable debug messages.", action="store_true"
    )

    args = parser.parse_args()

    if args.setup:
        setup_data = scrape(
            args.url, args.endpoint, setup=True, debug=args.debug
        )
    else:
        scraped_json = scrape(
            args.url, args.endpoint, setup=False, debug=args.debug
        )

    if scraped_json:
        print(scraped_json)
    else:
        print("Scraping failed.")
