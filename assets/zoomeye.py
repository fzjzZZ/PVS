# coding: utf-8
from urllib.parse import quote
import os,requests,json,sys,getpass 
import argparse
access_token = ''
ip_list = []

def parse_args():
    """
    :return:进行参数的解析
    """
    description = "you should add those parameter"                   
    parser = argparse.ArgumentParser(description=description)        
                                                                    
    help = "Please follow the rules"
    parser.add_argument('-p',"--page",help = "Please enter pages",type = int)                  
    parser.add_argument('-g',"--grammar",help = "Please enter zoomeye grammar",type = str)  
    args = parser.parse_args()                                             
    return args


#输入用户名密码连接
def login():
    global access_token
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
        # print(access_token)
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
    # 将 token 格式化并添加到 HTTP Header 中
    headers = {
        'Authorization' : 'JWT ' + access_token
    }
    #print(headers)
    for page in range(1,page + 1):
        try:         
            r = requests.get(f'https://api.zoomeye.org/host/search?query="{restart}"&facet=app,os&page=' + str(page),headers = headers)
            r_decoded = r.json()
            #print(r_decoded)
            for x in r_decoded['matches']:
                print(x['ip']+":"+str(x['portinfo']['port']))
                ip_list.append(x['ip']+":"+str(x['portinfo']['port']))
            #print('[-] info : count ' + str(page * 10))
                        
        except Exception as e:
            # 若搜索请求超过 API 允许的最大条目限制 或者 全部搜索结束，则终止请求
            print('[-] info : ' + str(e))
    print(f'[-] info : 记录了 {len(ip_list)} 条数据')



def main(restart,page):
    login() #得到access_token
    restart_url = quote(restart)
    apiTest(restart_url,page)
    saveListToFile(f'.\\{restart}.txt',ip_list)

if __name__ == '__main__':
    args = parse_args()
    main(args.grammar,args.page)
