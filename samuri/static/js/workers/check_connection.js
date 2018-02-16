function check_conn() {
    let res = navigator.onLine;
    postMessage(res);
    setTimeout('check_conn()', 500);
}
check_conn();