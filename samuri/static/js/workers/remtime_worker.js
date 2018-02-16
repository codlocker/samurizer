let test_date, test_duration, rem_time;
self.addEventListener('message', function(event){
   let data = event.data;
   // console.log(typeof(data));
   test_date = data.test_date;
   test_duration = data.test_duration;
   get_time_difference();
});
function get_time_difference() {
    let date_now = new Date();
    let seconds = (date_now - test_date)/1000;
    // console.log(seconds, test_duration);
    if (seconds <= test_duration * 3600) {
        let remaining_time = test_duration * 3600 - seconds;
        let hrs = parseInt(remaining_time/3600);
        let mins = parseInt((remaining_time - hrs*3600) / 60);
        let secs = parseInt(remaining_time - hrs*3600 - mins*60);
        rem_time = `${hrs}:${mins}:${secs}`;
    } else {
        let hrs = parseInt(seconds / 3600);
        let mins = parseInt((seconds - hrs * 3600) / 60);
        let secs = parseInt(seconds - hrs * 3600 - mins * 60);
        rem_time = 0;
    }
    postMessage(rem_time);
    setTimeout("get_time_difference()",1000);
}
