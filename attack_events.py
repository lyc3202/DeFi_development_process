import os
import json
from openpyxl import load_workbook
import datetime

def calculate(data):
    created_at = data['created_at']
    closed_at = data['closed_at']
    temp = created_at.split('T')
    t = temp[1].split('Z')
    memp = closed_at.split('T')
    m = memp[1].split('Z')
    dt1 = datetime.datetime.strptime(temp[0] + ' ' + t[0], '%Y-%m-%d %H:%M:%S')
    dt2 = datetime.datetime.strptime(memp[0] + ' ' + m[0], '%Y-%m-%d %H:%M:%S')
    event_solved_time = (dt2 - dt1).senconds
    user=data['created_user']
    for c in data['comments_data']:
        comments_user = c['user']
        comments_time = c['created_at']
        if user == comments_user:
            value.append('null')
            continue
        memp = comments_time.split('T')
        m = memp[1].split('Z')
        dt1 = datetime.datetime.strptime(temp[0] + ' ' + t[0], '%Y-%m-%d %H:%M:%S')
        dt2 = datetime.datetime.strptime(memp[0] + ' ' + m[0], '%Y-%m-%d %H:%M:%S')
        value.append(str(dt2 - dt1))


    return event_solved_time,responded_time







if __name__ == "__main__":
    data_path='./data/useful_data/'
    path_list=os.listdir(data_path)
    ws = load_workbook('attack_events（2）.xlsx')
    sheets = ws.worksheets
    sheet1 = sheets[0]
    rows = sheet1.rows
    columns = sheet1.columns
    for i in range(2,92):
        row2 = []
        for row in sheet1[i]:
            if row.value!=None:
                row2.append(row.value)
        if len(row2)>1:
            attack_name = row2[0]
            mm = []
            for x in range(0,len(row2)-1):
                temp=row2[x+1].split('/')
                event_name=temp[0]
                event_num=temp[1]
                for filename in path_list:
                    file_name=filename.split('.')[0]
                    if event_name==file_name:
                        json_f=open('D:/code/web3/data/useful_data/'+filename)
                        json_data = json.load(json_f)
                        for y in range(0,len(json_data)):
                            if int(event_num)==json_data[y]['num']:
                                mm.append(json_data[y])
            with open('D:/code/web3/data/attack_events/' + attack_name + '.json', 'w') as f:
                        json.dump(mm, f, indent=4)
                        print("Saved issues to " + 'D:/code/web3/data/attack_events/' + attack_name + '.json')





    # for filename in path_list:
    #     if filename.__contains__(item_name):
    #         json_fn = path+filename
    # json_f='./data/metrics_result/'#存计算指标之后的数据的路径
    # result = calculate(json_fn, json_f)
