#!/usr/bin/env python3
import praw
import json

from bs4 import BeautifulSoup


class TranslationAndPost:
    def __init__(self):
        pass

    def linux_today(self, bp):
        r = bp.request_and_get('https://www.linuxtoday.com/', 'LinuxToday')
        if r is None:
            return

        result = ''
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > div > div')
        for s in sessions:
            try:
                span = s.span.text
            except AttributeError:
                continue
            if bp.yesterday_only_day != span.split()[1][0:2]:
                continue
            try:
                href = s.a['href']
            except TypeError:
                continue
            r_article = bp.request_and_get(href, 'LinuxToday')
            if r_article is None:
                continue
            soup_article = BeautifulSoup(r_article.text, 'html.parser')
            complete_href = ''
            for article in soup_article.find_all(bp.match_soup_class(['article'])):
                for idx, ps in enumerate(article.find_all('p')):
                    if idx == 0:
                        summary = ps.text
                    elif idx == 1:
                        try:
                            complete_href = ps.a['href']
                        except TypeError:
                            pass
                        break
            ko_title = bp.translate_text(s.a.text)
            ko_article = bp.translate_text(summary)
            if len(complete_href) == 0:
                continue
            temp = '<a href="%s" target="_blank"><font color="blue">%s</font></a><br>%s<br><a href="%s" target="_blank"><font color="red">🔗 전체내용 Link</font></a><br><div style="border:1px solid grey"><br>%s<br><br>"%s"</div><br><br>' % (href, s.a.text, summary, complete_href, ko_title, ko_article)
            result = '%s<br>%s' % (result, temp)
        return result

    def the_guardian(self, bp):
        r = bp.request_and_get('https://www.theguardian.com/business/economics', '가디언기사')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('div > div > div > ul > li > ul > li > div > div > a')
        for s in sessions:
            href = s['href']
            if href.find(bp.str_yesterday) == -1:
                continue
            result = []
            title = s.text
            ko_title = bp.translate_text(title)
            a_r = bp.request_and_get(href, '가디언기사')
            if a_r is None:
                continue
            a_soup = BeautifulSoup(a_r.text, 'html.parser')
            for ca in a_soup.find_all(bp.match_soup_class(['content__article-body'])):
                temp_text = ca.text
                break
            temp = temp_text.split('\n')
            article = [t for t in temp if len(t) > 150]
            result = bp.translate_text_list(article, 'en', 'ko')

            content = '<a href="%s" target="_blank"><font color="red">🔗 원본 Link(%s)</font></a><br><br><br>%s<br>' % (href, href, result)

            post_title = '[%s] %s(%s)' % (bp.today, ko_title, title)
            bp.tistory_post('trab', post_title, content, '766230')

    def nikkei_japan(self, bp):
        url = 'https://www.nikkei.com/access/'
        r = bp.request_and_get(url, '니케이신문')
        if r is None:
            return

        article = []
        base_url = 'https://www.nikkei.com'
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.find_all(bp.match_soup_class(['m-miM32_item'])):
            href = '%s%s' % (base_url, item.a['href'])
            ko_title = bp.translate_text(item.a.text, src='ja', dest='ko')
            title = '[%s] 니케이신문, %s' % (bp.today, ko_title)
            content = '<a href="%s" target="_blank"><font color="blue">%s<br>%s</font></a><br><br>' % (href, ko_title, item.a.text)
            a_r = bp.request_and_get(href, '니케이신문')
            if a_r is None:
                continue
            a_soup = BeautifulSoup(a_r.text, 'html.parser')
            article = []
            for article_text in a_soup.find_all(bp.match_soup_class(['cmn-article_text'])):
                for ps in article_text.find_all('p'):
                    article.append(ps.text)
            result = bp.translate_text_list(article, 'ja', 'ko')
            del article[:]
            if len(result) < 100:  # Too short article
                continue
            content = '%s<br>%s<br>' % (content, result)
            bp.tistory_post('trab', title, content, '766335')
        return

    def mainichi_daily(self, bp):
        url = 'https://mainichi.jp/ranking/daily/'
        r = bp.request_and_get(url, '마이니치신문')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        for i in range(1, 11):  # 1 ~ 10
            class_name = 'rank-%d' % i
            for rank in soup.find_all(bp.match_soup_class([class_name])):
                ko_title = ''
                midashi = rank.find('span', attrs={'class': 'midashi '})
                try:
                    title = midashi.text
                    ko_title = bp.translate_text(title, src='ja', dest='ko')
                except AttributeError:
                    midashi = rank.find('span', attrs={'class': 'midashi icon_plus'})
                    try:
                        title = midashi.text
                        ko_title = bp.translate_text(title, src='ja', dest='ko')
                    except AttributeError:
                        continue
                published = rank.find('p', attrs={'class': 'date'})
                href = rank.a['href']
                content = '<a href="%s" target="_blank"><font color="blue">%s<br>%s</font></a><br><br>%s<br>' % (href, ko_title, midashi.text, published)
                title = '[%s] 마이니치신문, %s' % (bp.today, ko_title)
                a_r = bp.request_and_get(rank.a['href'], '마이니치신문')
                if a_r is None:
                    continue
                a_soup = BeautifulSoup(a_r.text, 'html.parser')
                article = []
                for mt in a_soup.find_all(bp.match_soup_class(['main-text'])):
                    for txt in mt.find_all('p', attrs={'class': 'txt'}):
                        article.append(txt.text.strip())
                result = bp.translate_text_list(article, 'ja', 'ko')
                del article[:]
                if result is None:
                    continue
                elif len(result) < 100:
                    continue
                content = '%s%s<br><br>' % (content, result)
                bp.tistory_post('trab', title, content, '766335')

        return content

    def reddit_popular(self, bp):
        reddit = praw.Reddit(client_id=bp.reddit_cid,
                             client_secret=bp.reddit_csec, password=bp.reddit_pw,
                             user_agent='USERAGENT', username=bp.reddit_id)

        result = ''
        for idx, sub in enumerate(reddit.subreddit('popular').hot(limit=30)):
            ko_title = ''
            try:
                ko_title = bp.translate_text(sub.title)
            except json.decoder.JSONDecodeError:
                pass
            temp = '<a href="%s" target="_blank"><strong>[%d위] %s (score: ⬆ %s)</strong></a><pre>%s</pre><br>' % (
                   sub.url, idx + 1, sub.title, sub.score, ko_title)
            result = '%s<br>%s' % (result, temp)
        return result

    def wired_popular(self, bp):
        url = 'https://www.wired.com/'
        r = bp.request_and_get(url, 'Wired인기뉴스')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('div > div > div > div > div > div > aside > div > div > div > ul > li > a')
        for s in sessions:
            article = []
            post_title = ''
            try:
                href = '%s%s' % (url, s['href'])
                ko_title = bp.translate_text(s.h5.text)
                post_title = '[%s] %s(%s)' % (bp.today, ko_title, s.h5.text.strip())
            except TypeError:
                continue
            a_r = bp.request_and_get(href, 'Wired인기뉴스')
            if a_r is None:
                continue
            a_soup = BeautifulSoup(a_r.text, 'html.parser')
            for body in a_soup.find_all(bp.match_soup_class(['article-body-component'])):
                for body_p in body.find_all('p'):
                    if str(body_p).find('p class=') != -1:
                        continue
                    article.append(body_p.text)
            if len(article) == 0:
                continue
            result = '<a href="%s" target="_blank"><font color="red">🔗  원문: %s</font></a><br>' % (href, href)
            content = bp.translate_text_list(article, 'en', 'ko')
            result = '%s<br>%s' % (result, content)
            bp.tistory_post('trab', post_title, result, '766972')
        return

    def trab(self, bp):
        self.mainichi_daily(bp)
        return
        self.nikkei_japan(bp)
        self.mainichi_daily(bp)
        self.the_guardian(bp)

        title = '[%s] Reddit에서 인기있는 게시글 (1~30위)' % bp.today
        content = self.reddit_popular(bp)
        bp.tistory_post('trab', title, content, '766775')

        title = '[%s] Linux Today 새로운 소식' % bp.today
        content = self.linux_today(bp)
        bp.tistory_post('trab', title, content, '766104')

        if bp.now.day % 7 == 0 or bp.now.day % 7 == 3:
            self.wired_popular(bp)  # twice a week
