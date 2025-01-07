from bs4 import BeautifulSoup

import requests


def getResponse(url: str): # add in if the http is not included format the url
    try:
        response = requests.get(url=url)
        response.raise_for_status()

        if response.ok:
            return response.text
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.reason}")


    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        
def crawHtmlForForms(html:str):
    doc = BeautifulSoup(html,"html.parser")
    
    forms = doc.find_all("form")
    
    if len(forms) == 0:
        # search for divs 
        div = doc.find_all("div")
        
        if len(div) == 0:
            raise Exception("No forms found in the HTML. Cannot proceed.")

        print(div) # debugging 
        formsList = []
        for elements in div: 
            
            form = elements.find_all("form")
            if forms:
                formsList.append(form)
                
        if len(formsList) == 0:
            raise Exception("No forms found in the HTML. Cannot proceed.")
        else:
            return formsList

            
                
    else:
        return forms
        
        
    #recursivly find all links to a website
def crawlUrl(rootUrl:str):
    pass
    
    
    

            
            
        
        
        
        
    
    
        
        
print(crawHtmlForForms(getResponse("http://google.com")))
        
        
