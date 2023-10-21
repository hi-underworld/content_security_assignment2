import requests
from bs4 import BeautifulSoup
import json

# 发送HTTP GET请求获取网页内容
url = "https://tiyu.baidu.com/major/home/杭州亚运会/tab/亚运项目"
response = requests.get(url)

sports = []
# 检查是否成功获取页面
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Find all sports names
    sports_elements = soup.find_all(class_="sport-project-name c-line-clamp1")
    sports_names = [sports.text.strip() for sports in sports_elements]

    sports = list(set(sports_names))

    # Print the dictionary
    print(sports)

    # 存储到文件
    with open('sports_names.txt', 'w', encoding='utf-8') as file:
        json.dump(sports, file)

else:
    print("Failed to retrieve the page. Status code:", response.status_code)

