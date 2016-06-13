It is a simple console email client that based on Selenium WebDriver and Python.  
#####Running:  
	python email_client.py  
It works only with https://www.ukr.net/ service yet.  

----------------

If you choose to add to this email client your favorite email service,  
create in the file `email_services.py` a subclass of `EmailService` class and override attributes and methods that are marked for override.  
Then in the file `email_client.py` create an instance of your class (see the comments in the source code).  


#####Requirements:  
	sudo apt-get firefox #if it not install yet  
	sudo apt-get install xvfb  
	pip install selenium  
	pip install pyvirtualdisplay  

#####Note:
Test the program with low CPU load.  
At high load program is unstable.  
Most likely, it is caused by the fact that the browser, that was run and works in invisible mode,  
works slower than expected (meaning pauses in the program)  
This email client can send and receive only simple text emails.  
It just a proof of concept.




