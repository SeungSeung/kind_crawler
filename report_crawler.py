import requests
from bs4 import BeautifulSoup
import pandas as pd
from pypdf import PdfReader
from tqdm import tqdm
import time
import numpy as np


def report_crawler(start,end):
    date_list=[]
    text_list=[]
    name_list=[]
    for i in tqdm(range(start,end,1)):
    
        html = requests.get(f"https://finance.naver.com/research/company_list.naver?&page={i}")
        bs4 = BeautifulSoup(html.text,'html5lib')
        obj = bs4.find("table",{"class":"type_1"}).tbody
        obj = [_ for _ in obj.find_all("tr") if _.find("a") is not None]
    # lmap = [{"Title":_.find("a",{"class":"stock_item"})["title"], "Publisher":_.find_all("td")[2].text, "Link": _.find("td",{"class":"file"}).a['href']} for _ in obj]
        date = bs4.find_all("td",{"class":"date","style":"padding-left:5px"})
        date_list.extend(date)
        for num in range(len(obj)):
            try:
                response=requests.get(obj[num].find('td',{"class":"file"}).a.attrs['href'])
            except Exception:
                response=None
            title=obj[num].find('a',{"class":"stock_item"}).get_text()
            name_list.append(title)
            pdf = open("pdf"+str(1)+".pdf", 'wb')
            if response!=None:
                pdf.write(response.content)
            pdf.close()
            if response!=None:
                try:
                    reader = PdfReader("pdf1.pdf")
                    number_of_pages = len(reader.pages)
                    text_sum=""
                    for pg in range(number_of_pages):
                        page = reader.pages[pg]
                        try:
                            text = page.extract_text()
                            text=","+text
                            text_sum+=text
                        except Exception as e:
                            pass
                    text_sum.replace('\n',"")
                    text_list.append([text_sum])

                except Exception as e:
                    text_list.append(np.nan)
            else:
                text_sum=np.nan
                text_list.append([text_sum])
            
            
    data={'date':date_list,'name':name_list,'report':text_list}
    df=pd.DataFrame(data,columns=['date','name','report'])
    df['date']=[day.text for day in df['date']]
    df['date']=[f'20{i[0:2]}-{i[3:5]}-{i[6:8]}'  for i in df['date']]
    df['date']=pd.to_datetime(df['date'])
    return df

