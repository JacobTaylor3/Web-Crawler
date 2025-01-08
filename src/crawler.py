from bs4 import BeautifulSoup

import requests

from urllib.parse import urlparse, urljoin, urlunparse


#go over if I should catch the ejection for a get request and continue the program not terminate it. Like in the get request

def getHtml(url: str):  # add in if the http is not included format the url
    PREFIX = "https://"  # update this so we only validate urls also update for http
    if not any(ext in url for ext in [".com", ".org", ".net"]):
        raise Exception("Not a website/valid URL")

    if PREFIX not in url:
        url = PREFIX + url

    try:
        response = requests.get(url=url)

        response.raise_for_status()

        if response.ok:
            return response.text
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.reason}"
            )

    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")


def crawHtmlForForms(html: str):
    forms = BeautifulSoup(html, "html.parser").find_all("form")

    if len(forms) == 0:
        raise Exception("No forms found in the HTML. Cannot proceed.")

    else:
        return forms


# recursively find all links to a website
def crawlWebsite(rootUrl: str) -> list:
    return crawlerHelper(set(), rootUrl)


def crawlerHelper(setUrl: set, listOfLinks:list, url: str) -> list:
    # base case
    if url in set or len(set) == 500 or urlDepth(url) > 3:
        return list
    
    setUrl.add(url)
    responseHtml = getHtml(url)
    
    hrefList = BeautifulSoup(responseHtml, "html.parser").find_all("a")
    
    if len(hrefList) ==0:
        return list
    
    else:
        for href in hrefList:
           data =  href.get("href")
           listOfLinks.append(data)
    
    return crawlerHelper(setUrl,listOfLinks,listOfLinks.pop()) #need to figure out this logic

    #maybe return a list of urls that are closure like [crawlerHelper(url),crawlerHelper(url),crawlerHelper(url)]
    
        
# -1 if not a valid url
def urlDepth(url: str) -> int:
    urlPath = urlparse(url).path

    return len(list(filter(None, urlPath.split("/"))))


def normalizeUrl(base_url: str, relative_url: str) -> str:
    """
    Normalize a URL by combining a base URL with a relative URL
    and ensuring the resulting URL is consistent and complete.

    Args:
        base_url (str): The base URL (e.g., the page where the relative URL was found).
        relative_url (str): The relative or inconsistent URL to be normalized.

    Returns:
        str: A normalized, absolute URL.
    """
    # Combine base and relative URLs
    absolute_url = urljoin(base_url, relative_url)

    # Parse the combined URL to handle fragments and inconsistencies
    parsed_url = urlparse(absolute_url)

    # Rebuild the URL without fragments and redundant components
    normalized_url = urlunparse(
        (
            parsed_url.scheme,  # Keep the scheme (e.g., http, https)
            parsed_url.netloc,  # Keep the network location (e.g., example.com)
            parsed_url.path,  # Keep the path (e.g., /about)
            "",  # Clear params (rarely used in modern URLs)
            parsed_url.query,  # Keep query parameters (e.g., ?key=value)
            "",  # Remove fragment (e.g., #section)
        )
    )

    return normalized_url

list1 = list()
crawlerHelper(set(),list1,"https://fantasyislandsalem.com")
print(list1)
