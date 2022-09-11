import random
import sys
import time

import requests

proxy = sys.argv[1]
proxy = 'http://' + proxy

USER_AGENTS = [
    'Windows 10/ Edge browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Windows 7/ Chrome browser: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/47.0.2526.111 Safari/537.36',
    'Mac OS X10/Safari browser: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Linux PC/Firefox browser: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Chrome OS/Chrome browser: Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) WebKit/8611 (KHTML, like Gecko) Mobile/18G82 [FBAN/FBIOS;FBDV/iPhone12,1;FBMD/iPhone;FBSN/iOS;FBSV/14.7.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBIA/FBIOS]',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    'Opera/9.80 (Linux armv7l) Presto/2.12.407 Version/12.51 , D50u-D1-UHD/V1.5.16-UHD (Vizio, D50u-D1, Wireless)',
]

# try:
#     res = requests.get(url='http://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5.0)

#     print(f'Response: {proxy}')
#     print('statusCode:', res.status_code)
#     print('IP:', res.json())
# except:
#     print('Proxy Failed', file=sys.stderr)


# print()
# print('testing amazon....')

# random.seed(time.time())

headers = {
    'cookie': 'ubid-main=132-3328027-0221839; lc-main=en_US; aws-target-data={"support":"1"}; aws-target-visitor-id=1648219294824-603866.35_0; s_fid=37DBDA3AF3DE1AC9-0DDE501E97C94E84; av-timezone=America/Chicago; session-id-apay=140-0176172-3215905; i18n-prefs=USD; sst-main=Sst1|PQEQ0XU-6oP1ti_5rPCZS472CaEj9tHeR56MGq2XzcqiHVuOVCIlLtNes0hqvBEVefT0CqgIbJGLyd1--qe4jDqQfXdb-cLyzLj-ORWPGnLErfjV17-qRzVY3lp2B6RB7VjG72KTUtuvfDUXa50K3FZ8ZQWAwSqDY65hmKK1wU4cKpc0hVX2i10utZFLhh0z7GSzo6FBjfUnqSc-mDut68e_BtxVOXvRApgDtxoMvUE2GPeUuQTPsSQl9odY8h6hXYLbry4J8Af1mdRplKuu3x-fBRRicjN3xnD2D-V7G14oXqc; aws-session-id=960-2143631-4793487; aws-analysis-id=960-2143631-4793487; _mkto_trk=id:112-TZM-766&token:_mch-aws.amazon.com-1656657737778-19041; aws-session-id-time=1658716396l; aws-ubid-main=235-0136171-5775686; regStatus=registered; x-main=BN1sN1fiEdrnpLYOky9rMQZkFguYGr6V; at-main=Atza|IwEBIHb-0YGHldMsAn1A5y5CR2AnbrxXvkohGl2klNZLDXQGKMQ7oTScE0PfKpT12nJmGBfke5MKfVrUVY2ivdL6-v24LAXfh_vwtyFviXTtxrOHiyltqywT6HZGkRIv30GPl5Br8JXhmYsMPlEkZjC7TkrcBH5Bq-u_izxTQDaAa35zbytL0DGfLVPDek71XroSfvZrgRXIT2nnwpbG2e52x98E; sess-at-main="OLcUBn46PiFqM9eSJWv7dQwF9m+cWxG7XZXs7WHKL3k="; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6IjNhYWFiODU3LTRlZjItNGRjNi1iOTEwLTI4Y2IwYmZiNDM3ZSJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiMXc4UXF6Q1FTQUFuWDcrNjM0XC83SzlSVGhVWWFcL2hPeEpZSXlVaW5UVk5zPSIsImFybiI6ImFybjphd3M6aWFtOjo1ODc5OTQ3MTkyMzY6cm9vdCIsInVzZXJuYW1lIjoiTml0c3VhMzY1In0.E1i9DNzRG8Dz5r2F-XbkWJ-tk5zp1A2U_9LlPJd7clpfXH0R1rBgbNm-NSsMNK9jN_WdkAkIom823cRMJSHhxOdyj0N7tABvas5FSywNQAmpxK4_4cVmazZP9tHQ8uam; aws-userInfo={"arn":"arn:aws:iam::587994719236:root","alias":"","username":"Nitsua365","keybase":"1w8QqzCQSAAnX7+634/7K9RThUYa/hOxJYIyUinTVNs\u003d","issuer":"http://signin.aws.amazon.com/signin","signinType":"PUBLIC"}; AMCV_7742037254C95E840A4C98A6@AdobeOrg=1585540135|MCIDTS|19216|MCMID|70658676524204512601950038163077909189|MCAAMLH-1660930833|9|MCAAMB-1660930833|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1660333233s|NONE|MCAID|NONE|vVersion|4.4.0; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiNDg0ZDk0Iiwia2V5IjoiZjhOZTZBeDU5MEY2UkNBamwwL1VMOGhBMVIzQXl5eVZKdEhZV3JNVDM3eFJ2MVJoZmVxZkhoVVdRYTlaamUyQVpWdHBqUDlVUy9VdGpBVmlSc3FyUDNiWE1EMm1WUHVSQ3cxcmd1c1BhZFpsTVpMS1lQajhuL1c1aE1VUkNRNlpqRnFPNG5UVnZOc0RuTEl1d2ROSXcwdGV6SGRISWtaQVYyR000QmxKVmxVWlN4UXVVZDZ6MlpmMGcvY2hPejZhYlRpWldjdU1IZ2RJSWdJS0Y5Rjl6N2lHOHBmcXdXNmVPWUx0UFNQbmw3TXZiUU1lOS9kbVg4MFNmVE9oVnFXWG90cXZaT1ZsNkc1azZhajgzSVpaOVZuQnkrSWpXNGdiU2laZk9oSHJGSTl4aFFaeHg5TU4zUmdlM2xvU1JuWkdMR0RHdmFJVGJjUm9BYVlxaFpvS0N3PT0ifQ==; session-id=139-9300706-1032015; session-id-time=2082787201l; skin=noskin; session-token="idbBIfqzyLtGSJFyCmRZL5tbP3at9VA90f82Zbu41tT/sha9VHLxiF89e+O6szrefiqTbdHIib17gsg8lZVtXLX4V3SUd6/yGvvzUcU+NOz433nXmsXpAMaOO1Dq0DYg8VFK6ccW09t67TmwBYwqevamCyCM24izQARtMMltGd989AJXQ82ZFTVypcDbx8bdZUsyjsdXoiWWLTM+2Ci7izmTfEZ4saU0AzaI5pyE1XNgmb7SnIXjog=="; csm-hit=tb:s-VESE9ADT10MEXBJZNDM5|1662924596109&t:1662924596434&adb:adblk_no',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': random.choice(USER_AGENTS),
    'content-type': 'text/html;charset=UTF-8'
}

res = requests.get(url='https://www.amazon.com/',
                   proxies={'http': proxy, 'https': proxy},
                   headers=headers,
                   timeout=4.0)

print(f'Response: {proxy}')
print('statusCode:', res.status_code)
print('headers', res.headers)

if int(res.status_code) != 200:
    raise Exception("Status not 200")

# print('IP:', res.json())

