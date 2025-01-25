from bs4 import BeautifulSoup

from urllib.parse import urlparse, urljoin, urlunparse

import utils

import logging

import httpx

import asyncio

import time

# Configure logging

utils.enableLogging()


async def formClosure(link: str):
    try:
        return {
            link: BeautifulSoup(await getHtml(link), "html.parser").find_all("form")
        }
    except Exception:
        return {link: []}


async def crawHtmlForForms(
    linksSet: set,
):  # async this send out all the http requests at once.
    logging.info("Crawl Finished")

    results = await asyncio.gather(*(formClosure(link) for link in linksSet))

    return {key: value for d in results for key, value in d.items() if value}


async def extractDataForms(data: dict):
    pass


# recursively find all links to a website
async def crawlWebsite(url: str, max_depth) -> list:
    return await crawlerHelper(
        set(),
        set(),
        url.strip("/"),
        urlparse(url).scheme + "://" + urlparse(url).netloc,
        max_depth=max_depth,
    )


async def crawlerHelper(
    seen: set, setLinks: set, url: str, baseDomain: str, max_depth: int
) -> set:
    # base case
    if url in seen or len(seen) == 50 or urlDepth(url) > max_depth:  #
        return setLinks

    seen.add(url)

    try:
        responseHtml = await getHtml(url)
        setLinks.add(url)
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
            updateLink = normalizeUrl(baseDomain, data).lower().rstrip("/")
            if isValidUrl(updateLink, baseDomain) and updateLink not in seen:
                setLinks.add(updateLink)

        for link in setLinks:  # if link not in seen:
            await crawlerHelper(seen, setLinks, link, baseDomain, max_depth=max_depth)
        return setLinks


def urlDepth(url: str) -> int:
    return len(list(filter(None, urlparse(url).path.split("/"))))


def isValidUrl(url: str, baseDomain):
    return (
        not url.lower().endswith(tuple(utils.FILETYPES))
        and urlparse(url).scheme + "://" + urlparse(url).netloc == baseDomain
    )


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


def checkLink(url: str):
    HTTPS = "https://"
    HTTP = "http://"
    if not any(ext in url for ext in [".com", ".org", ".net"]):
        logging.error(f"'{url}' is Not a website/valid URL")
        raise Exception("Not a  valid website/valid URL")

    if not (url.startswith(HTTPS) or url.startswith(HTTP)):
        return "".join(HTTPS + url)
    return url


# ex google.com/robots.txt
async def crawlRobotTxt(url: str, baseurl: str):
    html = await getHtml(url)

    filtered = [
        x
        for x in [
            x.removeprefix("Disallow:")
            .removeprefix("Allow:")
            .removeprefix("Sitemap:")
            .strip()
            for x in html.split("\n")
            if x.strip()
        ]
        if not x.startswith("User-agent:") and "#" not in x
    ]

    fullpath = [
        # Keep the original link if it starts with "http://" or "https://"
        x
        if x.startswith("http://") or x.startswith("https://")
        # Otherwise, add "https://" + baseurl
        else f"https://{baseurl}{x}"
        for x in filtered
    ]

    return fullpath


async def getHtml(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url, headers=headers, follow_redirects=True, timeout=10
            )
            response.raise_for_status()
            # Raise an exception for HTTP errors
            logging.info(
                f" Received Response for {url} Time elapsed: {response._elapsed.total_seconds()} seconds "
            )
            return response.text
    except httpx.HTTPStatusError:
        raise Exception(
            f"Request failed for {url} with status code {response.status_code}"
        )
    except httpx.RequestError as error:
        logging.error(f"Request failed for {url}. Error: {str(error)}")
        raise


async def main(url):
    crawlResults = await crawlWebsite(url, 3)
    return await crawHtmlForForms(crawlResults)


# if __name__ == "__main__":
# start_time = time.time()
# print(asyncio.run(main(checkLink("https://spillaneandson.com"))))
# total_time = time.time() - start_time
# logging.info(f"Program Finished in: {total_time} seconds")

asyncio.run(crawlRobotTxt("https://google.com/robots.txt", "google.com"))


# normalize url only works when theres a protocol https or http but our functions parse.netloc does not include it so the valid url function and normalize function doesnt work
# fixed this by prepending the protocol and "://" to a link maybe modularize so its cleaner? maybe some edge cases im not thinking off
# Need to check the url to see if its valid or not like urls without a protocol or .com to either add the protocol or terminate for user input
# Right now this only works when the protocol is included doesn't if not

# if the user wants to crawl the robots.txt just add it to the set of links
