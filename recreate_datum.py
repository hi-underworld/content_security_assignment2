import os
import shutil

source_folder = 'avatars'  # 替换为实际的路径
destination_folder = 'new_avatars'  # 替换为实际的路径

# 获取原始文件夹中的所有子文件夹（运动文件夹）
sport_folders = os.listdir(source_folder)

# 遍历每个运动文件夹
for sport_folder in sport_folders:
    sport_folder_path = os.path.join(source_folder, sport_folder)
    
    # 获取每个国家文件夹
    country_folders = os.listdir(sport_folder_path)

    # 遍历每个国家文件夹
    for country_folder in country_folders:
        country_folder_path = os.path.join(sport_folder_path, country_folder)

        # 获取该国家文件夹中的所有人名文件夹
        person_folders = os.listdir(country_folder_path)

        # 创建新的目标国家文件夹
        destination_country_folder = os.path.join(destination_folder, country_folder)
        os.makedirs(destination_country_folder, exist_ok=True)

        # 将每个人名文件夹复制到新的国家文件夹
        for person_folder in person_folders:
            person_folder_path = os.path.join(country_folder_path, person_folder)
            destination_person_folder = os.path.join(destination_country_folder, person_folder)
            if not os.path.exists(destination_person_folder):
                shutil.copytree(person_folder_path, destination_person_folder)
                print("create folder: " + destination_country_folder + destination_person_folder)
print("操作完成")
