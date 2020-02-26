document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on("connect", () => {

        // Tells server that user has joined
        socket.emit('joined');

        // Each button should emit a "submit message" event
        document.querySelector("#sendbutton").onclick = () => {

            // Get current time and send to server
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();

            // gets message from the user input and adds to variable
            let msg = document.getElementById("myMessage").value;

            // Sends server information via socket
            socket.emit("submit message", { "msg": msg, "timestamp": timestamp });

            // Resets input field
            document.getElementById("myMessage").value = "";
        };

        // Leave button emits a leave event
        document.querySelector('#leavebutton').onclick = () => {

            
            socket.emit('leave');
            localStorage.removeItem('last_channel');
            windows.location.replace('/');

        }

        // Logout button emits leave event also
        document.querySelector('#logout').onclick = () => {

            socket.emit('leave');
        }
    });


    // emits join or leave messages 
    socket.on('status', data => {

        // Broadcast message of joined user.
        let row = '<' + `${data.msg}` + '>'
        document.querySelector('#chat').value += row + '\n';

        //Save user current channel on localStorage
        localStorage.setItem('last_channel', data.channel)
    })


    // Emits messages 
    socket.on('announce message', data => {


        let row = '<' + `${data.timestamp}` + '> - ' + '[' + `${data.user}` + ']:  ' + `${data.msg}`

        document.querySelector('#chat').value += row + '\n';


    })

});