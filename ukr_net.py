# coding: utf-8
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert


class EmailService(object):
    """docstring for EmailService"""
    def __init__(self):
        self.email_service='your_email_service'
        self.driver=webdriver.Firefox()

    def _click_by_element(self,element_selector=''):
        elem=self.driver.find_element_by_css_selector(element_selector)
        elem.click()

    def _send_keys_element(self,element_selector='',text=''):
        elem=self.driver.find_element_by_css_selector(element_selector)
        elem.send_keys(text)

    def _send_keys_element_by_name(self,element_selector='',text=''):
        elem=self.driver.find_element_by_name(element_selector)
        elem.send_keys(text)

    def _press_submit(self,element_selector=''):
        elem=self.driver.find_element_by_css_selector(element_selector)
        elem.submit()

    def open_email(self):
        '''Override this method in a child class'''
        pass

    def write_letter(self):
        '''Override this method in a child class'''
        pass

    def letter_list(self):
        '''Override this method in a child class'''
        pass


class UkrNetService(EmailService):
    """docstring for UkrNetService"""
    def __init__(self):
        super(UkrNetService, self).__init__()
        self.email_service='https://www.ukr.net/'

    def open_email(self):
        email_service='https://www.ukr.net/'
        log=unicode(raw_input('enter your login: '))
        pas=unicode(raw_input('enter your pass: '))

        self.driver.get(email_service)
        # login =self.driver.find_element_by_css_selector('div.login input')
        # login.send_keys(log)
        self._send_keys_element(element_selector='div.login input',text=log)#enter login

        # password=self.driver.find_element_by_css_selector('div.password input')
        # password.send_keys(pas)
        self._send_keys_element(element_selector='div.password input',text=pas)#enter pass

        # submit_butt=self.driver.find_element_by_css_selector('div.submit button')
        # submit_butt.submit()
        self._press_submit(element_selector='div.submit button')

        self.driver.implicitly_wait(10)

        # letters=self.driver.find_element_by_css_selector('ul.user-info li a.mails')
        # letters.click()
        self._click_by_element(element_selector='ul.user-info li a.mails')#transition to the page with a list of letters

    def _switch_to_simpletext_mode(self):
        simple_text_butt=self.driver.find_element_by_css_selector('div.fmedit-panel a')
        if simple_text_butt.text==u'Простий текст' or simple_text_butt.text==u'Простой текст':
            self.driver.implicitly_wait(5)
            simple_text_butt.click()
            self.driver.implicitly_wait(5)
            Alert(self.driver).accept()

    def write_letter(self):
        try:
            to_email=raw_input('enter the email of the recipient: ')
            subject=unicode(raw_input('enter the subject of the email: '))
            text=unicode(raw_input('enter your the text of the email: '))

            #letter_list_window=driver.window_handles[1]
            self.driver.switch_to_window(self.driver.window_handles[1])

            # write_letter_butt=self.driver.find_element_by_css_selector('div.compose-link-box a.compose-message-link')
            # write_letter_butt.click()
            self._click_by_element(element_selector='div.compose-link-box a.compose-message-link')#write_letter_button click

            self._switch_to_simpletext_mode()

            self.driver.implicitly_wait(5)

            # to_field=self.driver.find_element_by_css_selector('input#toField')
            # to_field.send_keys(to_email)
            self._send_keys_element(element_selector='input#toField',text=to_email)# enter to_field (an email)

            # subject_field=self.driver.find_element_by_name('subject')
            # subject_field.send_keys(subject)
            self._send_keys_element_by_name(element_selector='subject',text=subject) #enter the subject of the email

            # letter_text=self.driver.find_element_by_css_selector('textarea#text')
            # letter_text.send_keys(text)
            self._send_keys_element(element_selector='textarea#text',text=text) #enter the text of the email

            # send_letter_butt=self.driver.find_element_by_css_selector('span.send-button.button input')
            # send_letter_butt.click()
            self._click_by_element(element_selector='span.send-button.button input')# send an email

            print "The letter was sent"
            print '---'*8
            self.driver.switch_to_window(self.driver.window_handles[0])#switch to main window
        except:
            print "Error.The letter was not sent"
            print '---'*8

    def letter_list(self):
        num=int(raw_input("enter how many recent emails' subjects you want to see: "))
        letter_list_window=self.driver.window_handles[1]
        self.driver.switch_to_window(letter_list_window)

        tbody=self.driver.find_element_by_css_selector('table.grid.search-enabled tbody#msglist_rows')
        rows_list=tbody.find_elements_by_css_selector('tr')[:num]# the part of the list of rows
        for index,row in enumerate(rows_list, start=1):
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
            print '%s | %s\t%s\t%s'%(index,from_title,subject,date)
            print '---'*8
        self.driver.switch_to_window(self.driver.window_handles[0])#switch to main window


#uncomment this lines (if you want to see a list of subjects(table)) and run python ukr_net.py
ukr_net=UkrNetService()
ukr_net.open_email()# open https://www.ukr.net/ service, open list of letters
ukr_net.letter_list()#parsing list of subjects(table) and getting subjects and additional info
ukr_net.driver.quit()#close all windows

#uncomment this lines (if you want to send email) and run python ukr_net.py
# ukr_net=UkrNetService()
# ukr_net.open_email()
# ukr_net.write_letter()
# ukr_net.driver.quit()#close all windows