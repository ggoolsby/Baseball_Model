from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from xlwt import Workbook

wb = Workbook()

def createWB():
    """
    implements the simple_get method to pull down HTML from baseball reference 
    creates excel workbook to write data
    """
    
    years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

    for year in years:
        sheet = wb.add_sheet(year)
        sheet.write(0,0, "Game Date")
        sheet.write(0,1, "Away Team")
        sheet.write(0,2, "Away Team Score")
        sheet.write(0,3, "Home Team")
        sheet.write(0,4, "Home Team Score")

        rawHTML = simple_get("https://www.baseball-reference.com/leagues/MLB/"+year+"-schedule.shtml")

        print(len(rawHTML))
    
        wb.save('game_data.xls')


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
    
createWB()
