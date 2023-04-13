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

/*parsed HTML*/
$(function(){
	$(".maxheight").each(function(){
		$(this).contents().wrapAll("<div class='box_inner'></div>");
	})
	$(".maxheight2").each(function(){
		$(this).contents().wrapAll("<div class='box_inner'></div>");
	})
    $(".maxheight3").each(function(){
		$(this).contents().wrapAll("<div class='box_inner'></div>");
	})


})
/*add event*/
$(window).bind("resize", height_handler).bind("load", height_handler)
function height_handler(){
	if($(window).width()>465){
		$(".maxheight").equalHeights();
	}else{
		$(".maxheight").equalHeights();
	}
	if($(window).width()>740){
		$(".maxheight2").equalHeights();
	}else{
		$(".maxheight2").equalHeights();
	}
    if($(window).width()>740){
		$(".maxheight3").equalHeights();
	}else{
		$(".maxheight3").equalHeights();
	}

}
/*glob function*/
(function($){
	$.fn.equalHeights=function(minHeight,maxHeight){
		tallest=(minHeight)?minHeight:0;
		this.each(function(){
			if($(">.box_inner", this).outerHeight()>tallest){
				tallest=$(">.box_inner", this).outerHeight()
			}
		});
		if((maxHeight)&&tallest>maxHeight) tallest=maxHeight;
		return this.each(function(){$(this).height(tallest)})
	}
})(jQuery)


}
/*
     FILE ARCHIVED ON 04:02:40 Jan 18, 2019 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:07:26 Apr 13, 2023.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  captures_list: 146.842
  exclusion.robots: 0.088
  exclusion.robots.policy: 0.077
  RedisCDXSource: 16.728
  esindex: 0.009
  LoadShardBlock: 109.059 (3)
  PetaboxLoader3.datanode: 124.843 (5)
  load_resource: 166.076 (2)
  PetaboxLoader3.resolve: 81.335 (2)
*/