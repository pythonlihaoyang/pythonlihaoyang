#%%
import requests ,re
from bs4 import BeautifulSoup
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

def requestsdata(urln):#输入url 转换成可供bs4操作的数据汤
    r=requests.get(urln,headers=header)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'html.parser')
    return  soup

def savehtml(name,html_url):#写入html到本地
    r=requests.get(html_url,headers=header)
    r.encoding='utf-8'
    with open('D:\系统默认\桌面\data python\html+foto\\'+name+'.html', 'w+', encoding='UTF-8-sig') as fw:
        fw.write(r.text)

def savepdf(name,pdf_url):#传入文件名称，和文件的url地址。写入pdf文件到本地
    r=requests.get(pdf_url)
    with open('D:\系统默认\桌面\data python\html+foto\\'+name,'wb+') as f:
        f.write(r.content)

for v in range(1,127):
    a=0
    url='https://rgl.faa.gov/Regulatory_and_Guidance_Library/rgFinalRule.nsf/1fea64a7e354259285256aca00749e6f!OpenView&Start=1&Count=200&Expand={}#{}'.format(v,v)
    with open('result.txt','a+',encoding='utf-8') as f:
        for i in requestsdata(url).find_all('a',{'target':'_blank'}):#提取该网页所有符合的a标签
            a+=1
            html_name=str(v)+'-'+str(a)
            print('已爬取网站文章：'+html_name)
            try:
                title_url='https://rgl.faa.gov/'+i.get('href')
                savehtml(html_name,title_url)
                f.write('[Link]:'+title_url+'\n')
            except:
                f.write('[Link]:'+'\n')
            try:
                title=i.text
                f.write('[Title/Subject]:'+title+'\n')
            except: 
                f.write('[Title/Subject]:'+'\n')
            
            
            try:
                soup=requestsdata(title_url)#文章所在网页的代码汤
                data_number=soup.find_all('div',{'id':'xSec2'},{'style':'display: block;'})
            except:
                continue
            try:
                ment=list(set(re.findall('\d+-\d+|\d+\w+-\d+',str(data_number))))#\d*代表允许数字出现n次-{1}表示-号必须出现一次
                ment_str=",".join(ment)
                f.write('[Amendment]:'+ment_str+'\n')
            except:
                f.write('[Amendment]:'+'\n')
            try:
                part_s=re.findall('Parts\s\d+\w*',str(data_number))[0]
                f.write('[Current Folder]:'+part_s+'\n')
            except:
                f.write('[Current Folder]:'+'\n') 
                url_data=soup.find('a',{'style':'display: inline-block; text-align: center'})
                f.write('[Htmlname]:'+html_name+'.html'+'\n')         
            try:
                pdf_name=url_data['title']
                pdfurl='https://rgl.faa.gov/'+url_data['href']
                savepdf(html_name+'_'+pdf_name,pdfurl)
                f.write('[Filename]:'+html_name+'_'+pdf_name+'\n')
            except:
                f.write('[Filename]:'+'\n')
            f.write('---------------------------------------------------------------'+'\n')

print('爬取完毕')

#%%