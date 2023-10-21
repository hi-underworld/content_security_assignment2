import requests
from bs4 import BeautifulSoup
import json

# 读取文本文件
with open('sports_names.txt', 'r', encoding="utf-8") as file:
    sports = json.load(file)

sport_team_data = {}
for sport in sports:
    url = "https://tiyu.baidu.com/major/discipline/" + sport + "/match/杭州亚运会/tab/运动员"
    # 发送HTTP GET请求获取网页内容

    response = requests.get(url)
    # 检查是否成功获取页面
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Find all elements with class="match-team-group"
        team_blocks = soup.find_all(class_="match-team-group")

        # Initialize an empty dictionary to store the data
        team_data = {}

        # Iterate through each team block
        for team_block in team_blocks:
            # Find the team name
            team_name_element = team_block.find(class_="m-c-color name c-line-clamp1")
            team_name = team_name_element.text.strip()
            
            # Find all player names
            player_elements = team_block.find_all(class_="name c-line-clamp1")
            player_names = [player.text.strip() for player in player_elements]
            
            # Add the team and player names to the dictionary
            team_data[team_name] = player_names

        # Print the dictionary
        sport_team_data[sport] = team_data

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

print(sport_team_data)
# 存储到文件
with open('sports_team_names.txt', 'w', encoding="utf-8") as file:
    json.dump(sport_team_data, file, ensure_ascii=False, indent=4)