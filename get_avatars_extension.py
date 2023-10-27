import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import requests
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


edge_options = Options()
edge_options.page_load_strategy = 'eager'
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Edge(options=edge_options)


# 读取文本文件
with open('sports_names.txt', 'r', encoding="utf-8") as file:
    sports = json.load(file)

print(sports)

if os.path.exists('tmp.txt'):
    with open('tmp.txt', 'r', encoding="utf-8") as file:
        tmp = json.load(file)
        tmp_sport = tmp['sport']
        tmp_country = tmp['country']
        tmp_name = tmp['name']
else:
    tmp_sport = 0
    tmp_country = 0
    tmp_name = 0

base_directory = "avatars"
for i in range(tmp_sport,len(sports)):
    sport = sports[i]

    url = "https://tiyu.baidu.com/major/discipline/" + sport + "/match/杭州亚运会/tab/运动员"

    # 发送HTTP GET请求获取网页内容
    driver.get(url)
    
    # 等待一段时间，以确保页面加载完成（可以根据需要调整等待时间）
    time.sleep(3)
    
    # 获取完整的页面内容
    html = driver.page_source
    
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements with class="match-team-group"
    team_blocks = soup.find_all(class_="match-team-group")
    
    print(len(team_blocks))
    # Initialize an empty dictionary to store the data
    team_data = {}

    sport_directory = os.path.join(base_directory, sport)
    if not os.path.exists(sport_directory):
        os.mkdir(sport_directory)
    
    for j in range(tmp_country,len(team_blocks)):
        team_block = team_blocks[j]
        # Find the team name
        team_name_element = team_block.find(class_="m-c-color name c-line-clamp1")
        team_name = team_name_element.text.strip()

        # Create a directory for the team if it doesn't exist
        team_directory = os.path.join(sport_directory, team_name)

        if not os.path.exists(team_directory):
            os.mkdir(team_directory)

        logo_name_blocks = team_block.find_all(class_ ="match-c-team-item m-c-line-bottom c-blocka c-team-item m-c-color m-c-bottom-line-1px OP_LOG_BTN wa-match-team-second-items")
        for k in range(tmp_name,len(logo_name_blocks)):
            print(tmp_sport,tmp_country,tmp_name)
            logo_name_block = logo_name_blocks[k]
            name_element = logo_name_block.find(class_="name c-line-clamp1")
            name = name_element.text.strip()

            leaf_url = logo_name_block.get('href')

            if leaf_url != None:      
                print(leaf_url)
                driver.get(leaf_url)
                

                # 模拟滚动到页面底部
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            
                driver.execute_script("window.scrollBy(0, -200);")
                # 设置等待时间上限（以秒为单位）
                
            
                wait = WebDriverWait(driver, 3)

                status = 0
                try:
                    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "album-list")))
                    print("Found album-list")
                    status = 1
                except:
                    print("Failed to find album-list")
                
            
                try:
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='albumList']")))
                    print("Found albumList_")
                    status = 2
                except:
                    print("Failed to find albumList_")

                if status == 0:
                    print("Failed to get album_url")
                else:
                    if status == 1:
                        album_block = driver.find_element(By.CLASS_NAME, "more-link") 
                    
                    elif status == 2:
                        album_block = driver.find_element(By.CSS_SELECTOR, "[class*='albumLink']") 

                    album_url = album_block.get_attribute('href')

                    response = requests.get(album_url)

                    if response.status_code == 200:
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        pic_block = soup.find(class_="album-list")

                        pic_urls = pic_block.find_all('a', class_="album-cover")

                        print(len(pic_urls) )
                        name_directory = os.path.join(team_directory, name)

                        if not os.path.exists(name_directory):
                            os.mkdir(name_directory)

                        count = 0
                        for pic_url in pic_urls:
                            url = "https://baike.baidu.com" + pic_url.get('href')
                            response = requests.get(url)
                            if response.status_code == 200:
                                html = response.text
                                soup = BeautifulSoup(html, 'html.parser')
                                target_classes = ["pic-item","pic-item selected"]
                                pics = soup.find_all(class_=target_classes)
                                print(len(pics))
                                for pic in pics:
                                    if count >= 10:
                                        break
                                    else:
                                        pic_data = pic.find('img')
                                        if pic_data == None:
                                            continue
                                        else:
                                            pic_data = requests.get(pic_data.get('src')).content
                                            pic_filename = os.path.join(name_directory, f"{name}_{str(count)}.jpg")
                                            with open(pic_filename, 'wb') as file:
                                                file.write(pic_data)
                                            print(f"Downloaded pic {str(count)}for {team_name} - {sport} - {name}")
                                            count +=1
                            else:
                                print(f"Failed to download pic for {team_name} - {sport} - {name}")
            if k == len(logo_name_blocks) - 1:
                if j < len(team_blocks) - 1:
                    tmp_sport = i
                    tmp_country = j + 1
                    tmp_name = 0
                else:
                    tmp_sport = i + 1
                    tmp_country = 0
                    tmp_name = 0
            else:
                tmp_sport = i
                tmp_country = j 
                tmp_name = k + 1

            with open('tmp.txt', 'w', encoding="utf-8") as file:
                json.dump({'sport':tmp_sport,'country':tmp_country,'name':tmp_name}, file)


# 关闭浏览器
driver.quit()