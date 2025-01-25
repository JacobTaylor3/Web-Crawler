import httpx
import logging
import asyncio
import utils

from tabulate import tabulate

utils.enableLogging()




async def sendRequest(url: str):
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
            logging.info(
                f" Received Response for {url} status code: {response.status_code} Time elapsed: {response._elapsed.total_seconds()} seconds "
            )
            return {"url": url, "statusCode": response.status_code}

    except httpx.RequestError as error:
        logging.error(f"Request failed for {url}. Error: {str(error)}")
        return {"url": url, "statusCode": -1}


def generateLinks(filePath: str):
    try:
        with open(filePath, "r") as file:
            wordlist = file.read().splitlines()
            return [
                element.strip()
                for element in wordlist
                if element.strip() and not element.startswith("#")
            ]

    except FileNotFoundError as e:
        print(e.filename)


async def bruteForceWordList(wordlist: list, baseUrl: str):
    responses = []
    for word in wordlist:
        responses.append(await sendRequest(baseUrl + word))

    return responses

def filterResponse(responses,statusCode:int):
    
    return [element for element in responses if element["statusCode"] == statusCode]



response = asyncio.run(
        bruteForceWordList(
            generateLinks("files\\wordlists\\wordpress.txt"), "https://spillaneandson.com"
        )
    )

print(tabulate(filterResponse(response,200), headers="keys", tablefmt="grid"))

#look into ways where we can limit requests sent to the server. Rate limiting