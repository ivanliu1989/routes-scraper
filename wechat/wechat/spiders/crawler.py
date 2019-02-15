import requests


def headers_to_dict(headers):
    """
    将字符串
    '''
    Host: mp.weixin.qq.com
    Connection: keep-alive
    Cache-Control: max-age=
    '''
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


def crawl():
    # url中的参数需要根据自己的情况做调整
    url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTA5NjAyMA==&scene=126&bizpsid=0&devicetype=android-19&version=27000334&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=mG5PIqAHg2jAY%2B6NQAJtsyEedBCeybGVZzm4RzZefynPWKfgdSyywrnG6soSsQ0w&wx_header=1"

    headers = """
Host: mp.weixin.qq.com
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
x-wechat-uin: MjcxMTc3MDU3NQ%3D%3D
x-wechat-key: 2a1ec6e06caed27b836a61fc016d19630bc9bab942ce171b106ace8c331b9f785595603bac6c514ead11d032813dafeafc98eb8ccbe01b5f9dc9fda54823bd7c994ca164c5deb65c1e3825cff18d8084
User-Agent: Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 MMWEBID/2090 MicroMessenger/7.0.3.1400(0x27000334) Process/toolsmp NetType/WIFI Language/zh_CN
Accept-Encoding: gzip,deflate
Accept-Language: zh-AU,en-US;q=0.8
Cookie: rewardsn=; wxtokenkey=777; wxuin=2711770575; devicetype=android-19; version=27000334; lang=zh_CN; pass_ticket=mG5PIqAHg2jAY+6NQAJtsyEedBCeybGVZzm4RzZefynPWKfgdSyywrnG6soSsQ0w; wap_sid2=CM+riY0KElxtbFZYTF9DT0FKLXJGMGpMOEhGbmdkMkRpbDRWeUFNUFkzbDZJVFhUSmRsQ2pLeGM2WlBEQ3ZpclJ6WVNUR1BKTmpXWjVrTV92VGotS212cktKZVNDLVFEQUFBfjCGv5rjBTgNQJVO
X-Requested-With: com.tencent.mm
    """
    headers = headers_to_dict(headers)
    response = requests.get(url, headers=headers, verify=False)
    print(response.text)
    if '<title>验证</title>' in response.text:
        raise Exception("获取微信公众号文章失败，可能是因为你的请求参数有误，请重新获取")
    data = extract_data(response.text)
    for item in data:
        print(item)


def extract_data(html_content):
    """
    从html页面中提取历史文章数据
    :param html_content 页面源代码
    :return: 历史文章列表
    """
    import re
    import html
    import json

    rex = "msgList = '({.*?})'"
    pattern = re.compile(pattern=rex, flags=re.S)
    match = pattern.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        for item in articles:
            print(item)
        return articles


if __name__ == '__main__':
    crawl()
