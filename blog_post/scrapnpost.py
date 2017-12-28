#!/usr/bin/env python3
import json
import praw
import re
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from blog_post.define import ADSENSE_MIDDLE


class ScrapAndPost:
    def __init__(self):
        pass

    def koreagov_news(self, bp):
        base_url1 = 'http://www.korea.kr/policy/mainView.do?'
        base_url2 = 'http://www.korea.kr/policy/policyPhotoView.do?'
        result = '<font color="blue">[한국 정책 뉴스]</font><br>'
        for i in range(1, 5):  # maybe 1~3 pages per a day
            url = 'http://www.korea.kr/policy/mainList.do?pageIndex=%d&srchRepCodeType=&repCodeType=&repCode=&startDate=%4d-%02d-%02d&endDate=%4d-%02d-%02d&srchWord=#goView' % (
                  i,
                  bp.now.year, bp.now.month, bp.now.day,
                  bp.now.year, bp.now.month, bp.now.day)
            r = bp.request_and_get(url, '정책뉴스')
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            for thumb in soup.find_all(bp.match_soup_class(['thumb'])):
                try:
                    conn_url = thumb.a['onclick'].split("'")[1]
                except TypeError:
                    continue
                except KeyError:
                    continue

                if conn_url.startswith('newsId='):
                    href = '%s%s' % (base_url1, conn_url)
                else:
                    href = '%s%s' % (base_url2, conn_url)

                img = thumb.find('img')
                title = bp.check_valid_string(img['alt'])
                result = '%s<br><a href="%s" target="_blank">- %s</a>' % (result, href, title)
        return result

    def realestate_daum(self, bp):
        r = bp.request_and_get('http://realestate.daum.net/news', 'daum부동산')
        if r is None:
            return

        result = '<font color="blue">[Daum 부동산 뉴스]</font><br>'
        soup = BeautifulSoup(r.text, 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['link_news'])):
            try:
                href = f['href']
            except TypeError:
                continue
            title = bp.check_valid_string(f.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def realestate_mbn(self, bp):
        r = bp.request_and_get('http://news.mk.co.kr/newsList.php?sc=30000020', 'mbn부동산')
        if r is None:
            return

        result = '<font color="blue">[매일경제 부동산 뉴스]</font><br>'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['art_list'])):
            href = f.a['href']
            title = bp.check_valid_string(f.a['title'])
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def realestate_hankyung(self, bp):
        r = bp.request_and_get('http://land.hankyung.com/', '한국경제부동산')
        if r is None:
            return

        result = '<font color="blue">[한국경제 부동산 뉴스]</font><br>'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        sessions = soup.select('div > h2 > a')
        for s in sessions:
            if s['href'] == 'http://www.hankyung.com/news/kisarank/':
                continue
            href = s['href']
            title = bp.check_valid_string(s.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def realestate_naver(self, bp):
        r = bp.request_and_get('http://land.naver.com/news/headline.nhn', 'Naver부동산')
        if r is None:
            return

        base_url = 'http://land.naver.com'
        result = '<font color="blue">[Naver 부동산 뉴스]</font><br>'
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('div > div > div > div > div > dl > dt > a')
        for s in sessions:
            href = '%s%s' % (base_url, s['href'])
            title = bp.check_valid_string(s.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)

        sessions = soup.select('div > ul > li > dl > dt > a')
        for s in sessions:
            if len(s.text) == 0:
                continue
            href = '%s%s' % (base_url, s['href'])
            title = bp.check_valid_string(s.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def financial_einfomax(self, bp):
        r = bp.request_and_get('http://news.einfomax.co.kr/news/articleList.html?sc_section_code=S1N16&view_type=sm', 'einfomax경제')
        if r is None:
            return

        base_url = 'http://news.einfomax.co.kr/news'
        result = ""
        result = '<font color="blue">[연합인포맥스 경제 뉴스]</font><br>'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['ArtList_Title'])):
            try:
                href = '%s/%s' % (base_url, f.a['href'])
            except TypeError:
                continue
            title = bp.check_valid_string(f.a.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def financial_chosun(self, bp):
        r = bp.request_and_get('http://biz.chosun.com/index.html', '조선일보경제')
        if r is None:
            return

        result = '<font color="blue">[조선일보 경제 뉴스]</font><br>'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['mc_art_lst'])):
            for li in f.find_all('li'):
                if li.a['href'].endswith('main_hot3'):  # 경제, 금융: main_hot1, main_hot2
                    break
                try:
                    href = li.a['href']
                except TypeError:
                    continue
                title = bp.check_valid_string(li.a.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def financial_joins(self, bp):
        r = bp.request_and_get('http://news.joins.com/money?cloc=joongang|home|section3', '중앙일보경제')
        if r is None:
            return

        base_url = 'http://news.joins.com'
        result = '<font color="blue">[중앙일보 경제 뉴스]</font><br>'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['default_realtime'])):
            for li in f.find_all('li'):
                try:
                    href = '%s%s' % (base_url, li.a['href'])
                except TypeError:
                    continue
                title = bp.check_valid_string(' '.join(li.text.strip().split()[1:-2]))
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def realestate_hani(self, bp):
        r = bp.request_and_get(' http://www.hani.co.kr/arti/economy/property/home01.html', '한겨례부동산')
        if r is None:
            return

        result = '<font color="blue">[한겨례 부동산 뉴스]</font><br>'
        base_url = 'http://www.hani.co.kr'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for article in soup.find_all(bp.match_soup_class(['article-area'])):
            href = '%s%s' % (base_url, article.a['href'])
            article = article.text.strip().split('\n')
            title = bp.check_valid_string(article[0])
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def realestate_nocut(self, bp):
        r = bp.request_and_get('http://www.nocutnews.co.kr/news/list?c1=203&c2=204&ltype=1', '노컷뉴스부동산')
        if r is None:
            return

        result = '<font color="blue">[노컷뉴스 부동산 뉴스]</font><br>'
        base_url = 'http://www.nocutnews.co.kr'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        news = soup.find(bp.match_soup_class(['newslist']))
        for dt in news.find_all('dt'):
            href = '%s%s' % (base_url, dt.a['href'])
            title = bp.check_valid_string(dt.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def realestate_nate(self, bp):
        url = 'http://news.nate.com/subsection?cate=eco03&mid=n0303&type=c&date=%s&page=1' % bp.today
        r = bp.request_and_get(url, 'Nate부동산')
        if r is None:
            return

        result = '<font color="blue">[네이트 부동산 뉴스]</font><br>'
        soup = BeautifulSoup(r.text, 'html.parser')
        for news in soup.find_all(bp.match_soup_class(['mlt01'])):
            span = news.find('span', attrs={'class': 'tb'})
            tit = span.find('strong', attrs={'class': 'tit'})
            title = bp.check_valid_string(tit.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, news.a['href'], title)
        return result

    def realestate_donga(self, bp):
        r = bp.request_and_get('http://news.donga.com/List/Economy/RE', '동아일보부동산')
        if r is None:
            return

        result = '<font color="blue">[동아일보 부동산 뉴스]</font><br>'
        soup = BeautifulSoup(r.text, 'html.parser')
        for alist in soup.find_all(bp.match_soup_class(['articleList'])):
            tit = alist.find('span', attrs={'class': 'tit'})
            title = bp.check_valid_string(tit.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, alist.a['href'], title)
        return result

    def get_reddit(self, bp, category='til'):
        result = ''
        reddit = praw.Reddit(client_id=bp.reddit_cid,
                             client_secret=bp.reddit_csec, password=bp.reddit_pw,
                             user_agent='USERAGENT', username=bp.reddit_id)

        if category == 'til':
            # for submission in reddit.subreddit('redditdev+learnpython').top('all'):
            for idx, sub in enumerate(reddit.subreddit('todayilearned').hot(limit=30)):
                temp = '<a href="%s" target="_blank">[%d] %s (⬆ %s)</a><br><pre>%s</pre><br>' % (sub.url, idx + 1, sub.title, sub.score, bp.translate_text(sub.title))
                result = '%s<br>%s' % (result, temp)
            content = '<font color="red">[레딧(Reddit) 오늘 배운거]</font>%s<br>' % result
        elif category == 'programming':
            for idx, sub in enumerate(reddit.subreddit('programming').hot(limit=30)):
                temp = '<a href="%s" target="_blank">[%d] %s (⬆ %s)</a><br><pre>%s</pre><br>' % (sub.url, idx + 1, sub.title, sub.score, bp.translate_text(sub.title))
                result = '%s<br>%s' % (result, temp)
            content = '<font color="red">[레딧(Reddit) Programming]</font>%s<br>' % result

        elif category == 'worldnews':
            for idx, sub in enumerate(reddit.subreddit('worldnews').hot(limit=30)):
                temp = '<a href="%s" target="_blank">[%d] %s (⬆ %s)</a><br><pre>%s</pre><br>' % (sub.url, idx + 1, sub.title, sub.score, bp.translate_text(sub.title))
                result = '%s<br>%s' % (result, temp)
            content = '<font color="red">[레딧(Reddit) 세계뉴스]</font>%s<br>' % result

        return content

    def hacker_news(self, bp):
        result = ''
        # p=1, rank 1~30, p=2, rank 30~60 ...
        for i in range(1, 2):
            url = 'https://news.ycombinator.com/news?p=%d' % i
            r = bp.request_and_get(url, 'HackerNews')
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            for f in soup.find_all(bp.match_soup_class(['athing'])):
                title = bp.check_valid_string(f.text)
                for s in f.find_all(bp.match_soup_class(['storylink'])):
                    href = s['href']
                    temp = '<a href="%s" target="_blank">%s</a><br><pre>%s</pre><br>' % (href, title, bp.naver_papago_nmt(title))
                    result = '%s<br>%s' % (result, temp)
        content = '<font color="red">[해커뉴스(Hacker News)]</font>%s<br>' % result
        return content

    def realestate_news(self, bp):
        result = '<h3>뉴스 언론사 목록</h3><br><strong> 노컷뉴스, Naver, Nate, Daum, 동아일보, 매일경제, 한겨례, 한국경제</strong><br><br>'

        content = self.realestate_nocut(bp)  # 노컷뉴스
        result = '%s<br><br><br>%s' % (result, content)
        content = self.realestate_naver(bp)  # Naver
        result = '%s<br><br><br>%s' % (result, content)
        content = self.realestate_nate(bp)  # Nate
        result = '%s<br><br><br>%s' % (result, content)
        content = self.realestate_daum(bp)  # Daum
        result = '%s<br><br><br>%s' % (result, content)

        result = '%s<br><br>%s<br><br>' % (result, ADSENSE_MIDDLE)  # add advertise

        content = self.donga_news(bp, 'http://news.donga.com/List/Economy/RE', '부동산')  # 동아일보
        result = '%s<br><br><br>%s' % (result, content)
        content = self.realestate_mbn(bp)  # 매일경제
        result = '%s<br><br><br>%s' % (result, content)
        content = self.realestate_hani(bp)  # 한겨례
        result = '%s<br><br><br>%s' % (result, content)
        content = self.realestate_hankyung(bp)  # 한국경제
        result = '%s<br><br><br>%s' % (result, content)
        return result

    def financial_news(self, bp):
        result = ''

        content = self.donga_news(bp, 'http://news.donga.com/Economy', '경제')  # 동아일보
        result = '%s<br><br><br>%s' % (result, content)
        content = self.financial_einfomax(bp)
        result = '%s<br><br><br>%s' % (result, content)
        content = self.financial_chosun(bp)
        result = '%s<br><br><br>%s' % (result, content)
        content = self.financial_joins(bp)
        result = '%s<br><br><br>%s' % (result, content)

        return result

    def get_exhibit_image(self, href):
        try:
            page = urllib.request.urlopen(href)
        except UnicodeEncodeError:
            return None
        base_url = href.split('/')
        base_url = '%s//%s' % (base_url[0], base_url[2])

        soup = BeautifulSoup(page, 'html.parser')
        for img in soup.find_all('img', {'src': re.compile(r'(jpe?g)|(png)$')}):
            if img['src'].find('logo') != -1:
                if img['src'].find('http') != -1:
                    return img['src']
                else:
                    img_link = '%s/%s' % (base_url, img['src'])
                    return img_link
        else:
            icon_link = soup.find("link", rel="shortcut icon")
            try:
                icon_image_link = icon_link['href']
                return icon_image_link
            except TypeError:
                return None

    def oversea_exhibition(self, bp):
        request_url = 'http://www.gep.or.kr/rest/overseasExhibition?serviceKey=%s&from=%s&to=%s&pageRows=20&pageNumber=1&type=json' % (bp.korea_data_key, bp.yesterday, bp.today)

        req = urllib.request.Request(request_url)
        try:
            res = urllib.request.urlopen(req)
        except UnicodeEncodeError:
            self.logger.error('[overseasExhibition] UnicodeEncodeError')
            return

        result = ''
        data = res.read().decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        js = json.loads(str(soup))
        for exhibit in js['overseasExhibitionListArray']:
            href = exhibit['homepage']
            if not href.startswith('http://'):
                href = 'http://%s' % href

            img_link = self.get_exhibit_image(href)
            if img_link is None:
                img_link = '#'

            exitem = exhibit['exhibitionItem']
            exitem = exitem.replace(r'\r', '<br>').replace(r'\r\n', '<br>').replace('\\r\\n', '<br>')

            temp = '<a href="%s" target="_blank"><font color="red">%s(%s)</font></a><br>전시항목: %s<br>일정: %s<br>스폰서: %s<br>주소: %s  ☎ :%s (%s %s)<br><a href="mailto:%s">Email: %s</a> (%s년 부터 %s 개최)<br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="100"></a></center><br>' % (
                   href, exhibit['exhibitionTitleKor'], exhibit['exhibitionTitleEng'],
                   exitem, exhibit['openingTerm'], exhibit['sponsor'],
                   exhibit['address'], exhibit['telephone'],
                   exhibit['openingCountry'], exhibit['openingCity'],
                   exhibit['email'], exhibit['email'],
                   exhibit['firstOpeningYear'], exhibit['openingCycle'],
                   href, img_link)
            result = '%s<br>%s' % (result, temp)
        return result

    def sacticket(self, bp):  # 예술의 전당
        driver = webdriver.PhantomJS()
        driver.implicitly_wait(3)
        url = 'https://www.sacticket.co.kr/SacHome/ticket/reservation'
        driver.get(url)
        html = driver.page_source

        result = '<h2><font color="blue">[예술의 전당]</font></h2><br>'
        soup = BeautifulSoup(html, 'html.parser')
        for p in soup.find_all(bp.match_soup_class(['ticket_list_con'])):
            for poster in p.find_all(bp.match_soup_class(['poster'])):
                for pa in poster.find_all('img'):
                    thumbnail = (pa['src'])
            if thumbnail.endswith('no_result.png'):
                continue
            for content in p.find_all(bp.match_soup_class(['content'])):
                try:
                    c_info = content.a['onclick'].split("'")
                    page_id = c_info[1]
                    page_type = c_info[3]
                    if page_type == 'E':
                        category = "[전시]"
                        link = 'https://www.sacticket.co.kr/SacHome/exhibit/detail?searchSeq=%s' % page_id
                    elif page_type == 'P':
                        category = "[공연]"
                        link = 'https://www.sacticket.co.kr/SacHome/perform/detail?searchSeq=%s' % page_id
                    else:
                        continue

                    for idx, ca in enumerate(content.find_all('a')):
                        if idx == 0:
                            title = ca.text
                        elif idx == 1:
                            if ca.text != '무료':
                                price = '유료'
                            else:
                                price = ca.text

                    temp = '<font color="red">%s</font><br>%s %s<br><br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center>' % (title, category, price, link, thumbnail)
                    result = '%s<br>%s' % (result, temp)
                except TypeError:
                    continue
        driver.quit()
        return result

    def coex_exhibition(self, bp):
        r = bp.request_and_get('http://www.coex.co.kr/blog/event_exhibition?list_type=list', 'Coex전시')
        if r is None:
            return

        result = '<h2><font color="blue">[코엑스]</font></h2><br>'
        soup = BeautifulSoup(r.text, 'html.parser')
        exhibition_url = 'http://www.coex.co.kr/blog/event_exhibition'
        for a in soup.find_all('a', href=True):
            thumbnail = ''
            if a['href'].startswith(exhibition_url) is False:
                continue

            for img in a.find_all('img'):
                thumbnail = img['src']

            if len(thumbnail) == 0:
                continue

            for idx, li in enumerate(a.find_all('li')):
                if idx % 5 == 0:
                    category = li.text
                elif idx % 5 == 1:
                    spans = li.find_all('span', attrs={'class': 'subject'})
                    for span in spans:
                        subject = span.text
                    spans = li.find_all('span', attrs={'class': 'url'})
                    for span in spans:
                        url = span.text
                    url = 'http://%s' % url
                elif idx % 5 == 2:
                    period = li.text
                elif idx % 5 == 3:
                    price = li.text
                elif idx % 5 == 4:
                    location = li.text
                    temp = '<a href="%s" target="_blank"><font color="red">%s (%s)</font></a><br>%s, %s, %s<br><br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center>' % (url, subject, category, period, location, price, url, thumbnail)
                    result = '%s<br>%s' % (result, temp)
        return result

    def aladin_book(self, bp, query_type='ItemNewAll', max_result=30):  # max 50
        url = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=%s&QueryType=%s&MaxResults=%d&start=1&SearchTarget=Book&output=js&Cover=big&Version=20131101' % (bp.aladin_key, query_type, max_result)

        r = bp.request_and_get(url, '알라딘도서')
        if r is None:
            return
        content = ''
        soup = BeautifulSoup(r.text, 'html.parser')
        books = json.loads(str(soup))

        for book in books['item']:
            title = book['title']
            link = book['link']
            desc = book['description']
            img_link = book['cover']
            publisher = book['publisher']
            priceSales = book['priceSales']
            # priceStandard = book['priceStandard']
            categoryName = book['categoryName']
            author = book['author']

            temp = '<a href="%s" target="_blank"><font color="red">%s</font></a><br>%s, %s, %s 원<br>%s<br><br>%s<br><br><center><a href="%s" target="_blank"> <img border="0" align="middle" src="%s" width="200" height="250"></a></center>' % (link, title, author, publisher, priceSales, categoryName, desc, link, img_link)
            content = '%s<br><br>%s' % (content, temp)
        return content

    def kdi_research(self, bp):  # 한국개발연구원
        thema = {'A': '거시/금융',
                 'B': '재정/복지',
                 'C': '노동/교육',
                 'D': '국제/무역',
                 'E': '산업조직',
                 'F': '경제발전/성장',
                 'G': '북한경제/경제체계',
                 'H': '농업/환경/자원',
                 'I': '지역경제',
                 'J': '기타'}

        result = ''
        base_url = 'http://www.kdi.re.kr'
        for t, value in thema.items():
            result = '%s<br><br><strong><font color="red">[%s]</font></strong>' % (result, value)
            url = 'http://www.kdi.re.kr/research/subjects_list.jsp?tema=%s' % t
            r = bp.request_and_get(url, '한국개발연구원')
            if r is None:
                return
            soup = BeautifulSoup(r.text, 'html.parser')
            sessions = soup.select('li > div > a')
            for s in sessions:
                result_url = '%s%s' % (base_url, s['href'])
                title = bp.check_valid_string(s.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, result_url, title)
        return result

    def get_visit_korea(self, bp):  # 대한민국 구석구석 행복여행
        r = bp.request_and_get('http://korean.visitkorea.or.kr/kor/bz15/where/festival/festival.jsp', '대한민국구석구석여행')
        if r is None:
            return

        base_url = 'http://korean.visitkorea.or.kr/kor/bz15/where/festival'
        result = '<font color="blue">[대한민국 구석구석 여행]</font><br>'
        soup = BeautifulSoup(r.text, 'html.parser')
        for s in soup.find_all(bp.match_soup_class(['item'])):
            if s.h3 is None:
                continue
            result_url = '%s/%s' % (base_url, s.a['href'])
            desc = repr(s.h3)[4: -6]
            img = s.find('img')
            thumbnail = img['src']
            for info in s.find_all(bp.match_soup_class(['info2'])):
                for span in info.find_all('span', {'class': 'date'}):
                    result = '%s<br><strong><a href="%s" target="_blank"><font color="red">%s</font></a></strong><br>%s<br>' % (
                             result, result_url, desc, span.text)
                    result = '%s<center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center>' % (
                             result, result_url, thumbnail)
                    break
        return result

    def domestic_exhibition(self, bp):
        result = ''

        content = self.coex_exhibition(bp)
        result = '%s<br><br><br>%s' % (result, content)
        content = self.sacticket(bp)
        result = '%s<br><br><br>%s' % (result, content)

        return result

    def opinion_hani(self, bp):
        r = bp.request_and_get('http://www.hani.co.kr/arti/opinion/home01.html?_fr=mt0', '한겨례Opinion')
        if r is None:
            return

        result = '<font color="blue">[한겨례 사설, 칼럼]</font>'
        base_url = 'http://www.hani.co.kr'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for article in soup.find_all(bp.match_soup_class(['article'])):
            for li in article.find_all('li'):
                li_href = '%s%s' % (base_url, li.a['href'])
                li_text = li.text.strip().split('\n')
                title = bp.check_valid_string(li_text[0])
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, li_href, title)
            href = '%s%s' % (base_url, article.a['href'])
            article = article.text.strip().split('\n')
            title = bp.check_valid_string(article[0])
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def donga_news(self, bp, url, category):
        r = bp.request_and_get('http://news.donga.com/Column/', '동아일보')
        if r is None:
            return

        result = '<font color="blue">[동아일보 %s]</font>' % category
        soup = BeautifulSoup(r.text, 'html.parser')
        for alist in soup.find_all(bp.match_soup_class(['articleList'])):
            tit = alist.find('span', attrs={'class': 'tit'})
            title = bp.check_valid_string(tit.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, alist.a['href'], title)
        return result

    def opinion_mbn(self, bp):
        r = bp.request_and_get('http://opinion.mk.co.kr/list.php?sc=30500003', '매일경제Opinion')
        if r is None:
            return

        result = '<font color="blue">[매일경제 사설, 칼럼]</font>'
        base_url = 'http://opinion.mk.co.kr/'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['article_list'])):
            for dt in f.find_all('dt'):
                href = '%s%s' % (base_url, dt.a['href'])
                title = bp.check_valid_string(dt.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_hankyung(self, bp):
        r = bp.request_and_get('http://news.hankyung.com/opinion', '한국경제Opinion')
        if r is None:
            return
        result = '<font color="blue">[한국경제 사설, 칼럼]</font>'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for inner_list in soup.find_all(bp.match_soup_class(['inner_list'])):
            for li in inner_list.find_all('li'):
                li_title = li.find('strong', attrs={'class': 'tit'})
                if li_title is None:
                    break
                title = bp.check_valid_string(li_title.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, li.a['href'], title)

            tit = inner_list.find('strong', attrs={'class': 'tit'})
            title = bp.check_valid_string(tit.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, inner_list.a['href'], title)
        return result

    def opinion_chosun(self, bp):
        r = bp.request_and_get('http://biz.chosun.com/svc/list_in/list.html?catid=1F&op_s', '조선일보Opinion')
        if r is None:
            return

        result = '<font color="blue">[조선일보 사설, 칼럼]</font>'
        base_url = 'http://biz.chosun.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['list_vt'])):
            for li in f.find_all('li'):
                dt = li.find('dt')
                href = '%s%s' % (base_url, li.a['href'])
                title = bp.check_valid_string(dt.a.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_joins(self, bp):
        r = bp.request_and_get('http://news.joins.com/opinion?cloc=joongang|home|section1', '중앙일보Opinion')
        if r is None:
            return

        result = '<font color="blue">[중앙일보 사설, 칼럼]</font>'
        base_url = 'http://news.joins.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for head in soup.find_all(bp.match_soup_class(['opinion_home_headline'])):
            for li in head.find_all('li'):
                href = '%s%s' % (base_url, li.a['href'])
                title = bp.check_valid_string(li.a.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)

        for today in soup.find_all(bp.match_soup_class(['opinion_home_today'])):
            for li in today.find_all('li'):
                href = '%s%s' % (base_url, li.a['href'])
                mg = li.find('strong', attrs={'class': 'mg'})
                title = bp.check_valid_string(mg.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_hankook(self, bp):
        r = bp.request_and_get('http://www.hankookilbo.com/op.aspx', '한국일보Opinion')
        if r is None:
            return
        result = '<font color="blue">[한국일보 사설, 칼럼]</font>'
        base_url = 'http://www.hankookilbo.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for col in soup.find_all(bp.match_soup_class(['editorial_column'])):
            for li in col.find_all('li'):
                href = '%s%s' % (base_url, li.a['href'])
                title = bp.check_valid_string(li.a.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_gyunghyang(self, bp):
        r = bp.request_and_get('http://news.khan.co.kr/kh_news/khan_art_list.html?code=990000', '경향신문Opinion')
        if r is None:
            return

        result = '<font color="blue">[경향신문 사설, 칼럼]</font>'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for news_list in soup.find_all(bp.match_soup_class(['news_list'])):
            for li in news_list.find_all('li'):
                try:
                    title = bp.check_valid_string(li.a['title'])
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, li.a['href'], title)
                except KeyError:
                    title = bp.check_valid_string(li.text.split('\n')[1])
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, li.a['href'], title)
        return result

    def opinion_kookmin(self, bp):
        url = 'http://news.kmib.co.kr/article/list.asp?sid1=opi&sid2=&sdate=%s' % bp.yesterday
        r = bp.request_and_get(url, '국민일보Opinion')
        if r is None:
            return

        base_url = 'http://news.kmib.co.kr/article'
        result = '<font color="blue">[국민일보 사설]</font>'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for nws_list in soup.find_all(bp.match_soup_class(['nws_list'])):
            for dl in nws_list.find_all('dl'):
                if dl.text == '등록된 기사가 없습니다.':
                    result = '%s<br>현재 %s<br>' % (result, dl.text)
                    return result
                dt = dl.find('dt')
                href = '%s/%s' % (base_url, dt.a['href'])
                title = bp.check_valid_string(dt.a.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_segye(self, bp):
        r = bp.request_and_get('http://www.segye.com/opinion', '세계일보Opinion')
        if r is None:
            return

        result = '<font color="blue">[세계일보 사설, 칼럼]</font>'
        base_url = 'http://www.segye.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for title_1 in soup.find_all(bp.match_soup_class(['title_1'])):
            href = '%s%s' % (base_url, title_1.a['href'])
            title = bp.check_valid_string(title_1.a.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        for title_2 in soup.find_all(bp.match_soup_class(['title_2'])):
            href = '%s%s' % (base_url, title_2.a['href'])
            title = bp.check_valid_string(title_2.a.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_moonhwa(self, bp):
        r = bp.request_and_get('http://www.munhwa.com/news/section_list.html?sec=opinion&class=0', '문화일보Opinion')
        if r is None:
            return

        result = '<font color="blue">[문화일보 사설, 칼럼]</font>'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for d14b_333 in soup.find_all(bp.match_soup_class(['d14b_333'])):
            title = bp.check_valid_string(d14b_333.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, d14b_333['href'], title)
        return result

    def opinion_news(self, bp):
        result = '언론사 목록<br><strong> 경향신문, 국민일보, 동아일보, 매일경제, 문화일보, 세계신문, 중앙일보, 조선일보, 한겨례, 한국경제, 한국일보</strong><br><br>'

        content = self.opinion_gyunghyang(bp)  # 경향신문
        result = '%s<br><br><br>%s' % (result, content)
        content = self.opinion_kookmin(bp)  # 국민일보
        result = '%s<br><br><br>%s' % (result, content)
        content = self.donga_news(bp, 'http://news.donga.com/Column/', '사설, 칼럼')  # 동아일보
        result = '%s<br><br><br>%s' % (result, content)
        content = self.opinion_mbn(bp)  # 매일경제
        result = '%s<br><br><br>%s' % (result, content)
        content = self.opinion_moonhwa(bp)  # 문화일보
        result = '%s<br><br><br>%s' % (result, content)
        content = self.opinion_segye(bp)  # 세계신문
        result = '%s<br><br><br>%s' % (result, content)

        result = '%s<br><br>%s<br><br>' % (result, ADSENSE_MIDDLE)  # add advertise

        content = self.opinion_joins(bp)  # 중앙일보
        result = '%s<br><br><br>%s' % (result, content)
        content = self.opinion_chosun(bp)  # 조선일보
        result = '%s<br><br><br>%s' % (result, content)
        content = self.opinion_hani(bp)  # 한겨례
        result = '%s<br><br><br>%s' % (result, content)
        content = self.opinion_hankyung(bp)  # 한국경제
        result = '%s<br><br><br>%s' % (result, content)
        content = self.opinion_hankook(bp)  # 한국일보
        result = '%s<br><br><br>%s' % (result, content)

        return result

    def weekday(self, bp):
        title = '[%s] 국내 주요언론사 사설, 칼럼 (ㄱ,ㄴ순)' % bp.today
        content = self.opinion_news(bp)
        bp.tistory_post('scrapnpost', title, content, '767067')  # 사설, 칼럼

        title = '[%s] 부동산 뉴스 헤드라인 모음(노컷뉴스, Naver, Nate, Daum, 동아일보, 매일경제, 한겨례, 한국경제)' % bp.today
        content = self.realestate_news(bp)
        bp.tistory_post('scrapnpost', title, content, '765348')

        title = '[%s] 경제 금융 뉴스 헤드라인 모음(연합인포맥스, 조선일보, 중앙일보)' % bp.today
        content = self.financial_news(bp)
        bp.tistory_post('scrapnpost', title, content, '765357')

        title = '[%s] 정책뉴스' % bp.today
        content = self.koreagov_news(bp)
        bp.tistory_post('scrapnpost', title, content, '766948')  # korea department

        title = '[%s] Reddit에 공유된 오늘 내가 배운것(Today I Learned)' % bp.today
        content = self.get_reddit(bp, 'til')
        bp.tistory_post('scrapnpost', title, content, '765395')

    def weekend(self, bp):
        title = '[%s] Reddit의 세계뉴스' % bp.today
        content = self.get_reddit(bp, 'worldnews')
        bp.tistory_post('scrapnpost', title, content, '765357')

        title = '[%s] Reddit의 Programming 관련 소식' % bp.today
        content = self.get_reddit(bp, 'programming')
        bp.tistory_post('scrapnpost', title, content, '765668')  # IT news

        title = '[%s] Hacker News (Ranking 1~30)' % bp.today
        content = self.hacker_news(bp)
        bp.tistory_post('scrapnpost', title, content, '765668')  # IT news

    def scrapnpost(self, bp):
        if bp.week_num < 5:
            self.weekday(bp)

        if bp.week_num == 0:
            title = '[%s] Reddit의 세계뉴스' % bp.today
            content = self.get_reddit(bp, 'worldnews')
            bp.tistory_post('scrapnpost', title, content, '765357')
            title = '[%s] 해외 전시 정보' % bp.today
            content = self.oversea_exhibition(bp)
            bp.tistory_post('scrapnpost', title, content, '765395')
        elif bp.week_num == 1:
            title = '[%s] Reddit의 Programming 관련 소식' % bp.today
            content = self.get_reddit(bp, 'programming')
            bp.tistory_post('scrapnpost', title, content, '765668')  # IT news
        elif bp.week_num == 2:
            title = '[%s] Hacker News (Ranking 1~30)' % bp.today
            content = self.hacker_news(bp)
            bp.tistory_post('scrapnpost', title, content, '765668')  # IT news
        elif bp.week_num == 3:
            title = '[%s] 주목할 만한 신간 리스트 - 국내도서 20권(알라딘)' % bp.today
            content = self.aladin_book(bp, 'ItemNewSpecial', 20)
            bp.tistory_post('scrapnpost', title, content, '765395')
            title = '[%s] 베스트셀러 - 30권(알라딘)' % bp.today
            content = self.aladin_book(bp, 'Bestseller', 30)
            bp.tistory_post('scrapnpost', title, content, '765395')
        elif bp.week_num == 4:
            title = '[%s] 코엑스, 예술의 전당(공연, 전시)' % bp.today
            content = self.domestic_exhibition(bp)
            bp.tistory_post('scrapnpost', title, content, '765395')
            title = '[%s] 국내 축제, 행사 일정 (대한민국 구석구석 행복여행)' % bp.today
            content = self.get_visit_korea(bp)  # 대한민국 구석구석 행복여행
            bp.tistory_post('scrapnpost', title, content, '765395')

        # content = self.kdi_research(bp)
        # title = '[%s] KDI 한국개발연구원 연구주제별 보고서' % today
        # bp.tistory_post('scrapnpost', title, content, '766948')  # korea department
