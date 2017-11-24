"""
描述：第一个爬虫案例：爬取小猪短租网（www.xiaozhu.com）杭州地区短租房信息
     信息包括：标题、地址、价格、房东名称、房东性别、房东头像的链接
date:2017-11-23
"""

import requests
from bs4 import BeautifulSoup
import time

# 加入请求头伪装成浏览器，以便更好的抓取数据
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/62.0.3202.94 Mobile Safari/537.36'}

# res = requests.get('http://hz.xiaozhu.com', headers=headers)
# print(res)


def judg_sex(class_name):
    '''
    判断房主性别的函数
    :param class_name:
    :return: ‘男’or ‘女’
    '''
    if class_name == ['member_icol']:
        return '女'
    else:
        return '男'


def get_links(url):
    '''
    定义获取详细页URL的函数
    '''
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    links = soup.select('#page_list > ul > li > a')  # links为URL列表
    for link in links:
        href = link.get('href')  # href是Hypertext Reference的缩写。意思是指定超链接目标的URL
        get_info(href)  # 对循环中的每个url依次调用get_info函数


def get_info(url):
    '''
    定义获取详细网页中信息的处理函数
    '''
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    # 获取标题
    tittles = soup.select(' div.pho_info > h4')
    # 获取地址
    addresses = soup.select('  div.pho_info > p > span ')
    # 获取价格
    prices = soup.select('#pricePart > div.day_l > span')
    # 获取房东姓名
    names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    # 获取房东性别
    sexs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > div')
    # 获取房东头像链接
    imgs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')

    for tittle, address, price, name, sex, img in zip(tittles,
                                                      addresses, prices, names, sexs, imgs):
        data = {
            'tittle': tittle.get_text().strip(),
            'address': address.get_text().strip(),
            'price': price.get_text(),
            'name': name.get_text(),
            'sex': judg_sex(sex.get("class")),
            'img': img.get('src')
        }
        # print(data)

        # 因为python中字典对(key,value)的存储是无序的，因此直接迭代输出字典(key,value)对是无规律的
        # 设置一个列表来保存key值得顺序，可以按自己想要的顺序输出
        keys = ['tittle', 'address', 'price', 'name', 'sex', 'img']
        for key in keys:
            print(key, data[key])


if __name__ == '__main__':
    urls = ['http://hz.xiaozhu.com/search-duanzufang-p{}-0/'.format(number)
            for number in range(1, 11)]
    for single_url in urls:
        print("single_url: ", single_url)
        get_links(single_url)
        time.sleep(2)  # 睡眠2秒,防止网页请求频率太快导致爬虫失败




