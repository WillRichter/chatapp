import os, sys
from collections import deque
from datetime import datetime
from flask import Flask, session, render_template, flash, jsonify, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "pumpkin"
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
socketio = SocketIO(app)



# Keeps a list of users that have logged in
users = []


# Keeps a list of channels created by users
channels = []


# Create a dictonary to save channel messages to
channelMessages = dict()



# Loads index page showing lists of users and channels
@app.route("/", methods=['GET', 'POST'])
@login_required
def index():

    username = session["username"]

    return render_template("index.html", channels=channels, users=users, username=username)





# Saves username into global variable and logs in, redirects to index page
@app.route("/signin", methods=["GET","POST"])
def signin():

    # Takes username from input field and adds to variable
    username = request.form.get("username")

    if request.method == "POST":

        #Check to see if the field is empty
        if len(username) < 1 or username is '':
            return render_template("error.html", message = "please enter a username to continue")

        # Check to see if username is already in use
        if username in users:
            return render_template("error.html", message="Username Taken")

        # Appends username to users global variable
        users.append(username)

        # Stores username in session vairable
        session['username'] = username

        # Make session permanent
        session.permanent = True

        return redirect("/")

    else:
        return render_template("login.html")




# Logs user out
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    """ Logout user from list and delete cookie."""

    # Remove from list
    try:
        users.remove(session['username'])
    except ValueError:
        pass

    # Delete cookie
    session.clear()

    # Redirect to the index page
    return redirect("/")




@app.route("/create_channel", methods = ["GET", "POST"])
@login_required
def create_channel():

    # Take user channel name and make into variable
    newChannel = request.form.get("channel_name")
    
    if request.method =="POST":

        # Return error if channel form is empty
        if len(newChannel) < 1 or "":
            return render_template("error.html", message="please enter a name for new channel")

        # Return error if channel name is already taken
        elif newChannel in channels:
            return render_template("error.html", message="channel name already taken")

        # Append new channel to the global channel variable
        channels.append(newChannel)

        # Makes new channel messages a double ended queue to allow old messages be deleted from the beginning
        channelMessages[newChannel] = deque()

        return redirect("/channel/" + newChannel)

    else:
        return render_template("index.html", users=users, channels=channels)


@app.route("/channel/<channel>", methods=["GET", "POST"])
@login_required
def enter_channel(channel):

    #Saves current channels as session variable
    session['current_channel'] = channel


    return render_template("channel.html", channels=channels, messages=channelMessages[channel] )


# Provides channels messages in JSON format
@app.route("/api/channel/<channel>")
def api_chat(channel):

    # Creates a new list for channels 
    ChannelMessages = []

    # Loop through messages in channel and add to new list
    for messages in channelMessages[channel]:
        ChannelMessages.append(messages)


    # return new list in JSON
    return jsonify(ChannelMessages)



# Enters the user into the channel/room they selected
@socketio.on('joined', namespace='/')
def join():

    username = session.get('username')

    room = session.get('current_channel')

    join_room(room)

    # Emits to the room that a user has joined
    emit('status', {'userJoined' : session.get('username'), 'channel' : room, 'msg': session.get('username') + ' has entered the room'}, room=room, broadcast=True)




# Allows user to leave the channel/room they were in
@socketio.on('leave', namespace='/')
def leave():

    username = session.get('username')

    room = session.get('current_channel')

    leave_room(room)

    # Emits to the room that a user has left
    emit('status', {'userLeft' : session.get('username'), 'channel' : room, 'msg': session.get('username') + ' has left the room'}, room=room, broadcast=True)



# Takes user message from client browser and then broadcasts back to everyone in the room
@socketio.on('submit message', namespace='/')
def send_message(data):

    room = session.get('current_channel')
    msg = data["msg"]
    timestamp = data["timestamp"]

    # Deletes the earliest messages once amount surpasses 100
    if len(channelMessages[room]) > 100:
        channelMessages[room].pop(0)

    # Appends new messages to room dict
    channelMessages[room].append([timestamp, session.get('username'), msg])

    # Broadcasts messages to everyone in the room
    emit('announce message', {'user': session.get('username'), 'msg': msg, "timestamp":timestamp}, room=room, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
