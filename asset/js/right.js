/*
 * http://127.0.0.1:8080/asset/js/include/header.js?v=20151002
 */
document.write('<script type="text/javascript" src="'+v_072_domain_name+'/asset/js/favorite.js?v=20160427"></script>');
document.write('<script type="text/javascript" src="'+v_072_domain_name+'/common/right.do"></script>');

function __GET_FAVORITE_COUNT__()
{
	var arr_json = favoriteObjInfo.favorite.listAll();
	return Number(arr_json.length).toLocaleString('en');
}
function __GET_FAVORITE_HTML__(page_no)
{
	var _html_ = ""
	
	var arr_json = favoriteObjInfo.favorite.listAll();	
	var v_tot_count = arr_json.length;
	
	if( v_tot_count <= 0){
		_html_ = ""
		_html_+="<div class=\"recentList\">";
		_html_+="	<ul>";
		_html_+="		<li class=\"noResult\" style=\"display:\"><p>최근 본 상품이 <br>없습니다.</p></li>";
		_html_+="	</ul>";
		_html_+="</div>";
		$("#id_right_favority_lists").html(_html_);
		return false; 
	}
	
	var v_scale = 3;
	var v_total_page = (v_tot_count%v_scale) > 0 ? parseInt((v_tot_count/v_scale))  + 1 :     parseInt((v_tot_count/v_scale));
	var v_page_start = ((page_no - 1) * v_scale) + 1;
	var v_page_end = page_no * v_scale;
	
	var increase = 1;
	_html_ = "";
	_html_+="<div class=\"recentList\">";
	_html_+="<ul>";
	$.each(arr_json, function(i, data){
		if(v_page_start<=increase && increase<=v_page_end)
		{
			_html_+="	<li>";
			_html_+="		<a href=\""+data.link_url+"\" class=\"unit\">";
			_html_+="			<img src=\""+data.img_url+"\" alt=\"\">";
			_html_+="			<div class=\"hoverInfo\">";
			_html_+="				<p class=\"tit shortCut\">"+data.title+"</p>";
			_html_+="				<p class=\"price\">"+ (parseInt(data.price) < 0 ? "-" : Number(data.price).toLocaleString('en') + "원") +"</p>";
			_html_+="			</div>";
			_html_+="		</a>";
			//_html_+="		<a href=\"#none\" class=\"close txtImg\">close</a>";
			_html_+="	</li>";
		}
		increase++;
	});
	_html_+="</ul>";
	_html_+="</div>";
	
	_html_+="<div class=\"btnArea\">";
	_html_+="<a href=\"javascript:;\" onclick=\"__GET_FAVORITE_HTML__("+(page_no<=1 ? 1 : page_no-1)+")\" class=\"btn prev txtImg\">이전</a>";
	_html_+="<p><em>"+page_no+"</em> / "+v_total_page+"</p>";
	_html_+="<a href=\"javascript:;\" onclick=\"__GET_FAVORITE_HTML__("+(page_no<v_total_page ? page_no + 1 : page_no)+")\" class=\"btn next txtImg\">다음</a>";
	_html_+="</div>";
	
	$("#id_right_favority_lists").html(_html_);
	__SET_FAVORITE_EVENT();
}
function __SET_FAVORITE_EVENT()
{
	$(".recentList li").mouseover(function(){
		$(this).addClass('on');
	});
	$(".recentList li").mouseout(function(){
		$(this).removeClass('on');
	});
}

/* 공통 > footer > quickRight > 토글  */
function __SET_QUICK_RIGHT_BTN__(args)
{
	var is_cookie_open = objInfo.jqueryCommon.getCookie("cookie_quick_right_open");
	is_cookie_open = (is_cookie_open==""  || is_cookie_open=="true") ? true : false;
	
	switch(args){
		case "init":
			if(is_cookie_open){
				$('#quickRightCont').animate({'right':'0px'},'fast');
				if(!$('#quickRightBtn').hasClass('on')) $('#quickRightBtn').addClass('on');
			}else{
				$('#quickRightCont').animate({'right':'-120px'},'1500');
				if($('#quickRightBtn').hasClass('on')) $('#quickRightBtn').removeClass('on');		
			}
			break;
		case "click":
			var v_open = "true";
			if($('#quickRightBtn').hasClass('on')) //화면닫기
			{
				$('#quickRightCont').animate({'right':'-120px'},'1500');
				$('#quickRightBtn').removeClass('on');

				v_open = "false";
			}else{ //화면열기
				$('#quickRightCont').animate({'right':'0px'},'fast');
				$('#quickRightBtn').addClass('on');
			}	
			
			//쿠키세팅
			var expdate = new Date();
            expdate.setTime(expdate.getTime() + 1000 * 3600 * 24 * 30); // 30일
            objInfo.jqueryCommon.setCookie("cookie_quick_right_open", v_open, expdate);
			break;
	}
}

/* 공통 > footer > quickRight > top 클릭  */
function quickRight() {
	var item = $('.quickRight');
		var headerH = $('.ttangHeader').height()-$('.gnb').height(); 
		var scroll = $(window).scrollTop();
		$(item).css({'top':headerH}); 		
	if(headerH > scroll){
		$(item).css({'top':headerH-scroll});			
	}
	else {
		$(item).css({'top':0});
		if (headerH < scroll) {
			$(item).css({'top':0});				
		}
		else {
		}
	}
}
$(window).load(function() { quickRight(); });
$(window).resize(function() { quickRight() });
$(window).scroll(function() { quickRight(); });
