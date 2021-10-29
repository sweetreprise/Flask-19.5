
let score = 0;
let timeleft = 60;
const words = [];

// submits ajax request to server with user submitted guess and provides
// some feedback to the user on the result's of their guess
$(document).ready(function() {
    $('form').on('submit', function(event) {

        $.ajax({
            data : {
                guess: $('#guess').val()
            },
            type : 'POST',
            url : '/process'
        })
        .done(function(data) {
            if (data.result === "ok" && words.indexOf(data.guess) === -1) {
                $('#success').text(`word added! '${data.guess}'`).show();
                $('#error').hide();
                $('#words').append(`<li>${data.guess}</li>`)

                words.push(data.guess);
                updateScore(data.guess_length);
            }
            else if(data.result === "not-on-board" || data.result === "not-word") {
                $('#error').text(`Sorry, '${data.guess}' is an invalid word!`).show();
                $('#success').hide();
            }
            else if(words.indexOf(data.guess) !== -1) {
                $('#error').text(`Sorry, '${data.guess}' has already been guessed!`).show();
                $('#success').hide();
            }
        });

        event.preventDefault();
        $('#guess').val("");

    });
});

// sends a request to show user's final score
function postScore() {

    $.ajax({
        data : JSON.stringify({ score: score }),
        type : 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        url : '/score'
    })
    .done(function(data) {
        if(data.brokeRecord) {
            $('#final-score').text(`Congrats! New record: ${score}`).show();
        }
        else {
            $('#final-score').text(`Final score: ${score}`).show();
        }
    });
}

// gives a 60 second countdown at the start of the game
let countdownID = setInterval(countdown, 1000);

function countdown() {
    timeleft--;
    $('#countdown').text(`Seconds left: ${timeleft}`);
    if(timeleft <= 0) {
        clearInterval(countdownID);
        $('form').hide();
        $('#current-score').hide();
        $('#countdown').text(`Time is up!`);
        $('#success').hide();
        $('#error').hide();
        $('#words').hide();
        postScore();
    }
}

// updates user's score based on length of guess
function updateScore(guess_length) {

    score += guess_length
    $('#current-score').text(`Current Score: ${score}`)
}


// restarts the setInterval countdown
// function restartCountdown() {
//     countdownID = setInterval(countdown, 1000);
// }


// click event for restart button; resets score and timer
// $('#restart').on('click', function(event) {
    
//     clearInterval(countdownID);
//     score = 0;
//     timeleft = 20;

    
//     $('#current-score').text(`Current Score: ${score}`).show();
//     $('#countdown').text(`Seconds left: ${timeleft}`);
//     $('#final-score').hide();
//     $('form').show();
    
//     restartCountdown();
// });





