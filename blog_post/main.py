"""blog posting"""
# -*- coding: utf-8 -*-
import cgitb
import json
import logging
import newspaper
import os
import re
import urllib.request

from datetime import datetime, timedelta
from googletrans import Translator
from goose3 import Goose
from newspaper import Article
from random import choice
from requests import get, codes
from selenium import webdriver
from seleniumrequests import Chrome
from time import sleep

from blog_post.scrapnpost import ScrapAndPost
from blog_post.trab import TranslationAndPost
from blog_post.dexa import DailyLifeAndPost
from blog_post.yettu import NaverPost
from blog_post.define import USER_AGENTS

cgitb.enable(format='text')


class BlogPost:
    def __init__(self):
        self.g = Goose()
        self.t = Translator()

        self.now = datetime.now()
        self.now_m1 = datetime.now() - timedelta(days=1)  # now - 1 is yesterday
        self.today = '%4d%02d%02d' % (self.now.year, self.now.month, self.now.day)
        self.yesterday = '%4d%02d%02d' % (self.now_m1.year, self.now_m1.month, self.now_m1.day)
        self.str_yesterday = '%4d/%s/%02d' % (self.now_m1.year, self.now_m1.strftime("%b").lower(), self.now_m1.day)
        self.yesterday_only_day = '%02d' % (self.now_m1.day)
        self.week_num = datetime.today().weekday()

        self.chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
        self.tistory_id = os.environ.get('TISTORY_ID')
        self.tistory_pw = os.environ.get('TISTORY_PAW')
        self.tistory_cid = os.environ.get('TISTORY_CLIENT_ID')
        self.tistory_redirect = os.environ.get('TISTORY_REDIRECT')
        self.tistory_token = self.get_tistory_token()

        self.naver_cid = os.environ.get('NAVER_BLOG_CLIENT_ID')
        self.naver_csec = os.environ.get('NAVER_BLOG_CLIENT_SECRET')
        self.naver_id = os.environ.get('NAVER_ID')
        self.naver_pw = os.environ.get('NAVER_PAW')
        self.naver_redirect = os.environ.get('NAVER_BLOG_REDIRECT')
        self.naver_token = self.get_naver_token()

        self.korea_data_key = os.environ.get('DATA_APT_API_KEY')
        self.finlife_key = os.environ.get('FINLIFE_KEY')
        self.aladin_key = os.environ.get('ALADIN_TTB_KEY')

        self.reddit_cid = os.environ.get('REDDIT_CLIENT_ID')
        self.reddit_csec = os.environ.get('REDDIT_CLIENT_SECRET')
        self.reddit_id = os.environ.get('REDDIT_ID')
        self.reddit_pw = os.environ.get('REDDIT_PAW')

        log_path = '%s/log' % (os.getenv("HOME"))
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        log_file = '%s/blogpost_%s.log' % (log_path, self.today)
        # Write file - DEBUG, INFO, WARN, ERROR, CRITICAL
        # Console display - ERROR, CRITICAL
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('[%(levelname)8s] %(message)s')
        ch.setFormatter(formatter)
        logging.basicConfig(filename=log_file,
                            format='[%(asctime)s] (%(levelname)8s) %(message)s',
                            datefmt='%I:%M:%S',
                            level=logging.INFO)
        self.logger = logging.getLogger('[BP]')
        self.logger.addHandler(ch)

    # Referrence from
    # https://github.com/gleitz/howdoi/blob/master/howdoi/howdoi.py
    # http://docs.python-requests.org/en/master/user/advanced/
    def request_and_get(self, url, name):
        try:
            r = get(url, headers={'User-Agent': choice(USER_AGENTS)})
            if r.status_code != codes.ok:
                self.logger.error('[%s] request error, code=%d', name, r.status_code)
                return None
            return r
        except:
            self.logger.error('[%s] connect fail', name)
            return None

    def get_news_summary(self, url):
        article = Article(url)
        article.download()
        try:
            article.parse()
        except newspaper.article.ArticleException:
            return ' '
        article.nlp()
        return article.summary

    def check_valid_string(self, text):
        text = text.strip()
        text = text.replace("'", "").replace('"', '').replace('·', ',')
        return text

    def get_tistory_token(self):  # http://www.tistory.com/guide/api/index
        driver = webdriver.Chrome(self.chromedriver_path)
        driver.implicitly_wait(3)
        driver.get('https://www.tistory.com/auth/login?redirectUrl=http%3A%2F%2Fwww.tistory.com%2F')
        driver.find_element_by_name('loginId').send_keys(self.tistory_id)
        driver.find_element_by_name('password').send_keys(self.tistory_pw)
        driver.find_element_by_xpath('//*[@id="authForm"]/fieldset/div/button').click()

        req_url = 'https://www.tistory.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=token' % (self.tistory_cid, self.tistory_redirect)
        driver.get(req_url)

        ################################################################################
        # XXX: 티스토리 브라우져 인증이 필요하도록 설정해둔 경우
        # 맨처음 시도할 때는 아래의 코드의 주석을 풀고 한번 해줘야함
        #
        # driver.find_element_by_xpath('//*[@id="contents"]/div[4]/button[1]').click()
        #
        ################################################################################
        redirect_url = driver.current_url
        print(redirect_url)
        temp = re.split('access_token=', redirect_url)
        token = re.split('&state=', temp[1])[0]
        driver.quit()
        return token

    def tistory_post(self, blog_name, title, content, category):
        webdriver = Chrome()
        response = webdriver.request('POST', 'https://www.tistory.com/apis/post/write', data={"access_token": self.tistory_token, "blogName": blog_name, 'title': title, 'content': content, 'category': category, 'visibility': '2'})
        webdriver.quit()
        print(response)

    def get_naver_token(self):
        driver = webdriver.Chrome(self.chromedriver_path)  # driver = webdriver.PhantomJS()
        driver.implicitly_wait(3)
        driver.get('https://nid.naver.com/nidlogin.login')
        driver.find_element_by_name('id').send_keys(self.naver_id)
        driver.find_element_by_name('pw').send_keys(self.naver_pw)
        driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

        state = "REWERWERTATE"
        req_url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=%s&redirect_uri=%s&state=%s' % (self.naver_cid, self.naver_redirect, state)

        driver.get(req_url)
        ##########################
        # XXX: 최초 1회 수행해서 동의 해야함
        # driver.find_element_by_xpath('//*[@id="confirm_terms"]/a[2]').click()
        ##########################
        redirect_url = driver.current_url
        temp = re.split('code=', redirect_url)
        code = re.split('&state=', temp[1])[0]
        driver.quit()
        print(redirect_url)

        url = 'https://nid.naver.com/oauth2.0/token?'
        data = 'grant_type=authorization_code' + '&client_id=' + self.naver_cid + '&client_secret=' + self.naver_csec + '&redirect_uri=' + self.naver_redirect + '&code=' + code + '&state=' + state

        request = urllib.request.Request(url, data=data.encode("utf-8"))
        request.add_header('X-Naver-Client-Id', self.naver_cid)
        request.add_header('X-Naver-Client-Secret', self.naver_redirect)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        token = ''
        if rescode == 200:
            response_body = response.read()
            js = json.loads(response_body.decode('utf-8'))
            token = js['access_token']
        else:
            self.logger.error("Error Code:" + rescode)
            return None

        if len(token) == 0:
            return None
        print(token)
        return token

    def naver_post(self, title, content, category='1'):
        header = "Bearer " + self.naver_token  # Bearer 다음에 공백 추가
        url = "https://openapi.naver.com/blog/writePost.json"
        title = urllib.parse.quote(title)
        contents = urllib.parse.quote(content)
        data = "title=" + title + "&contents=" + contents + '&categoryNo=' + category
        request = urllib.request.Request(url, data=data.encode("utf-8"))
        request.add_header("Authorization", header)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            self.logger.info(response_body.decode('utf-8'))
        else:
            self.logger.error("Error Code:" + rescode)

    def naver_papago_nmt(self, words):
        enc_text = urllib.parse.quote(words)
        data = 'source=en&target=ko&text=' + enc_text
        url = 'https://openapi.naver.com/v1/papago/n2mt'
        request = urllib.request.Request(url)
        request.add_header('X-Naver-Client-Id', self.naver_cid)
        request.add_header('X-Naver-Client-Secret', self.naver_csec)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            translated = json.loads(response_body.decode('utf-8'))
            return (translated['message']['result']['translatedText'])
        else:
            self.logger.error('Error Code:' + rescode)
            return ' '

    def naver_papago_smt(self, words):
        enc_text = urllib.parse.quote(words)
        data = 'source=en&target=ko&text=' + enc_text
        url = "https://openapi.naver.com/v1/language/translate"
        request = urllib.request.Request(url)
        request.add_header('X-Naver-Client-Id', self.naver_cid)
        request.add_header('X-Naver-Client-Secret', self.naver_csec)
        try:
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        except urllib.error.HTTPError as e:
            self.logger.error('urlopen failed', str(e))
            return ' '
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            translated = json.loads(response_body.decode('utf-8'))
            return (translated['message']['result']['translatedText'])
        else:
            self.logger.error('Error Code:' + rescode)
            return ' '

    def translate_text(self, text, src='en', dest='ko'):
        if src is not 'ja':
            ja_text = self.t.translate(text, src=src, dest='ja').text
            ko_text = self.t.translate(ja_text, src='ja', dest=dest).text
        else:
            ko_text = self.t.translate(text, src=src, dest=dest).text
        return ko_text

    def translate_text_list(self, article, src='en', dest='ko'):
        result = []
        for line in article:
            if len(line) == 0:
                result.append('<br>')
                continue
            sleep(0.5)  # 500 msec
            try:
                if src is not 'ja':
                    ja_text = self.t.translate(line, src=src, dest='ja').text
                    ko_text = self.t.translate(ja_text, src='ja', dest=dest).text
                else:
                    ko_text = self.t.translate(line, src=src, dest=dest).text
            except:
                print('[Translate Error]', line)
                return None
            result.append(ko_text)

        return '<br>'.join(result)

    def match_soup_class(self, target, mode='class'):
        def do_match(tag):
            classes = tag.get(mode, [])
            return all(c in classes for c in target)
        return do_match


def do_run(bp):
    sap = ScrapAndPost()
    sap.scrapnpost(bp)
    sleep(5)  # 5 sec

    np = NaverPost()
    np.naver_posting(bp)
    # sleep(5)  # Naver no sleep

    dap = DailyLifeAndPost()
    dap.dexa(bp)
    sleep(5)  # 5 sec

    tap = TranslationAndPost()
    tap.trab(bp)
    return


def main():
    bp = BlogPost()
    do_run(bp)


if __name__ == '__main__':
    main()
