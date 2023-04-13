var _____WB$wombat$assign$function_____ = function(name) {return (self._wb_wombat && self._wb_wombat.local_init && self._wb_wombat.local_init(name)) || self[name]; };
if (!self.__WB_pmw) { self.__WB_pmw = function(obj) { this.__WB_source = obj; return this; } }
{
  let window = _____WB$wombat$assign$function_____("window");
  let self = _____WB$wombat$assign$function_____("self");
  let document = _____WB$wombat$assign$function_____("document");
  let location = _____WB$wombat$assign$function_____("location");
  let top = _____WB$wombat$assign$function_____("top");
  let parent = _____WB$wombat$assign$function_____("parent");
  let frames = _____WB$wombat$assign$function_____("frames");
  let opener = _____WB$wombat$assign$function_____("opener");

/* panel */
include('jquery.cookie.js');
//----Include-Function----
function include(url){ 
  document.write('<script src="js/'+ url + '"></script>'); 
  return false ;
}
$(window).scroll(
    function(){
        if (
            $(this).scrollTop() > 0) {
                $("#advanced").css({position:'fixed'});
            }else{
                $("#advanced").css({position:'relative'});
            }
        }
);  
$(function(){
    var
        strCookies1 = $.cookie('panel1')
    ,   isAnimate = false
    ,   isOpen = false
    ;

    if(strCookies1==null){
        $.cookie('panel1', 'closed');
        strCookies1 = $.cookie('panel1');
        isOpen = false;
    }

    if(strCookies1=='opened'){
        $("#advanced").css({marginTop:'0px'}).removeClass('closed');
        isOpen = true;
        $('#stuck_container').trigger('rePosition', 50); //for sticky menu
    }else{
        $("#advanced").css({marginTop:'-50px'}).addClass('closed');
        isOpen = false;
        $('#stuck_container').trigger('rePosition', 0); //for sticky menu
    }

    $("#advanced .trigger").click(
        function(){
            if(!isOpen){
                $(this).find('strong').animate({opacity:0}).parent().parent('#advanced').removeClass('closed').animate({marginTop:'0px'}, 300);
                $.cookie('panel1','opened');
                strCookies1=$.cookie('panel1');

                isOpen = true;
                $('#stuck_container').trigger('rePosition', 50);
            }else{
                $(this).find('strong').animate({opacity:1}).parent().parent('#advanced').addClass('closed').animate({marginTop:'-50px'}, 300)
                $.cookie('panel1','closed');
                strCookies1=$.cookie('panel1');
                
                isOpen = false;
                $('#stuck_container').trigger('rePosition', 0); //for sticky menu
            }
        }
    )
});
/*--------- end panel *------------*/

//year sccript

var currentYear = (new Date).getFullYear();
$(document).ready(function() {
$("#copyright-year").text( (new Date).getFullYear() );
});


jQuery(function(){
      jQuery('.sf-menu').mobileMenu();
    })
$(function(){
// IPad/IPhone
  var viewportmeta = document.querySelector && document.querySelector('meta[name="viewport"]'),
    ua = navigator.userAgent,
 
    gestureStart = function () {
        viewportmeta.content = "width=device-width, minimum-scale=0.25, maximum-scale=1.6, initial-scale=1.0";
    },
 
    scaleFix = function () {
      if (viewportmeta && /iPhone|iPad/.test(ua) && !/Opera Mini/.test(ua)) {
        viewportmeta.content = "width=device-width, minimum-scale=1.0, maximum-scale=1.0";
        document.addEventListener("gesturestart", gestureStart, false);
      }
    };
scaleFix();

// Menu Android
if(window.orientation!=undefined){
 var regM = /ipod|ipad|iphone/gi,
  result = ua.match(regM)
 if(!result) {
  $('.sf-menu li').each(function(){

   if($(">ul", this)[0]){
    $(">a", this).toggle(
     function(){
      return false;
     },
     function(){
      window.location.href = $(this).attr("href");
     }
    );
   } 
  })
 }
}
});
/* ------ fi fixed position on Android -----*/
var ua=navigator.userAgent.toLocaleLowerCase(),
 regV = /ipod|ipad|iphone/gi,
 result = ua.match(regV),
 userScale="";
if(!result){
 userScale=",user-scalable=0"
}
document.write('<meta name="viewport" content="width=device-width,initial-scale=1.0'+userScale+'">')
/*--------------*/

}
/*
     FILE ARCHIVED ON 15:29:24 Jan 11, 2019 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:07:31 Apr 13, 2023.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  captures_list: 538.684
  exclusion.robots: 0.088
  exclusion.robots.policy: 0.078
  cdx.remote: 0.054
  esindex: 0.007
  LoadShardBlock: 508.396 (3)
  PetaboxLoader3.datanode: 209.363 (5)
  load_resource: 500.809 (2)
  PetaboxLoader3.resolve: 344.008 (2)
*/