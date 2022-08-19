# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import time

from scrapy import signals
from scrapy.http import Request
import base64
from urllib.parse import unquote, urlunparse
# from urllib.request import getproxies, proxy_bypass, _parse_proxy

from scrapy.exceptions import NotConfigured
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.python import to_bytes
# from scrapy.conf import settings
# from scrapy import log
import random

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class AmazonscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            print(r.headers)
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AmazonscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # newReq = Request(url=request.url)
        # newReq.meta['proxy'] = 'http://10.112.219.43:1832'
        # return newReq
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class ProxiesMiddleware:
    def __init__(self, settings):
        file = open('proxies.txt', 'r')
        self.proxies = list(map(lambda x: x.strip('\n'), file.readlines()))
        random.seed(time.time())
        self.proxy = random.choice(self.proxies)
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy
        pass

class ShowHeadersMiddleware:
    def process_request(self, request, spider):
        print(f'Request Headers: {request.headers}\n')

    def process_response(self, request, response, spider):
        print(f'Response Headers: {response.headers}\n')
        return response

# class HttpProxyMiddleware:
#
#     def __init__(self, auth_encoding='latin-1'):
#         self.auth_encoding = auth_encoding
#         self.proxies = {}
#         for type_, url in getproxies().items():
#             try:
#                 self.proxies[type_] = self._get_proxy(url, type_)
#             # some values such as '/var/run/docker.sock' can't be parsed
#             # by _parse_proxy and as such should be skipped
#             except ValueError:
#                 continue
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
#             raise NotConfigured
#         auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING')
#         return cls(auth_encoding)
#
#     def _basic_auth_header(self, username, password):
#         user_pass = to_bytes(
#             f'{unquote(username)}:{unquote(password)}',
#             encoding=self.auth_encoding)
#         return base64.b64encode(user_pass)
#
#     def _get_proxy(self, url, orig_type):
#         proxy_type, user, password, hostport = _parse_proxy(url)
#         proxy_url = urlunparse((proxy_type or orig_type, hostport, '', '', '', ''))
#
#         if user:
#             creds = self._basic_auth_header(user, password)
#         else:
#             creds = None
#
#         return creds, proxy_url
#
#     def process_request(self, request, spider):
#         creds, proxy_url = None, None
#         if 'proxy' in request.meta:
#             if request.meta['proxy'] is not None:
#                 creds, proxy_url = self._get_proxy(request.meta['proxy'], '')
#         elif self.proxies:
#             parsed = urlparse_cached(request)
#             scheme = parsed.scheme
#             if (
#                 (
#                     # 'no_proxy' is only supported by http schemes
#                     scheme not in ('http', 'https')
#                     or not proxy_bypass(parsed.hostname)
#                 )
#                 and scheme in self.proxies
#             ):
#                 creds, proxy_url = self.proxies[scheme]
#
#         self._set_proxy_and_creds(request, proxy_url, creds)
#
#     def _set_proxy_and_creds(self, request, proxy_url, creds):
#         if proxy_url:
#             request.meta['proxy'] = proxy_url
#         elif request.meta.get('proxy') is not None:
#             request.meta['proxy'] = None
#         if creds:
#             request.headers[b'Proxy-Authorization'] = b'Basic ' + creds
#             request.meta['_auth_proxy'] = proxy_url
#         elif '_auth_proxy' in request.meta:
#             if proxy_url != request.meta['_auth_proxy']:
#                 if b'Proxy-Authorization' in request.headers:
#                     del request.headers[b'Proxy-Authorization']
#                 del request.meta['_auth_proxy']
#         elif b'Proxy-Authorization' in request.headers:
#             del request.headers[b'Proxy-Authorization']