import requests
import time
from bs4 import BeautifulSoup

def meta_redirect(content): #retrieve url from meta refresh
    soup  = BeautifulSoup(content,"lxml")

    result=soup.find("meta",attrs={"http-equiv":"refresh"})
    if result:
        wait,text=result["content"].split(";")
        if text.strip().lower().startswith("url="):
            url=text[4:]
            return url
    return None

def check_closed(content): #
    soup  = BeautifulSoup(content,"lxml")
    p = list(soup.find("a", text="3012").parent.next_siblings)[21].string
    return p

with open('logins.txt', "r") as f:
    data = f.read().split()
    values = {
        "sid" : data[0],
        "PIN": data[1]
    }

dept = 'MATH'
course = '263'
crn = '3012'

post = 'term_in=201901&sel_subj=dummy&sel_subj='+dept+'&SEL_CRSE='+course+'&SEL_TITLE=&BEGIN_HH=0&BEGIN_MI=0&BEGIN_AP=a&SEL_DAY=dummy&SEL_PTRM=dummy&END_HH=0&END_MI=0&END_AP=a&SEL_CAMP=dummy&SEL_SCHD=dummy&SEL_SESS=dummy&SEL_INSTR=dummy&SEL_INSTR=%25&SEL_ATTR=dummy&SEL_ATTR=%25&SEL_LEVL=dummy&SEL_LEVL=%25&SEL_INSM=dummy&sel_dunt_code=&sel_dunt_unit=&call_value_in=&rsts=dummy&crn=dummy&path=1&SUB_BTN=View+Sections'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}

with requests.Session() as s:
    url = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin'
    s.get(url) #load page once to get cookies
    redirect_post = s.post(url, data = values, headers = headers)
    new_url = 'https://horizon.mcgill.ca/' + meta_redirect(redirect_post.content)
    s.get(new_url) #actually login
    r = s.post('https://horizon.mcgill.ca/pban1/bwskfcls.P_GetCrse', data = post, headers = headers)
    rem = check_closed(r.content)

    print("The course " + dept + " " + course + " CRN=" + crn + " has " + rem + " seats remaining.")
