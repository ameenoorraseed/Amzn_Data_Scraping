import requests
from bs4 import BeautifulSoup
import json,csv

import concurrent.futures
from datetime import datetime


        
    
headers = {
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.amazon.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


#with open("d:\check.txt",'w') as f:
#    f.write("2023-03-08")
    
    
def price():
    a=soup.text.partition('price')[0]
    a = a.replace('\n','')
    b=a.split().index('Price')
    price = a.split()[b+1]
    tt=''
    if price[0] == '$':
        for i in price:
            if i.isdigit() or i=='.':
                tt += i
                
        return tt
    else:
        return None

cdate = datetime.today().strftime('%Y-%m-%d')



#with open("d:\check.txt",'w') as f:
#    f.write("2023-03-08")

    
def stock():
    s = soup.get_text()
    #print(s)
    if 'Currently unavailable.' in s:
        return None
    return 'In Stock'
    
def delivery():
    aa=soup.text
    aa = aa.splitlines()
    t = ''
    global p
    for i in aa:
        
        if 'Shipping & Import Fees' in i:
            p = i
        if "Delivery" in i:
            t+= i
            break
    #print(t.split())
    t = t.split()
    
    s = t[0]+' '+' '.join(t[-4:])
    if 'Become' in s:
        s = None
    try:
        s=s.replace('Book DepositoryBooks With ','')
    except:
        pass
    return s
        
        
def main():
    c = 0
    print('working')
    global page
    global soup
    with open("urls.txt",'r') as urllist, open('output.csv','w',newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Url','asin','stock','price','free delivery'])

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            for URL in urllist.read().splitlines():
                page = requests.get(URL,headers=headers)
                soup = BeautifulSoup(page.content, "html.parser")
                asin = URL.split("/")[-1]
                print(f'fetching data of {URL}')
                try:
                    executor.map(writer.writerow([URL,asin,stock(),price(),delivery()]), urllist.read().splitlines())
                    c +=1
                except:
                    executor.map(writer.writerow([URL,asin,stock(),None,delivery()]), urllist.read().splitlines())
                    c +=1
                    

            
            #executor.map([URL,asin,stock(),p,free()], )



#with open("d:\check.txt",'r') as f:
#    if cdate=="2023-03-08":
#        print('please contact author for payment')

#    else:
main()


