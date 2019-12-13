# -*- coding: utf-8 -*-
import pyfofa,argparse,os,sys
from threading import Thread
from time import sleep
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
        sys.exit()

def save(res,grammar):
    with open(f'./result/{grammar}.txt','a') as f:
        for i in res:
            f.write(i+'\n')

def parse_args():
    """
    解析参数
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
        sys.exit()


def dump(grammar,client,page):
    res = []
    for j in range(5):
        try:
            data = client.get_data(grammar,page,"host,ip")
            break
        except:
            print(f'[*] error:网络连接不稳定,请稍后再试')
            sys.exit()
    if data['error'] == True:
        print(f'[*] error:{data["errmsg"]}')
        print('[*] exit!')
        sys.exit()
    for j in data['results']:
        if 'https' in j[0]:
            res.append(j[0])
        else:
            res.append('http://' + j[0])
    print('██',end = '')
    save(res,grammar)


def Get_Data(grammar,Page,first,client): 
    folder = os.path.exists('.\\result')
    if not folder:  
        os.makedirs('.\\result')  

    with open(f'./result/{grammar}.txt','w') as f:
        f.write('')
    print("[*] info: 小主稍安勿躁,正在收集中")

    for page in range(first,Page + first):
        t = Thread(target = dump,args = (grammar,client,page))
        t.start()
    t.join()
    sleep(5)
    print()
    print(f'[*] info:共收集{Page * 100},并保存在./result/{grammar}.txt中')
        
def main():
    args = parse_args()
    client = check_user()
    Get_Data(args.grammar,args.page,args.first,client)
    

if __name__ == '__main__':
    main()

