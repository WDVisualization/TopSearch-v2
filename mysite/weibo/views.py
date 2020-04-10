import json
from os import path
import collections
import pymysql
import jieba
from wordcloud import WordCloud
from django.http import HttpResponse
from django.shortcuts import render

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='qwh263625', db='spider', charset='utf8')
cursor = db.cursor()


# Create your views here.
def index(request):
    telist = wdcld(request)
    data = json.loads(telist.content)
    print(data)
    # import requests
    # import json
    # api_request = requests.get("http://127.0.0.1:8000/list")
    # api = json.loads(api_request.content)
    # return render(request,'index.html', {"api": api})
    return render(request, 'index.html', {"data": data})

# 词云
def wdcld(request):
    try:
        sql = "select keywords from weibo"
        cursor.execute(sql)
        datas = cursor.fetchall()
        db.commit()
        str = ""  # 需要解析的字符串
        for data in datas:
            str += data[0]
        word_list = jieba.lcut(str)
        # 分词后在单独个体之间加上空格

        # 对词语进行出现次数统计
        te = {};
        for w in word_list:
            if len(w) == 1:
                continue
            else:
                te[w] = te.get(w, 0) + 1

        # 次数排序
        telists = list(te.items())
        telists.sort(key=lambda x: x[1], reverse=True)
        # 输出次数前TOP20的词语
        ranklist = []
        for i in range(0, 20):
            print(telists[i])
            ranklist.append(telists[i])

        newstr = " ".join(word_list)
        wordcloud = WordCloud(
            font_path="C:\\Windows\\Fonts\\msyh.ttc"
        ).generate(newstr)

        d = path.dirname(__file__) + '\static\image'
        wordcloud.to_file(path.join(d, 'test.png'))

        res = {'msg': '操作成功', 'code': 200, 'data': ranklist}
    except:
        res = {'msg': '操作失败', 'code': 400}
        print('出现错误')
    return HttpResponse(json.dumps(res, ensure_ascii=False))


def lists(request):
    try:
        sql = "select * from weibo"
        cursor.execute(sql)
        datas = cursor.fetchall()
        db.commit()
        objects_list = []
        for data in datas:
            d = collections.OrderedDict()
            # d['id'] = data[0]
            d['rank'] = data[1]
            d['keywords'] = data[2]
            d['flow'] = data[3]
            d['url'] = data[4]
            objects_list.append(d)
            # print(objects_list)

        res = {'msg': '查询数据成功', 'code': 400, 'data': objects_list}
    except:
        print('出现错误')
        res = {'msg': '查询失败', 'code': 200}
    return HttpResponse(json.dumps(res, ensure_ascii=False))
