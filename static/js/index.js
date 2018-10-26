$(document).ready(function(){
 
  $('#btn').click(function(){
    
    $('#btn').addClass("hide");
    $('#carg').removeClass("hide");
    window.location.href = '/perfil/'+$('#nick').val();  
  })

  
});








