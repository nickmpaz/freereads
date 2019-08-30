# Freereads

## About 

A terminal-based application that searches Library Genesis for e-books and 
displays the results. The user can then download the book, and the application
will send it directly to their Amazon Kindle.

Freereads is built with Python. The terminal display is handled with curses. 
Interaction with Library Genesis and its mirror sites is done with Requests 
and BeautifulSoup4. Emailing is done through Gmail's smtp server.

## Demo

<img src="https://i.imgur.com/F5g0k4e.gif" alt="Freereads Demo" width="100%">

## Installation

### Download and setup

Run the following commands:

    $ git clone https://github.com/nickmpaz/freereads.git && cd freereads
    $ sudo pip3 install -r requirements.txt
    $ mv .env.example .env

### Edit the .env file

Fill out the following information:

    SENDER_EMAIL="your_gmail_address"
    SENDER_PASSWORD="your_gmail_password"
    RECEIVER_EMAIL="your_kindle_email_address"

For a Gmail account to be used by the application, it must "allow less secure apps" 
(It may be smart to create a seperate Gmail account for this application). 
How to do this: 

- <https://devanswers.co/allow-less-secure-apps-access-gmail-account/>

Whichever Gmail account you use, the account must be added to your Amazon account as an 
approved email. How to do this: 

- <https://www.amazon.com/gp/help/customer/display.html?ie=UTF8&nodeId=201974240>


### Starting the application

    $ python3 freereads.py

