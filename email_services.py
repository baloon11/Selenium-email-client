# coding: utf-8
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert


class EmailService(object):
    """The parent class for all classes that implement the api to email services"""
    def __init__(self):
        self.email_service='your_email_service'
        self.driver=webdriver.Firefox()
        self.name='Name of the email service. Override this arrt in a child class'

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
    """The class for ukr.net service"""
    def __init__(self):
        super(UkrNetService, self).__init__()
        self.email_service='https://www.ukr.net/'
        self.name='ukr.net'

    def open_email(self,log,pas):
        ''' this method open https://www.ukr.net/ service, open list of letters'''
        email_service='https://www.ukr.net/'
        self._send_keys_element(element_selector='div.login input',text=log)#enter login
        self._send_keys_element(element_selector='div.password input',text=pas)#enter pass
        self._press_submit(element_selector='div.submit button')
        self.driver.implicitly_wait(10)
        self._click_by_element(element_selector='ul.user-info li a.mails')#transition to the page with a list of letters

    def _switch_to_simpletext_mode(self):
        simple_text_butt=self.driver.find_element_by_css_selector('div.fmedit-panel a')
        if simple_text_butt.text==u'Простий текст' or simple_text_butt.text==u'Простой текст':
            self.driver.implicitly_wait(5)
            simple_text_butt.click()
            self.driver.implicitly_wait(5)
            Alert(self.driver).accept()

    def _logout(self):
        self._click_by_element(element_selector='div.user-name a')

    def write_letter(self):
        try:
            to_email=raw_input('enter the email of the recipient: ').strip()
            subject=raw_input('enter the subject of the email: ').strip()
            text=raw_input('enter your the text of the email: ')
            self.driver.switch_to_window(self.driver.window_handles[1])# switch to letter list window
            self._click_by_element(element_selector='div.compose-link-box a.compose-message-link')#write_letter_button click
            self._switch_to_simpletext_mode()
            self.driver.implicitly_wait(5)
            self._send_keys_element(element_selector='input#toField',text=to_email)# enter to_field (an email)
            self._send_keys_element_by_name(element_selector='subject',text=subject) #enter the subject of the email
            self._send_keys_element(element_selector='textarea#text',text=text) #enter the text of the email
            self._click_by_element(element_selector='span.send-button.button input')# send an email
            print "The letter was sent"
            print '---'*8
            self.driver.close()#close the window with a form for sending the letter.
            self.driver.switch_to_window(self.driver.window_handles[0])#switch to main window
            self._logout()
        except:
            print "Error.The letter was not sent"
            print '---'*8
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])#switch to main window
            self._logout()

    def letter_list(self):
        num=int(raw_input("enter how many recent emails' subjects you want to see: "))
        self.driver.switch_to_window(self.driver.window_handles[1])# switch to letter list window
        tbody=self.driver.find_element_by_css_selector('table.grid.search-enabled tbody#msglist_rows')
        rows_list=tbody.find_elements_by_css_selector('tr')[:num]# the part of the list of rows
        for index,row in enumerate(rows_list, start=1):
            out_line=[]
            cols_list=row.find_elements_by_css_selector('td')# list of cols in current row
            # in each cols_list are 7 cols
            from_col=cols_list[2].find_element_by_css_selector('a') #from title (link)
            from_title=unicode(from_col.get_attribute("title"))
            subject=unicode(cols_list[3].find_element_by_css_selector('span').text)
            date=unicode(cols_list[4].get_attribute("title"))
            print '%s | %s\t%s\t%s'%(index,from_title,subject,date)
            print '---'*8
        self.driver.close()#close the window with the letter list.
        self.driver.switch_to_window(self.driver.window_handles[0])#switch to main window
        self._logout()

    def read_letter(self):
        num=int(raw_input("enter what email (what number) do you want to read: "))
        self.driver.switch_to_window(self.driver.window_handles[1])# switch to letter list window
        tbody=self.driver.find_element_by_css_selector('table.grid.search-enabled tbody#msglist_rows')
        row=tbody.find_elements_by_css_selector('tr')[num-1]# row in(email in email list) that you want to read
        row.click()
        from_email=self.driver.find_element_by_css_selector('div.center-info a.from').text
        subject=self.driver.find_element_by_css_selector('div.center-info span.subject').text
        text=self.driver.find_element_by_css_selector('div#displayBody.body pre').text
        print'==='*8
        print 'from: ',from_email
        print 'subject: ', ' '.join(subject.split(' ')[1:])
        print 'text: ',text
        print'==='*8
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])#switch to main window
        self._logout()