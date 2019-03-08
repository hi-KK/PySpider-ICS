#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Created on 2019-02-22 14:22:23
# Project: ICS_CERT
# Author: KEYONE @ https://github.com/hi-KK

from pyspider.libs.base_handler import *

Headers2 = [
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Encoding', 'gzip, deflate'),
    ('Accept-Language', 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
    ('Connection', 'keep-alive'),
    ('Cookie', '_ga=GA1.2.1524773403.1542244241; _ga=GA1.3.1524773403.1542244241; has_js=1; _gid=GA1.2.1787487130.1550814632; _gid=GA1.3.1787487130.1550814632'),
    ('Host', 'ics-cert.us-cert.gov'),
    ('Referer','https://ics-cert.us-cert.gov/advisories'),
    ('Upgrade-Insecure-Requests', '1'),
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0')
]

StartUrl = 'https://ics-cert.us-cert.gov/advisories'


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(StartUrl, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.view-content ul a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('.pager-next > a').items():
            self.crawl(each.attr.href,callback=self.index_page, headers=Headers2)
    @config(priority=2)
    
    
    def detail_page(self, response):
        #fields = response.etree.xpath('//*[@id="ncas-content"]/div/div/div')
        risk = ''.join(response.etree.xpath('//*[@id="ncas-content"]/div/div/div/p[1]//text()')).strip()
        cvss = ''.join(response.etree.xpath('//*[@id="ncas-content"]/div/div/div/ul[1]/li[1]//text()')).strip()
        attention = ''.join(response.etree.xpath('//*[@id="ncas-content"]/div/div/div/ul[1]/li[2]/text()')).strip()
        vendor = ''.join(response.etree.xpath('//*[@id="ncas-content"]/div/div/div/ul[1]/li[3]/text()')).strip()
        equipment = ''.join(response.etree.xpath('//*[@id="ncas-content"]/div/div/div/ul[1]/li[4]/text()')).strip()
        vulnerability = ''.join(response.etree.xpath('//*[@id="ncas-content"]/div/div/div/ul[1]/li[5]/text()')).strip()
        impact_product = ''.join(response.etree.xpath('//*[@id="ncas-content"]/div/div/div/ul[2]/li//text()')).strip()
        
        
        #solution = ''.join(response.etree.xpath('//*[@id="ncas-content"]/div/div/div/h2[4]p//text()')).strip()

        return {
            "title": response.doc('#page-sub-title').text(),
            "icsa_id": response.doc('#page-title').text(),
            "risk": risk,
            "cvss": cvss,
            "attention": attention,
            "vendor": vendor,
            "equipment": equipment,
            "vulnerability": vulnerability,
            "impact_product":impact_product,
            #"solution":solution,
        }
