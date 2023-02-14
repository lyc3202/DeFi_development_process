import json
import os

keywords=['goldfi']    #Keywords describing an attack

# # keywords=['private_variable','secrets','secret']
# path='D:/code/web3/data/match_result'
# txt_name = os.listdir(path)
# for i in txt_name:
#     txt=i.split('.')
#     keywords.append(txt[0])
file_path="D:/code/web3/data/useful_data"
files = os.listdir(file_path)
for file in files:
        f_name=str(file)
        data_path=file_path+'/'+f_name
        result_path = 'D:/code/bert/data/'+f_name
        data_content = open(data_path,encoding='utf-8')
        json_data=json.load(data_content)
        for i in json_data:
            for j in range(len(keywords)):
                if i['body']:
                    if (keywords[j].lower() in i['body'].lower()) or (keywords[j].lower() in i['title'].lower()):
                        path = './data/keywords_match_result/' + keywords[j] + '.txt'
                        m = open(path, mode='a',encoding='utf-8')
                        m.write(f_name)
                        m.write('\n')
                        m.write(str(i['num']))
                        m.write('\n')
                        m.write(i['title'])
                        m.write('\n')
                        m.write(i['body'])
                        m.write('\n')
                        m.write('\r\n')
                        m.close()