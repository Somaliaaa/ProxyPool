import json
import re
from .utils import get_page
from pyquery import PyQuery as pq
import time


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies


    def crawl_daili66(self):
        for page in range(1, 5):
            start_url = 'http://www.66ip.cn/{}.html'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_goubanjia(self):
        start_url = 'http://www.goubanjia.com/'
        html = get_page(start_url)

        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                # print(td)
                pattern = re.compile('<.*?\sstyle="display:.*?;">(.*?)</.*?>', re.S)
                items = re.findall(pattern, str(td))
                ip_address = ''.join(items)
                pattern_port = re.compile('.*?<span\sclass="port\s.*?">(.*?)</span>', re.S)

                ip_port = re.findall(pattern_port, str(td))
                address_port = ip_address + ':' + ip_port[0]
                yield address_port

    def crawl_ip3366(self):
        for page in range(1, 11):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_kuaidaili(self):
        for i in range(1, 5):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            time.sleep(1)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')

    def crawl_xicidaili(self):
        for page in range(1, 7):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(page)
            html = get_page(start_url)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')

    def crawl_iphai(self):
        urls = ['http://www.iphai.com/free/ng', 'http://www.iphai.com/']
        for start_url in urls:
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')

    def crawl_89ip(self):
        for page in range(1, 21):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(page)
            html = get_page(start_url)
            if html:
                pattern = re.compile('<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>', re.S)
                items = re.findall(pattern, html)
                for item in items:
                    address = item[0].strip('\n\t')
                    port = item[1].strip('\n\t')
                    yield (address + ':' + port)

    def crawl_data5u(self):
        urls = ['http://www.data6u.com/free/gnpt/index.shtml', 'http://www.data5u.com/free/gnpt/index.shtml',
                'http://www.data5u.com/']
        for start_url in urls:
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
                re_ip_address = ip_address.findall(html)
                for address, port in re_ip_address:
                    result = address + ':' + port
                    yield result.replace(' ', '')