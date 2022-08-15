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
    'cookie': 'skin=noskin; ubid-main=135-0638948-2171523; lc-main=en_US; s_fid=610D523867D1C3D2-15C442AF9CFC3A91; s_cc=true; av-timezone=America/Chicago; aws_lang=en; AMCVS_7742037254C95E840A4C98A6@AdobeOrg=1; aws-target-visitor-id=1649187451076-913190; aws-target-data={"support":"1"}; aws-mkto-trk=id:112-TZM-766&token:_mch-aws.amazon.com-1649187451143-26835; session-id=143-9823454-0854113; i18n-prefs=USD; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiYTYxM2M2Iiwia2V5IjoiSEhVaFRhdDYxc2wzSnhtUmJ2M04vM3RDN1dGZVdoTEhRTThUSVQ1MmlnRmwxMmdRakMyTXNYc3gyd0lxTEY5TnkvNDRuaERhM1cya0VLRmZ3eGM4MEVWNHFCeWx3bUdDdnMwT2d2UEIzL0xGQ2hQRzZJYndsZGJ4elQzUGw4TVArbmtXcGFtOFgzM2tjUE94TjdNVHdNV1JvTDdFWmJBUmI2OENGSi9QVjhFV0pBOUc3cDhjVi9yb2o2MFNNTHhrT3h1Y09MSXN0UnRHOFpVajc4eUZwNjBHZUd4T1RCSlA5RWVTOWNUS3NJV0dPSUJ1c0ppNTNPQ2xmT0NTdWExZkJ3Wlk2em1ZNUNFT0JwaE5jckVIQ0E4V1g3YjdXUlNsZzVXQUFDU1NjODZxcUkzMjNyZ0RreW92ek9LWXNaYWxvMDZMd0NDcTVuK1pZejZtMTdXOXFRPT0ifQ==; x-main=aIktuMIszu4OPhus1QMO8x9VO69SVX1C; at-main=Atza|IwEBIA7S_VIcd7uApkcqdIKZMuq1nd3FbeyBtXYNvpkw430UsJd5SxcDt929YjZI8oAiYwld35taaK3IayUc5aUO-VLaHiIpN_MMaunkcg3PO0t0YIxqlHku_iYFyRfVKDnzVRq--fx1uvmpAj-LDfuB-Ps4ye5BU0aTeQamd3gjHWe6hoTCdnMo8OnCkpwcCZUzjjeDWJkb5qQ6EpKtHG16cpMf2chIEq0-AQNLWbgjRm0WZg; sess-at-main="CASMzAQL3H/iwpELTeEJDR5efsn5LXJ2pTnRoW+yW1U="; sst-main=Sst1|PQGCYU0HPcwgkimMQJh6jC7yCYEaecIHAiO7OK5AnI5bjLoltzBAZZ9P5_hnigq84v-sYqnmmIYRYF52Ea_-PE8ksx3mRbv1wtq3vcNZrqTqqKeVINQ8Z5MdPOvvegLBb1FO9ESvpv7HEDUtiDetn3Yi7Nxf89w_ajGHVQWzgUMpECsQcXKVxNIDH3vsd7MijX-yllCxOcuQdJ2r0jZ2ZHv2-Rr-im_CPjFMm8a2LZb4W45tlvzhyHOS6IrWk_R7vPUJEJ--mCp1BVUczXxnlInVKjnjtUCD5JU-3NDXFUqarPE; x-amz-captcha-1=1657496134983661; x-amz-captcha-2=RqBqVZlnM6O+qM9Z7rl1bA==; s_vnum=2080749365397&vn=3; s_nr=1658615801200-Repeat; s_dslv=1658615801201; s_ppv=22; aws-ubid-main=160-6644325-6600727; s_eVar60=ft_card; awsc-color-theme=light; awsc-uh-opt-in=; aws-reg-aid=d99b9f16e7062ab0ccdfa8068e4ff4dd32b2951264c4ec4dfa65e1fd2926a2ee; aws-reg-guid=d99b9f16e7062ab0ccdfa8068e4ff4dd32b2951264c4ec4dfa65e1fd2926a2ee; regStatus=registered; s_sq=[[B]]; _rails-root_session=V1QydlIwNVFOVko2MXJVYkZqQTg3b05xQ0U4eWdzRUZ2MitHa2JBOWdPS3dUSWQxdjZrM1hUNEcrYnhITDRLQ3NVSEpPbGcwV1FKa1QxWnlHdkVWKzROTXlaRldGMC8yT1ZPRUNVUlVuLy9jSUp0dGQzdVo4aGs5Zm9TSnhLS2ZpWjF5L0pLbUVRcUJ4VTVXeUE5SWdjK0RveXFDVDFpcmZwNlFtUHRWcnE0amlSSWVDRkJEWnpEbFdoeXc3TlRlLS1yRFdobmhOQlE0dDhmT0VnNUdnT0hRPT0=--b9c0c210f161d4f692556f05693dc2c08b36cfee; session-id-time=2082787201l; AMCV_7742037254C95E840A4C98A6@AdobeOrg=1585540135|MCIDTS|19219|MCMID|76279335507180357620435907903678868968|MCAID|NONE|MCOPTOUT-1660445985s|NONE|vVersion|4.4.0; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6IjNhYWFiODU3LTRlZjItNGRjNi1iOTEwLTI4Y2IwYmZiNDM3ZSJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiMTlnYXNNbGlJcW55Ums0RzRMMXQ5SXU2T1hiRExWU3ZaWDVpdDA4SkdpMD0iLCJhcm4iOiJhcm46YXdzOmlhbTo6NTg3OTk0NzE5MjM2OnJvb3QiLCJ1c2VybmFtZSI6Ik5pdHN1YTM2NSJ9.I38bjIQuz3ECiSFRKuM7ck3oJJg031xScZwAIK97apZa4W9MywYvpRJkhKDbvzD1kQRVSezQAmcbIrglprmaBPaEm_QjelqMIPjVPBzv8iDWnVgOXwmX9IJW1kK-o64T; aws-userInfo={"arn":"arn:aws:iam::587994719236:root","alias":"","username":"Nitsua365","keybase":"19gasMliIqnyRk4G4L1t9Iu6OXbDLVSvZX5it08JGi0\u003d","issuer":"http://signin.aws.amazon.com/signin","signinType":"PUBLIC"}; noflush_awsccs_sid=cc3d50d4a591d80766a8a75e4187a8cfa15fb4d507f06047720680a6622e4baf; session-token="GHzEztBLw1b7Zq5pUw3aaqBypAgZKwoUj9kLbCGeOWvWE6dA39DCwtyKxaicSBpcTT8HgxTwmxaW/INdXEbqvly+G7CMQMysSp1TEOJCdy3KmCEcb1M1FgqluXRsoyrJD7JLuaxNeKDtssW9jcs9aBQSDgSpy0qfAOKn3Ww9Qt7KDmRZvbBxANOtrzYDGXmtg0wKdbj0M/KREXHm2e/+rA8pic/AAF39iJAUfz972+pphZGBWpQNcg=="; csm-hit=tb:G53707EH1YAMH9C2W9ZB+s-G53707EH1YAMH9C2W9ZB|1660525993385&t:1660525993385&adb:adblk_yes',
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

