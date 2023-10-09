import argparse
import requests
import json
from datetime import datetime
from urllib.parse import urlparse
from get_user_agent_pls import fetch_user_agent

def fetch_headers_and_cookies(url, debug=False, user_agent_browser=None, user_agent_os=None):
    """Fetches headers and cookies from the given URL.

    Args:
        url (str): The URL to fetch headers and cookies from.
        debug (bool): Whether to enable debugging output.
        user_agent_browser (str): The browser to use for the user agent.
        user_agent_os (str): The operating system to use for the user agent.

    Returns:
        tuple: Headers and cookies as dictionaries, along with request headers if debug is enabled.
    """    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }
    
    if user_agent_browser or user_agent_os:
        user_agent = fetch_user_agent(user_agent_browser, user_agent_os)
        headers['User-Agent'] = user_agent

    response = requests.get(url, headers=headers)
    request_headers = dict(response.request.headers) if debug else None

    if debug:
        print(f"DEBUG: Full Request: {response.request.__dict__}")
        print(f"DEBUG: Status Code: {response.status_code}")
        print(f"DEBUG: Response Headers: {response.headers}")

    return response.headers, response.cookies.get_dict(), request_headers

def main():
    """Main function to execute the script."""    
    parser = argparse.ArgumentParser(description='Fetch headers and cookies from a URL.')
    parser.add_argument('--url', required=True, help='URL to fetch headers and cookies from')
    parser.add_argument('--save-as', required=False, help='File name to save headers and cookies to')
    parser.add_argument('--debug', action='store_true', help='Enable debugging output')
    parser.add_argument('--save-html', action='store_true', help='Save the fully rendered HTML page')
    parser.add_argument('--save-html-as', required=False, help='File name to save the fully rendered HTML page to')
    parser.add_argument('--user-agent-browser', choices=['chrome', 'edge', 'firefox', 'safari'], help='Browser to use for the user agent')
    parser.add_argument('--user-agent-os', choices=['windows', 'macos', 'linux'], help='Operating system to use for the user agent')

    args = parser.parse_args()

    parsed_url = urlparse(args.url)
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    domain_name = parsed_url.netloc.replace('.', '_')

    response_headers, cookies, request_headers = fetch_headers_and_cookies(args.url, args.debug, args.user_agent_browser, args.user_agent_os)

    data_to_save = {'response': {'headers': dict(response_headers), 'cookies': cookies}}
    if request_headers:
        data_to_save['request'] = {'headers': request_headers}

    json_filename = args.save_as if args.save_as else f"{current_datetime}-{domain_name}.json"
    with open(json_filename, 'w') as f:
        json.dump(data_to_save, f, indent=4)

    if args.save_html or args.save_html_as:
        response = requests.get(args.url, headers=request_headers)
        html_filename = args.save_html_as if args.save_html_as else f"{current_datetime}-{domain_name}.html"
        with open(html_filename, 'w') as f:
            f.write(response.text)

    print(f"Headers and cookies have been saved to {json_filename}")

if __name__ == "__main__":
    main()
