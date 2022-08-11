import requests
import parsel
import prettytable as pt
 
headers = {
    'Referer': 'https://so.******.com/?wd=%E9%9B%B7%E7%A5%9E4',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
 
 
def response(url):
    resp = requests.get(url=url, headers=headers).text
    return resp
 
 
def get_url(url):
    resp = response(url)
    selec = parsel.Selector(resp)
    # film_id = re.findall('<a class="a".*?data-id="(.*?)".*?title="(.*?)/.*?</a>', resp)
    film_url = selec.css('body > div.div.lists > div.left > ul > li > a::attr(href)').getall()
    # title = selec.css('body > div.div.lists > div.left > ul > li> div > h3 > a::text').getall()
    return film_url
 
 
def get_download_url(url):
    resp = response(url)
    selec = parsel.Selector(resp)
    download_url = selec.css('body > div.div.item > div.left > div.btdown > ul > li > a::attr(href)').getall()
    return download_url
 
 
def get_seed(url):
    resp = response(url)
    select = parsel.Selector(resp)
    seed = select.css('body > div.div.lists > div.left h3 b::text').getall()
    return seed
 
 
def run(url):
    seed = get_seed(url)
    down_url = get_url(url)
    tb = pt.PrettyTable()
    tb.field_names = ['序号', '标题', '种子', '评分']
    num = 0
    download_url = []
    for film_url in down_url:
        # print(film_url)
        respons = response(film_url)
        selector = parsel.Selector(respons)
        score = selector.css('body > div.div.item > div.left > div.main > ul > li:nth-child(8)::text').get()
        title = selector.css('body > div.div.item > div.left > div.main > ul > li > h1::text').get()
        down_link = get_download_url(film_url)
        download_url.append(down_link)
        tb.add_row([num, title, score, seed[num]])
        num += 1
    print(tb)
    while True:
        print('--------想要翻页请输入大于19的数字---------')
        index = int(input('请输入想要下载的链接(-1退出)：'))
        if index == -1:
            break
        elif index > 19:
            print('请输入页码大于1')
            main()
        else:
            if seed[index] == '无种':
                print('无种')
            else:
                print(download_url[index])
 
 
def main():
    key = input('请输入你想要下载的内容：')
    page = input('请从1开始请输入你想要的搜索页数：')
    url = f'https://so.******.com/?wd={key}&page={page}'
    run(url)
 
 
if __name__ == '__main__':
    main()
# 手动翻页
