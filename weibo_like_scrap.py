#"-*-coding:utf-8 -*-"
#'''
#@File    :   weibo_like_scrap
#@Time    :   2021-12-21
#@Author  :   Moonvee 
#@Version :   1.0
#@Contact :   moonvee@outlook.com
#@License :   (C)Copyright 2021, Moonvee
#@Desc    :   A weibo spider.

import requests
import re
import time
import csv

def get_zpz_num(link):
    headers = {
        "user-Agent" : "Mozilla/5.0 (...此处替换为自己账号信息...",
        "Cookie": "...此处替换为自己账号信息..."
    }
    r = requests.get(link, headers= headers)
    html = r.text

    title_list = re.findall('<./em><em>(.*?)<./em><./span>',html)
    #results = '转发'+title_list[1] + '评论'+title_list[2] + '点赞'+title_list[3]

    return title_list

def get_urls(file):
    rowlist = []
    reader = csv.DictReader(file)
    for row in reader:
        rowlist.append(row['url'])
    return rowlist


def out_data_title(path):
    csv_writer = csv.writer(open(path, "a+", newline=''))
    csv_writer.writerow(['links','zhuanfa','pinglun','dianzan'])

        
def out_data(path,row):
    with open(path, "a+", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(row)


if __name__ == '__main__':
    mylist = []
    count = 0
    countok = 0
    countfalse = 0
    
    filein = open("weibo_like_scrap\\data.csv", "r")
    fileout ="weibo_like_scrap\\out.csv"
    
    urls = get_urls(filein)
    out_data_title(fileout)
    
    for links in urls:
        try:
            result = get_zpz_num(links)
            mylist.append((links,result[1],result[2],result[3]))
            time.sleep(2)
            countok += 1
            count += 1
            print('第',count,'条成功')
            

            if isinstance(count/200,int) :
              time.sleep(60)
            
        except:
            mylist.append((links,'fail','fail','fail'))
            countfalse += 1
            count += 1
            print('第',count,'条失败')
        
        out_data(fileout,mylist)
        mylist = []

    print('本次共处理', countok+countfalse , '条数据，成功 ',countok, ' 条，失败 ',countfalse,' 条')
    
