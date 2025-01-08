from bs4 import BeautifulSoup

import requests


def getResponse(url: str):  # add in if the http is not included format the url
    PREFIX = "https://"  # update this so we only validate urls
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


def crawlerHelper(set: set, url: str) -> list:
    pass


def normalizeUrl(relativeUrl: str):
    pass


print(crawHtmlForForms(getResponse("google.com")))
