$(document).ready(function(){


  $('.sidenav').sidenav();


  $('#altAssassins').click(function(){
    
    $('#todos').addClass("hide");
    $('#magos').addClass("hide");
    $('#guerreiros').addClass("hide");
    $('#cacadores').addClass("hide");
    $('#assassinos').removeClass("hide");
    $('#guardioes').addClass("hide");
  })

  $('#altWarriors').click(function(){
    
    $('#todos').addClass("hide");
    $('#magos').addClass("hide");
    $('#guerreiros').removeClass("hide");
    $('#cacadores').addClass("hide");
    $('#assassinos').addClass("hide");
    $('#guardioes').addClass("hide");
  })

  $('#altMages').click(function(){
    
    $('#todos').addClass("hide");
    $('#magos').removeClass("hide");
    $('#guerreiros').addClass("hide");
    $('#cacadores').addClass("hide");
    $('#assassinos').addClass("hide");
    $('#guardioes').addClass("hide");
  })

  $('#altHunters').click(function(){
    
    $('#todos').addClass("hide");
    $('#magos').addClass("hide");
    $('#guerreiros').addClass("hide");
    $('#cacadores').removeClass("hide");
    $('#assassinos').addClass("hide");
    $('#guardioes').addClass("hide");
  })
  $('#altGuardians').click(function(){
    
    $('#todos').addClass("hide");
    $('#magos').addClass("hide");
    $('#guerreiros').addClass("hide");
    $('#cacadores').addClass("hide");
    $('#assassinos').addClass("hide");
    $('#guardioes').removeClass("hide");
  })
});



