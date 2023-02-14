import os
import json
import datetime
import numpy as np

def median(list):
    a=np.array(list)
    median = np.median(a)
    return median

def average(list):
    a=np.array(list)
    average = np.mean(a)
    return average

def calculate(name,data):
    solved_info={}
    solved_info['attack_name']=name
    solved_info['solved_time(h)']={}
    solved_info['solved_developer']={}
    #解决时间的最大值、最小值、平均值、中位数
    if data:
        temp = []
        for i in range(0, len(data)):
            created_at = data[i]['created_at'].split('T')[0] + ' ' + data[i]['created_at'].split('T')[1].split('Z')[0]
            closed_at = data[i]['closed_at'].split('T')[0] + ' ' + data[i]['closed_at'].split('T')[1].split('Z')[0]
            dt1 = datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            dt2 = datetime.datetime.strptime(closed_at, '%Y-%m-%d %H:%M:%S')
            temp.append((dt2 - dt1).seconds)
        # 数据单位为小时
        solved_info['solved_time(h)']['max'] = round(max(temp) / 3600, 2)
        solved_info['solved_time(h)']['min'] = round(min(temp) / 3600, 2)
        solved_info['solved_time(h)']['median'] = round(median(temp) / 3600, 2)
        solved_info['solved_time(h)']['average'] = round(average(temp) / 3600, 2)
        # 解决人员的最大值、最小值、平均值、中位数
        temp2 = []
        for i in range(0, len(data)):
            created_user = data[i]['created_user']
            if data[i]['comments_data']:
                if created_user in data[i]['comments_data']['user_login']:
                    count = len(data[i]['comments_data']['user_login'])
                else:
                    count = len(data[i]['comments_data']['user_login']) + 1
            else:
                count = 1
            temp2.append(count)
        solved_info['solved_developer']['max'] = max(temp2)
        solved_info['solved_developer']['min'] = min(temp2)
        solved_info['solved_developer']['median'] = int(median(temp2))
        solved_info['solved_developer']['average'] = round(average(temp2), 2)
    return solved_info






if __name__ == "__main__":
    data_path='./data/attack_events/'
    path_list=os.listdir(data_path)
    mm = []
    for filename in path_list:
        file_name = filename.split('.')[0]
        json_f = open('D:/code/web3/data/attack_events/' + filename)
        json_data = json.load(json_f)
        mm.append(calculate(file_name,json_data))
    with open('D:/code/web3/data/solved_info.json', 'w') as f:
        json.dump(mm, f, indent=4)
        print("Saved issues to " + 'D:/code/web3/data/solved_info.json')