# coding=utf-8
from bs4 import BeautifulSoup  # 网页解析，获取数据
import urllib.request
import re

# baseurl = "https://movie.douban.com/top250?start="
# baseurl = "https://www.pixiv.net/bookmark.php"
# baseurl = "https://i.pximg.net/img-original/img/2020/02/11/15/43/55/79416681_p0.jpg"
# baseurl = "https://i.pximg.net/img-original/img/2020/05/04/20/14/39/81292498_p0.jpg"
# baseurl= "https://i.pximg.net/img-original/img/2019/11/23/00/00/11/77941126_p0.png"
# baseurl = "https://i.pximg.net/img-original/img/2020/06/08/00/00/17/82169888_p0.png"
baseurl = "https://i.pximg.net/img-original/img/2020/06/05/21/06/50/82109697_p0.jpg"

"https://i.pximg.net/c/150x150/img-master/img/   2020/06/05/21/06/50/82109697   _p0_master1200.jpg"



# findLink = re.compile(r'<a href="(.*)">')
# findImageSrc =re.compile(r'<img.*src="(.*?)"')
# findTitle =re.compile(r'<span class="title">(.*?)<')
# findRating = re.compile(r'<span class="rating_num".*>(.*?)<')
# findJudge = re.compile(r'<span>(\d*)人评价</span>')

findImageSrc = re.compile(r'<a href="/artworks/(\d+)"')


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 1):  # 调用获取页面信息的函数，10次
        # url = baseurl + str(i * 25)
        # url = baseurl

        url = "https://i.pximg.net/img-original/img/2020/06/08/00/00/17/82169888_p0.png"
        html = askURL(url)  # 保存获取到的网页源码

    # 2.逐一解析数据
    # soup = BeautifulSoup(html, "html.parser")
    # for item in soup.find_all('div', class_='item'):
    # for item in soup.find_all('li', class_='image-item'):
    # print(item)
    # print(soup)
    # data = []
    # item = str(item)
    # link = re.findall(findImageSrc, item)[0]
    # print("\"https://www.pixiv.net/artworks/"+link+"\",")

    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    headers = {
        "Referer": "https://www.pixiv.net/artworks/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 "
                      "Safari/537.36 ",
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
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read()#.decode("utf-8")
        f = open("123.jpg","wb")
        f.write(html)
        f.close()
        print(type(html))
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


getData(baseurl)
