#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from blog_post.dexa import DailyLifeAndPost
from blog_post.scrapnpost import ScrapAndPost


class NaverPost:
    def __init__(self):
        self.dap = DailyLifeAndPost()
        self.sap = ScrapAndPost()

    def naver_celeb(self, bp):
        r = bp.request_and_get('http://entertain.naver.com/home', 'Naver연예')
        if r is None:
            return

        result = '<font color="blue">[Naver에서 가장 많이 본 연예뉴스]</font><br>'
        soup = BeautifulSoup(r.text, 'html.parser')
        cnt = 0
        for section in soup.find_all(bp.match_soup_class(['home_hit_grid'])):
            for home in section.find_all(bp.match_soup_class(['rank_news_ct'])):
                href = home.a['href']
                temp = home.find('a', attrs={'class': 'title'})
                title = bp.check_valid_string(temp.text)
                temp = home.find('a', attrs={'class': 'summary'})
                summary = ''
                try:
                    summary = temp.text.strip()
                except AttributeError:
                    pass
                for img in home.find_all('img'):
                    thumbnail = img['data-src']
                    break

                temp = '<a href="%s" target="_blank"><strong>%d. %s</strong></a><br>%s<br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center><br>' % (
                       href, cnt + 1, title, summary, href, thumbnail)
                result = '%s<br>%s' % (result, temp)
                cnt += 1
                if cnt == 10:  # 1~5, 5~10(연예), 11~15(audio), 15~20(video)
                    return result

        return result

    def daum_celeb(self, bp):
        r = bp.request_and_get('http://media.daum.net/entertain', 'Daum연예')
        if r is None:
            return
        result = '<font color="blue">[Daum에서 가장 많이 본 연예뉴스]</font><br>'
        soup = BeautifulSoup(r.text, 'html.parser')
        for section in soup.find_all(bp.match_soup_class(['section_manyhits'])):
            thumbnail = ''
            for l in section.find_all(bp.match_soup_class(['link_cont'])):
                try:
                    href = l['href']
                except TypeError or KeyError:
                    continue
                for img in l.find_all('img'):
                    thumbnail = (img['src'])
                    break
                title = l.text.strip().split('\n')
                if int(title[0]) > 3:
                    temp = '<a href="%s" target="_blank"><strong>%s. %s</strong></a><br><br>' % (
                           href, title[0], ' '.join(title[1:]))
                else:
                    temp = '<a href="%s" target="_blank"><strong>%s. %s</strong></a><br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center><br>' % (
                           href, title[0], ' '.join(title[1:]), href, thumbnail)
                result = '%s<br>%s' % (result, temp)
        return result

    def nate_celeb(self, bp):
        url = 'http://news.nate.com/rank/interest?sc=ent&p=day&date=%s' % bp.today
        r = bp.request_and_get(url, 'Nate연예')
        if r is None:
            return
        result = '<font color="blue">[Nate에서 가장 많이 본 연예뉴스]</font><br>'
        soup = BeautifulSoup(r.text, 'html.parser')
        cnt = 1
        for rank in soup.find_all(bp.match_soup_class(['postRankSubjectList'])):
            for mlt in rank.find_all(bp.match_soup_class(['mlt01'])):
                for img in mlt.find_all('img'):
                    thumbnail = (img['src'])
                    break
                href = mlt.a['href']
                temp = mlt.text.strip().replace('\t', '')
                title = temp.split('\n')
                temp = '<a href="%s" target="_blank"><strong>%s. %s</strong><br></a><br>%s<br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="50" height="50"></a></center><br>' % (
                       href, cnt, title[0], ' '.join(title[1:]), href, thumbnail)
                result = '%s<br>%s' % (result, temp)
                cnt += 1
        return result

    def entertainment(self, bp):
        result = ''

        content = self.naver_celeb(bp)
        result = '%s<br>%s' % (result, content)
        content = self.daum_celeb(bp)
        result = '%s<br>%s' % (result, content)
        content = self.nate_celeb(bp)
        result = '%s<br>%s' % (result, content)

        return result

    def hani_car(self, bp):
        r = bp.request_and_get('http://www.hani.co.kr/arti/economy/car/home01.html', '한겨례자동차')
        if r is None:
            return
        result = '<font color="blue">[한겨례 자동차 뉴스]</font><br>'
        base_url = 'http://www.hani.co.kr'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for article in soup.find_all(bp.match_soup_class(['article-area'])):
            href = '%s%s' % (base_url, article.a['href'])
            article = article.text.strip().split('\n')
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, article[0])
        return result

    def nocut_car(self, bp):
        r = bp.request_and_get('http://www.nocutnews.co.kr/news/list?c1=203&c2=209&ltype=1', '노컷뉴스자동차')
        if r is None:
            return
        base_url = 'http://www.nocutnews.co.kr'
        result = '<font color="blue">[노컷뉴스 자동차 뉴스]</font><br>'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        news = soup.find(bp.match_soup_class(['newslist']))
        for dt in news.find_all('dt'):
            href = '%s%s' % (base_url, dt.a['href'])
            title = bp.check_valid_string(dt.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def nate_car(self, bp):
        r = bp.request_and_get('http://auto.nate.com/', 'Nate자동차')
        if r is None:
            return

        result = '<font color="blue">[네이트 자동차 뉴스]</font><br>'
        # soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        soup = BeautifulSoup(r.text, 'html.parser')
        for news in soup.find_all(bp.match_soup_class(['broadcast_webzine01_list'])):
            for li in news.find_all('li'):
                href = li.a['href']
                title = bp.check_valid_string(li.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def car_news(self, bp):
        result = ''

        content = self.hani_car(bp)
        result = '%s<br><br><br>%s' % (result, content)
        content = self.nocut_car(bp)
        result = '%s<br><br><br>%s' % (result, content)
        content = self.nate_car(bp)
        result = '%s<br><br><br>%s' % (result, content)

        return result

    def hyundai_curture_center(self, bp):
        result = '<strong><font color="blue">[현대백화점 문화센터 추천강좌]</font></strong><br><br>'
        base_url = 'https://www.ehyundai.com'
        lcode = {'압구정본점': '210',
                 '무역센터점': '220',
                 '천호점': '260',
                 '신촌점': '270',
                 '미아점': '410',
                 '목동점': '420',
                 '부천중동점': '430',
                 '킨텍스점': '450',
                 '부산점': '240',
                 '울산동구점': '250',
                 '울산점': '290',
                 '대구점': '460',
                 '충청점': '470',
                 '판교점': '480',
                 '디큐브시티(신도림)점': '490',
                 '가든파이브(송파)점': '750', }
        result = '%s<pre>' % result
        cnt = 1
        for location, code in lcode.items():
            part_url = 'http://www.ehyundai.com/newCulture/CT/CT010200_L.do?stCd=%s' % code
            result = '%s<a href="%s" target="_blank">%d. %s</a><br>' % (result, part_url, cnt, location)
            cnt += 1
        result = '%s</pre>' % result

        for location, code in lcode.items():
            result = '%s<br><br><font color="red">[%s]</font><br>' % (result, location)
            url = 'http://www.ehyundai.com/newCulture/CT/CT010200_L.do?stCd=%s' % code
            r = bp.request_and_get(url, '현대백화점문화센터')
            if r is None:
                return
            soup = BeautifulSoup(r.text, 'html.parser')
            for best in soup.find_all(bp.match_soup_class(['best_lecturelist'])):
                for li in best.find_all('li'):
                    href = '%s%s' % (base_url, li.a['href'])
                    date = li.find('span', attrs={'class': 'date'})
                    fee = li.find('span', attrs={'class': 'fee'})
                    result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong><br>%s<br>%s<br>' % (
                             result, href, li.a.text.strip(), date.text, fee.text)
        return result

    def lotte_curture_center(self, bp):
        result = '<strong><font color="blue">[롯데백화점 문화센터 추천강좌]</font></strong><br><br>'
        lcode = {'본점(명동)': '0001', '잠실점': '0002', '청량리점': '0004',
                 '부산본점': '0005', '관악점': '0006', '광주점': '0007',
                 '분당점': '0008', '부평점': '0009', '영등포점': '0010',
                 '일산점': '0011', '대전점': '0012', '강남점': '0013',
                 '포항점': '0014', '울산점': '0015', '동례점': '0016',
                 '창원점': '0017', '안양점': '0018', '인천점': '0020',
                 '노원점': '0022', '대구점': '0023', '상인점': '0024',
                 '전주점': '0025', '미아점': '0026', '센텀시티점': '0027',
                 '건대스타시티점': '0028',
                 '광복점': '0333', '중동점': '0334', '구리점': '0335',
                 '안산점': '0336', '김포공항점': '0340', '평촌점': '0341',
                 '수원점': '0349', '마산점': '0354', }

        result = '%s<pre>' % result
        cnt = 1
        for location, code in lcode.items():
            part_url = 'https://culture.lotteshopping.com/CLSS_list.do?taskID=L&pageNo=1&vpStrCd=&vpKisuNo=&vpClassCd=&vpTechNo=&pStrCd=%s&pLarGbn=&pMidGbn=&pClsFee=&pDayGbnAll=&pDayTime=&pStatus=&pKisuValue=C&pClsNm=&pClsNmTemp=&pTechNm=&pTechNmTemp=' % code
            result = '%s<a href="%s" target="_blank">%d. %s</a><br>' % (result, part_url, cnt, location)
            cnt += 1
        result = '%s</pre>' % result
        for location, code in lcode.items():
            result = '%s<br><br><font color="red">[%s]</font><br>' % (result, location)
            url = 'https://culture.lotteshopping.com/CLSS_list.do?taskID=L&pageNo=1&vpStrCd=&vpKisuNo=&vpClassCd=&vpTechNo=&pStrCd=%s&pLarGbn=&pMidGbn=&pClsFee=&pDayGbnAll=&pDayTime=&pStatus=&pKisuValue=C&pClsNm=&pClsNmTemp=&pTechNm=&pTechNmTemp=' % code

            r = bp.request_and_get(url, '롯데백화점문화센터')
            if r is None:
                return
            soup = BeautifulSoup(r.text, 'html.parser')
            for i1, article in enumerate(soup.find_all(bp.match_soup_class(['article']))):
                if i1 == 0:  # side menu
                    continue
                for i2, tr in enumerate(article.find_all('tr')):
                    if i2 == 0:  # category
                        continue
                    onclick = tr.find('input', {'name': 'chk'}).get('onclick')
                    on_split = onclick.split("'")
                    href = 'https://culture.lotteshopping.com/CLSS_view.do?taskID=L&pageNo=1&vpStrCd=%s&vpKisuNo=%s&vpClassCd=%s' % (on_split[1], on_split[3], on_split[5])

                    for i3, td in enumerate(tr.find_all('td')):
                        info = td.text.strip().split()
                        if i3 == 2:
                            title = ' '.join(info)
                        elif i3 == 3:
                            author = ' '.join(info)
                        elif i3 == 4:
                            date = ' '.join(info)
                        elif i3 == 5:
                            price = ' '.join(info)
                    result = '%s<br><strong><a href="%s" target="_blank">%s(%s)</a></strong><br>%s<br>%s<br>' % (
                             result, href, title, author, date, price)
        return result

    def naver_posting(self, bp):
        if bp.naver_token is None:
            bp.logger.error('get_naver_token failed')
            return

        # title = '[%s] 많이 클릭된 연예 뉴스 모음(Naver, Daum, Nate)' % bp.today
        # content = self.entertainment(bp)
        # bp.naver_post(title, content)

        # title = '[%s] 자동차 뉴스 모음(한겨례, 노컷뉴스, Nate)' % bp.today
        # content = self.car_news(bp)
        # bp.naver_post(title, content)

        title = '[%s] 국내 주요언론사 사설, 칼럼 (ㄱ,ㄴ,ㄷ 순)' % bp.today
        content = self.sap.opinion_news(bp)
        bp.naver_post(title, content)

        title = '[%s] 정책뉴스' % bp.today
        content = self.sap.koreagov_news(bp)
        bp.naver_post(title, content)

        title = '[%s] Reddit에 공유된 오늘 내가 배운것(Today I Learned)' % bp.today
        content = self.sap.get_reddit(bp, 'til')
        bp.naver_post(title, content)

        if bp.week_num == 0:  # monday
            title = '[%s] 국내 축제, 행사 일정 (대한민국 구석구석 행복여행)' % bp.today
            content = self.sap.get_visit_korea(bp)  # 대한민국 구석구석 행복여행
            bp.naver_post(title, content, '8')

            self.dap.fixed_deposit(bp, vendor='naver')  # 예금

        elif bp.week_num == 1:
            title = '[%s] 롯데백화점 각 지점별 문화센터 일정' % bp.today
            content = self.dap.lotte_curture_center(bp)
            bp.naver_post(title, content, '8')

            self.dap.savings(bp, vendor='naver')  # 예금

        elif bp.week_num == 2:
            title = '[%s] 현대백화점 각 지점별 문화센터 추천강좌 일정' % bp.today
            content = self.dap.hyundai_curture_center(bp)
            bp.naver_post(title, content, '8')

        elif bp.week_num == 3:
            title = '[%s] Reddit의 세계뉴스' % bp.today
            content = self.sap.get_reddit(bp, 'worldnews')
            bp.naver_post(title, content)

            title = '[%s] 코엑스, 예술의 전당(공연, 전시)' % bp.today
            content = self.domestic_exhibition(bp)
            bp.naver_post(title, content, '8')

        elif bp.week_num == 4:
            content = self.sap.oversea_exhibition(bp)
            title = '[%s] 해외 전시 정보' % bp.today
            bp.naver_post(title, content, '8')
        return
