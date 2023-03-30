/*********************************************
* 파일명: link.js
* 기  능: SNS링크관련 유틸리티
* 만든이: 이진환
* 날  짜: 2016-03-29
**********************************************/
// 0. 기본 오브젝트 변수
var linkObjInfo	= new Object();
linkObjInfo.shortUrl = new shortUrl();
linkObjInfo.facebook = new facebook();
linkObjInfo.twitter = new twitter();

/**
 * 단축URL관련
 */
function shortUrl(){}
shortUrl.prototype.url = "";
shortUrl.prototype.excute = function () 
{
	this.url = (this.url == null || this.url == "") ? window.location.href : this.url;
	
	var v_link_url = "";
	$.ajax({
		 url: "/common/shorturl.do"
		,type:"GET"
		,async:false
		,dataType:"text"
		,contentType:"application/x-www-form-urlencoded; charset=UTF-8" 
	    ,data:{
	    	url : this.url
	    }
		//통신성공시 처리
		,success:function(data){
			var json_rdata = eval(data);
			//v_link_url = json_rdata.url;
			v_link_url = json_rdata.result.url;
		}
		//통신에러발생시 처리
		,error:function(request,status,error){
			alert(status);
		}
   });	
	return v_link_url;
};

/**
 * 페이스북 연동
 */
function facebook(){}
facebook.prototype.excute = function (link_url) 
{
	linkObjInfo.shortUrl.url = link_url;
	this.link_url = linkObjInfo.shortUrl.excute();
	
	if($('head').find('meta[property^="og"]').size() == 0) {
		$('head').append('<meta property="og:type" content="website" />');
		$('head').append('<meta property="og:title" content="" />');
		$('head').append('<meta property="og:description" content="'+ this.link_url +'" />');
	}
	else {
		$('meta[property="og:type"]').attr("content", "website");
		$('meta[property="og:title"]').attr("content", "");
		$('meta[property="og:description"]').attr("content", this.link_url);
	}
	
    var url = "http://www.facebook.com/sharer.php?u="+ this.link_url;
    window.open(url, "_win_sns_pop", "width=640,height=380,lef=0,top=0,location=no,menubar=no,status=no,scrollbars=no,resizable=no,titlebar=no,toolbar=no");
};

/**
 * 트위터 연동
 */
function twitter(){}
twitter.prototype.excute = function (link_url) 
{
	linkObjInfo.shortUrl.url = link_url;
	this.link_url = linkObjInfo.shortUrl.excute();
	
	var url ="https://twitter.com/intent/tweet?text=&url="+ this.link_url;
    window.open(url, "_win_sns_pop", "width=640,height=380,lef=0,top=0,location=no,menubar=no,status=no,scrollbars=no,resizable=no,titlebar=no,toolbar=no");
};