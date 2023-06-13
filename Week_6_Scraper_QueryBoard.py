#!/usr/bin/env python
# coding: utf-8

# Goals
# ===
# 1. Scrape data from public Web site: Introduce how to scrape the information of companies from Taiwan Stock Exchange. 如果從公開的資源中抓取資料？：介紹如何從台灣股市交易公司抓取上市公司資料.
#       
# 2. Implement the QueryBoard: make a streamlit artifact which avails for querying company's ticker in stock market and vice vera. 製造一個查詢上市公司的代碼系統.
# 
# 3. [Streamlit artifact](https://cchuang2009-streamlit-scrapper-query-tai-ind-query-jxprre.streamlit.app/), app link
# 
# 
# Note
# ---
# If any error occured, in which displayed warning "xxx Module not found...", use the following to install i:
# ```
# pip install xxx
# ```

# In[ ]:





# In[10]:


import streamlit as st
import pandas as pd


# In[2]:


# https://www.twse.com.tw/zh/page/products/stock-code2.html
# TAI_TWO_ind="https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"

TAI_ind='https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
# data encoded in Traditional Chinese, 資料使用繁體中文編碼
df=pd.read_html(TAI_ind,encoding='cp950')




# In[3]:


# the data in the first page (table)
# only the first feature, 有價證券代號及名稱, we want, 
# df[0]


# In[20]:


# df[0][0][2:]
#   first table, 第一個表格
#      feature 0, 欄位 0
#         start from third rows, i.e. 2

# df[0][0][2:].values


# In[21]:


# extract data and split by '\u3000', 利用字元 '\u3000' 將每一個欄位分成兩個, 
# create two-column DataFrame, 
data = df[0][0][2:].str.split('\u3000', n=1, expand=True)

# create two-column DataFrame, 將上述的兩個公開的資料成為新的欄位
df1 = pd.DataFrame({'Symbol': data[0], 'Name': data[1]})

# convert ticker to yahoo tick,  將上市公司的代碼變成 yahoo 代碼
df1['Symbol'] = df1['Symbol'].apply(lambda x: x + '.TW')


# In[22]:


df1.head()


# In[24]:


# remove any null value in cell, 去掉沒資料的欄位
df1.fillna('', inplace=True)

# and save to a file, used in later, 並存成檔案供日後使用
df1.to_csv("TWSE_TW-1.csv",index=False)


# Techniques by ChatGPT
# ---
# Honestly, this is almost completed by chatGPT, amazing! 這也是 chatGPT 完成的，神奇吧!
# 
# In the following Query airtifact is implemented by streamlit; the comments are the statements used for chatGPT, enjoy!. 下列的應用程式是使用 streamlit 完成的，註解裡面的陳述，記載了如何使用 chatGPT.
# 
# ```python
# # 1. If use python to get the data as follows:
# 
# #TAI_ind='https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
# #df=pd.read_html(TAI_ind,encoding='cp950')
# #df[0][0][2:].values
# 
# # 2. Use Python to slice df[0][0][2:] into 2 two column Dataframe by space
# # 3. slice by \u3000
# # 4. convert each cell in the first column by adding  '.TW'
# # 5. use streamlit to make a query system for column1 by column2 and vice versa
# # (*)6. 增加中英文 internationalization, (i18n) 選擇
# 
# # main code
# import streamlit as st
# import pandas as pd
# 
# # read data from the URL and create DataFrame
# 
# df1=pd.read_csv("TWSE_TW-1.csv",index_col=0)
# df1.fillna('', inplace=True)
# set up Streamlit app
# st.title("TWSE Stock Search, 台灣股票代號查詢")

# add search box and dropdown
# search_term = st.text_input("Enter search term, 輸入查詢資料:")
# search_by = st.selectbox("Search by column:", options=['公司代碼', '公司名稱'])

# search for matching rows
# if search_term:
#     if search_by == 'Symbol':
#         result = df1[df1['Symbol'].str.contains(search_term)]
#     elif search_by == 'Name':
#         result = df1[df1['Name'].str.contains(search_term)]
#     else:
#         result = pd.DataFrame()
#     st.write(result)
# ```

# In[27]:


df2=pd.read_csv("TWSE_TW-1.csv")
df2.head()


# In[11]:


df1=pd.read_csv("TWSE_TW-1.csv")
# df1[df1['Symbol'].str.contains('3008.TW')]


# Note
# ---
# 1. Automatically detect whether the client comes from Taiwan, 自動判斷是我來自台灣的使用者 
#    - download [GeoLite2-Country.mmdb](https://git.io/GeoLite2-Country.mmdb), and put it on the sub-folder, data. 將下載的檔案放在子目錄中 data/.
#    - In brief, check whether the client's IP comes from Taiwan; if yes, return True, else return False. 如果使用者的
#    網址來自台灣，則回 True，或者為 False.
#    - code
# 
# ```python 
# import geoip2.database
# 
# # path to GeoLite2-Country.mmdb file
# reader = geoip2.database.Reader('path/to/GeoLite2-Country.mmdb')
# 
# def is_client_from_taiwan(ip_address):
#     try:
#         response = reader.country(ip_address)
#         if response.country.iso_code == 'TW':
#             return True
#     except:
#         pass
#     return False
# 
# # example usage
# client_ip = '123.456.789.123' # replace with actual client IP address
# if is_client_from_taiwan(client_ip):
#     print('Client is from Taiwan')
# else:
#     print('Client is not from Taiwan')
# ```

