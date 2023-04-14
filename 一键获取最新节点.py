'''
-*- coding: utf-8 -*-
@Author: 顺虞
@Date:   2023-4-13 23:41:50
@Last Modified by:   顺虞
@Last Modified time: 2023-4-14 11:13:06
'''

import sys
import requests
from lxml import etree

# 检测网址路径是否可用
def check_useable(res):
    if res.status_code == 404:
        print("SITE ERROR!")
        sys.exit()
    if res.status_code == 403:
        print("Has been banned!")
        sys.exit()
    return True

# 从主站获取最新页面链接
def get_link_from_site(siteurl):
    siteresponse = requests.get(siteurl)
    if check_useable(siteresponse) == True:
        sitehtml = siteresponse.text
        sitetree = etree.HTML(sitehtml)
        newest_link = sitetree.xpath('/html/body/div/main/div/div[1]/div[2]/ul/li[1]/div[2]/a/@href')[0]
        return newest_link

# 从页面获取最新文件链接
def get_yaml_from_link(newest_link):
    linkresponse = requests.get(newest_link)
    if check_useable(linkresponse) == True:
        linkhtml = linkresponse.text
        linktree = etree.HTML(linkhtml)
        newest_yaml = linktree.xpath('/html/body/div[1]/main/div/div[1]/div[1]/div[2]/div[2]/div[1]/p[23]/text()')[0]
        return newest_yaml

# 获取并读写yaml文件
def save_yaml(newest_yaml,file_path):
    fp = open(f"{file_path}", "wb")
    res = requests.get(url=newest_yaml)
    fp.write(res.content)
    fp.close()
    return True

if __name__ == '__main__':
    file_path = r"C:\Users\12652\Desktop\clash.yaml"
    siteurl = 'https://freenode.me/'
    newest_link = get_link_from_site(siteurl)
    newest_yaml = get_yaml_from_link(newest_link)
    if save_yaml(newest_yaml,file_path) == True:
        print('''                          Finished!
        Your File Has Been Saved In ''' + file_path)