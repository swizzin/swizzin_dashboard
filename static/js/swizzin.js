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