import os
import json

def get_useful_data(f_name,data_path):
    file_name=f_name.split('&')[0]+'_'+f_name.split('&')[1]
    result_path='./data/useful_data/'+file_name
    pr_f = open(data_path)
    pr_data = json.load(pr_f)
    mm = []
    for i in range(0, len(pr_data)):
        if pr_data[i]['state']=="closed":
            if pr_data[i]['number']:
                widget = {}
                widget['projcts_name']=file_name
                widget['num'] = pr_data[i]['number']
                widget['created_user']=pr_data[i]['user']['login']
                widget['created_at']=pr_data[i]['created_at']
                widget['closed_at']=pr_data[i]['closed_at']
                print(pr_data[i]['number'])
                if 'pull_request' in pr_data[i]:
                    widget['merged_at']=pr_data[i]['pull_request']['merged_at']
                else:widget['merged_at']=[]
                if pr_data[i]['labels']:
                    widget['label'] = pr_data[i]['labels'][0]['name']
                else:
                    widget['label'] = []
                if pr_data[i]['comments_data']:
                    widget['comments_data']={}
                    widget['comments_data']['created']=[]
                    widget['comments_data']['user_login']=[]
                    for x in range(0,len(pr_data[i]['comments_data'])):
                        widget['comments_data']['created'].append(pr_data[i]['comments_data'][x]['created_at'])
                        widget['comments_data']['user_login'].append(pr_data[i]['comments_data'][x]['user']['login'])
                else:widget['comments_data']=[]
                widget['title'] = pr_data[i]['title']
                widget['body'] = pr_data[i]['body']
                mm.append(widget)
    with open(result_path + '.json', 'w') as f:
        json.dump(mm, f, indent=4)
        print("Saved issues to " + result_path)


if __name__ == '__main__':
    file_path='./data/raw_data/'
    files = os.listdir(file_path)
    for file in files:
        f_name = str(file)
        print(f_name)
        data_path='./data/raw_data/'+f_name
        get_useful_data(f_name,data_path)