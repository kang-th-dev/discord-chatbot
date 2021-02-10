from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import parse
import datetime

def timeSet():
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    return nowDate
     
def getWeatherInfo(locationInput):
    try:
        response = urlopen('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query='+parse.quote(locationInput+" 날씨"))
        soup = BeautifulSoup(response, 'html.parser')

        #crawling
        location = soup.find('span',class_="btn_select").get_text()
        temperature = str(soup.find('p',class_="info_temperature").get_text()).replace("도씨","")
        info = soup.find('p',class_="cast_txt").get_text()

        weather_info = {
            "location":location,
            "temperature":temperature,
            "info":info,
            "date":timeSet()
        }
        return weather_info
    except:
        return "none"

def getAirpollution(locationInput):
    try:
        response = urlopen('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query='+parse.quote(locationInput+" 미세먼지"))
        soup = BeautifulSoup(response, 'html.parser')

        #crawling
        location = soup.find('span',class_="select_text").get_text()
        airPollution = str(soup.find('div',class_="state_info").get_text()).replace(' ','')

        airPollution_info = {
            "location":location,
            "airPollution":airPollution,
            "date":timeSet()
        }
        return airPollution_info
    except:
        return "none"

def getNews(subject):
    newLink = dict()
    try:
        if subject == "사회": subject = "/society"
        elif subject == "정치": subject = "/politics"
        elif subject == "경제": subject = "/economic"
        elif subject == "국제": subject = "/foreign"
        elif subject == "문화": subject = "/culture"
        elif subject == "IT": subject = "/digital"
        else: return "none"
        print(subject)
        response = urlopen('https://news.daum.net'+subject)
        soup = BeautifulSoup(response, 'html.parser')

        for anchor in soup.find_all('a',class_="link_txt"):
            if anchor["data-tiara-layer"] == "article_main":
                newLink[anchor.get_text()] = anchor.get('href', '/')

        return newLink
    except:
        return newLink

'''
print(getWeatherInfo(locationInput))
print(getAirpollution(locationInput))
'''