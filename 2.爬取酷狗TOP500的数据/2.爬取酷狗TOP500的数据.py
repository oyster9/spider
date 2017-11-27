'''
爬取酷狗音乐网->榜单->酷狗TOP500的信息
包括：排名、歌手、歌曲和歌曲时长
'''

import requests
from bs4 import BeautifulSoup
import time

# 加入请求头,用于伪装成浏览器
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}



# 定义获取信息的函数
def get_info(url):
    web_data = requests.get(url, headers=headers)
    # print(web_data) # <Response [200]> 连接成功
    soup = BeautifulSoup(web_data.text, 'lxml')
    # 排名
    ranks = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_num ')
    # 标题（包含歌手-歌曲）
    titles = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > a')
    # 歌曲时长
    times = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_tips_r > span')

    for rank, title, time in zip(ranks, titles, times):
        data = {
            'rank':rank.get_text().strip(),
            'singer':title.get_text().split('-')[0],
            'song':title.get_text().split('-')[1],
            'time':time.get_text().strip()
        }
        print(data)


# 程序主入口
if __name__ == '__main__':
    urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1, 24)]
    for url in urls:
        get_info(url)
    time.sleep(2) # 睡眠2秒
