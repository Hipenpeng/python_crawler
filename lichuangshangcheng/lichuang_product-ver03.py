# -*- coding: utf-8 -*-
# /usr/bin/env python

'''
Author: dcp
Email: pdcfighting@163.com
Wechat: pycharm1314
Blog: https://blog.csdn.net/pdcfighting
公众号: Python爬虫与数据挖掘

date: 2019/3/26 16:30
desc:
'''

import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import xlwt
import json

data = []
js_items = []

def get_url(url):
    response = requests.get(url).text
    pattern = '<a class="child-item-a" href="(.*?)">'
    links = re.findall(pattern, response, re.S)
    # for link in links:
    #     get_detail(link)
    get_deail(links[0])


def get_deail(url):

    # page = 1
    response = requests.get(url).text.encode("latin1").decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')
    # try:
    #     tbodys = soup.find_all('tbody')
    #     # print(tbodys[0])
    #     # part_2
    #     for tbody in tbodys:
    #         part_2 = tbody.find(attrs={'class': 'two'})
    #         title = part_2.find(attrs={'class': 'two-tit ellipsis'}).a.get_text().strip()
    #         li_tags = part_2.find_all('li')
    #         pruduct_number = li_tags[0].get_text().strip()
    #         store_size = li_tags[1].get_text().strip()
    #         band = li_tags[2].get_text().strip()
    #         xinghao = li_tags[3].get_text().strip()
    #         description = part_2.find(attrs={'class': 'lower'}).div.get_text().strip()
    #         # print(title, pruduct_number, store_size, band, xinghao, description)
    #
    #         # part_3
    #         part_3 = tbody.find(attrs={'class': 'three'})
    #         li_tags = part_3.find_all('li')
    #         zengzhishui = li_tags[0].get_text().strip()
    #         try:
    #             start1_end9 = li_tags[1].get_text().strip()
    #         except:
    #             start1_end9 = ''
    #
    #         try:
    #             start10_end29 = li_tags[2].get_text().strip()
    #         except:
    #             start10_end29 = ''
    #
    #         try:
    #             start30_end99 = li_tags[3].get_text().strip()
    #         except:
    #             start30_end99 = ''
    #
    #         try:
    #             start100_end499 = li_tags[4].get_text().strip()
    #         except:
    #             start100_end499 = ''
    #
    #         try:
    #             start500_end999 = li_tags[5].get_text().strip()
    #         except:
    #             start500_end999 = ''
    #
    #         try:
    #             start1000 = li_tags[6].get_text().strip()
    #         except:
    #             start1000 = ''
    #
    #         # part_4
    #         part_4 = tbody.find(attrs={'class': 'ffour'})
    #         li_tags = part_4.find_all('li')
    #         pan_list = li_tags[0].get_text().strip()
    #         recent_buy = li_tags[1].get_text().strip()
    #         inventory = li_tags[2].get_text().strip()
    #         status = li_tags[3].get_text().strip()
    #
    #         data.append([title, pruduct_number, store_size, band, xinghao, description, zengzhishui,
    #                      start1_end9, start10_end29, start30_end99, start100_end499, start500_end999, start1000,
    #                      pan_list, recent_buy, inventory, status])
            # print(data)
            # with open('product.txt', 'w', encoding='utf-8') as fp:
            #     fp.write(str(data))
            # print('任务完成!')

    try:
        #  第2页...
        total_number = soup.find(attrs={'id': 'totalNums'}).get_text()
        # print(total_number)
        page_number = int(int(total_number) / 30) + 1
        print(page_number)
        for i in range(2, page_number+1):
            print('==========0')
            post_data = {
                'catalogNodeId': url_number,
                'pageNumber': i,
                'querySortBySign': 0,
                'showOutSockProduct': 1,
                'queryProductGradePlateId': '',
                'queryProductArrange': '',
                'keyword': '',
                'queryBeginPrice': '',
                'queryEndPrice': '',
                'queryProductStandard': '',
                'queryParameterValue': '',
                'lastParamName': '',
                'baseParameterCondition': 'undefined',
                'parameterCondition': ''
            }
            print('==========1')
            main_url = 'https://list.szlcsc.com/products/list'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                "Referer": "https://list.szlcsc.com/catalog/{}.html".format(url_number),
            }
            result_data = requests.post(main_url, data=post_data, headers=headers).json()
            print('==========2')
            datas = result_data["productRecordList"]
            print('==========3')
            try:
                for data in datas:
                    # price = data["numberprices"].split(",")
                    js_items.append((data["lightCatalogName"] + "/" + data["lightProductName"], data["lightProductCode"],
                                     data["lightBrandName"], data["lightStandard"], data["lightProductModel"],
                                     data["lightProductIntro"], "", data["numberprices"],
                                     "", "", "", "", "",
                                     "1" + data["productMinEncapsulationUnit"] + data["productMinEncapsulationNumber"] + "个", data["encapsulateProductMinEncapsulationNumber"] + data["encapsulateProductMinEncapsulationUnit"],
                                     data["validStockNumber"], "status"))
                    print(js_items)

                    # 写入excel
                    newTable = 'test.xls'  # 表格名称
                    wb = xlwt.Workbook(encoding='utf-8')  # 创建excel文件，声明编码
                    ws = wb.add_sheet('test1')  # 用于创建表格
                    headDate = ['商品名称', '商品编号', '封装大小', '品牌', '型号', '描述',
                                '增值税', '1 ~ 9 个', '10 ~ 29 个', '30 ~ 99 个', '100 ~ 499 个', '500 ~ 999 个', '1000 个以上',
                                '大小', '近期约售', '库存', '状态']  # 表格头部信息
                    for column in range(0, 17):
                        ws.write(0, column, headDate[column], xlwt.easyxf('font: bold on'))
                        # 0代表第一行，column代表列，headDate[column]代表列的数据，xlwt.easyxf('font: bold on')是将字体加粗
                    # 爬取到的内容写入Excel表格
                    index = 1
                    # for item in data:  # items代表职位信息
                    #     # print item
                    #     for i in range(0, 17):
                    #         ws.write(index, i, item[i])  # 行，列，数据
                    #     index += 1

                    for js_item in js_items:  # items代表职位信息
                        # print item
                        for j in range(0, 17):
                            ws.write(index, j, js_item[j])  # 行，列，数据
                        index += 1
                        wb.save(newTable)  # 保存表格
                    print('任务完成!')
            except:
                pass


    except:
        print('some error!')

# def write_file(data):
#     with open('product.txt', 'w', encoding='utf-8') as fp:
#         fp.write(str(data))
#     print('任务完成!')



if __name__ == '__main__':
    # url = 'https://www.szlcsc.com/catalog.html'
    # get_url(url)
    url = 'https://list.szlcsc.com/catalog/11047.html'
    regex_str = 'https://list.szlcsc.com/catalog/(\d+).html'
    match_obj = re.match(regex_str, url)
    if match_obj:
        url_number = match_obj.group(1)
        print(url_number)
    get_deail(url)
    # write_file(data)