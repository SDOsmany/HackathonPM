import requests
from bs4 import BeautifulSoup
import re
from bs4.element import Tag  # Import Tag for type checking
import json

LINKS = [
    "https://devpost.com/software/genopets-zs1la5",
    "https://devpost.com/software/find-satoshi",
    "https://devpost.com/software/soapy-finance",
    "https://devpost.com/software/jswap-finance",
    "https://devpost.com/software/darleygo",
    "https://devpost.com/software/pinc-stands-for-personal-inclusive-and-collaborative",
    "https://devpost.com/software/hera-njv7mw",
    "https://devpost.com/software/solanasail",
    "https://devpost.com/software/cryptovend-tablet-ui",
    "https://devpost.com/software/okex-fly-game",
    "https://devpost.com/software/oxs-timelock-staking-app",
    "https://devpost.com/software/customer-experience-shifting-towards-new-normal",
    "https://devpost.com/software/feed-the-need-9a0wcx",
    "https://devpost.com/software/sportsin",
    "https://devpost.com/software/mean-dao",
    "https://devpost.com/software/superpay",
    "https://devpost.com/software/samayal-stuff",
    "https://devpost.com/software/travis-traffic-realtime-assistant-via-internet-service",
    "https://devpost.com/software/nirbhaya",
    "https://devpost.com/software/class-diagrams-for-bitbucket-u7fsp0",
    "https://devpost.com/software/employee-connekt",
    "https://devpost.com/software/demetergift-g8orhs",
    "https://devpost.com/software/urban-reality-the-elevation-of-perfection",
    "https://devpost.com/software/vserveu",
    "https://devpost.com/software/genopets-zs1la5",
    "https://devpost.com/software/find-satoshi",
    "https://devpost.com/software/soapy-finance",
    "https://devpost.com/software/jswap-finance",
    "https://devpost.com/software/darleygo",
    "https://devpost.com/software/pinc-stands-for-personal-inclusive-and-collaborative",
    "https://devpost.com/software/hera-njv7mw",
    "https://devpost.com/software/solanasail",
    "https://devpost.com/software/cryptovend-tablet-ui",
    "https://devpost.com/software/okex-fly-game",
    "https://devpost.com/software/oxs-timelock-staking-app",
    "https://devpost.com/software/customer-experience-shifting-towards-new-normal",
    "https://devpost.com/software/feed-the-need-9a0wcx",
    "https://devpost.com/software/sportsin",
    "https://devpost.com/software/mean-dao",
    "https://devpost.com/software/superpay",
    "https://devpost.com/software/samayal-stuff",
    "https://devpost.com/software/travis-traffic-realtime-assistant-via-internet-service",
    "https://devpost.com/software/nirbhaya",
    "https://devpost.com/software/class-diagrams-for-bitbucket-u7fsp0",
    "https://devpost.com/software/employee-connekt",
    "https://devpost.com/software/demetergift-g8orhs",
    "https://devpost.com/software/urban-reality-the-elevation-of-perfection",
    "https://devpost.com/software/vserveu",
    "https://devpost.com/software/genopets-zs1la5",
    "https://devpost.com/software/find-satoshi",
    "https://devpost.com/software/soapy-finance",
    "https://devpost.com/software/jswap-finance",
    "https://devpost.com/software/darleygo",
    "https://devpost.com/software/pinc-stands-for-personal-inclusive-and-collaborative",
    "https://devpost.com/software/hera-njv7mw",
    "https://devpost.com/software/solanasail",
    "https://devpost.com/software/cryptovend-tablet-ui",
    "https://devpost.com/software/okex-fly-game",
    "https://devpost.com/software/oxs-timelock-staking-app",
    "https://devpost.com/software/customer-experience-shifting-towards-new-normal",
    "https://devpost.com/software/feed-the-need-9a0wcx",
    "https://devpost.com/software/sportsin",
    "https://devpost.com/software/mean-dao",
    "https://devpost.com/software/superpay",
    "https://devpost.com/software/samayal-stuff",
    "https://devpost.com/software/travis-traffic-realtime-assistant-via-internet-service",
    "https://devpost.com/software/nirbhaya",
    "https://devpost.com/software/class-diagrams-for-bitbucket-u7fsp0",
    "https://devpost.com/software/employee-connekt",
    "https://devpost.com/software/demetergift-g8orhs",
    "https://devpost.com/software/urban-reality-the-elevation-of-perfection",
    "https://devpost.com/software/vserveu",
    "https://devpost.com/software/genopets-zs1la5",
    "https://devpost.com/software/find-satoshi",
    "https://devpost.com/software/soapy-finance",
    "https://devpost.com/software/jswap-finance",
    "https://devpost.com/software/darleygo",
    "https://devpost.com/software/pinc-stands-for-personal-inclusive-and-collaborative",
    "https://devpost.com/software/hera-njv7mw",
    "https://devpost.com/software/solanasail",
    "https://devpost.com/software/cryptovend-tablet-ui",
    "https://devpost.com/software/okex-fly-game",
    "https://devpost.com/software/oxs-timelock-staking-app",
    "https://devpost.com/software/customer-experience-shifting-towards-new-normal",
    "https://devpost.com/software/feed-the-need-9a0wcx",
    "https://devpost.com/software/sportsin",
    "https://devpost.com/software/mean-dao",
    "https://devpost.com/software/superpay",
    "https://devpost.com/software/samayal-stuff",
    "https://devpost.com/software/travis-traffic-realtime-assistant-via-internet-service",
    "https://devpost.com/software/nirbhaya",
    "https://devpost.com/software/class-diagrams-for-bitbucket-u7fsp0",
    "https://devpost.com/software/employee-connekt",
    "https://devpost.com/software/demetergift-g8orhs",
    "https://devpost.com/software/urban-reality-the-elevation-of-perfection",
    "https://devpost.com/software/vserveu",
    "https://devpost.com/software/genopets-zs1la5",
    "https://devpost.com/software/find-satoshi",
    "https://devpost.com/software/soapy-finance",
    "https://devpost.com/software/jswap-finance",
    "https://devpost.com/software/darleygo",
    "https://devpost.com/software/pinc-stands-for-personal-inclusive-and-collaborative",
    "https://devpost.com/software/hera-njv7mw",
    "https://devpost.com/software/solanasail",
    "https://devpost.com/software/cryptovend-tablet-ui",
    "https://devpost.com/software/okex-fly-game",
    "https://devpost.com/software/oxs-timelock-staking-app",
    "https://devpost.com/software/customer-experience-shifting-towards-new-normal",
    "https://devpost.com/software/feed-the-need-9a0wcx",
    "https://devpost.com/software/sportsin",
    "https://devpost.com/software/mean-dao",
    "https://devpost.com/software/superpay",
    "https://devpost.com/software/samayal-stuff",
    "https://devpost.com/software/travis-traffic-realtime-assistant-via-internet-service",
    "https://devpost.com/software/nirbhaya",
    "https://devpost.com/software/class-diagrams-for-bitbucket-u7fsp0",
    "https://devpost.com/software/employee-connekt",
    "https://devpost.com/software/demetergift-g8orhs",
    "https://devpost.com/software/urban-reality-the-elevation-of-perfection",
    "https://devpost.com/software/vserveu",
    "https://devpost.com/software/genopets-zs1la5",
    "https://devpost.com/software/find-satoshi",
    "https://devpost.com/software/soapy-finance",
    "https://devpost.com/software/jswap-finance",
    "https://devpost.com/software/darleygo",
    "https://devpost.com/software/pinc-stands-for-personal-inclusive-and-collaborative",
    "https://devpost.com/software/hera-njv7mw",
    "https://devpost.com/software/solanasail",
    "https://devpost.com/software/cryptovend-tablet-ui",
    "https://devpost.com/software/okex-fly-game",
    "https://devpost.com/software/oxs-timelock-staking-app",
    "https://devpost.com/software/customer-experience-shifting-towards-new-normal",
    "https://devpost.com/software/feed-the-need-9a0wcx",
    "https://devpost.com/software/sportsin",
    "https://devpost.com/software/mean-dao",
    "https://devpost.com/software/superpay",
    "https://devpost.com/software/samayal-stuff",
    "https://devpost.com/software/travis-traffic-realtime-assistant-via-internet-service",
    "https://devpost.com/software/nirbhaya",
    "https://devpost.com/software/class-diagrams-for-bitbucket-u7fsp0",
    "https://devpost.com/software/employee-connekt",
    "https://devpost.com/software/demetergift-g8orhs",
    "https://devpost.com/software/urban-reality-the-elevation-of-perfection",
    "https://devpost.com/software/vserveu",
    "https://devpost.com/software/genopets-zs1la5",
    "https://devpost.com/software/find-satoshi",
    "https://devpost.com/software/soapy-finance",
    "https://devpost.com/software/jswap-finance",
    "https://devpost.com/software/darleygo",
    "https://devpost.com/software/pinc-stands-for-personal-inclusive-and-collaborative",
    "https://devpost.com/software/hera-njv7mw",
    "https://devpost.com/software/solanasail",
    "https://devpost.com/software/cryptovend-tablet-ui",
    "https://devpost.com/software/okex-fly-game",
    "https://devpost.com/software/oxs-timelock-staking-app",
    "https://devpost.com/software/customer-experience-shifting-towards-new-normal",
    "https://devpost.com/software/feed-the-need-9a0wcx",
    "https://devpost.com/software/sportsin",
    "https://devpost.com/software/mean-dao",
    "https://devpost.com/software/superpay",
    "https://devpost.com/software/samayal-stuff",
    "https://devpost.com/software/travis-traffic-realtime-assistant-via-internet-service",
    "https://devpost.com/software/nirbhaya",
    "https://devpost.com/software/class-diagrams-for-bitbucket-u7fsp0",
    "https://devpost.com/software/employee-connekt",
    "https://devpost.com/software/demetergift-g8orhs",
    "https://devpost.com/software/urban-reality-the-elevation-of-perfection",
    "https://devpost.com/software/vserveu",
    "https://devpost.com/software/genopets-zs1la5",
    "https://devpost.com/software/find-satoshi",
    "https://devpost.com/software/soapy-finance",
    "https://devpost.com/software/jswap-finance",
    "https://devpost.com/software/darleygo",
    "https://devpost.com/software/pinc-stands-for-personal-inclusive-and-collaborative",
    "https://devpost.com/software/hera-njv7mw",
    "https://devpost.com/software/solanasail",
    "https://devpost.com/software/cryptovend-tablet-ui",
    "https://devpost.com/software/okex-fly-game",
    "https://devpost.com/software/oxs-timelock-staking-app",
    "https://devpost.com/software/customer-experience-shifting-towards-new-normal",
    "https://devpost.com/software/feed-the-need-9a0wcx",
    "https://devpost.com/software/sportsin",
    "https://devpost.com/software/mean-dao",
    "https://devpost.com/software/superpay",
    "https://devpost.com/software/samayal-stuff",
    "https://devpost.com/software/travis-traffic-realtime-assistant-via-internet-service",
    "https://devpost.com/software/nirbhaya",
    "https://devpost.com/software/class-diagrams-for-bitbucket-u7fsp0",
    "https://devpost.com/software/employee-connekt",
    "https://devpost.com/software/demetergift-g8orhs",
    "https://devpost.com/software/urban-reality-the-elevation-of-perfection",
    "https://devpost.com/software/vserveu",
    "https://devpost.com/software/genopets-zs1la5",
    "https://devpost.com/software/find-satoshi",
    "https://devpost.com/software/soapy-finance",
    "https://devpost.com/software/jswap-finance",
    "https://devpost.com/software/darleygo",
    "https://devpost.com/software/pinc-stands-for-personal-inclusive-and-collaborative",
    "https://devpost.com/software/hera-njv7mw",
    "https://devpost.com/software/solanasail",
    "https://devpost.com/software/cryptovend-tablet-ui",
    "https://devpost.com/software/okex-fly-game",
    "https://devpost.com/software/oxs-timelock-staking-app",
    "https://devpost.com/software/customer-experience-shifting-towards-new-normal",
    "https://devpost.com/software/feed-the-need-9a0wcx",
    "https://devpost.com/software/sportsin",
    "https://devpost.com/software/mean-dao",
    "https://devpost.com/software/superpay",
    "https://devpost.com/software/samayal-stuff",
    "https://devpost.com/software/travis-traffic-realtime-assistant-via-internet-service",
    "https://devpost.com/software/nirbhaya",
    "https://devpost.com/software/class-diagrams-for-bitbucket-u7fsp0",
    "https://devpost.com/software/employee-connekt",
    "https://devpost.com/software/demetergift-g8orhs",
    "https://devpost.com/software/urban-reality-the-elevation-of-perfection",
    "https://devpost.com/software/vserveu"
]

