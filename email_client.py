# coding: utf-8
import sys
from email_services import UkrNetService
from pyvirtualdisplay import Display


def choice_service():
    print 'What email service do want to use:'
    print 'ukr.net --> enter 1'
    print 'google email --> enter 2 (not available yet)'
    email_service=int(raw_input())
    if email_service==1:
        service=UkrNetService()
    #in this place you may add new email services
    return service

def choice_command():
    print 'Enter what you want to do:'
    print'-- send a letter'
    print'-- view a list of writing letters'
    print'-- read a certain letter'
    print '(Commands: letter_list ,read_letter,write_letter)'
    command=str(raw_input()).strip()
    if command=='letter_list' or command=='read_letter' or command=='write_letter':
        return command
    else:
        print 'you entered an error command'
        return False

def continue_func():
    while True:
        cont=raw_input('You want to continue?(yes/no): ').strip().lower()
        if cont=='yes' or cont=='no':
            if cont=='yes':
                return True
            else:
                print 'Bye!'
                display.stop()
                sys.exit(0)
        else:
            print 'you entered an error command'
            continue

def run_command(command):
    service.open_email()
    getattr(service, command)()
    service.driver.quit()


display = Display(visible=0, size=(800, 600))
display.start()
service=choice_service()
print 'you have chosen',service.name
while True:
    command=choice_command()
    if command==False:
        continue
    else:
        run_command(command)
        if continue_func():
            continue