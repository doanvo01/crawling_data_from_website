import time
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_content_from_major(baseurl, clubid, menuid, until_day):
    """
    Crawls posts from Naver Cafe until the given `until_day`.

    Args:
        baseurl (str): Base URL for crawling.
        clubid (str): Naver Cafe Club ID.
        menuid (str): Naver Cafe Menu ID.
        until_day (str): Stop crawling when reaching this date (YYYY.MM.DD).
    """
    until_date = datetime.strptime(until_day, "%Y.%m.%d")
    print("Collecting data until day: ", until_date)
    page = 1
    while True:
        time.sleep(1) 

        driver.get(
            f"https://cafe.naver.com/ArticleList.nhn?search.clubid={clubid}"
            f"&search.menuid={menuid}&search.boardtype=L&search.totalCount=150"
            f"&search.cafeId={clubid}&search.page={page}"
        )

        driver.switch_to.frame("cafe_main")
        time.sleep(1)

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all articles
        articles = soup.find_all(class_="inner_list")
        if not articles:
            print("No more articles found. Stopping.")
            break  # Stop if no articles are found

        for idx, link_full in enumerate(articles):
            article_id = link_full.find(class_='article')['href'].split('articleid=')[-1]
            if article_id[-1] == 'e':
                article_id = article_id.split('&')[0]

                link_ = baseurl + article_id
                print(f"Crawling: {link_}")
                time.sleep(1.5)

                driver.get(link_)
                driver.switch_to.frame("cafe_main")
                time.sleep(1)

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Extract post date
                date_element = soup.find('span', class_='date')
                if date_element:
                    post_date_str = date_element.text.strip()
                    try:
                        post_date = datetime.strptime(post_date_str, "%Y.%m.%d. %H:%M")  # Convert to datetime
                        print("post_date", post_date)
                        if post_date < until_date:
                            print(f"Stopping crawl at page {page}: Found older post from {post_date}")
                            driver.quit()  # Close driver
                            return  # Stop function
                    except ValueError:
                        print(f"Skipping: Invalid date format - {post_date_str}")
                        continue  # Skip post if date is invalid

                # Extract categories
                categories = soup.find('a', class_='link_board')
                category_text = categories.text.strip() if categories else ""

                # Extract title
                title = soup.find('h3', class_='title_text')
                title_text = title.text.strip() if title else ""

                # Extract content
                content_section = soup.find('div', class_="se-main-container")
                news_content = ""
                if content_section:
                    parts = content_section.find_all(['p'])
                    prev_part = None
                    for part in parts:
                        if part.find('a', href=re.compile(r"https://cafe.naver.com/infotrade/")):
                            part.decompose()  # Remove unwanted links
                        if "■" in part.text:
                            part.decompose()  # Remove unwanted characters

                        if prev_part and prev_part.name == "blockquote":
                            news_content += "</ref>\n" + part.text.strip() + "\n"
                        else:
                            news_content += part.text.strip() + "\n"

                        prev_part = part

                # Extract comments
                text_comment = soup.find('span', class_='text_comment')
                comment_text = text_comment.text.strip() if text_comment else ""

                # Save post data
                page_content = {
                    "published_date": post_date_str,
                    "categories": category_text,
                    "title_text": title_text,
                    "content": news_content,
                    "text_comment": comment_text,
                    "url": link_,
                    "crawled_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                }

                # Save to file
                current_date = time.strftime("%Y%m%d", time.localtime())
                with open(f"./{current_date}_{menuid}.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps(page_content, ensure_ascii=False) + "\n")
                print("Saved new content")
        print("ALL posts comsumed\nGO TO NEXT PAGE")
        page += 1  # Move to next page

    driver.quit()  # Close driver after finishing



# driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# Naver login url / your id / your passward
url='https://nid.naver.com/nidlogin.login'

id_ = ''  #'insert ID'
pw = ''  # 'insert Password'
    
driver.get(url)
driver.implicitly_wait(1)

# Naver login 네이버 로그인
driver.execute_script("document.getElementsByName('id')[0].value=\'"+ id_ + "\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'"+ pw + "\'")
driver.find_element(by=By.XPATH,value='//*[@id="log.login"]').click()
time.sleep(1)


# wanted naver cafe url
baseurl='https://cafe.naver.com/infotrade/'
clubid = '20941625' # what is your naver cafe's clubid? / 네이버 카페 클럽 아이디 입력
#menuid = '61' # what is your naver cafe's menuid? / 네이버 카페 클럽 게시판 입력(필요시)
#61: 무역서류 관련
#62: 무역상식 및 용어
#64: 인코텀스
#71: 운송 및 통관
#63: 결제(T/T, L/C 등)
#312: FTA
#362: 관세 환급
#409: 특송(DHL 등)&EMS
#458: 계약(다양한 형태)
#menuids = [61]
           #,62,64,71,63,312, 362,409,458]
menuids = [61,62,64,71,63,312, 362,409,458]

    # ASSUME LOGIN  SUCCESS
until_day = "2025.03.20"
for menuid in menuids:
    get_content_from_major(baseurl, clubid, menuid, until_day)
