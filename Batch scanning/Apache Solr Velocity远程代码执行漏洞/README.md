# **Apache Solr Velocity远程代码执行漏洞**

## 受影响系统

Apache Solr <=8.2.0

## 环境

`python 3`

## 使用

1. 使用资产收集脚本收集使用 Solr 的服务器

   eg: python zoomeye -g solr -p 10

2. 将生成的 `solr.txt`与脚本存放到一起并执行脚本,结束后生成`have_attack.txt` 文件

   ![image-20191207170526719](C:\Users\95830\AppData\Roaming\Typora\typora-user-images\image-20191207170526719.png)