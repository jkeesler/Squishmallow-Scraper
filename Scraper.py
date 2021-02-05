import requests
from bs4 import BeautifulSoup
import re
import SMS
import time
import sys

class Error404(Exception):
    pass


time_break = 30 #minuites
repeat_text = False

def check_product(url):
    SentMessage = False
    
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        if response.status_code != 200:
            raise Error404('There was an error accessing the webpage. Error Code: {}'.format(response.status_code))
        
        else:
            for ele in soup.find_all('p', class_='stock'):
                print('Searching')
                if 'in' in ele.text.lower():
                    ItemName = soup.find('h1', class_="product_title").text
                    stock_string = ele.text.lower()
                    NumInStock = int(re.search(r'\d+', stock_string).group())
                
                    if SentMessage == False:
                        print('There are {} {} in stock'.format(NumInStock, ItemName))
                        SMS.send('There are {} {} in stock'.format(NumInStock, ItemName), number, carrier)
                        if repeat_text == False:
                            SentMessage = True  
                        else:
                            pass
                        
                    else:
                        pass
                    
                elif 'out' in ele.text.lower():
                    print('Currently Out of Stock')
            
                else:
                    pass
        time.sleep(60 * time_break)

def check_product_category(url):
    SentMessage = False
    
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        if response.status_code != 200:
            raise Error404('There was an error accessing the webpage. Error Code: {}'.format(response.status_code))
            
        elif list(soup.find_all('p', class_='woocommerce-info')):
            print("Currently Out of Stock")
            
        else:    
            
            StockMessage = ""
            
            if ProductFlag == False:
                
                for ele in soup.find_all('span', class_='gtm4wp_productdata'):
                    ItemName = ele.get('data-gtm4wp_product_name')
                    NumInStock = ele.get('data-gtm4wp_product_stocklevel')
                    
                    if NumInStock == '':
                        NumInStock = 'Unknown'
                        
                    message_fragment = 'There are '+ NumInStock + ' ' + ItemName + ' in stock\n'
                    StockMessage += message_fragment
                    
                if SentMessage == False:
                    SMS.send(StockMessage, number, carrier)
                
                    if repeat_text == False:
                        SentMessage = True  
                    else:
                        pass
                else:
                    pass
                    
          ##################          
            elif ProductFlag == True:
                
                for ele in soup.find_all('span', class_='gtm4wp_productdata'):
                    ItemName = ele.get('data-gtm4wp_product_name').lower()
                    NumInStock = ele.get('data-gtm4wp_product_stocklevel')
                    
                    if NumInStock == '':
                        NumInStock = 'Unknown'
                    else:
                        pass
                        
                    if LookingFor in ItemName:
                        message_fragment = 'There are ' + NumInStock + ' ' + ItemName + " in stock\n"
                        StockMessage += message_fragment
                        
                        if SentMessage == False:
                            SMS.send(StockMessage, number, carrier)
                
                            if repeat_text == False:
                                SentMessage = True  
                            else:
                                pass
                        else:
                            pass
                        
        time.sleep(60 * time_break)

greeting = 'Hello, what Squishmallow Product/Product Category Would You Like To Track (Please Provide A URL): '
url = input(greeting)

number = input('Please input a phone number for messaging (e.g 1234567890): ')

carrier = input('What carrier do you use: ')
carrier = carrier.lower()

SpecificProduct = input('Are You Looking For A Specific Squishmallow [Y/N]: ')
if SpecificProduct.lower() == 'y':
    ProductFlag = True
    LookingFor = input('What Is The Name Of The Squishmallow You Are Looking For (e.g. Jack): ').lower()
else:
    ProductFlag = False

if 'product-category' in url:
    check_product_category(url)
elif 'product' in url:
    check_product(url)
elif url == 'https://squishmallows.com/':
    check_product_category(url)