from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import os
import scraper.constant as CONST
from scraper.email_sender import Email

class Scraper(webdriver.Chrome):
    def __init__(self , tearDown = False , data =[]):
        self.tearDown = tearDown
        os.environ['PATH']+=CONST.DRIVER_PATH

        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        super(Scraper , self).__init__(options=options)
        

        self.data = data
    
    def land_first_page(self):
        self.get(CONST.URL)
    

    def sign_in(self , username=442102672 ,password= 'RQCE!@vmwo52'):
        self.implicitly_wait(10)

        #sign in'
        pull_down = self.find_element(By.CSS_SELECTOR , 'div[class^="pui-dropdown-trigger"]')
        pull_down.click()

        student_option = self.find_element(By.CSS_SELECTOR , 'li[data-label="طالب"]')
        student_option.click()

        user_name = self.find_element(By.ID , 'username')
        user_name.send_keys(442102672)
       
        password = self.find_element(By.ID , 'password')
        password.send_keys('RQCE!@vmwo52')

        login_btn = self.find_element(By.ID , 'loginButton')
        login_btn.click()

        academy_btn = self.find_element(By.ID , 'menuForm:menuTable:3:categories')
        academy_btn.click()

        check_btn = self.find_element(By.ID,'menuForm:menuTable:3:services:3:urlMenu')
        check_btn.click()
        add_btn = self.find_element(By.CLASS_NAME,'addButton')
        add_btn.click()
    

    def scrap(self):
        self.implicitly_wait(60)
        table = self.find_element(By.XPATH , '/html/body/center/div[12]/div[2]/div[2]/div[3]/form/table[4]/tbody/tr[2]/td/table/tbody/tr[3]/td/table/tbody')
        self.implicitly_wait(60)
        elements = table.find_elements(By.CSS_SELECTOR,'tr[align="center"]')
        data =[]
        for element in elements:
            try:
                sign = str(element.find_element(By.CSS_SELECTOR,'td[class^="ROW"]').get_attribute('innerHTML').strip().replace('&nbsp;',''))
                name = str(element.find_element(By.CSS_SELECTOR,'td[class^="ROW_LEFT"]').get_attribute('innerHTML').strip().replace('&nbsp;',''))
                data.append(sign+' '+name)
            except:
                break
        
        self.filter_data(data)
           
        
        


    ''' page = self.page_source
        soup = BeautifulSoup(page,'lxml')
        table = soup.find_all('table')[1]'''

        
    def reload(self):
        back_btn = self.find_element(By.CLASS_NAME,'backButton')
        back_btn.click()

        time.sleep(2)
        add_btn = self.find_element(By.CLASS_NAME,'addButton')
        add_btn.click()
    def filter_data(self , data : list):
        #remove old data
        for d in self.data:
            if not data.__contains__(d):
                self.data.remove(d)

        #update data 
        for d in data:
            if not self.data.__contains__(d):
                #send mail about a new appointment had been available
                mail = Email("s.a.a.d.alsahly.al.sahly@gmail.com","sz0d.717@gmail.com","lrfvkpwggojixkow")
                mail.send_mail(f"{d}",f"")
                self.data.append(d)


     #context protocole
    def __enter__(self):
        return self
    
    def __exit__(self,exc_type,exc_value,exc_traceback):
        if self.tearDown:
            self.close()
            self.quit()