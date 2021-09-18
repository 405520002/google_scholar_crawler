from selenium import webdriver
import pandas as pd
import time
import datetime
import re
import os
import json
import urllib.request
import random
import sys

author = "Nico Zheng"
email = "nico921113[at]gmail.com"

# keywords = ["online communities"]  # search keywords
# journals = ['information systems research', 'mis quarterly', 'journal of management information systems',
#              'journal of the association for information systems', 'management science', 'operational research',
#              'information & management', "decision support systems", "european journal of information systems"]
# fpath = "/Users/Nico/test/test_googlecrawer2"   # output file folder
# chromedriver_path = ""  # modify this if you need to use local chromedriver

alias = {'information systems research':"ISR", 'mis quarterly':'MISQ', 'journal of management information systems':"JMIS",'journal of the association for information systems':"JAIS", 'management science':'MS', 'operational research':"OR",
    "information & management": "I&M", "decision support systems": "DSS", "european journal of information systems": "EJIS"}


'''
crawl google scholar search results and save pdf if the file was avaliable.

requirements:
    - selenium  `pip install selenium`
    - webdriver `brew install webdriver`
    - requests `pip install requests`
    - openpyxl `pip install openpyxl`

will create local file folders based on keywords and journal as following:
$ tree test_googlecrawer -d
test_googlecrawer
└── wikipedia
    ├── information systems research
    ├── journal of management information systems
    ├── journal of the association for information systems
    ├── management science
    ├── mis quarterly
    └── operational research

in each folder, there is a log file recorded detailed search results (author, title, journal, year and whether pdf is avaliable)
also avaliable pdf files.
the pdf file renamed as:
author-year-title-journal.pdf
'''

## global functions
def downloadPdf(output, link):
    '''
    write pdf file based on link address.
    
    '''
    
    time.sleep(random.randint(3,10))
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(link,output)
    


def parse(infobox):
    infobox = infobox.lower().split("-")
    infobox = [c.strip() for c in infobox]
    author = infobox[0].split(",")[0].split(" ")[1]  # extract last name
    journal = infobox[1].split(",")[0] # extract journal, "..." may be init, otherwise, we need to get bibtex diredctly, much more time-consuming
    year = infobox[1].split(",")[1].strip()  # extract year
    return author, journal, year

class Article:
    def __init__(self, keywords, folder):
        self.keywords = keywords   # search keywords
        self.output_folder = folder   # output folder
        self.createFolder()
        self.total_articles = {}

    def createFolder(self):
        self.output_fpath = "/".join([self.output_folder, self.keywords])
        if not os.path.exists(self.output_fpath):
            os.makedirs(self.output_fpath)  # creaet output folder if there is not one.
            print('creating folder {0}'.format(self.output_fpath))

    def getInfo(self, article, driver):
        default = {"title": "NA", "author": "NA", "journal": "NA", "year":"NA", "log": "NA", "citation":"NA"}
        default['title'] = article.find_element_by_class_name("gs_rt").text.lower()
        default['title'] = re.sub("[^a-z0-9\ \-\:]", "", default['title'])
        default['title'] = re.sub("pdf\ ", "", default['title'])
        infobox = article.find_element_by_class_name("gs_a").text
        default['author'], default['journal'], default['year'] = parse(infobox)
        default['citation'] = article.find_element_by_css_selector("div[class=gs_fl]").find_element_by_css_selector("a[href^='/scholar?cites']").text.split(" ")[-1]
        default['pdf']=article.find_element_by_class_name("gs_or_ggsm [href]").get_attribute('href')
        return default


    def getFileName(self):
        by = ["author", "year", "title", "journal"]
        filename = "-".join([self.info[c] for c in by]) + ".pdf"
        print(filename)
        return filename

    def fit(self, article, driver, num):
        default = {"title": "NA", "author": "NA", "journal": "NA", "year":"NA", "log": "NA", "citation":"NA"}
        #try:
        self.info = self.getInfo(article, driver)
        #except:
            #self.info = default
        if self.info != default:
            self.filename = self.getFileName()
            self.info['filename'] = self.filename
            output = self.output_fpath + "/" + self.filename
        
            try:
                downloadPdf(output, self.info['pdf'])
            except:
                self.log = self.info['log'] + "||| pdf download error"
        self.total_articles[num] = self.info

def run(keywords, recursive = 6):
    '''
    search based on keywords and journals combinations
    recursive is the number of request pages.
    '''
    if not chromedriver_path:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Chrome(chromedriver_path)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.get('https://scholar.google.com/')
    for i in keywords:
        cnt = 1
        articles = Article(i, fpath)
        search_keyword = " ".join([i.lower()]) ## generate search keyword like "wikipedia source: 'mis quarterly'"
        print("current search key: {0}".format(search_keyword))
        input_element = driver.find_element_by_name("q")
        input_element.clear()
        input_element.send_keys(search_keyword)
        input_element.submit()
        time.sleep(random.randint(2,5))
        for n in range(recursive):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elements = driver.find_elements_by_css_selector("div[class=gs_r\ gs_or\ gs_scl]")  #find article boxs
            for e in elements:
                try:
                    articles.fit(e, driver, cnt)
                except:
                    print("page {} number {} parse error!".format(n, cnt))
                cnt += 1
            try:
                
                driver.find_element_by_xpath('//*[@id="gs_nm"]/button[2]/span/span[1]').click()
                time.sleep(random.randint(3,10))
            except:
                try:
                    driver.find_element_by_xpath('//*[@id="gs_n"]/center/table/tbody/tr/td[12]/a/b').click()
                    time.sleep(random.randint(3,10))
                except Exception as e:
                    print('error: ',e)
                    print('cant find next page')
                    break   # break the loop if can't find next page
        log = pd.DataFrame(articles.total_articles).T  # generate log files
        now = datetime.datetime.now()
        log.to_csv(articles.output_fpath+"/"+"logfile_{}.csv".format(now.strftime("%m-%d-%Y")),encoding='utf_8_sig')
    driver.quit()
    

        


if __name__ == '__main__':
    path=os.getcwd()
    print(path)
    f=open(path[:-4]+'config.json')
    config = json.load(f)  # read config
    keywords = config['keywords']
    fpath = config['fpath']
    require_pages=config['require_pages']
    chromedriver_path = config['chromedriver_path']
    run(keywords, recursive=require_pages)
