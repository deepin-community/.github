#!/usr/bin/python3
import json
import sys
'''
./update.py repo-list.txt 传入仓库列表自动生成json文件

'''

with open(sys.argv[1],'r') as f: #将你需要更新的项目放在 need-update 文件中
    jsons=f.readlines()
jsontext = '{"branches":["master"],"src":"workflow-templates/call-clacheck.yml","dest":"deepin-community/icu/.github/workflows/call-clacheck.yml"}'
for i in jsons:
    jsondata = json.loads(jsontext)
    jsondata['dest'] = 'deepin-community/' + i.strip('\n') + '/.github/workflows/call-clacheck.yml'
    jsonarr = []
    jsonarr.append(jsondata)
    js=json.dumps(jsonarr,indent=2,separators=(',', ': '))
#    print (jsondata['dest'])
#    print (jsonarr)
    f = open(i.strip('\n') + '.json','a')
    f.write(js)
    f.close()

    

