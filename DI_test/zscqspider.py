import json
from datetime import datetime
import requests
from lxml import etree
import pymysql


class MysqlConn(object):
    def __init__(self):
        self.MYSQLCONFIG = {
            'host': '192.168.114.128',
            'port': 3306,
            'user': 'root',
            'password': 'admin123',
            'db': 'zhishichanquan',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**self.MYSQLCONFIG)
        self.cursor = self.conn.cursor()
    @property
    def fields(self):
        sql = 'select * from cases_infos'
        self.cursor.execute(sql)
        description = self.cursor.description
        fields = [x[0] for x in description][1::]
        return fields

    def insert_data(self,obj):
        fields = self.fields
        fields_num = len(fields)
        str_fields = ','.join(fields)
        str_fields_num = ','.join(['%s' for i in range(fields_num)])
        insert_sql = 'insert into cases_infos({}) values({})'.format(str_fields,str_fields_num)
        print(insert_sql)
        self.cursor.executemany(insert_sql,(i for i in obj))
        self.conn.commit()




    def __str__(self):
        return self.MYSQLCONFIG['user'] + '写入' + self.MYSQLCONFIG['db'] + '数据库'


class ZldsjSpider(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_data = {
            'username': self.username,
            'password': self.password,
        }

        self.form_data = {
            'select-key:expressCN': '((( % )))',
            'select-key:express': '',
            'select-key:thesaurus': '',
            'select-key:cross': '',
            'select-key:searchType': '',
            'select-key:buttonItem': '',
            'select-key:expressCN2Val': '',
            'select-key:expressCN2': ' ',
            'select-key:_keyWord': '名称',
            'select-key:_keyWordStr': '名称',
            'select-key:languageSelect': '',
            'attribute-node:patent_cache-flag': 'false',
            'attribute-node:patent_page-row': '50',
            'attribute-node:patent_sort-column': '-RELEVANCE',

        }
        self.record_ajax_url = 'http://search.zldsj.com/txnDecisionListRecord.ajax'

    # 登录
    @property
    def login(self):
        session = requests.session()
        login_url = 'http://search.zldsj.com/txn999999.do'
        data = session.post(login_url, data=self.login_data, timeout=None).text
        return session

    def selector(self, form_data):
        html = self.login.post(self.record_ajax_url, data=form_data).content
        selector = etree.HTML(html)
        return selector

    # 返回总的form表单提交数据 生成器 用于分页
    def get_all_form_data(self):
        form_data = self.form_data
        form_data['attribute-node:patent_start-row'] = 1
        form_data['attribute-node:patent_page'] = 1
        selector = self.selector(form_data)
        info = selector.xpath('//attribute-node/patent_record-number/text()')
        record_total_num = int(info[0]) if len(info) > 0 else 0
        pages = divmod(record_total_num, 50)
        # 获取总页数
        pages_num = pages[0] + 1 if pages[1] else pages[0]
        for patent_page in range(1, pages_num + 1):
            start_row = (patent_page - 1) * 50 + 1
            form_data = self.form_data
            form_data['attribute-node:patent_start-row'] = str(start_row)
            form_data['attribute-node:patent_page'] = str(patent_page)
            yield form_data

    # 返回案件数据 字典 生成器对象 case_items = self.make_make_case_items(form_data)
    def make_case_items(self, form_datas):
        for form_data in form_datas:
            selector = self.selector(form_data)
            infos = selector.xpath('//patent')
            page = form_data['attribute-node:patent_page']
            print('{}页 infos有 {} 条数据'.format(page, len(infos)))
            infos = selector.xpath('//patent')
            #后来知道 超过200页没有数据
            if int(page) <= 200:
                for info in infos:
                    # 案件标题 一种纤维乙醇生产废水的预处理方法
                    tio = info.xpath('tio/text()')[0] if info.xpath('tio/text()') else None
                    # 案件id CID0020121016F116918201116T0N9GA5010001
                    cid = info.xpath('cid/text()')[0]
                    # 决定号 116918
                    ridn = info.xpath('ridn/text()')[0]
                    # 决定日 2016/11/28 00:00:00
                    ridd = info.xpath('ridd/text()')[0] if info.xpath('ridd/text()') else None
                    # 请求人 中国石油化工股份有限公司;中国石油化工股份有限公司抚顺石油化工研究院
                    riapo = info.xpath('riapo/text()')[0] if info.xpath('riapo/text()') else None
                    # 法律依据 专利法第二十二条第三款
                    rilb = info.xpath('rilb/text()')[0] if info.xpath('rilb/text()') else None
                    # 申请号 CN201210404192.3
                    ano = info.xpath('ano/text()')[0] if info.xpath('ano/text()') else None
                    # 不知道什么字段CN102012000404192
                    ans = info.xpath('ans/text()')[0] if info.xpath('ans/text()') else None
                    # 申请日 2012/10/23 00:00:00
                    ad = info.xpath('ad/text()')[0] if info.xpath('ad/text()') else None
                    # 复审决定 复审决定
                    ridt = info.xpath('ridt/text()')[0] if info.xpath('ridt/text()') else None
                    # 专利类型 发明
                    pk = info.xpath('pk/text()')[0] if info.xpath('pk/text()') else None
                    # 复审决定结果 撤销原决定
                    ridv = info.xpath('ridv/text()')[0] if info.xpath('ridv/text()') else None
                    case_url = 'http://search.zldsj.com/txnDecisionDetail.do?select-key:ID={}&select-key:RIDN={}'.format(cid, ridn)
                    item = {}
                    item['tio'] = tio
                    item['cid'] = cid
                    item['ridn'] = ridn
                    item['ridd'] = ridd
                    item['riapo'] = riapo
                    item['rilb'] = rilb
                    item['ano'] = ano
                    item['ans'] = ans
                    item['ad'] = ad
                    item['ridt'] = ridt
                    item['pk'] = pk
                    item['ridv'] = ridv
                    item['case_url'] = case_url
                    item['req_url'] = self.record_ajax_url
                    item['page'] = page
                    item['create_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
                    yield item
            else:
                break

    def parse_detail_selector(self, url):
        html = self.login.get(url).content
        parse_detail_selector = etree.HTML(html)
        return parse_detail_selector

    def parse_detail(self, items):
        for item in items:
            case_url = item['case_url']
            selector = self.parse_detail_selector(case_url)

    def make_datas(self):
        form_datas = self.get_all_form_data()
        items = self.make_case_items(form_datas)
        for item in items:
            if item:
                data = []
                for field in fields:
                    data.append(item[field])
                yield data
            else:
                continue
    def run(self):
        obj = self.make_datas()
        db.insert_data(obj)


    def __str__(self):
        return self.username


if __name__ == '__main__':
    db = MysqlConn()
    conn = db.conn
    cursor = db.cursor
    fields = db.fields

    print(fields)

    username = 'wuhandong'
    password = 'wuhandong'
    zldsjspider = ZldsjSpider(username, password)
    print(zldsjspider)
    zldsjspider.run()