# In[1]:


import geoip2.database

# path to GeoLite2-Country.mmdb file
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')


# In[3]:


def is_client_from_taiwan(ip_address):
    try:
        response = reader.country(ip_address)
        if response.country.iso_code == 'TW':
            return True
    except:
        pass
    return False

# example usage
client_ip = '163.25.114.1' # replace with actual client IP address
if is_client_from_taiwan(client_ip):
    print('Client is from Taiwan')
else:
    print('Client is not from Taiwan')


# In[7]:


#import streamlit as st
import requests

def get_client_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        return ip
    except Exception as e:
        print(str(e))
        return None

# example usage
ip_address = get_client_ip()
if ip_address:
#     st.write('Client IP Address:', ip_address)
    print('Client IP Address:', ip_address)
    print(is_client_from_taiwan(ip_address))
else:
#     st.write('Failed to retrieve client IP address')
    print('Failed to retrieve client IP address')


# In[15]:


# return 'zh' if comes from Taiwan, else 'en', 如果使用者來自台灣回傳 ' zh', 否則 'en'
def locate():
    ip_address = get_client_ip()
    if is_client_from_taiwan(ip_address):
       return 'zh'
    else:
       return 'en'


# Get the Client's location, and display the related Query board: as follows:
# 
# ```python
# import pandas as pd
# import streamlit as st
# 
# import requests
import geoip2.database
# 
# # path to GeoLite2-Country.mmdb file, download it to the sub-folder: data
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
# 
# # translations
translations = {
    'en': {'title': 'Taiwan Stock Exchange - Search',
           'search_option': 'Search by',
           'symbol_option': 'Symbol',
           'name_option': 'Name',
           'search_term': 'Enter search term',
           'no_results': 'No results found',
           'language': 'Language',
           'search': 'Search'},
    'zh': {'title': '台灣證券交易所 - 搜尋',
           'search_option': '搜尋方式',
           'symbol_option': '代號',
           'name_option': '名稱',
           'search_term': '輸入搜尋關鍵字',
           'no_results': '查無結果',
           'language': '語言',
           'search': '搜尋'}
}

# read data
TAI_ind = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
df = pd.read_html(TAI_ind, encoding='cp950')
df1 = pd.DataFrame(df[0][0][2:].str.split('\u3000').tolist(), columns=['Symbol', 'Name'])

#df1=pd.read_csv("TWSE.csv",index_col=0)
df1=pd.read_csv("TWSE_TW-1.csv")
df1.fillna('', inplace=True)
# set up state
state = st.session_state

# detect where client comes from
def is_client_from_taiwan(ip_address):
    try:
        response = reader.country(ip_address)
        if response.country.iso_code == 'TW':
            return True
    except:
        pass
    return False
# 
# 
def get_client_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        return ip
    except Exception as e:
        print(str(e))
        return None

def locate():
    ip_address = get_client_ip()
    if is_client_from_taiwan(ip_address):
       return 'zh'
    else:
       return 'en'   

state.lang=locate()

state.search_by = translations[state.lang]['symbol_option']
state.search_term = ''

### the original code without detecting client's location

if 'lang' not in state:
   state.lang = 'en'
if 'search_by' not in state:
   state.search_by = translations[state.lang]['symbol_option']
if 'search_term' not in state:
   state.search_term = ''
    
# set up sidebar
st.sidebar.title(translations[state.lang]['language'])
# set the defaulted value 
if state.lang=='en':
    state.lang = st.sidebar.radio('', ['en', 'zh'])
else:
    state.lang = st.sidebar.radio('', ['en', 'zh'],index=1)

st.sidebar.title(translations[state.lang]['search_option'])
state.search_by = st.sidebar.radio('', [translations[state.lang]['symbol_option'],
                                        translations[state.lang]['name_option']])
state.search_term = st.sidebar.text_input(translations[state.lang]['search_term'], state.search_term)

# set up main page
st.title(translations[state.lang]['title'])
search_by = state.search_by
search_term = state.search_term
# 
# search data
if st.button(translations[state.lang]['search']):
    if search_by == translations[state.lang]['symbol_option']:
        result = df1[df1['Symbol'].str.contains(search_term.upper())]
    elif search_by == translations[state.lang]['name_option']:
        result = df1[df1['Name'].str.contains(search_term, case=False)]
    else:
        result = df1

    # display search results
    if len(result) > 0:
        st.write(result)
    else:
        st.write(translations[state.lang]['no_results'])

st.session_state['state'] = state
# 
# ```
# 
# Also created "requirements.txt" as follows:
# ```
# geoip2
# ```

# In[13]:


# df1[df1['Symbol'].str.contains('3008')]


# In[ ]:




