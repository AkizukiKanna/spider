# coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
import re
import time
import os


def main():
    # while True:
    #     # 获取收藏总页数 int类型
    #     try:
    #         totalPageNum = getTotalPageNum(baseurl)
    #         print("总页数为： %d" % totalPageNum)
    #         break
    #     except Exception as result:
    #         print(result)

    totalPageNum = getTotalPageNum(baseurl)
    print("总页数为： %d" % totalPageNum)

    # 爬取网页
    datalist = getData(baseurl, totalPageNum)
    # datalist = getData(baseurl, 11)

    dbpath = "movie.db"
    # 3.保存数据
    # saveData(datalist,savepath)
    # saveData2DB(datalist, dbpath)

    # askURL("https://movie.douban.com/top250?start=")


# 定义规则
# 每页最后一页的序号
findLastPageNum = re.compile(r'<li.*>(\d+)<')
# 提取data-src属性中的链接
findDataSrc = re.compile(r'data-src="(.*?)"')
# 提取图片链接中间的时间码
findPicDate = re.compile(r'img/(.*?)_p')
# 提取图片后缀名
findSuffix = re.compile(r'[^\.]\w*$')
# 获取最后一个/后的所有字符
findName = re.compile(r'[^/]+(?!.*/)')


# 获取收藏总页数
def getTotalPageNum(baseurl):
    max = -1
    current = 1

    while True:
        url = baseurl + str(current)
        html = askURL(url, headers)
        # 测试是否获取页面
        # print(html)

        # 解析页面
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("ul.page-list>li")
        # for item in soup.select("ul.page-list>li"):
        lastItem = items.pop()
        # lastPageNum是str
        lastPageNum = re.findall(findLastPageNum, str(lastItem)).pop()
        # print(lastPageNum)
        lastPageNum = int(lastPageNum)
        current = lastPageNum

        # 判断当前页是不是最后一页
        if current > max:
            max = current
        elif current == max:
            break

    return max


# 爬取网页
def getData(baseurl, totalPageNum):
    # i从1递增循环到总页数
    for i in range(1, totalPageNum + 1):
        # for i in range(11,12):
        url = baseurl + str(i)
        html = askURL(url, headers)

        # 开始解析
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="_layout-thumbnail"):
            print("正在处理收藏页第%d页中的内容：" % i)
            item = str(item)
            # print(item)
            # 提取data-src连接
            dataSrc = re.findall(findDataSrc, item)[0]
            # print(dataSrc)
            # 获得单个图片原图链接
            originalDataSrc = getOriginalDataSrc(dataSrc)
            # 图片链接不为空字符串时下载
            if originalDataSrc != "":
                # 保存图片到本地
                flag = savePicture2Home(originalDataSrc)
                if flag:
                    print("更新完毕")
                    return 1
                # pass
                # break
    return 1


# 得到指定一个URL的网页内容
def askURL(url, headers):
    header = headers
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=header)
    html = ""
    while True:
        try:
            response = urllib.request.urlopen(request, timeout=5)
            html = response.read().decode("utf-8")

            break

        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
                # 是超时异常就继续循环
                if str(type(e.reason)) != "<class 'socket.timeout'>":
                    break

                time.sleep(3)

    return html


# 保存数据
def saveData2DB(datalist, dbpath):
    pass


# 把获取到的图片链接处理成原图链接
def getOriginalDataSrc(dataSrc):
    picDate = ""
    suffix = ""
    originalDataSrc = ""

    try:
        # 当图片不存在时出现异常,返回空字符串
        picDate = re.findall(findPicDate, dataSrc)[0]
    except IndexError as e:
        print(e)
        return originalDataSrc

    suffix = re.findall(findSuffix, dataSrc)[0]

    originalDataSrc = "https://i.pximg.net/img-original/img/" + picDate + "_p0." + suffix
    # print(originalDataSrc)

    return originalDataSrc


# 保存图片到本地
def savePicture2Home(originalDataSrc_):
    originalDataSrc = originalDataSrc_
    header = headers

    flag = False
    while True:
        request = urllib.request.Request(originalDataSrc, headers=header)
        try:
            response = urllib.request.urlopen(request, timeout=5)
            html = response.read()
            print(originalDataSrc)

            picName = re.findall(findName, originalDataSrc)[0]

            flag = os.path.isfile(floder + picName)
            print("文件是否存在：" + str(flag))

            # 存在同名文件，证明已经更新完毕，退出
            if flag:
                break

            # 真正下载保存
            f = open(floder + picName, "wb")
            f.write(html)
            f.close()

            print("已下载保存为：" + picName)

            break
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
                if e.code == 404:
                    originalDataSrc = originalDataSrc.replace(".jpg", ".png")
                    continue

            if hasattr(e, "reason"):
                print(e.reason)
                if str(type(e.reason)) == "<class 'socket.timeout'>":
                    time.sleep(3)

    return flag


