#!/usr/bin/env python
# coding: utf-8

# In[4]:

import re
import time
from selenium import webdriver
import csv
import pandas as pd
from bs4 import BeautifulSoup 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from urllib.request import urlretrieve
import os
import json


# driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# Naver login url / your id / your password
url='https://nid.naver.com/nidlogin.login'
id_ = 'insert your id '
pw = 'insert your password'
    
driver.get(url)
driver.implicitly_wait(1)

# Naver login
driver.execute_script("document.getElementsByName('id')[0].value=\'"+ id_ + "\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'"+ pw + "\'")
driver.find_element(by=By.XPATH,value='//*[@id="log.login"]').click()
time.sleep(1)


def get_content_from_major(baseurl, clubid, menuid):


    # login time you should login within 1 sec
    time.sleep(1)

    # ASSUME LOGIN  SUCCESS
    num_page = 50  # how many pages do you want to extract? 

    ##########################################################################


    for page in range(1,num_page+1):

        driver.get("https://cafe.naver.com/ArticleList.nhn?search.clubid="
                   +str(clubid)
                   +"&search.menuid="+str(menuid)
                   +"&search.boardtype=L&search.totalCount=150&search.cafeId="+str(clubid)+"&search.page="+ str(page)
                  )


        driver.switch_to.frame("cafe_main")

        time.sleep(1)  
        driver.implicitly_wait(1)

        # BeautifulSoup
        driver_page_source = driver.page_source
        soup = BeautifulSoup(driver_page_source, 'html.parser')

        #  class
        article = soup.find_all(class_="inner_list")
        find_one = 0
        for idx_wow,link_full in enumerate(article):
            idid = link_full.find(class_='article')['href'].split('articleid=')[-1]
            if idid[-1] == 'e':
                if find_one == 0:
                    find_idx = idx_wow
                    find_one += 10
                idid = idid.split('&')[0]
                link_ = baseurl + idid 
                print(link_)
                time.sleep(1.5)
                print('page', page , 'line' , idx_wow + 1)
                driver.get(link_)
                driver.switch_to.frame("cafe_main")
                time.sleep(1)
                driver.implicitly_wait(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                time.sleep(5)
                page_content = {}
                date = soup.find('span', class_='date')
                #print(date)
                if date:
                    page_content['published_date'] = date.text.strip()
                    
                categories = soup.find('a', class_='link_board')
                #print(categories)
                if date:
                    page_content['categories'] = categories.text.strip()
                                      
                title = soup.find('h3', class_='title_text')
                if title:
                    page_content['title_text'] = title.text.strip()
                #print(title)
                content = soup.find('div', class_="se-main-container")
                if content:

                    parts = content.find_all(['p'])
                    news_content = ""
                    prev_part = None
                    # Texts to remove Ad
                    texts_to_remove = [
                                        "■ 게시판을 이용해서 견적 문의 금지",
                                        "■ 해상/항공 등의 운송비 견적 문의는 카페와 제휴한 다음의 업체로 해주세요. ",
                                        "■ 해상/항공 등의 운송비 견적 문의는 카페와 제휴한 다음의 업체로 해주세요.",
                                        ]

                    for part in parts[:-1]:
                        if part.name == "p":
                            if part.find('a', href=re.compile(r"https://cafe.naver.com/infotrade/") ):
                                part.decompose()
                            if part.text.strip() in texts_to_remove:
                                part.decompose()
                            if prev_part and prev_part.name == "blockquote":

                                news_content += "</ref>\n" + part.text.strip() + "\n"
                            else:
                                news_content += part.text.strip() + "\n"

                        elif part.name == "blockquote":
                            if prev_part and prev_part.name != "blockquote":
                                news_content += "<ref>" + part.text.strip() + "\n"
                            else:
                                news_content += part.text.strip() + "\n"
                        elif part.name == "h2":
                            news_content +="<subquestion>" + part.text.strip()+ "</subquestion>" + "\n"
                        else:
                            news_content += part.text.strip() + "\n"
                        prev_part = part
                    # pprint(news_content)
                    print(news_content)
                    page_content['content'] = news_content

                    text_comment = soup.find('span', class_='text_comment')
                    print(text_comment)
                    if text_comment:
                        page_content['text_comment'] = text_comment.text.strip()

                    # pprint(item)
                    
                    #refs = content.find_all('a')
                    #page_content['refs'] = [ref.text.strip() for ref in refs]

                    page_content['url'] = link_
                    page_content['crawled_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                    with open(f"./data_qa_Naver_infotrade_{menuid}.jsonl", "a", encoding="utf-8") as f:
                        f.write(json.dumps(page_content, ensure_ascii=False) + "\n")


        print("ALL posts comsumed\nGO TO NEXT PAGE")
# wanted naver cafe url
baseurl='https://cafe.naver.com/infotrade/'
clubid = 'insert your clubid' # what is your naver cafe's clubid? 
#menuid = '61' # what is your naver cafe's menuid? 

menuids = [61,
           #62,64,71,63,312, 362,409,458,247,376,562, 246,471,72,346
           ]
for menuid in menuids:
    get_content_from_major(baseurl, clubid, menuid)