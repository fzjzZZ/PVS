# -*- coding: utf-8 -*-
import pyfofa,argparse

def check_user():
	'''
	请将邮箱以及API值填入此处
	'''
	email = ''
	key = ''
	client = pyfofa.FofaAPI(email,key)
	userinfo = client.get_userinfo()
	try:
		print('[*] success!')
		print(f'用户名:\t\t{userinfo["username"]}\nvip等级:\t\t{userinfo["vip_level"]}\n剩余F币:\t\t{userinfo["fcoin"]}\n\n')
		return client
	except:
		print(f'[*] error:{userinfo["errmsg"]}')
		print('[*] exit!')
		exit()
def save(res,grammar):
	with open(f'.//result//{grammar}.txt','w') as f:
		for i in res:
			f.write(i+'\n')
	print(f'[*] info:共收集{len(res)},并保存在.//result//{grammar}.txt中')
	exit()

def parse_args():
    """
    :return:进行参数的解析
    """
    description = "you should add those parameter"                   
    parser = argparse.ArgumentParser(description=description)        
                                                                    
    help = "Please follow the rules"
    parser.add_argument('-g',"--grammar",help = "Please enter zoomeye grammar",type = str)  
    parser.add_argument('-p',"--page",help = "Please enter pages",type = int,default = 1)                  
    parser.add_argument('-f',"--first",help = "Please enter the start page. The default is 1",type = int,default = 1)  
    args = parser.parse_args()  

    if args.grammar:                                          
    	return args
    else:
    	print("usage: fofa_pro.py [-h] [-g GRAMMAR] [-p PAGE] [-f FIRST]")
    	exit()

def Get_Data(grammar,page,first,client):
	res = []
	print("[*] info: 小主稍安勿躁,正在收集中")
	for i in range(first,page+first):
		data = client.get_data(grammar,i,"host,ip")
		if data['error'] == True:
			print(f'[*] error:{data["errmsg"]}')
			print('[*] exit!')
			if res:
				save(res,grammar)
		for j in data['results']:
			if 'https' in j[0]:
				res.append(j[0])
			else:
				res.append('http://' + j[0])
	save(res,grammar)

def main():
	args = parse_args()
	client = check_user()
	Get_Data(args.grammar,args.page,args.first,client)
	

if __name__ == '__main__':
	main()

