#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Created on 2019-02-22 11:15:46
# Project: ICS_CNVD_ALL
# Author: KEYONE @ https://github.com/hi-KK

from pyspider.libs.base_handler import *

Headers2 = [
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Encoding', 'gzip, deflate'),
    ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
    ('Connection', 'keep-alive'),
    ('Cookie', '__jsluid=fabe0b42b024cf678a08a53ce857caf8'),
    ('Host', 'ics.cnvd.org.cn'),
    ('Upgrade-Insecure-Requests', '1'),
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
]

StartUrl = 'http://ics.cnvd.org.cn/?max=20&offset='


class Handler(BaseHandler):
    crawl_config = {
        "headers": {
            "User-Agent": "BaiDuSpider", #配置用户代理，模拟百度蜘蛛
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(StartUrl, callback=self.index_page)
        
#1、response.json用于解析json数据
#2、response.doc返回的是PyQuery对象
#3、response.etree返回的是lxml对象
#4、response.text返回的是unicode文本
#5、response.content返回的是字节码        

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        #使用response.doc引入css选择器，获取所有链接        
        for each in response.doc('html>body>div.con>div.con_left>div.list>table>tbody#tr>tr>td>a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        #使用response.doc引入css选择器，定位下一页链接    
        for each in response.doc('html>body>div.con>div.con_left>div.list>div.pages.clearfix>a.nextLink').items():
            self.crawl(each.attr.href,callback=self.index_page, headers=Headers2)
            

    @config(priority=2)
    def detail_page(self, response):
        #使用pyspider的response.etree來引入xpath选择器
        items = response.etree.xpath('/html/body//div[@class="tableDiv"]/table/tbody/tr')
        cnvd_cveid = 0
        cnvd_bugid = 0
        for item in items:
            
            cnvd_title = ''.join(item.xpath('td[@class="alignRight"]/text()')).strip()
            
            cnvd_text = ''.join(item.xpath('td[last()]/text()')).strip()

            if cnvd_title == 'CNVD-ID':
                cnvd_id = cnvd_text

            elif cnvd_title == '公开日期':
                cnvd_time = cnvd_text

            elif cnvd_title == '危害级别':
                cnvd_level = ''.join(cnvd_text.split()).replace('()', '')

            elif cnvd_title == '影响产品':
                cnvd_impact = ''.join(cnvd_text.split())

            elif cnvd_title == 'CVE ID':
                cnvd_text = ''.join(item.xpath('td/a/text()')).strip()
                cnvd_cveid = cnvd_text

            elif cnvd_title == 'BUGTRAQ ID':
                cnvd_text = ''.join(item.xpath('td/a/text()')).strip()
                cnvd_bugid = cnvd_text

            elif cnvd_title == '漏洞描述':
                cnvd_description = ''.join(cnvd_text.split())

            elif cnvd_title == '参考链接':
                cnvd_reference = ''.join(item.xpath('td/a/text()')).strip()

            elif cnvd_title == '漏洞解决方案':
                cnvd_solution = ''.join(cnvd_text.split())

            elif cnvd_title == '厂商补丁':
                cnvd_text = ''.join(item.xpath('td/a/text()')).strip()
                cnvd_patch = cnvd_text

            elif cnvd_title == '更新时间':
                cnvd_update = cnvd_text
            else:
                print('')
                
        return {
            #"url": response.url,
            "cnvd_title":response.doc('h1').text(),
            
            "cnvd_id":cnvd_id,
            "cnvd_date":cnvd_time,
            "cnvd_level":cnvd_level,
            "cnvd_product":cnvd_impact,
            "cnvd_cve_id":cnvd_cveid,
            "cnvd_bug_id":cnvd_bugid,
            "cnvd_description":cnvd_description,
            "cnvd_reference":cnvd_reference,
            "cnvd_solution":cnvd_solution,
            "cnvd_patch":cnvd_patch,
            "cnvd_update":cnvd_update
        }

