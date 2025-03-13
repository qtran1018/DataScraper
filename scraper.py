from bs4 import BeautifulSoup
import requests
import pandas as pd

data = []

bizcounter = 0
addcounter = 0
phonecounter = 0

#Gets data for the url search params that gives all listings.
try:
    url = "https://business.worcesterchamber.org/list/searchalpha/0?q=0&o=alpha&an=True&"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    businesses = soup.find_all('div', class_="gz-list-card-wrapper col-sm-6 col-md-4")

    for business in businesses:

        #Finds names
        #NOTE: can maybe take the  alt text from inside
        try:
            name = business.find("span", class_="gz-img-placeholder").text
            bizcounter+=1
        except:
            try:
                name = business.find("img", class_="img-fluid gz-results-img")['alt']
                bizcounter+=1
            except:
                #name = "(empty)"
                continue

        #Finds addresses
        try:
            street = business.find("span", class_="gz-street-address").text.strip()
            addcounter+=1
        except:
            street = ""
        try:
            address = business.find("div", itemprop="citystatezip").text.strip().replace('\n', '|')
            city,state,zip_code = address.split("|")
        except:
            address = ""
            city = ""
            state = ""
            zip_code = ""

        #Finds phone number
        try:
            phone = business.find("li",class_="list-group-item gz-card-phone").text.strip()
            phonecounter+=1
        except:
            phone = ""

        data.append([name, street, city, state, zip_code, phone])

except Exception as e:
    print(e)

df = pd.DataFrame(data, columns=['Name','Street','City','State','ZIP','Phone'])

df.to_csv('info.csv')

print("Business",bizcounter)
print("Address", addcounter)
print("Phone",phonecounter)