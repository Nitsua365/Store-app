import random
import sys
import time

import requests

proxy = input("Enter Proxy (<host>:<port>): ")
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

try:
    res = requests.get(url='http://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5.0)

    print(f'Response: {proxy}')
    print('statusCode:', res.status_code)
    print('IP:', res.json())
except:
    print('Proxy Failed', file=sys.stderr)


print()
print('testing amazon....')

random.seed(time.time())

headers = {
    'cookie': 'session-id=144-5395395-3083840; ubid-main=134-4057652-2778664; aws_lang=en; AMCVS_7742037254C95E840A4C98A6@AdobeOrg=1; s_cc=true; aws-target-visitor-id=1660844286774-45180; aws-target-data={"support":"1"}; aws-mkto-trk=id:112-TZM-766&token:_mch-aws.amazon.com-1660844286778-15119; aws-ubid-main=920-2161231-5414858; regStatus=registered; awsc-color-theme=light; awsc-uh-opt-in=; skin=noskin; lc-main=en_US; i18n-prefs=USD; s_fid=6CA203E70F799E1F-0D5818B404ED82E9; x-main="by0kEEoqptES14NYkiiC@Zyz27Y?r9jF"; at-main=Atza|IwEBIKFgOIor90cDlIOehNyRunU8tPyHJPAqxi5KC1UGrLwuhwHm45Swx_5OBl2D_LVteIGbm_KrdAHMdBiimdvx6Mlu1fkXy0gfJ1LLEbFK4wlGCaVg6WiNxs-syr3Q8bj1rVqqrvOVUsT39wFst_R2bKgDv47tewRZnN2WAbtxALfhgko0l1hZ3zq_X-cF5XFGjWjWW5TmSN0jMSRVVqgeFV0cEebUy1yZs-60sdthKNPD_cpe_N6AMNtKHpHT9qlObn3nzD-PCqVhRqfgj6u1jNfS_cuA0OCgDzYAo5VogNG-lg; sess-at-main="N85sbZQqMA7y8AojMHd7d8f7hKFZn0arGnP6j8pvL1g="; sst-main=Sst1|PQFfOKcLnM3mK8FCiQDWpyEcCR0KBWgPGcwgtTyWejh-Re4uVfPhSeVZ_1Co51Rd5fJq4BTItZBaGn-v0R7n9ei6B091yAt2NkfHrfIWp2p2FEvwuH6j89V9T16nJ6HjNugkt5dZ89KdnjF5kB4P60u7GQoiNU2t2U4FaR4vXqCV9e5hJZdK6GX9BdFfILrwWG1Flm59q0l6OppMctlmlzZd8xOkG9Bk4CZ3oS-VDmRb8w_0nnCeMh93u7lBKGrJrA-rwHtLZQRdAO9oPrrSnpF9ZSi5VeJoudPlcGmMVAAwOHg; _rails-root_session=eXhWbjVab21CQkdCSlBBNDFuZ0prZUY4K3JuRTErZ3l3ejllYjJ2UjQ3UTlqWXlFc1ZQT1ZlRjJKampBTm1PM0hzcVBKZ0ZTTS96bUZzdHNWTHVOb3l5WHdRUStOdURNcEZ0eEFnL2kxbjZLWE45WExYTG1OQ1dqd3BWQVhaVGJnNFhJeXBPajcyOG1NaG93Z1lqRXozZE9aaythYXBmNXRTREFkK09CNGIvVWpqb2FZUGt2SGJkVmpINzF3S3BRLS1NeTEzejE0ZHA0OC9GK2xUZVJLd1NRPT0=--e8763cbf91c9c628e3f466b9647d8946e68e496f; s_sq=[[B]]; session-id-time=2082787201l; av-timezone=America/Chicago; AMCV_7742037254C95E840A4C98A6@AdobeOrg=1585540135|MCIDTS|19232|MCMID|86127435547658711443813455016714315852|MCAID|NONE|MCOPTOUT-1661637902s|NONE|vVersion|4.4.0; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6IjNhYWFiODU3LTRlZjItNGRjNi1iOTEwLTI4Y2IwYmZiNDM3ZSJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiSDF3NFhNbU1MZWhvdGRPaGhTXC9Fa0ROVEFvbDJlajc2WVluVVNBQ1R0Wk09IiwiYXJuIjoiYXJuOmF3czppYW06OjU4Nzk5NDcxOTIzNjpyb290IiwidXNlcm5hbWUiOiJOaXRzdWEzNjUifQ.Q6ydyTmVpEHvF115hVlIFb48UMbZWK3GgG1eJKFVJcN1QprJQV0PYHaZXkjHfImbVBBOcynHR7EwJ6vFrIzar_0i2JQoaJmxjCdjLN_sJo9AAE3WzmqJvhY3GJYjAUKp; aws-userInfo={"arn":"arn:aws:iam::587994719236:root","alias":"","username":"Nitsua365","keybase":"H1w4XMmMLehotdOhhS/EkDNTAol2ej76YYnUSACTtZM\u003d","issuer":"http://signin.aws.amazon.com/signin","signinType":"PUBLIC"}; noflush_awsccs_sid=3fabcfce92f63bf51af9cd96456bacc2b2766a99e3187e051f2d41a5b5051dee; aws-signer-token_us-east-1=eyJrZXlWZXJzaW9uIjoiV0tGbGVWdWVLUXBIbnJIcERTRHZNU0VzaVVEcnlDWUgiLCJ2YWx1ZSI6Ik1hcXJmTXJDMHJaV3dXZ2ppOC85U1JKeWlVd3k3eUJ2RGs4VUpLNDg1a009IiwidmVyc2lvbiI6MX0=; session-token="GItaBitd/IqdkhDgVkfjXDPjZVt8A4yR+4iCorqkq4pqN6xUjAS0eFXW0EKXgyhVeoC9IGTi/jSLV44GgySIQwizj47p3UuDDfiTAtUekKB4aRcacKrwHezAwQJORR3bJjDaKqhNaEH2GI145bEWerporjc+oinOhqxvRiK87JaAHZcXirG8s5+VA7DaBcygQHJoP7b0dc85XokPW/P1lgOy1KYj1jDwPRlCdWkFUR/T+dAQIDOnzw=="; csm-hit=tb:s-GCSRYXE3RZ1YF9H7TYR0|1661640946423&t:1661640946903&adb:adblk_yes',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': random.choice(USER_AGENTS),
    'content-type': 'text/html;charset=UTF-8'
}

res = requests.get(url='https://www.amazon.com/',
                   proxies={'http': proxy, 'https': proxy},
                   headers=headers,
                   timeout=5.0)

print(f'Response: {proxy}')
print('statusCode:', res.status_code)
print('headers', res.headers)
# print('IP:', res.json())

