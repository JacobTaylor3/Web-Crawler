from bs4 import BeautifulSoup

import requests

from urllib.parse import urlparse, urljoin, urlunparse

import utils


# go over if I should catch the ejection for a get request and continue the program not terminate it. Like in the get request


def getHtml(url: str):  # add in if the http is not included format the url
    PREFIX = "https://"  # update this so we only validate urls also update for http
    if not any(ext in url for ext in [".com", ".org", ".net"]):
        raise Exception("Not a website/valid URL")

    if PREFIX not in url:
        url = PREFIX + url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com",
        }

        response = requests.get(
            url=url, allow_redirects=True, timeout=10, headers=headers
        )

        response.raise_for_status()

        if response.ok:
            return response.text
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.reason}"
            )

    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        raise


def crawHtmlForForms(
    linksSet: set,
):  # async this send out all the http requests at once.
    dictForms = {}
    for link in linksSet:
        try:
            dictForms[link] = BeautifulSoup(getHtml(link), "html.parser").find_all(
                "form"
            )

        except Exception:
            continue
    return {k: v for k, v in dictForms.items() if v != []}


def extractDataForms(data: dict):
    pass


# recursively find all links to a website
def crawlWebsite(url: str) -> list:
    return crawlerHelper(
        set(),
        set(),
        url.strip("/"),
        urlparse(url).scheme + "://" + urlparse(url).netloc,
    )


def crawlerHelper(seen: set, setLinks: set, url: str, baseDomain: str) -> set:
    # base case
    if url in seen or len(seen) == 500 or urlDepth(url) > 3:  #
        return setLinks

    seen.add(url)
    setLinks.add(url)

    try:
        responseHtml = getHtml(url)
    except Exception:
        return setLinks

    hrefList = BeautifulSoup(responseHtml, "html.parser").find_all("a")

    if not hrefList:
        return setLinks

    else:
        for href in hrefList:
            data = href.get("href")
            if not data:
                continue
            updateLink = urlPath(data, baseDomain).lower().rstrip("/")
            if isValidUrl(updateLink, baseDomain) and updateLink not in seen:
                setLinks.add(updateLink)

        for link in setLinks:
            return crawlerHelper(seen, setLinks, link, baseDomain)


# -1 if not a valid url
def urlDepth(url: str) -> int:
    urlPath = urlparse(url).path

    return len(list(filter(None, urlPath.split("/"))))


def isValidUrl(url: str, baseDomain):
    return (
        not url.lower().endswith(tuple(utils.FILETYPES))
        and urlparse(url).scheme + "://" + urlparse(url).netloc == baseDomain
    )


def urlPath(url: str, baseDomain: str):
    if (
        urlparse(url).scheme == ""
        and urlparse(url).netloc == ""
        and urlparse(url).path != ""
    ):
        return normalizeUrl(baseDomain, url)  # relative to absolute

    else:
        return url  # absoluteurl


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


data = crawlWebsite("https://www.google.com")
data2 = crawlWebsite("https://google.com")
# print(data)
print(data2)


# normalize url only works when theres a protocal https or http but our functions parse.netloc does not include it so the valid url function and normalize function doesnt work

# Right now this only works when the protocal is included doesnt if not
