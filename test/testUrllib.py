# coding=utf-8
import urllib.request

# 获取一个get请求
# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode("utf-8"))

# 获取一个post请求
# import urllib.parse
#
# data = bytes(urllib.parse.urlencode({"r1": 1, "r2": "2"}), encoding="utf-8")
# response = urllib.request.urlopen("http://httpbin.org/post", data=data)
# print(response.read().decode("utf-8"))

# 超时处理
# try:
#     response = urllib.request.urlopen("http://httpbin.org/get", timeout=0.01)
#     print(response.read().decode("utf-8"))
# except urllib.error.URLError as timeout:
#     print("超时了！%s" % timeout)


url = "http://www.douban.com"
data = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.97 "
                  "Safari/537.36 "
}
req = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))
"https://i.pximg.net/img-original/img/2020/06/12/14/03/45/82263970_p1.png"
"https://i.pximg.net/img-original/img/2020/06/12/14/03/45/82263970_p0.png"