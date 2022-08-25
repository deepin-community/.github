#!/usr/bin/python3
import json
import sys
'''
./update.py repo-list.txt 传入仓库列表自动生成json文件

'''
with open(sys.argv[1],'r') as f: #将你需要更新的项目放在 need-update 文件中
    jsons=f.readlines()
jsontext = '{"branches":["master"],"src":"workflow-templates/backup-to-gitlab.yml","dest":"deepin-community/icu/.github/workflows/call-clacheck.yml"}'
jsontext1 = '{"branches":["master"],"src":"workflow-templates/call-build-deb.yml","dest":"deepin-community/icu/.github/workflows/call-build-deb.yml"}'
for i in jsons:
    with open(i.strip('\n') + '.json','r') as f:
        data=json.load(f)
        print(data)
    jsondata = json.loads(jsontext)
    jsondata1 = json.loads(jsontext1)
    # dest=addJson['dest'].split("/")
    # dest[-1]="call-license-check.yml" #替换为自己的yaml文件
    # dest="/".join(dest)
    jsondata['dest'] = 'deepin-community/' + i.strip('\n') + '/.github/workflows/backup-to-gitlab.yml'
    jsondata1['dest'] = 'deepin-community/' + i.strip('\n') + '/.github/workflows/call-build-deb.yml'   
   #data.append(jsondata)
    data.append(jsondata1)
    print(data)
    js=json.dumps(data,indent=2,separators=(',', ': '))
    with open(i.strip('\n') + '.json','w') as f:
        f.write(js)
    f.close()