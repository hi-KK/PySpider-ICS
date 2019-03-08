#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-02-25 10:12:04
# Project: SIEMENS_CERT
# Author: KEYONE @ https://github.com/hi-KK

from pyspider.libs.base_handler import *

Headers2 = [
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Encoding', 'gzip, deflate'),
    ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
    ('Connection', 'keep-alive'),
    ('Host', 'cert-portal.siemens.com'),
    ('Upgrade-Insecure-Requests', '1'),
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
]

StartUrl = 'https://cert-portal.siemens.com/productcert/json/advisories.json'


class Handler(BaseHandler):

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(StartUrl, callback=self.detail_page, headers=Headers2)
        
#1、response.json用于解析json数据
#2、response.doc返回的是PyQuery对象
#3、response.etree返回的是lxml对象
#4、response.text返回的是unicode文本
#5、response.content返回的是字节码        

    @config(age=10 * 24 * 60 * 60)
#利用send_message，将单个页面的多个结果，for循环后，每个dict结果，都调用send_message去发送message给自己的项目，在收到message的地方，再返回dict结果。

#http://docs.pyspider.org/en/latest/apis/self.send_message/

    def detail_page(self, response):
        for i, each in enumerate(response.json):
            self.send_message(self.project_name, {
                "id": each['id'],
                'title': each['title'],
                "products":each['products'],
                "cve_id":each['cve-ids'],
                "last_update":each['last_update'],
                "pdf_url":each['pdf_url'],
                #有部分字段在老漏洞信息中没有,如果添加会报错
             }, url="%s#%s" % (response.url, i))
            
    @config(priority=2)
        
    def on_message(self, project, msg):
        return msg
 