if __name__ == "__main__":  # 当程序执行时
    # 全局变量
    baseurl = "https://www.pixiv.net/bookmark.php?rest=show&p="
    totalPageNum = 0
    floder = "E:\myPictures\\"
    headers = {
        "Referer": "https://www.pixiv.net/artworks/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36",
        "cookie": "first_visit_datetime_pc=2020-01-10+22%3A34%3A46; yuid_b=IFUWZYg; p_ab_id=8; p_ab_id_2=7; "
                  "p_ab_d_id=218959166; _ga=GA1.2.1267203264.1578663290; "
                  "PHPSESSID=11675086_MbwvQ4iP93vpUdv9funy1lKZaoaimuwM; c_type=23; a_type=0; b_type=1; "
                  "module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name"
                  "%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C"
                  "%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C"
                  "%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A"
                  "%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible"
                  "%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A"
                  "%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22"
                  "%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A"
                  "%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C"
                  "%22visible%22%3Atrue%7D%5D; login_ever=yes; "
                  "__utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=11675086=1^9"
                  "=p_ab_id=8=1^10=p_ab_id_2=7=1^11=lang=zh=1; ki_r=; "
                  "__gads=ID=b1d666dcc40ad735:T=1579527662:S=ALNI_Mbwr9qtwnKiiXck2Hsue1QQ84L7ow; "
                  "adr_id=9QoL6aA6Yr3LmLCAVJb2YtgZF9zi13aPRABBW64tFFmSmBsa; ki_s=204128%3A0.0.0.0.0; "
                  "_fbp=fb.1.1586866752102.2120369726; privacy_policy_agreement=2; "
                  "_td=8f52b870-cd82-49bb-a9ac-471d7bc206e2; __utmz=235335808.1590055309.36.4.utmcsr=t.co|utmccn=("
                  "referral)|utmcmd=referral|utmcct=/e3HU5TpFwM; "
                  "__cfduid=d59899b9a9e36c34dcee1ce5521390f061591410619; "
                  "categorized_tags=6sZKldb07K~8NpFhmNqI1~BeQwquYOKY~CADCYLsad0~DU9jLF-LB5~EGefOqA6KB~HggoqlYqNr"
                  "~IRbM9pb4Zw~IVwLyT8B6k~Qa8ggRsDmW~RcahSSzeRf~b8b4-hqot7~iFcW6hPGPU~pvU1D1orJa; "
                  "tag_view_ranking=RTJMXD26Ak~Lt-oEicbBr~azESOjmQSV~KN7uxuR89w~jH0uD88V6F~tgP8r-gOe_~ETjPkL0e6r"
                  "~0xsDLqCEW6~Ie2c51_4Sp~Bd2L9ZBE8q~faHcYIP1U0~BtXd1-LPRH~RybylJRnhJ~cbmDKjZf9z~wKl4cqK7Gl"
                  "~w8ffkPoJ_S~RcahSSzeRf~65aiw_5Y72~lxfrUKMf9f~Pt9XriSgeT~X_1kwTzaXt~5oPIfUbtd6~pzzjRSV6ZO"
                  "~qcYo_5oqVP~pYlUxeIoeg~28gdfFXlY7~v3nOtgG77A~y3RUmuZ1U0~kdkWnz2DyL~zyKU3Q5L4C~x_jB0UM4fe"
                  "~7WfWkHyQ76~5jQydRTLzH~nQRrj5c6w_~b1s-xqez0Y~HY55MqmzzQ~L58xyNakWW~q303ip6Ui5~QzKFCsGzn"
                  "-~PBxKNk7VAD~BhqIXEb2EA~8NpFhmNqI1~DU9jLF-LB5~CiSfl_AE0h~EUwzYuPRbU~rqnJSF7cpq~xha5FQn_XC"
                  "~I8PKmJXPGb~iFcW6hPGPU~EGefOqA6KB~uW5495Nhg-~K8esoIs2eW~PTyxATIsK0~GNtSSjSHgG~Bx3XxRyJlI"
                  "~u8McsBs7WV~mN7k7MZ5SW~eVxus64GZU~3LOiwUdki2~NBK37t_oSE~wUw07XxW8B~2EpPrOnc5S~NXxDJr1D_u"
                  "~enEDtQTJS4~n7YxiukgPF~XDEWeW9f9i~q0cY8_KmiN~5EjOeQ9rhR~1HSjrqSB3U~VTeFUlRxgl~CrFcrMFJzz"
                  "~IyRhOdNpxG~GNcgbuT3T-~mzJgaDwBF5~rNWcU0S3yo~yv-MdmoUJ0~eVBXl1t9y6~KrZGK03ZBi~MhieHQxNXo"
                  "~MM6RXH_rlN~Qa8ggRsDmW~gpglyfLkWs~_pwIgrV8TB~MSNRmMUDgC~wBaT7BbUEi~v7Qz4joCBq~Itu6dbmwxu"
                  "~vFXX3OXCCb~mFuvKdN_Mu~y3NlVImyly~3r9E8FVuwx~MwT2M45J6E~NGpDowiVmM~ZXRBqRlFWu~jk9IzfjZ6n"
                  "~4SyVAI2yYS~xjfPXTyrpQ~1Xn1rApx2-~gVfGX_rH_Y~jhuUT0OJva; "
                  "__utma=235335808.1267203264.1578663290.1591623721.1591763532.41; __utmc=235335808; __utmt=1; "
                  "ki_t=1579002097588%3B1591763541009%3B1591763541009%3B30%3B40; __utmb=235335808.2.10.1591763532; "
                  "tags_sended=1 "
    }
    # 调用函数
    main()
    # init_db("movietest.db")
    print("爬取完毕！")
