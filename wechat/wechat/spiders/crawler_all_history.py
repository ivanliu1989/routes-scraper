# -*- coding: utf-8 -*-

import logging
import time
import requests

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def str_to_dict(headers):
    """
    将"Host: mp.weixin.qq.com"格式的字符串转换成字典类型
    转换成字典类型
    :param headers: str
    :return: dict
    """
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        h = h.strip()
        if h:
            k, v = h.split(":", 1)
            d_headers[k] = v.strip()
    return d_headers


class WeiXinCrawler:
    def crawl(self, offset=0):
        """
        爬取更多文章
        :return:
        """
        url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MTA5NjAyMA==&f=json&offset={offset}&count=10&is_ok=1&scene=126&uin=777&key=777&pass_ticket=mG5PIqAHg2jAY%2B6NQAJtsyEedBCeybGVZzm4RzZefynPWKfgdSyywrnG6soSsQ0w&wxtoken=&appmsg_token=996_7dDcPuBAmv2HxZhYfS74socUK_MniYtv4x-VIg~~&x5=0&f=json".format(offset=offset)  # appmsg_token 也是临时的

        headers = """
Host: mp.weixin.qq.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 MMWEBID/2090 MicroMessenger/7.0.3.1400(0x27000334) Process/toolsmp NetType/WIFI Language/zh_CN
X-Requested-With: XMLHttpRequest
Accept: */*
Referer: https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTA5NjAyMA==&scene=126&bizpsid=0&devicetype=android-19&version=27000334&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=mG5PIqAHg2jAY%2B6NQAJtsyEedBCeybGVZzm4RzZefynPWKfgdSyywrnG6soSsQ0w&wx_header=1
Accept-Encoding: gzip,deflate
Accept-Language: zh-AU,en-US;q=0.8
Cookie: rewardsn=; wxtokenkey=777; wxuin=2711770575; devicetype=android-19; version=27000334; lang=zh_CN; pass_ticket=mG5PIqAHg2jAY+6NQAJtsyEedBCeybGVZzm4RzZefynPWKfgdSyywrnG6soSsQ0w; wap_sid2=CM+riY0KElxjX1BQWTRrcjdFb2E3ZlU0V0kxbUZvdDRhNWl4ZHZkX3JRdzBPb2RaNkhOX05QcF9jQUFKd003X09hMUZJZDJVX2pPbDZQMW12QVdEUmhmUksxLU1CLVFEQUFBfjDo5JrjBTgNQJVO
"""
        headers = str_to_dict(headers)
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            msg_list = result.get("general_msg_list")
            logger.info("抓取数据：offset=%s, data=%s" % (offset, msg_list))
            # 递归调用
            has_next = result.get("can_msg_continue")
            if has_next == 1:
                next_offset = result.get("next_offset")
                time.sleep(2)
                self.crawl(next_offset)
        else:
            # 错误消息
            # {"ret":-3,"errmsg":"no session","cookie_count":1}
            logger.error("无法正确获取内容，请重新从Fiddler获取请求参数和请求头")
            exit()


if __name__ == '__main__':
    crawler = WeiXinCrawler()
    crawler.crawl()


from mongoengine import connect
# 连接 mongodb，无需事先创建数据库
connect('weixin', host='localhost', port=27017)