def get_devpost_description(devpost_url):
    """
    Fetches and attempts to extract content from the div with id="app-details-left"
    on a Devpost project page.

    Args:
        devpost_url (str): The URL of the Devpost project page.

    Returns:
        str or None: The extracted text content from the specified div,
                     or None if it could not be fetched or the div was not found.
    """
    try:
        # Send a GET request to the Devpost URL
        # Added a User-Agent header to mimic a browser, as some sites block default requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(devpost_url, headers=headers, timeout=10) # Added a timeout and headers
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Find the div with id="app-details-left" ---
        description_container = soup.find('div', id='app-details-left')

        description_text = None
        if description_container:
            # Extract text from the container, preserving line breaks where possible
            description_text = description_container.get_text(separator='\n').strip()
            print(f"Successfully found and extracted content from #app-details-left on {devpost_url}")
        else:
            print(f"Could not find div with id='app-details-left' for {devpost_url}. HTML structure might be different or content is missing.")

        return description_text

    except requests.exceptions.Timeout:
        print(f"Timeout occurred while fetching {devpost_url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching {devpost_url}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while parsing {devpost_url}: {e}")
        return None

d_list = list(map(lambda link: {"url": link, "content": get_devpost_description(link)}, LINKS))
print(f"{d_list=}")
with open("big_data.json", "w") as file:
    json.dump(d_list, file, indent=4)