import requests
import time
from bs4 import BeautifulSoup

with open('logins.txt', "r") as f:
    data = f.read().split()
    values = {
        "sid" : data[0],
        "PIN": data[1]
    }
    dept = data[2]
    course = data[3]
    crn = data[4]

post = 'term_in=201901&sel_subj=dummy&sel_subj='+dept+'&SEL_CRSE='+course+'&SEL_TITLE=&BEGIN_HH=0&BEGIN_MI=0&BEGIN_AP=a&SEL_DAY=dummy&SEL_PTRM=dummy&END_HH=0&END_MI=0&END_AP=a&SEL_CAMP=dummy&SEL_SCHD=dummy&SEL_SESS=dummy&SEL_INSTR=dummy&SEL_INSTR=%25&SEL_ATTR=dummy&SEL_ATTR=%25&SEL_LEVL=dummy&SEL_LEVL=%25&SEL_INSM=dummy&sel_dunt_code=&sel_dunt_unit=&call_value_in=&rsts=dummy&crn=dummy&path=1&SUB_BTN=View+Sections'
#need to change term_in, corresponds here to Winter 2019
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',}

with requests.Session() as s: #create session to save cookies
    url = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin'
    s.get(url) #load page once to get testID cookie
    redirect_post = s.post(url, data = values, headers = headers) #login but it sends to a meta-redirect
    new_url = 'https://horizon.mcgill.ca/' + meta_redirect(redirect_post.content) #parse redirect url
    s.get(new_url) #load main menu, optional most likely
    r = s.post('https://horizon.mcgill.ca/pban1/bwskfcls.P_GetCrse', data = post, headers = headers) #search courses
    rem = check_closed(r.content) #parse remaining courses

    print("The course " + dept + " " + course + " CRN=" + crn + " has " + rem + " seats remaining.")


def meta_redirect(content): #retrieve url from meta refresh
    soup  = BeautifulSoup(content,"lxml")

    result=soup.find("meta",attrs={"http-equiv":"refresh"})
    if result:
        wait,text=result["content"].split(";")
        if text.strip().lower().startswith("url="):
            url=text[4:]
            return url
    return None

def check_closed(content): #find the number of remaining seats for the crn
    soup  = BeautifulSoup(content,"lxml")
    p = list(soup.find("a", text=crn).parent.next_siblings)[21].string #ugly
    return p
