# coding: utf-8
from urllib.parse import quote
import os,requests,json,sys,getpass 

access_token = ''
ip_list = []

#输入用户名密码连接
def login():
    user = input('[-] input : username :')
    passwd = getpass.getpass('[-] input : password :')
    data = {
        'username' : user,
        'password' : passwd
    }               
    data_encoded = json.dumps(data)  # dumps 将 python 对象转换成 json 字符串
    try:
        r = requests.post('https://api.zoomeye.org/user/login',data = data_encoded)
        r_decoded = r.json() # loads() 将 json 字符串转换成 python 对象        
        access_token = r_decoded['access_token']
    except Exception as e:
        print('[-] info : username or password is wrong, please try again ')
        exit()



 
def saveListToFile(file,list):
    """
    将列表逐行写入文件中
    """
    s = '\n'.join(list)
    with open(file,'w') as f:
        f.write(s)
 
def apiTest(restart,page):
    """
    进行 api 使用测试
    """
    headers = {
        'Authorization' : 'JWT ' + access_token
    }
    for page in range(1,page + 1):
        try:         
            r = requests.get(f'https://api.zoomeye.org/host/search?query="{restart}"&facet=app,os&page=' + str(page),headers = headers)
            r_decoded = r.json()
            for x in r_decoded['matches']:
                print(x['ip']+":"+str(x['portinfo']['port']))
                ip_list.append(x['ip']+":"+str(x['portinfo']['port'])) 
        except Exception as e:
            # 若搜索请求超过 API 允许的最大条目限制 或者 全部搜索结束，则终止请求
            print('[-] info : ' + str(e))


    print(f'[-] info : 记录了 {len(ip_list)} 条数据')
def nonono():
			print(
'''
zoomeye.py [-h] -p num -l str 
	-l 				搜索语法(仅支持单个限制)
	-p 				页数(默认十页)
	-h 				zoomeye语法帮助
'''
			)

def help():
	print(
'''
                                            主机设备搜索

组件:
	app: 组件名
	ver: 组件版本                                        app:Apache
端口:				
	port: 端口号                                         port:3389
操作系统:			
	os: 操作系统	                                     os:linux
服务:			
	service:服务名称                                     service:webcam
主机名:										
	hostname: 分析结果中的“主机名”字段                 hostname:google.com
位置:			
	country: 国家或者地区代码			
	city: 城市名称                                       country:US
			
IP 地址:			
	ip: 搜索一个指定的 IP 地址                           ip: 8.8.8.8
CIDR:			
	IP 的 CIDR 网段。                                    cidr:8.8.8.8/24
			
			
                                            Web应用搜索
			


网站:			
	site:网站域名                                        site:google.com
标题:			
	title: 页面标题，在<title>                           title:Nginx
关键词:			
	keywords:<meta name="Keywords">定义的页面关键词      keywords:Nginx
描述:
	desc: <meta name="description">定义的页面说明。       desc:Nginx
HTTP 头:
	headers: HTTP 请求中的 Headers。                     headers:Server
'''
		)

def start():
	arg = sys.argv
	if len(arg) == 2 and arg[1] == '-h' :
		help()
		exit()
	elif len(arg) == 3 and arg[1] == '-l' :
		if type(arg[2]) is str:
			return arg[2],11
	elif len(arg) == 5 and '-l' in arg and '-p' in arg:
		xxx=0
		for i in range(len(arg)):
			#print(xxx)
			if arg[i] == '-l':
				if type(arg[i+1]) is str:
					restart = arg[i+1]
				else: 
					xxx = 1
			try:
				if arg[i] == '-p' :
					page = int(arg[i+1]) + 1
			except: 
				xxx=1
		if xxx == 0:
			return restart,page 
	
	nonono()
	exit()




def main(restart,page):
    login() #得到access_token
    restart_url = quote(restart)
    apiTest(restart_url,page)
    saveListToFile(f'.\\{restart}.txt',ip_list)

if __name__ == '__main__':

	restart,page = start()
	main(restart,page)
