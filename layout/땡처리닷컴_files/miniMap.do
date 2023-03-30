//document.write('				<ul class="menuList">					<li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "https", true)+'/member/login.do?fwd=aHR0cHM6Ly93d3cudHRhbmcuY29tL3Byb2R1Y3QvcGtnL3RoZW1lTGlzdC5kbz90aGVtZUtpbmQ9VVJHRU5UJm1ham9yQ2F0ZWdvcnlDZD1DMDAx">로그인</a></li>					<li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "https", true)+'/member/login.do">비회원예약확인</a></li>					<li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "https", true)+'/member/join.do">회원가입</a></li>				   <li class="more customer">						<a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/index.do" class="arr">고객센터</a>						<div class="submenu">							<ul>							   <li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/bbs/noticeList.do">공지사항</a></li>							   <li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/bbs/faqList.do">자주하는질문</a></li>							   <li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/bbs/qaList.do">질문과답변</a></li>							   <li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/group/orderList.do">단체견적신청</a></li>						   </ul>						</div>					</li>					<!--<li class="benefit"><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/etc/benefit.do">쿠폰/결제혜택</a></li>-->			   </ul>');
$("#id_ttang_header_mini_map").append('				<ul class="menuList">					<li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "https", true)+'/member/login.do?fwd=aHR0cHM6Ly93d3cudHRhbmcuY29tL3Byb2R1Y3QvcGtnL3RoZW1lTGlzdC5kbz90aGVtZUtpbmQ9VVJHRU5UJm1ham9yQ2F0ZWdvcnlDZD1DMDAx">로그인</a></li>					<li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "https", true)+'/member/login.do">비회원예약확인</a></li>					<li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "https", true)+'/member/join.do">회원가입</a></li>				   <li class="more customer">						<a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/index.do" class="arr">고객센터</a>						<div class="submenu">							<ul>							   <li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/bbs/noticeList.do">공지사항</a></li>							   <li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/bbs/faqList.do">자주하는질문</a></li>							   <li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/bbs/qaList.do">질문과답변</a></li>							   <li><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/help/group/orderList.do">단체견적신청</a></li>						   </ul>						</div>					</li>					<!--<li class="benefit"><a href="'+__072_PROTOCOL_REPLACE(v_072_domain_name, "http", true)+'/etc/benefit.do">쿠폰/결제혜택</a></li>-->			   </ul>');
	
/* 공통 > utility menu */ 
$(function(){
	$(".ttangHeader .util .more").mouseover(function(){	
		$(this).addClass("on");
	});
	$(".ttangHeader .util .more ").mouseout(function(){
		$(this).removeClass("on");
	});	 
});

function USR_SET_BOOKMARK()
{
	var title = "땡처리닷컴";
	var url = "http://www.ttang.com";
	
	 if(window.external && ('AddFavorite' in window.external)) { // IE Favorite
	 	window.external.AddFavorite(url,title); 
	 }else{
	 	alert("Ctrl+D 키를 누르시면 즐겨찾기에 추가하실수  있습니다.");
	 }
}
function USR_LAYER_POPUP(v_url, v_width, v_hight)
{
	$('.layerWrapLoad').html(""); //기존의 컨텐츠 내용을 지운다.
	$('.layerWrapLoad').bPopup({
		content:'iframe',
		loadUrl:v_url,
		iframeAttr:'scrolling="yes" frameborder="0" style="width:'+v_width+'px;height:'+v_hight+'px; overflow-x:hidden; "',
		scrollBar :false
	});
} <!-- 메인컨텐츠 영역 --> 