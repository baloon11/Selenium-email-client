# coding: utf-8

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert


driver = webdriver.Firefox()

def switch_to_simpletext_mode():
    simple_text_butt=driver.find_element_by_css_selector('div.fmedit-panel a')
    if simple_text_butt.text==u'Простий текст' or simple_text_butt.text==u'Простой текст':
        driver.implicitly_wait(5)
        simple_text_butt.click()
        driver.implicitly_wait(5)
        Alert(driver).accept()


def open_email():
    email_service='https://www.ukr.net/'
    log=unicode(raw_input('enter your login: '))
    pas=unicode(raw_input('enter your pass: '))

    driver.get(email_service)
    login =driver.find_element_by_css_selector('div.login input')
    login.send_keys(log)

    password=driver.find_element_by_css_selector('div.password input')
    password.send_keys(pas)

    submit_butt=driver.find_element_by_css_selector('div.submit button')
    submit_butt.submit()

    driver.implicitly_wait(10)
    letters=driver.find_element_by_css_selector('ul.user-info li a.mails')
    letters.click()


def write_letter():
    to_email=raw_input('enter the email of the recipient: ')
    subject=unicode(raw_input('enter the subject of the email: '))
    text=unicode(raw_input('enter your the text of the email: '))
    letter_list_window=driver.window_handles[1]
    driver.switch_to_window(letter_list_window)
    write_letter_butt=driver.find_element_by_css_selector('div.compose-link-box a.compose-message-link')
    write_letter_butt.click()
    switch_to_simpletext_mode()
    driver.implicitly_wait(5)
    to_field=driver.find_element_by_css_selector('input#toField')
    to_field.send_keys(to_email)

    subject_field=driver.find_element_by_name('subject')
    subject_field.send_keys(subject)

    letter_text=driver.find_element_by_css_selector('textarea#text')
    letter_text.send_keys(text.decode())

    send_letter_butt=driver.find_element_by_css_selector('span.send-button.button input')
    send_letter_butt.click()
    print "The letter was sent"
    driver.switch_to_window(driver.window_handles[0])#switch to main window

#uncomment this lines (if you want to send email) and run python ukr_net.py
# open_email()# open https://www.ukr.net/ service, open list of letters
# write_letter()# write and send the letter
# time.sleep(10)
# driver.quit()#close all windows


class EmailService(object):
    """docstring for EmailService"""
    def __init__(self):
        self.email_service='your_email_service'
        #self.driver=webdriver.Firefox()

    def _click_by_element(self,element_selector=''):
        elem=self.driver.find_element_by_css_selector(element_selector)
        elem.click()

    def _send_keys_element(self,element_selector='',text=''):
        elem=self.driver.find_element_by_css_selector(element_selector)
        elem.send_keys(text)

    def _press_submit(self,element_selector=''):
        elem=self.driver.find_element_by_css_selector(element_selector)
        elem.submit()


class UkrNetService(EmailService):
    """docstring for UkrNetService"""
    def __init__(self):
        super(UkrNetService, self).__init__()
        self.email_service='https://www.ukr.net/'

    def letter_list(self):
        num=int(raw_input("enter how many emails' subjects you want to see: "))
        letter_list_window=driver.window_handles[1]
        driver.switch_to_window(letter_list_window)
        tbody=driver.find_element_by_css_selector('table.grid.search-enabled tbody#msglist_rows')
        rows_list=tbody.find_elements_by_css_selector('tr')[:num]# splice of thr list of rows
        for row in rows_list:
            out_line=[]
            cols_list=row.find_elements_by_css_selector('td')# list of cols in current row
            # in each cols_list are 7 cols
            from_col=cols_list[2].find_element_by_css_selector('a') #from title (link)
            from_title=unicode(from_col.get_attribute("title"))
            #print from_title
            subject=unicode(cols_list[3].find_element_by_css_selector('span').text)
            #print subject
            date=unicode(cols_list[4].get_attribute("title"))
            #print date
            print '%s\t%s\t%s'%(from_title,subject,date)
        driver.switch_to_window(driver.window_handles[0])#switch to main window

#uncomment this lines (if you want to see a list of emails) and run python ukr_net.py
# open_email()# open https://www.ukr.net/ service, open list of letters
# ukr_net=UkrNetService()
# ukr_net.letter_list()
# driver.quit()#close all windows