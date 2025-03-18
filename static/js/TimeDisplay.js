!(function() {
    var id_hours = document.getElementById('hours');
    var id_minutes = document.getElementById('minutes');
    var id_seconds = document.getElementById('seconds');

    var intival = setInterval(function() {
        const now = new Date();

        const hours = ('0' + now.getHours()).slice(-2);
        const minutes = ('0' + now.getMinutes()).slice(-2);
        const seconds = ('0' + now.getSeconds()).slice(-2);

        id_hours.innerText = hours;
        id_minutes.innerText = minutes;
        id_seconds.innerText = seconds;
    }, 10);
})();