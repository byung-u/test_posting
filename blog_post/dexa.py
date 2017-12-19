#!/usr/bin/env python3
import json

from bs4 import BeautifulSoup
from blog_post.define import ADSENSE_MIDDLE, BANK_CODE, LOAN_CODE, SAVINGS_BANK_CODE, INSURANCE_CODE, INVESTMENT_CODE


class DailyLifeAndPost:
    def __init__(self):
        pass

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
        result = '%s<br>%s<br>' % (result, ADSENSE_MIDDLE)

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
        result = '%s<br>%s<br>' % (result, ADSENSE_MIDDLE)
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

    def vic_market(self, bp):
        result = '<br>'
        base_url = 'http://company.lottemart.com'
        r = bp.request_and_get('http://company.lottemart.com/vc/info/branch.do?SITELOC=DK013', '빅마켓')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        for i1, vic in enumerate(soup.find_all(bp.match_soup_class(['vicmarket_normal_box']))):
            if i1 != 1:
                continue
            for i2, li in enumerate(vic.find_all('li')):
                if i2 % 5 != 0:
                    continue
                for img in li.find_all('img'):
                    thumbnail = '%s%s' % (base_url, img['src'])
                    break
                button = str(li.button).split("'")
                href = '%s%s' % (base_url, button[1])
                result = '%s<strong><a href="%s" target="_blank">%s<font color="red"></font></a></strong><br>' % (
                         result, href, li.h3.text)
                for ul in li.find_all('ul'):
                    for li2 in ul.find_all('li'):
                        temp = li2.text.strip().replace('\t', '').replace('\r', '')
                        temp_info = temp.split('\n')
                        infos = [t for t in temp_info if len(t) != 0]
                        result = '%s<br>%s: %s' % (result, infos[0], ' '.join(infos[1:]))
                result = '%s<br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center><br><br>' % (result, href, thumbnail)
        return result

    def join_deny(self, num):
        if num == '1':
            return '가입 제한없음'
        elif num == '2':
            return '서민전용 가입'
        elif num == '3':
            return '가입 일부제한'
        else:
            return 'Unknown'

    def dcls_end_day(self, day):  # 공시종료일
        if day is None:
            return '공시 종료일 미정'
        else:
            return '공시 종료일 ' + day

    def max_limit(self, money):  # 공시종료일
        if money is None:
            return '한도정보 없음'
        else:
            m = str(money)
            ret = m.endswith('00000000')
            if ret is True:
                return m[0:-8] + '억원'

            ret = m.endswith('0000000')
            if ret is True:
                return m[0:-7] + '천만원'
            else:
                return m + '원'

    def fixed_deposit(self, bp):
        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'
        for bank, code in BANK_CODE.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth=%s&topFinGrpNo=020000&pageNo=1&financeCd=%s' % (bp.finlife_key, code)
            r = bp.request_and_get(url, '금융감독원_예금금리정보')
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            js = json.loads(str(soup))
            result = '%s<h3>%s</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#  999999" style="border-collapse:collapse">' % (result, bank)
            result = '''%s<tr>
            <th>금융상품,가입방법</th>
            <th>우대조건</th>
            <th>가입대상</th>
            <th>최고한도</th>
            </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s으로 가입<br>➡ %s<br>➡ %s</td>' % (result, banks["fin_prdt_nm"], banks['join_way'], self.join_deny(banks['join_deny']), self.dcls_end_day(banks['dcls_end_day']))
                # result = '%s<td>%s</td>' % (result, banks["join_way"])
                result = '%s<td>%s</td>' % (result, banks["spcl_cnd"].replace('\n', '<br>'))
                # result = '%s<td>%s</td>' % (result, banks['join_member'])
                result = '%s<td>%s</td>' % (result, banks['etc_note'].replace('\n', '<br>'))
                result = '%s<td>%s</td>' % (result, self.max_limit(banks['max_limit']))
                result = '%s</tr>' % result
            result = '%s</table><br><br><br>' % result
        return result

    def get_specipic_mortgage_loan(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        elif group == '보험':
            code_info = INSURANCE_CODE
        elif group == '금융투자':
            code_info = INVESTMENT_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'

        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url, '금융감독원_주택담보대출정보')
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            js = json.loads(str(soup))
            if len(js['result']['baseList']) == 0:
                continue
            option_list_len = (len(js['result']['optionList']))
            result = '%s<h3>%s</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#  999999" style="border-collapse:collapse">' % (result, bank)
            result = '''%s<tr>
             <th>대출상품</th>
             <th>부대비용</th>
             <th>중도상환수수료</th>
             <th>연채 이자율</th>
             <th>금리</th>
             </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s으로 가입<br>➡ %s<br>➡ %s</td>' % (result, banks["fin_prdt_nm"], banks['join_way'], self.dcls_end_day(banks['dcls_end_day']), banks['loan_lmt'])
                result = '%s<td>%s</td>' % (result, banks["loan_inci_expn"].replace('\n', '<br>'))
                result = '%s<td>%s</td>' % (result, banks["erly_rpay_fee"].replace('\n', '<br>'))
                result = '%s<td>%s</td>' % (result, banks["dly_rate"].replace('\n', '<br>'))
                result = '%s<td>' % result
                for i in range(option_list_len):
                    result = '%s<br>[%s]<br> 담보:%s, %s<br><br>➡ 최저: %s<br>➡ 최대: %s<br>➡ 평균: %s<br>' % (
                             result,
                             js['result']['optionList'][i]['lend_rate_type_nm'],
                             js['result']['optionList'][i]['mrtg_type_nm'],
                             js['result']['optionList'][i]['rpay_type_nm'],
                             js['result']['optionList'][i]['lend_rate_min'],
                             js['result']['optionList'][i]['lend_rate_max'],
                             js['result']['optionList'][i]['lend_rate_avg'])
                result = '%s<td></tr>' % result
            result = '%s</table><br><br><br>' % result
        return result

    def mortgage_loan(self, bp):
        grp_code = {'020000': '은행',
                    '030300': '저축은행',
                    '050000': '보험', }
         # 030200(여신전문),  060000(금융투자)
        for gcode, group in grp_code.items():

            title = '[%s] %s 주택담보대출 금리 정보' % (bp.today, group)
            content = self.get_specipic_mortgage_loan(bp, gcode, group)
            if content is None:
                continue
            bp.tistory_post('dexa', title, content, '731649')

    # def rent_subsidy(bp):
    #     return

    def dexa(self, bp):
        title = '[%s] 롯데백화점 각 지점별 문화센터 일정' % bp.today
        content = self.lotte_curture_center(bp)
        bp.tistory_post('dexa', title, content, '730606')
        return

        # self.rent_subsidy(bp)
        # return
        self.mortgage_loan(bp)

        title = '[%s] 정기예금 금리 정보' % bp.today
        content = self.fixed_deposit(bp)
        bp.tistory_post('dexa', title, content, '731649')

        title = '[%s] 빅마켓 지점별 휴관일, 영업시간, 주소, 연락처 정보' % bp.today
        content = self.vic_market(bp)
        bp.tistory_post('dexa', title, content, '730606')

        title = '[%s] 현대백화점 각 지점별 문화센터 추천강좌 일정' % bp.today
        content = self.hyundai_curture_center(bp)
        bp.tistory_post('dexa', title, content, '730606')
