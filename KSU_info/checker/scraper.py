from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import checker.contsants as CONST
import pandas as pd


class Scraper(webdriver.Chrome):
    def __init__(self , tearDown = False):
        self.tearDown = tearDown
        #configering selenium driver path to the os
        os.environ['PATH']+=CONST.DRIVER_PATH

        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        super(Scraper , self).__init__(options=options)

        self.implicitly_wait(10)
        data =[]
    
    def land_first_page(self):
        self.get(CONST.URL)
        self.maximize_window()

    def choose_section(self,section_sign='عال'):
        #المقررات المطروحة
        button_1 = self.find_element(By.ID,'myForm:timetableTreeId')
        button_1.click()

        time.sleep(2)
        CS_IS = self.find_element(By.ID,'jtree16')
        CS_IS.click()

        CS = self.find_element(By.ID , 'jtree210')
        CS.click()

        CSCN = self.find_element(By.ID,'stree211')
        CSCN.click()


        section_field = self.find_element(By.ID,'myForm:courseCodeId')
        section_field.send_keys(section_sign)
        search_button = self.find_element(By.CSS_SELECTOR , 'a[onclick="validateRequest();"]')
        search_button.click()
    
    def scrap(self):
        table = self.find_element(By.ID,'myForm:timetable')
        subjects = table.find_elements(By.CSS_SELECTOR,'tr')[1:]
        n = len(subjects)
        list = []
        for x in range(n):
            sign = str(subjects[x].find_elements(By.CSS_SELECTOR,'td')[0].get_attribute('innerHTML').strip())
            name =str(subjects[x].find_elements(By.CSS_SELECTOR,'td')[1].get_attribute('innerHTML').strip())
            section = int(subjects[x].find_elements(By.CSS_SELECTOR,'td')[2].get_attribute('innerHTML').strip())
            activity = str(subjects[x].find_elements(By.CSS_SELECTOR,'td')[3].get_attribute('innerHTML').strip())
            if 'تمارين' not in activity and 'عملي' not in activity:
                credit_hours = int(subjects[x].find_elements(By.CSS_SELECTOR,'td')[4].get_attribute('innerHTML').strip())
            else:
                credit_hours =0
            sex = str(subjects[x].find_elements(By.CSS_SELECTOR,'td')[5].get_attribute('innerHTML').strip())
            status = str(subjects[x].find_elements(By.CSS_SELECTOR,'td')[6].find_element(By.CSS_SELECTOR,'span').get_attribute('innerHTML').strip())

            #details
            details = subjects[x].find_elements(By.CSS_SELECTOR,'td')[7].find_element(By.CSS_SELECTOR,'a[onclick^="javascript"]')
            details.click()
            print(x)

            #close details
            close_bttn = self.find_element(By.CSS_SELECTOR,'a[class*="pui-dialog-titlebar-close"]')
            close_bttn.click()

            list.append({'رمز المقرر':sign , 'سم المقرر':name , 'الشعبة' :section , 'النشاط ':activity , 'الساعات':credit_hours , 'sex' : sex , 'status' : status})
            
            if (x + 1) % 15 == 0:
                print(1)
                next_bttn = self.find_element(By.ID,'pag').find_element(By.CSS_SELECTOR,'span[class$="icon-seek-next"]')
                next_bttn.click()
                


        
        


    #context protocole
    def __enter__(self):
        return self
    
    def __exit__(self,exc_type,exc_value,exc_traceback):
        if self.tearDown:
            self.close()
            self.quit()