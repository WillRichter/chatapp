# Project 2

Web Programming with Python and JavaScript

This project was to make a web chat app app using Websockets. 

application.py - This holds all the python/Flask information for the server back end. The app routes direct the users to the desired pages as well as 
allowing them to create their usernames, logging in and logging out. The socketio routes take the information sent to the server from the javascript,
processes it and then sends the information back to the clients browser where it is then emitted to where it needs to be shown on the page. usernames,
messages, and channels are all stored as global variables so as to not need a database to store all the information. 


helpers.py - this python file contains the login required functions which allows only people who have signed in to see messages and create channels/

templates - This folder contains the templates I have used for the base of the web app. The templates are channel.html, error.html, index.html, layout.html,
login.html. I have a layout template which I have used to create the base detail of each page such as the nav bar and then used jinja2 to extend the layout 
to the other templates. 

static - Within the static folder I have three files, channel.js, index.js, and styles.css. The index.js file has the JavaScript used on the main page of the 
site, it stops the user from being able to submit the create channel form while it is empty. It also redirects the user to the last channel they were on if they
closed the browser while in one. channel.js has the JavaScript which has the websocket which emits user events to the server so that the information can be 
processed and sent back. Styles.css is my style sheet for the webapp. 

Users will be shown the signin pag if they haven't been on the site before. If the username has been taken the user will be shown an error page saying so. Once they
have chosen their user name they will be taken to the main page where they will find a list of channels and a form where they will be able create their own channel.
If a channel name is already in use they will be shown an error page. If the user clicks on a channel they will be taken to the channel page where a message will be
be displayed saying their username and that they have entered the channel. On this page they will be able to send messages to other users in the channel. The messages
provide the timestamp and the username of the person who has sent the message.  They will also be able to leave the channel which will prompt another message telling 
the other users that they have left since this information will be stored in the local storage of the users browser. 

Once the chat has reached 100 messages the earliest message will be deleted. If the user closes the browser while they are in a channel, when they next go to the site
they will be re-directed to the same channel. 

If the user goes the /api/channel/<channel> they will be shown all the messages which have been sent in a JSON format. 