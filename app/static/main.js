$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
}

$(document).ready(function() {

  // on form submission ...
  $('form').on('submit', function() {
    stock = $('input[name="stock"]').val();
    if(stock){
          $.get('/close/'+stock, {}, function(data1) {
            $('#close').html(data1);
            $.get('/obv/'+stock, {}, function(data2) {
                $('#obv').html(data2);
                $.get('/div/'+stock, {}, function(data3) {
                    $('#div').html(data3);
                },'html');
            },'html');
        },'html');
    }
  });
  var mystock = $.urlParam('stock');
  if(mystock == null) mystock = "A";
  if(mystock != 0){
   $('input[name=stock]').val(mystock);
  
    $.get('/close/'+mystock, {}, function(data1) {
        $('#close').html(data1);
        $.get('/obv/'+mystock, {}, function(data2) {
            $('#obv').html(data2);
            $.get('/div/'+mystock, {}, function(data3) {
                $('#div').html(data3);
            },'html');
        },'html');
    },'html');  
  }
  

});