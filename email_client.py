# coding: utf-8
import sys
from email_services import UkrNetService
from pyvirtualdisplay import Display


def choice_service():
    while True:
        print 'What email service do want to use:'
        print 'ukr.net --> enter 1'
        print 'google email --> enter 2 (not available yet)'
        email_service=int(raw_input())
        enter_num_serv=[1] # 1 is ukr.net, you may add a numder of your new email service.
        # checking, if this number(email_service) in the list of email services
        if enter_num_serv.count(email_service)!=0:
            if email_service==1:
                service=UkrNetService()
            #in this place you may add new email services as an instance of your_service_class
            return service
        else:
            print 'You selected an error email service. Try again'
            continue

def choice_command():
    print 'Enter what you want to do:'
    print'-- send a letter'
    print'-- view a list of writing letters'
    print'-- read a certain letter'
    print '(Commands: letter_list, read_letter, write_letter)'
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
                service.driver.quit()
                #display.stop()
                sys.exit(0)
        else:
            print 'You entered an error command.'
            continue

def run_command(command,log,pas):
    service.open_email(log,pas)
    getattr(service, command)()


# display = Display(visible=0, size=(800, 600))
# display.start()
service=choice_service()
service.driver.get(service.email_service)
print 'you have chosen',service.name
while True:
    log=raw_input('enter your login: ').strip()
    pas=raw_input('enter your pass: ').strip()
    if service.check_log_pas(log,pas):
        while True:
            command=choice_command()
            if command==False:
                continue
            else:
                run_command(command,log,pas)
                if continue_func():
                    continue
    else:
        print 'You entered an error login or password. Try again'
        continue