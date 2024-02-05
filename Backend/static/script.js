//Auto-close alerts
document.addEventListener("DOMContentLoaded", function() {
    var element = document.querySelector(".alert");
    var bootstrap_alert = new bootstrap.Alert(element);
    const alert_timeout = setTimeout(close_alert, 2500)
    function close_alert() {
        bootstrap_alert.close();
    }
});

//The developer can set the date when the elections will conclude
var countDownDate = new Date("Feb 5, 2024 22:00:00").getTime();

var changeTimer = setInterval(function() {
    var now = new Date().getTime();
    var diff = countDownDate - now;

    var days = Math.floor(diff / (1000 * 60 * 60 * 24));
    var hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((diff % (1000 * 60)) / 1000);

    document.getElementById("days").innerHTML = days;
    document.getElementById("hours").innerHTML = hours;
    document.getElementById("minutes").innerHTML = minutes;
    document.getElementById("seconds").innerHTML = seconds;

    //When the countdown is completed, the winner page will be accessible
    //and users will no longer be able to vote
    if(diff < 0) {
        clearInterval(changeTimer);
        document.getElementById("timer").innerHTML = "Countdown completed."
        document.getElementById("timer").classList.add("h2");
        document.getElementById("winner").style.display = "block";
        document.getElementById("candidates").style.display = "none";
    } else{
        document.getElementById("winner").style.display = "none";
        document.getElementById("candidates").style.display = "block";
    }

}, 1000);




