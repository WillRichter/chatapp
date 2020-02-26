    document.addEventListener('DOMContentLoaded', () => {


            // If the user has closed browser ona channel, they will be redirected to that channel
            if (localStorage.getItem('last_channel')) {
                let channel = localStorage.getItem('last_channel');
                window.location.replace('/channel/' + channel);
            } 



        // By default, submit button is disabled
        document.querySelector('#submit').disabled = true;

        // Enable button only if there is text in the input field
        document.querySelector('#channel_name').onkeyup = () => {
            if (document.querySelector('#channel_name').value.length > 0)
                document.querySelector('#submit').disabled = false;
            else
                // Disable button again after submit
                document.querySelector('#submit').disabled = true;
        };
        // Stop form from submitting
        return false; 


    });



