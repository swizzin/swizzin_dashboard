window.onload = function() {
  $.get('/stats/boot', function(data) {
    countUpFromTime(data, 'uptime');
  })
};
function countUpFromTime(countFrom, id) {
countFrom = new Date(countFrom).getTime();
var now = new Date(),
countFrom = new Date(countFrom),
timeDifference = (now - countFrom);

var secondsInADay = 60 * 60 * 1000 * 24,
secondsInAHour = 60 * 60 * 1000;

days = Math.floor(timeDifference / (secondsInADay) * 1);
hours = Math.floor((timeDifference % (secondsInADay)) / (secondsInAHour) * 1);
mins = Math.floor(((timeDifference % (secondsInADay)) % (secondsInAHour)) / (60 * 1000) * 1);
secs = Math.floor((((timeDifference % (secondsInADay)) % (secondsInAHour)) % (60 * 1000)) / 1000 * 1);

var idEl = document.getElementById(id);
idEl.getElementsByClassName('days')[0].innerHTML = days;
idEl.getElementsByClassName('hours')[0].innerHTML = hours;
idEl.getElementsByClassName('minutes')[0].innerHTML = mins;
idEl.getElementsByClassName('seconds')[0].innerHTML = secs;

clearTimeout(countUpFromTime.interval);
countUpFromTime.interval = setTimeout(function(){ countUpFromTime(countFrom, id); }, 1000);
}

$("#menu-toggle").click(function(e) {
e.preventDefault();
$("#wrapper").toggleClass("toggled");
});

function makePostRequest(url, data, callback) {
$.ajax({
  type: 'POST',
  url: url,
  data: data,
  contentType: "application/json",
  success: function (result) {
      if(typeof callback == 'function') {
        clearTimeout(timer);
        callback.call();
      }
  }
});
}

$(function(){
$("a[post=true]").each(function () {
    $(this).on('click', function () {
        makePostRequest(
            $(this).attr('phref'),
            $(this).attr('pdata'),
            appstatus
        );
    });
});
});

$(function(){
$("input[post=true]").each(function () {
    $(this).on('change', function () {
      var data = JSON.parse($(this).attr('pdata'));
      data.function = $(this).is(':checked') ? 'enable' : 'disable';
      data =  JSON.stringify(data)
        makePostRequest(
            $(this).attr('phref'),
            data,
            appstatus
        );
    });
});
});

$(document).ready(function(){
var protocol = window.location.protocol;
var socket = io.connect(protocol + '//' + document.domain + ':' + location.port + '/websocket');
socket.on('speed', function(result) {
  $('#current_rx').html(result.rx);
  $('#current_tx').html(result.tx)
  $('#current_interface').html(result.interface)
  return false;
});
socket.on('iowait', function(result) {
  $('#iowait-glance').html(result.iowait);
  return false;
});
});