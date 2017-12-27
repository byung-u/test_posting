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
                    result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong><br>%s<br>[%s]<br>' % (
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
                    result = '%s<br><strong><a href="%s" target="_blank">%s(%s)</a></strong><br>%s<br>[%s]<br>' % (
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

            ret = m.endswith('000000')
            if ret is True:
                return m[0:-6] + '백만원'

            ret = m.endswith('00000')
            if ret is True:
                return m[0:-5] + '십만원'
            else:
                return m + '원'

    def get_fixed_deposit(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'
        cnt = 0
        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url, '금융감독원_예금금리정보')
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            js = json.loads(str(soup))
            if len(js['result']['baseList']) == 0:
                continue
            result = '%s<h3>%s</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#  999999" style="border-collapse:collapse">' % (result, bank)
            result = '''%s<tr>
            <th>금융상품,가입방법</th>
            <th>우대조건</th>
            <th>가입대상</th>
            <th>최고한도</th>
            </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s 가입<br>➡ %s<br>➡ %s</td>' % (result, banks["fin_prdt_nm"], banks['join_way'], self.join_deny(banks['join_deny']), self.dcls_end_day(banks['dcls_end_day']))
                # result = '%s<td>%s</td>' % (result, banks["join_way"])
                result = '%s<td>%s</td>' % (result, banks["spcl_cnd"].replace('\n', '<br>'))
                # result = '%s<td>%s</td>' % (result, banks['join_member'])
                result = '%s<td>%s</td>' % (result, banks['etc_note'].replace('\n', '<br>'))
                result = '%s<td>%s</td>' % (result, self.max_limit(banks['max_limit']))
                result = '%s</tr>' % result
            result = '%s</table><br><br><br>' % result
            cnt += 1
            if cnt % 10 == 0:
                result = '%s<br>%s<br><br><br>' % (result, ADSENSE_MIDDLE)
        return result

    def get_specipic_mortgage_loan(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        elif group == '보험사':
            code_info = INSURANCE_CODE
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

    def get_specipic_private_loan(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '여신전문':
            code_info = LOAN_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        elif group == '보험사':
            code_info = INSURANCE_CODE
        elif group == '금융투자사':
            code_info = INVESTMENT_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'
        cnt = 0
        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/creditLoanProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url, '금융감독원_개인신용대출정보')
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
             <th>금리</th>
             </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s으로 가입<br>➡ %s<br></td>' % (
                         result,
                         banks["crdt_prdt_type_nm"],
                         banks['join_way'],
                         self.dcls_end_day(banks['dcls_end_day']))
                fin_prdt_cd = banks['fin_prdt_cd']
                result = '%s<td>' % result
                for i in range(option_list_len):
                    if fin_prdt_cd == js['result']['optionList'][i]['fin_prdt_cd']:

                        result = '%s<br>[%s]<br>- 은행:1~2등급,비은행:1~3등급 ➡ %s<br>- 은행:3~4등급,비은행:4등급➡ %s<br>- 은행:5~6등급,비은행:5등급➡ %s<br>- 은행:7~8등급,비은행:6등급➡ %s<br>- 은행:9~10등급,비은행:7~10등급➡ %s<br>' % (
                                 result,
                                 js['result']['optionList'][i]['crdt_lend_rate_type_nm'],
                                 js['result']['optionList'][i]['crdt_grad_1'],
                                 js['result']['optionList'][i]['crdt_grad_4'],
                                 js['result']['optionList'][i]['crdt_grad_5'],
                                 js['result']['optionList'][i]['crdt_grad_6'],
                                 js['result']['optionList'][i]['crdt_grad_10'])
                result = '%s</td></tr>' % result
            result = '%s</table><br><br><br>' % result
            cnt += 1
            if cnt % 10 == 0:
                result = '%s<br>%s<br><br><br>' % (result, ADSENSE_MIDDLE)
        return result

    def get_specipic_rent_subsidy(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '여신전문':
            code_info = LOAN_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        elif group == '보험사':
            code_info = INSURANCE_CODE
        elif group == '금융투자사':
            code_info = INVESTMENT_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'
        cnt = 0
        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url, '금융감독원_전세자금대출정보')
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
             <th>대출부대비용</th>
             <th>그외 수수료</th>
             <th>금리</th>
             </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s으로 가입<br>➡ 제한: <strong>%s</strong><br>➡ %s<br></td>' % (
                         result,
                         banks["fin_prdt_nm"],
                         banks['join_way'],
                         banks['loan_lmt'],
                         self.dcls_end_day(banks['dcls_end_day']))
                result = '%s<td>%s</td>' % (result, banks["loan_inci_expn"].replace('\n', '<br>'))
                result = '%s<td>[중도상환수수료]<br>%s<br><br>[연체 이자율]%s<br></td>' % (
                         result,
                         banks["loan_inci_expn"].replace('\n', '<br>'),
                         banks["erly_rpay_fee"].replace('\n', '<br>'))
                fin_prdt_cd = banks['fin_prdt_cd']
                result = '%s<td>' % result
                for i in range(option_list_len):
                    if fin_prdt_cd == js['result']['optionList'][i]['fin_prdt_cd']:
                        result = '%s<br>[%s]<br>%s<br><br>최저: %s<br>최고: %s<br> ' % (
                                 result,
                                 js['result']['optionList'][i]['rpay_type_nm'],
                                 js['result']['optionList'][i]['lend_rate_type_nm'],
                                 js['result']['optionList'][i]['lend_rate_min'],
                                 js['result']['optionList'][i]['lend_rate_max'])
                result = '%s</td></tr>' % result
            result = '%s</table><br><br><br>' % result
            cnt += 1
            if cnt % 10 == 0:
                result = '%s<br>%s<br><br><br>' % (result, ADSENSE_MIDDLE)
        return result

    def mortgage_loan(self, bp):
        grp_code = {'020000': '은행',
                    '030300': '저축은행',
                    '050000': '보험사', }
        # 030200(여신전문),  060000(금융투자)
        for gcode, group in grp_code.items():

            title = '[%s] %s 주택담보대출 금리 정보' % (bp.today, group)
            content = self.get_specipic_mortgage_loan(bp, gcode, group)
            if content is None:
                continue
            bp.tistory_post('dexa', title, content, '731649')

    def private_loan(self, bp):
        grp_code = {'020000': '은행',
                    '030200': '여신전문',
                    '030300': '저축은행',
                    '050000': '보험사', }
        for gcode, group in grp_code.items():

            title = '[%s] %s 개인신용대출 금리 정보' % (bp.today, group)
            content = self.get_specipic_private_loan(bp, gcode, group)
            if content is None:
                continue
            bp.tistory_post('dexa', title, content, '731649')

    def rent_subsidy(self, bp):
        grp_code = {'020000': '은행',
                    '030300': '저축은행',
                    '050000': '보험사', }

        for gcode, group in grp_code.items():

            title = '[%s] %s 전세자금대출 금리 정보' % (bp.today, group)
            content = self.get_specipic_rent_subsidy(bp, gcode, group)
            if content is None:
                continue
            bp.tistory_post('dexa', title, content, '731649')

    def get_specipic_savings(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '여신전문':
            code_info = LOAN_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        elif group == '보험사':
            code_info = INSURANCE_CODE
        elif group == '금융투자사':
            code_info = INVESTMENT_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'
        cnt = 0
        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url, '금융감독원_적금금리정보')
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            js = json.loads(str(soup))
            if len(js['result']['baseList']) == 0:
                continue
            option_list_len = (len(js['result']['optionList']))
            result = '%s<h3>%s</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#999999" style="  border-collapse:collapse">' % (result, bank)
            result = '''%s<tr>
                       <th width="150">적금상품</th>
                       <th>우대조건</th>
                       <th width="120">이자</th>
                       </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s으로 가입<br>➡ %s<br>➡ %s<br>➡ %s<br><br>➡ <strong>한도: 월 %s</strong></td>' % (
                         result,
                         banks["fin_prdt_nm"],
                         banks['join_way'],
                         banks['join_member'],
                         self.join_deny(banks['join_deny']),
                         self.dcls_end_day(banks['dcls_end_day']),
                         self.max_limit(banks['max_limit']))

                result = '%s<td>%s</td>' % (result, banks["spcl_cnd"].replace('\n', '<br>'))

                fin_prdt_cd = banks['fin_prdt_cd']
                result = '%s<td>' % result
                for i in range(option_list_len):
                    if fin_prdt_cd == js['result']['optionList'][i]['fin_prdt_cd']:
                        result = '%s<br><strong>[%s, %s]</strong><br>납입기간: %s개월<br><font color="red">저축금리: %s</font><br>최고우대금리: %s<br>' % (
                                 result,
                                 js['result']['optionList'][i]['intr_rate_type_nm'],
                                 js['result']['optionList'][i]['rsrv_type_nm'],
                                 js['result']['optionList'][i]['save_trm'],
                                 js['result']['optionList'][i]['intr_rate'],
                                 js['result']['optionList'][i]['intr_rate2'])
                result = '%s</td>' % result

            result = '%s</table><br><br><br>' % result
            cnt += 1
            if cnt % 10 == 0:
                result = '%s<br>%s<br><br><br>' % (result, ADSENSE_MIDDLE)
        return result

    def savings(self, bp):
        grp_code = {'020000': '은행',
                    '030300': '저축은행', }
        for gcode, group in grp_code.items():

            title = '[%s] %s 적금 금리 정보' % (bp.today, group)
            content = self.get_specipic_savings(bp, gcode, group)
            if content is None:
                continue
            bp.tistory_post('dexa', title, content, '731649')

    def fixed_deposit(self, bp):

        grp_code = {'020000': '은행',
                    '030300': '저축은행', }
        for gcode, group in grp_code.items():

            title = '[%s] %s 예금 금리 정보' % (bp.today, group)
            content = self.get_fixed_deposit(bp, gcode, group)
            if content is None:
                continue
            bp.tistory_post('dexa', title, content, '731649')

    def dividend_income(self, bp, rankTpcd, stkTpcd='1'):  # 주식 배당 관련 조회
        stkTpcd = '1'  # [1]보통주, [2]우선주
        listTpcd = { '11': '유가증권시장', '12': '코스닥시장',
                     '13': 'K-OTC',  '14': '코넥스시장', '50': '기타비상장', }
        result = ''
        for tcode, tname in listTpcd.items():
            if rankTpcd == '1':  # [1]시가배당율, [2]액면가배당율
                result = '%s<br><br><br><h3>%s 보통주 (시가배당율 순위)</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#999999" style="  border-collapse:collapse">' % (result, tname)
                result = '''%s<tr>
                 <th>배당순위</th>
                 <th>주식코드</th>
                 <th>주식회사</th>
                 <th>주당배당금</th>
                 <th><font color="red">시가배당율</font></th>
                 <th>액면가배당율</th>
                 </tr>''' % (result)
            else:
                result = '%s<br><br><br><h3>%s 보통주 (액면가배당율 순위)</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#999999" style="  border-collapse:collapse">' % (result, tname)
                result = '''%s<tr>
                 <th>배당순위</th>
                 <th>주식코드</th>
                 <th>주식회사</th>
                 <th>주당배당금</th>
                 <th>시가배당율</th>
                 <th><font color="red">액면가배당율</font></th>
                 </tr>''' % (result)
            for i in range(1, 3):
                url = 'http://api.seibro.or.kr/openapi/service/StockSvc/getDividendRankN1?year=2017&rankTpcd=' + rankTpcd + '&stkTpcd=' + stkTpcd + '&listTpcd=' + tcode + '&pageNo=' + str(i) + '&ServiceKey=' + bp.korea_data_key
                r = bp.request_and_get(url, '배당관련조회')
                soup = BeautifulSoup(r.text, 'lxml')
                for item in soup.items.find_all('item'):
                    result = '%s<tr>' % result
                    # print(item.caltotmarttpcd.text)
                    result = '%s<td align="center">%s</td>' % (result, item.num.text)
                    result = '%s<td align="center">%s</td>' % (result, item.shotnisin.text)
                    result = '%s<td align="center">%s</td>' % (result, item.korsecnnm.text)
                    result = '%s<td align="right">%s</td>' % (result, item.divamtperstk.text)
                    result = '%s<td align="right">%s</td>' % (result, item.divratecpri.text)
                    result = '%s<td align="right">%s</td>' % (result, item.divratepval.text)
                    result = '%s</tr>' % result
            result = '%s</table>' % result
            result = '%s<br>%s<br>' % (result, ADSENSE_MIDDLE)

        return result

    def dexa(self, bp):
        if bp.week_num == 0:  # monday

            title = '[%s] 롯데백화점 각 지점별 문화센터 일정' % bp.today
            content = self.lotte_curture_center(bp)
            bp.tistory_post('dexa', title, content, '730606')
            # self.rent_subsidy(bp)  # 전세자금대출

            # title = '[%s] 보통주 시가배당율 순위' % bp.today
            # content = self.dividend_income(bp, '1')
            # bp.tistory_post('dexa', title, content, '731649')

        elif bp.week_num == 1:

            title = '[%s] 현대백화점 각 지점별 문화센터 추천강좌 일정' % bp.today
            content = self.hyundai_curture_center(bp)
            bp.tistory_post('dexa', title, content, '730606')
            # self.private_loan(bp)  # 신용대출

            # title = '[%s] 보통주 액면가배당율 순위' % bp.today
            # content = self.dividend_income(bp, '2')
            # bp.tistory_post('dexa', title, content, '731649')

        elif bp.week_num == 2:

            self.fixed_deposit(bp)  # 예금

            # self.mortgage_loan(bp)  # 주택담보대출

            # title = '[%s] 우선주 시가배당율 순위' % bp.today
            # content = self.dividend_income(bp, '1', '2')
            # bp.tistory_post('dexa', title, content, '731649')

        elif bp.week_num == 3:

            self.savings(bp)  # 적금

            # title = '[%s] 우선주 액면가배당율 순위' % bp.today
            # content = self.dividend_income(bp, '2', '2')
            # bp.tistory_post('dexa', title, content, '731649')
        # elif bp.week_num == 4:
            # title = '[%s] 빅마켓 지점별 휴관일, 영업시간, 주소, 연락처 정보' % bp.today
            # content = self.vic_market(bp)
            # bp.tistory_post('dexa', title, content, '730606')
