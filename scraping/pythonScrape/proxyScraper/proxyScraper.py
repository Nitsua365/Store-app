import pandas as pd
import requests
import subprocess

url = 'https://free-proxy-list.net/'

# request proxy page
print('Getting proxy table...')
res = requests.get(url=url, timeout=4.0)

# read dataframe
df = pd.read_html(res.content)[0]

# filter dataframe 
df = df[(df["Https"].str.contains('yes'))][["IP Address", "Port"]]

# create proxy list and split into increments of 10 sublists
proxy_list = list(zip(list(df["IP Address"]), list(df["Port"])))
proxy_chunks = [proxy_list[i:i+10] for i in range(0, len(proxy_list), 10)]

print('testing proxies...')

# open proxy file
with open('../AmazonScraper/proxies.txt', 'r+') as proxy_file:

    result_proxies = set(map(lambda line: line.strip('\n'), proxy_file.readlines()))

    append_proxies = []

    for sublist in proxy_chunks:
        check_list = list(map(lambda x: subprocess.Popen(['python3', 'proxyTester.py', f'{x[0]}:{x[1]}'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL), sublist))
        
        # wait for all the requests to finish
        for i in check_list:
            i.wait()

        # only add good proxies
        filtered_list = map(lambda proxy: f'http://{proxy.args[2]}', filter(lambda x: x.returncode == 0 and not x.args[2] in result_proxies, check_list))

        append_proxies.extend(list(filtered_list))
        
    append_proxies = set(append_proxies)
    for i in append_proxies:
        print(i)
        proxy_file.write(f'{i}\n')