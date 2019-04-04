
# coding: utf-8

# In[ ]:


import numpy as np ,pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time


# In[ ]:


# id 可能需要根据实际电脑来设定
def get_time(start,end):
    Gre_cal,week_day,jieri,Lunar_cal,rest=[],[],[],[],[]
    root_url = 'https://wannianrili.51240.com/'
    browser = webdriver.Chrome() 
    browser.get(root_url) 
    html=browser.page_source                   
    y=2019
    times=y-start
    for _ in range(times):
        browser.find_element_by_xpath('//*[@id="jie_guo"]/div[1]/div[1]/div[1]/input[1]').click()
        time.sleep(2)
    for _ in range((end-start)*12):
        html=browser.page_source                   
        soup=BeautifulSoup(html,'lxml')
        tag_soup = soup.find(class_='wnrl_k')
        if tag_soup == None:  #日期处理
            print('Error')
        else:
            detail = tag_soup.find_all(class_='wnrl_k_you')
            for i in range(len(detail)):
                year=detail[i].find(class_='wnrl_k_you_id_biaoti').get_text()
                day=detail[i].find(class_='wnrl_k_you_id_wnrl_riqi').get_text()
                lunar=detail[i].find(class_='wnrl_k_you_id_wnrl_nongli').get_text()
                try:
                    festival=detail[i].find(class_='wnrl_k_you_id_wnrl_jieri_neirong').get_text()
                except:
                    festival=' '
                date=year[:4]+'-'+year[6:8]+'-'+day
                day=year[-3:]
                Gre_cal.append(date)
                week_day.append(day)
                jieri.append(festival)
                Lunar_cal.append(lunar)
            rest_jun = tag_soup.find_all(class_='wnrl_riqi')
            for i in range(len(rest_jun)):
                b=str(rest_jun[i])
                if  'wnrl_riqi_xiu' in b:
                    y=1 #休假
                elif 'wnrl_riqi_ban' in b:
                    y=2 # 需加班
                else:
                    y=0 #正常
                rest.append(y)
        browser.find_element_by_xpath('//*[@id="jie_guo"]/div[1]/div[1]/div[1]/input[4]').click()
        time.sleep(2)
    return pd.DataFrame(np.array([Gre_cal,Lunar_cal,week_day,jieri,rest]).T,
                            columns=['公历','农历','星期','节日','安排'])


# In[ ]:


def get_time(start,end=None):
    '''默认的end 是当前的天数'''
    if end:
        down_times=(end-start)*12 
        up_times=(end-time.localtime().tm_year)*12 - int(time.localtime().tm_mon)
    else:
        down_times=(time.localtime().tm_year-start)*12 + int(time.localtime().tm_mon)
        up_times=0
    print(up_times,down_times)
    root_url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E4%B8%87%E5%B9%B4%E5%8E%86&rsv_pq=e43bb70f000060c5&rsv_t=d945FpUQcvreJk7Ldz6LFngT7fj5HuefjETdW1xFuSctoT3Kk09%2BXRU5Jks&rqlang=cn&rsv_enter=1&rsv_sug3=13&rsv_sug1=13&rsv_sug7=101'
    browser = webdriver.Chrome() 
    browser.get(root_url) 
    html=browser.page_source 
    soup=BeautifulSoup(html,'lxml')
    days,fast,xiujia,years,months,weeks=[],[],[],[],[],[]
    weekday=['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
    print()
    for _ in range(up_times):
        browser.find_element_by_xpath('//*[@id="1"]/div[1]/div[1]/div[1]/div[1]/div[2]/a[2]').click()
        time.sleep(0.5)
        
    for _ in range(down_times):
        html=browser.page_source                   
        soup=BeautifulSoup(html,'lxml')
        year_month=soup.find_all(class_='c-dropdown2-btn')
        year=year_month[0].get_text()
        month=year_month[1].get_text()
        riqi =soup.find_all(class_='op-calendar-new-daynumber')
        jieri = soup.find_all(class_='op-calendar-new-table-almanac')
        work_rest=soup.find_all(class_='op-calendar-new-relative')
        for _ in range(len(work_rest)):
            s='op-calendar-new-table-other-month'
            if s not in str(work_rest[_]):
                day=riqi[_].get_text()
                days.append(day)
                fas=jieri[_].get_text()
                fast.append(fas)
                try:
                    xiu = work_rest[_].find(class_='op-calendar-new-table-holiday-sign').get_text()
                except:
                    xiu=' '
                weeks.append(weekday[_%7])
                xiujia.append(xiu)   
                months.append(month)
                years.append(year)
        browser.find_element_by_xpath('//*[@id="1"]/div[1]/div[1]/div[1]/div[1]/div[2]/a[1]').click()
        #time.sleep(1)
    return pd.DataFrame({'年份':years,'月份':months, '日期':days,'星期':weeks,'节假':fast,'加班':xiujia})

