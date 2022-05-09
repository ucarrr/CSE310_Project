Chapter 3
Web Socket & Restful
Team Blue
Muhammet Uçar-20180808085
Emine Ece Bayramer-20180808020
Eylül Yiğit-20180808016
 
We encountered some errors while running the codes.
flask module could not be found
For this we used:
“sudo rm -rf venv” line,
then we got this error:
 
For this, we used “sudo pigpiod”.
And then we used these to run the code:
“chmod -x flask_api_server.py”
“python flask_api_server.py”



All the important lines we used:
“python3 -m venv venv”
“source venv/bin/activate”
“pip install pip –upgrade”
“pip install -r requirements.txt”
“chmod -x flask_api_server.py”
“python flask_api_server.py”




 



After we created an API using Flask, in the window we open using HTML CSS codes, we use Localhost to change the brightness of the LED. 
For situations such as controlling the led lamp in this example, Restful would be more appropriate. It is communicated with a GET request only when we want to intervene.

We decided that the Websocket system would be more suitable for the program we were planning to install. We plan our application to progress in a two-way interaction, the user requests information from the application at any time, and the application informs the user of the changes at regular intervals through notifications. In order to achieve this, we thought that the Web Socket system was more useful than Restful, both financially and in terms of functionality.




