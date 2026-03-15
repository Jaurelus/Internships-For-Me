import requests
from bs4 import BeautifulSoup
import pandas as pd

pageNum=1
ucfLink= "https://career.ucf.edu/jobs/page/1/?ctag%5B0%5D=internships&stag%5B0%5D=information-technology&stag%5B1%5D=stem&sort=date"


positionTitles= []
companyNames = []
openDates= []
closeDates = []
data=[]

response = requests.get(ucfLink)
soup = BeautifulSoup(response.text, "html.parser")
pagDiv = soup.find(class_="pagination")
pagDiv = pagDiv.find_all(class_="page-numbers")
maxPages = int(pagDiv[4].text[-2:])

for i in range(maxPages-1):
    iterateLink = f"https://career.ucf.edu/jobs/page/{i+1}/?ctag%5B0%5D=internships&stag%5B0%5D=information-technology&stag%5B1%5D=stem&sort=date"
    print(i)
    response = requests.get(iterateLink)
    soup = BeautifulSoup(response.text, "html.parser")
    #Handle pagination conflicts

    #Handle taking the info from site 
    blocks = soup.find_all("div", class_="middle_block")
    for block in blocks:

        #Get the posiiton title/ Code
        entryTitle = block.find("h3")
        link = entryTitle.find("a")
        linkEnd = str(link)[0:-10].rfind("/")
        linkStart = str(link).find("=")
        positionTitle = link.text.strip()
        link = str(link)[linkStart+2:linkEnd+1]
        positionTitles.append(link)

        #Get the company name
        companyName =block.find(class_="company_name")
        companyName=companyName.text.strip()
        
        companyNames.append(companyName)

        #Get the open and close date for applications
        dates = block.find_all(class_="entry-meta-item")
        startDate= dates[0].text.strip()[21:]
        endDate = dates[1].text.strip()[31:]
        openDates.append(startDate)
        closeDates.append(endDate)

        #Check if keywords in description
        text = block.find("p").text
        if "software" or "frontend" or"backend" or "developer" or "Computer" in text:
            if "Electrical" in text:
                continue
            data.append([positionTitle, companyName, link, startDate,endDate, text])
        elif "HTML" or "Javascript" or "JS" or "Python" or "React" or "Java" or "CSS" in text:
            if "Electrical" in text:
                continue
            data.append([positionTitle, companyName, link, startDate,endDate, text])
        else:
            continue
    
df= pd.DataFrame(data,columns=["Position Title", "Company", "URL", "Opening Date", "Closing Date", "Description"])
print(df)
df.to_excel("Internships.xlsx", index=False)
