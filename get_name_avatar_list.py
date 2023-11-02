import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import requests


# 读取文本文件
with open('sports_names.txt', 'r', encoding="utf-8") as file:
    sports = json.load(file)

sport_team_data = {}

# 使用Selenium启动一个浏览器
driver = webdriver.Chrome()  # 需要安装Chrome驱动

print(sports)

for sport in sports:
    print(sport)

    url = "https://tiyu.baidu.com/major/discipline/" + sport + "/match/杭州亚运会/tab/运动员"
    
    # 发送HTTP GET请求获取网页内容
    driver.get(url)
    
    # 等待一段时间，以确保页面加载完成（可以根据需要调整等待时间）
    time.sleep(5)
    
    # 获取完整的页面内容
    html = driver.page_source
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all elements with class="match-team-group"
    team_blocks = soup.find_all(class_="match-team-group")
    
    print(len(team_blocks))
    # Initialize an empty dictionary to store the data
    team_data = {}
    
    # Iterate through each team block
    # for team_block in team_blocks:
    #     # Find the team name
    #     team_name_element = team_block.find(class_="m-c-color name c-line-clamp1")
    #     team_name = team_name_element.text.strip()
        
    #     # Find all player names
    #     player_elements = team_block.find_all(class_="name c-line-clamp1")
    #     player_names = [player.text.strip() for player in player_elements]
        
    #     # Add the team and player names to the dictionary
    #     team_data[team_name] = player_names
    
    # # Print the dictionary
    # sport_team_data[sport] = team_data

    base_directory = "avatars"
    for team_block in team_blocks:
        # Find the team name
        team_name_element = team_block.find(class_="m-c-color name c-line-clamp1")
        team_name = team_name_element.text.strip()

        # Create a directory for the team if it doesn't exist
        team_directory = os.path.join(base_directory, team_name)

        if not os.path.exists(team_directory):
            os.mkdir(team_directory)

        logo_name_blocks = team_block.find_all(class_ ="match-c-team-item m-c-line-bottom c-blocka c-team-item m-c-color m-c-bottom-line-1px OP_LOG_BTN wa-match-team-second-items")
        for logo_name_block in logo_name_blocks:
            leaf_url = logo_name_block.get('href')
            print(leaf_url)
            # 发送HTTP GET请求获取网页内容
            if leaf_url == None:
                continue
            
            driver.get(leaf_url)
            
            # 等待一段时间，以确保页面加载完成（可以根据需要调整等待时间）
            time.sleep(5)

            logo_element = logo_name_block.find(class_="logo-img-radius")
            logo_url = logo_element.get('src')
            name_element = logo_name_block.find(class_="name c-line-clamp1")
            name = name_element.text.strip()

            # Download the logo and save it to the team directory
            response = requests.get(logo_url)
            if response.status_code == 200:
                logo_data = response.content
                logo_filename = os.path.join(team_directory, f"{name}.jpg")
                with open(logo_filename, 'wb') as file:
                    file.write(logo_data)
                print(f"Downloaded logo for {team_name} - {name}")
            else:
                print(f"Failed to download logo for {team_name} - {name}")

# 关闭浏览器
driver.quit()

# print(sport_team_data)

# # 存储到文件
# with open('sports_team_names.txt', 'w', encoding="utf-8") as file:
#     json.dump(sport_team_data, file, ensure_ascii=False, indent=4)
