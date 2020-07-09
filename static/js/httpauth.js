function getHTTPObject() {
    var xmlhttp = false;
    if (typeof XMLHttpRequest != 'undefined') {
            try {
                    xmlhttp = new XMLHttpRequest();
            } catch (e) {
                    xmlhttp = false;
            }
    } else {
    /*@cc_on
    @if (@_jscript_version >= 5)
        try {
            xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try {
                xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (E) {
                xmlhttp = false;
            }
        }
    @end @*/
}
    return xmlhttp;
}

function login()
{
var username = document.getElementById("basic-username").value;
var password = document.getElementById("basic-password").value;
var http = getHTTPObject();
    //var url = "http://" + username + ":" + password + "@" + this.action.substr(7);
    var url = "/";
http.open("get", url, false, username, password);
http.send("");
    if (http.status == 200) {
            document.location = url;
    } else {
    alert("Incorrect username and/or password!");
}
return false;
}

document.onkeypress = enter;
function enter(e) {
if (e.which == 13) { login(); }
}