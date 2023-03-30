/*********************************************************************************************************************************
* 파일명: jquery-utils.js
* 기  능: 유틸리티 기능
* 만든이: 김승환
* 날  짜: 2015-11-17
 *********************************************************************************************************************************/
// 기본 오브젝트 변수
var objUtils = new Object();

/**
 * 페이징 처리를 한 후 HTML 결과를 리턴한다.
 */
objUtils.getPageNavHtml = function(pageNav, eventFunc) {
	// 페이지 HTML
	var pageHTML = "";

	// 이전 버튼
	if(pageNav.PREV_LINK != 0) {
		pageHTML += "<a href=\"javascript:\" page=\"" + pageNav.PREV_LINK + "\" onclick=\"" + eventFunc + "\" class=\"btn btn_prev\"><span>Prev</span></a>\n";
	}
	
	// 첫 페이지
	if(pageNav.PAGE_SCALE < pageNav.PAGE) {
		pageHTML += "<a href=\"javascript:\" page=\"1\" onclick=\"" + eventFunc + "\" class=\"num\">1</a>\n";
		pageHTML += "<span class=\"num\">...</span>\n";
	}
	
	// 페이지 목록
	for(var i = 0; i < pageNav.PAGE_LINK.length; i++) {
		pageHTML += "<a href=\"javascript:\" page=\"" + pageNav.PAGE_LINK[i].value + "\" onclick=\"" + eventFunc + "\" class=\"num " + (pageNav.PAGE_LINK[i].value == pageNav.PAGE ? "on" : "") + "\">" + pageNav.PAGE_LINK[i].value + "</a>\n";
	}

	// 마지막 페이지 
	if(pageNav.PAGE < pageNav.totalPage && pageNav.NEXT_LINK != 0) {
		pageHTML += "<span class=\"num\">...</span>\n";
		pageHTML += "<a href=\"javascript:\" page=\"" + pageNav.totalPage +"\" onclick=\"" + eventFunc + "\" class=\"num\">" + pageNav.totalPage + "</a>\n";
	}
	
	// 다음 버튼
	if(pageNav.NEXT_LINK != 0) {
		pageHTML += "<a href=\"javascript:\" page=\"" + pageNav.NEXT_LINK + "\" onclick=\"" + eventFunc + "\" class=\"btn btn_next\"><span>Next</span></a>";
	}
	
	return pageHTML;
}