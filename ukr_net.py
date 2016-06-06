# coding: utf-8
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert


driver = webdriver.Firefox()

def switch_to_simpletext_mode():
    simple_text_butt=driver.find_element_by_css_selector('div.fmedit-panel a')
    if simple_text_butt.text==u'Простий текст':
        driver.implicitly_wait(5)
        simple_text_butt.click()
        driver.implicitly_wait(5)
        Alert(driver).accept()


def open_email(email_service,log,pas):
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


def write_letter(to_email,subject,text):
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

open_email('https://www.ukr.net/','your_email','your_pass')# open https://www.ukr.net/ service, open list of letters
write_letter('to_email','test title','text of your letter')# write and send the letter
time.sleep(10)
driver.quit()#close all windows