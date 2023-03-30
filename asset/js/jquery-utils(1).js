/*********************************************
* 파일명: jquery-utils.js
* 기  능: JQUERY의 기능들을 유틸리티화 한다.
* 만든이: 이진환
* 날  짜: 2012-02-29
**********************************************/
// 0. 기본 오브젝트 변수
var objInfo	= new Object();
objInfo.jqueryAjax = new jqueryAjax(); //Ajax 관련 오브젝트
objInfo.jqueryUI = new jqueryUI(); //UI 관련 오브젝트
objInfo.jqueryCal = new jqueryCal(); //달력관련 오브젝트
objInfo.jqueryCommon = new jqueryCommon(); //공통 관련 오브젝트
objInfo.jqueryLoading = new jqueryLoading(); //로딩 관련 오브젝트
objInfo.webStorage = new webStorage(); //웹스토리지관련
objInfo.jqueryPopup = new jqueryPopup(); //팝업 오브젝트

/**
 * 공통 관련함수
 */
function jqueryCommon(){}
/*
 * 폼을 초기화한다.
 * 
 *@param 폼ID
 */ 
jqueryCommon.prototype.clearForm = function ( form ) {
    $(':input', form).each(function() {
        var type = this.type;
        var tag = this.tagName.toLowerCase(); // normalize case
        if (type == 'hidden' || type == 'text' || type == 'password' || tag == 'textarea')
            this.value = "";
        else if (type == 'checkbox' || type == 'radio')
            this.checked = false;
        else if (tag == 'select')
            this.selectedIndex = -1;
    });
};
jqueryCommon.prototype.accessLog = function(channelCode, accessGubun, cityCode, prodId) {
    $.ajax({    		
		 url: v_072_domain_name == null ? "" : v_072_domain_name + "/common/accessLog.do"
		,type:"POST"
		,dataType:"jsonp"
	    ,data:{
	  		 channelCode : channelCode
	 		,accessGubun : accessGubun
	 		,cityCode : cityCode
	 		,prodId : prodId
    	}
	    //통신을 시작할때 처리
		,beforeSend:function(){
		}
		//통신성공시 처리
		,success:function(args){
		}
		//통신이 완료된 후 처리
		,complete:function(){
		}
		//통신에러발생시 처리
		,error:function(request,status,error){
		}
    });
};
jqueryCommon.prototype.setCookie = function ( name, value, expires ) {
	var v_cookie_info = name + "=" + escape(value) + ";";
    v_cookie_info += " path=/;";
    v_cookie_info += (expires == null ? "" : " expires=" + expires.toGMTString());
    document.cookie = v_cookie_info;
};
jqueryCommon.prototype.getCookie = function ( Name ) {
	var search = Name + "="
    if (document.cookie.length > 0) { // DmE00! <3A$5G>n @V4Y8i
        offset = document.cookie.indexOf(search)
        if (offset != -1) { // DmE00! A8@gGO8i
            offset += search.length
            // set index of beginning of value
            end = document.cookie.indexOf(";", offset)
            // DmE0 0*@G 86Av87 @'D! @N5&=: 9xH# <3A$
            if (end == -1)
                end = document.cookie.length
            return unescape(document.cookie.substring(offset, end))
        }
    }
    return "";
};

/**
 * 달력관련함수
 */
function jqueryCal() { }
jqueryCal.prototype.layer_id = "";
jqueryCal.prototype.to_yyyymmdd;
jqueryCal.prototype.arr_holiday = []; 
jqueryCal.prototype.arr_week = new Array("일", "월", "화", "수", "목", "금", "토");
jqueryCal.prototype.arr_month = new Array(0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
jqueryCal.prototype.selectedDate = "";
jqueryCal.prototype.ret_object;
jqueryCal.prototype.callbackMethod = "";
jqueryCal.prototype.init = function ( objThis) {
	this.layer_id = this.layer_id + " ";

	$(this.layer_id).show();
    $(this.layer_id).offset({ top: (Number(objThis.offset().top) + Number(objThis.attr("top"))), left: (Number(objThis.offset().left) + Number(objThis.attr("left"))) });
    
    //cal setting
    var to_date = this.getDateObj(this.to_yyyymmdd);
    var to_yyyy = to_date.getFullYear();
    var to_mm = to_date.getMonth() + 1;
    
    this.setting_cal('init', to_yyyy, to_mm);
};
jqueryCal.prototype.setting_cal = function (mode, p_yyyy, p_mm ) {
    if ((p_yyyy % 4 == 0 && p_yyyy % 100) != 0 || p_yyyy % 400 == 0) { this.arr_month[2] = 29; } else { this.arr_month[2] = 28; } //2월달 표시

    //해당월의 첫날이 몇째주인지를 가져온다.
    var p_date = new Date(p_yyyy, p_mm - 1, 1);
    var p_day = p_date.getDay(); //0(일),1(월),2(화),3(수),4(목),5(금),6(토)

    //이전달
    var pre_date = new Date(p_date.getFullYear(), p_date.getMonth() - 1, 1);
    var pre_yyyy = pre_date.getFullYear();
    var pre_mm = pre_date.getMonth() + 1;

    //다음달
    var next_date = new Date(p_date.getFullYear(), p_date.getMonth() + 1, 1);
    var next_yyyy = next_date.getFullYear();
    var next_mm = next_date.getMonth() + 1;

    //화면에 노출
    var __html__ = "", v_cal_form_id = this.layer_id + "#id_cal_from_list";
    __html__ += "<div class=\"headerW\">";
    __html__ += "	<a href=\"javascript:;\" onclick=\"objInfo.jqueryCal.setting_cal('pre_view', " + pre_yyyy + "," + pre_mm + ");\" class=\"btnLeft\"><img src=\"/images/contents/util_calender_btn_left.png\" alt=\"\"></a>";
    __html__ += "	<a href=\"javascript:;\" onclick=\"$('"+v_cal_form_id+"').show();\" class=\"list\">" + p_yyyy + ". " + p_mm + "</a>";
    __html__ += "	<a href=\"javascript:;\" onclick=\"objInfo.jqueryCal.setting_cal('next_view', " + next_yyyy + "," + next_mm + ");\" class=\"btnRight\"><img src=\"/images/contents/util_calender_btn_right.png\" alt=\"\"></a>";
    __html__ += "	<div id=\"id_cal_from_list\" class=\"listCont\" style=\"display:none;\">";
    __html__ += "		<ul>";
    var temp_to_date = new Date();
    for(var i =0; i<12; i++)
	{
    	var temp_date = new Date(temp_to_date.getFullYear(), temp_to_date.getMonth() + i, 1);
        var temp_yyyy = temp_date.getFullYear();
        var temp_mm = temp_date.getMonth() + 1;
        var temp_date_view = temp_yyyy + "." + ((temp_mm<10) ? "0" + temp_mm : temp_mm);
    	
        __html__ += "		<li>";
        __html__ += "			<a href=\"#javascript:;\" onclick=\"objInfo.jqueryCal.setting_cal('next_view', " + temp_yyyy + "," + temp_mm + "); $('#id_cal_from_list').hide();\">"+temp_date_view+"</a>";
        __html__ += "		</li>";	
	}
    __html__ += "		</ul>";
    __html__ += "	</div>";
    __html__ += "</div>";
    __html__ += "<table class=\"tbl_cal\">";
    __html__ += "    <caption>달력</caption>";
    __html__ += "    <thead>";
    __html__ += "    <tr>";
    __html__ += "	    <th scope=\"col\" class=\"sun\">SUN</th>";
    __html__ += "	    <th scope=\"col\">MON</th>";
    __html__ += "	    <th scope=\"col\">TUE</th>";
    __html__ += "	    <th scope=\"col\">WED</th>";
    __html__ += "	    <th scope=\"col\">THU</th>";
    __html__ += "	    <th scope=\"col\">FRI</th>";
    __html__ += "	    <th scope=\"col\" class=\"sat\">SAT</th>";
    __html__ += "    </tr>";
    __html__ += "    </thead>";
    __html__ += "    <tbody id=\"id_cal_base_dd\">" + this.get_date_html(p_yyyy, p_mm, p_day) + "</tbody>";
    __html__ += "</table> ";

    $(this.layer_id + "#id_cal_base").html("");
    $(this.layer_id + "#id_cal_base").html(__html__);

    //이벤트등록
    $(this.layer_id + "#id_cal_base_dd tr td").click(function() {
        var select_date = $(this).attr("date");
 
        if (select_date != null) {
        	objInfo.jqueryCal.selectedDate = select_date;
        	$.globalEval(objInfo.jqueryCal.callbackMethod);
        	$(objInfo.jqueryCal.layer_id).hide();
        }
    });
    
    //holiday setting!
    var p_yyyymm = p_yyyy + "" + (p_mm<10?"0"+p_mm: p_mm);
    this.set_holiday_html(this.layer_id + "#id_cal_base_holiday", p_yyyymm);
};
jqueryCal.prototype.get_date_html = function(p_yyyy, p_mm, p_day) {
    var __html__ = "";
    {
        var increase = 0; dd = 1;
        for (var i = 0; i < 7 * 6; i++) {
        	var inc_style = "";
        	if(increase % 7 == 0) inc_style = "sun"; //일요일
        	if(increase % 7 == 6) inc_style = "sat"; //토요일
        	
            if (increase % 7 == 0) __html__ += "<tr>";
            {
                if (i < p_day || dd > this.arr_month[p_mm]) {
                    __html__ += "<td>&nbsp;</td>";
                } else {

                    var p_yyyymmdd = Number(p_yyyy + "" + (10 > p_mm ? "0" + p_mm : p_mm) + "" + (10 > dd ? "0" + dd : dd));
                    var class_name = "";

                    //디폴트 날짜를 세팅한다.
                    if (this.to_yyyymmdd == p_yyyymmdd) {
                        class_name = "today";
                    }
                    
                    //공유일인지를 체크한다.
                    if(this.is_holiday(p_yyyymmdd)) inc_style = "sun"; //공휴일

                	__html__ += "<td class=\"" + class_name + "\" date=\"" + (p_yyyy + "." + (10 > p_mm ? "0" + p_mm : p_mm) + "." + (10 > dd ? "0" + dd : dd)) + "\">";
                    __html__ += "<a href=\"javascript:;\" class=\""+ inc_style +"\">" + (10 > dd ? "0" + dd : dd) + "</a>";
                	__html__ += "</td>";

                    dd++;
                }
            }
            if (increase % 7 == 6) __html__ += "</tr>";
            increase++;
        }
    }
    return __html__;
};
jqueryCal.prototype.is_holiday = function (p_yyyymmdd) {
    var is_holiday = false;
	$.each(this.arr_holiday, function (index, value) {
		if(value.holiday==p_yyyymmdd){
			is_holiday = true;
		}
	});
	return is_holiday;
};
jqueryCal.prototype.set_holiday_html = function (p_layout_id, p_yyyymm) {
    var __html__ = "";
	$.each(this.arr_holiday, function (index, value) {
		if(value.yyyymm==p_yyyymm){
			__html__ += "<li><em>"+value.dd+"일 </em>"+value.title+"</li>";
		}
	});

    //view setting
	$(p_layout_id).html(__html__);
};
//날짜오브젝트를 리턴한다.
jqueryCal.prototype.getDateObj = function(p_yyyymmdd) {
    var yyyy = p_yyyymmdd.substring(0, 4);
    var mm = p_yyyymmdd.substring(4, 6);
    var dd = p_yyyymmdd.substring(6, 8);
    return new Date(yyyy, mm - 1, dd);
};

/**
 * UI 관련함수
 */
function jqueryUI() { }
/*
* spinner를 설정합니다. (/js/spin.min.js => http://fgnass.github.io/spin.js/)
*
* 
* @param 구분 : true 인 경우 보여줌, false인 경우 숨김
*/
jqueryUI.prototype.spinnerObj; //스핀객체
jqueryUI.prototype.spinnerOpt = {
    lines: 7, // The number of lines to draw
    length: 3, // The length of each line
    width: 3, // The line thickness
    radius: 3, // The radius of the inner circle
    corners: 1, // Corner roundness (0..1)
    rotate: 0, // The rotation offset
    direction: 1, // 1: clockwise, -1: counterclockwise
    color: '#000', // #rgb or #rrggbb or array of colors
    speed: 1, // Rounds per second
    trail: 60, // Afterglow percentage
    shadow: false, // Whether to render a shadow
    hwaccel: false, // Whether to use hardware acceleration
    className: 'spinner', // The CSS class to assign to the spinner
    zIndex: 2e9, // The z-index (defaults to 2000000000)
    top: 'auto', // Top position relative to parent in px
    left: 'auto' // Left position relative to parent in px
};
jqueryUI.prototype.spinner = function(mode, argID, v_lines, v_radius) {
    this.spinnerOpt['lines'] = v_lines == null ? 7 : v_lines;
    this.spinnerOpt['radius'] = v_radius == null ? 3 : v_radius;

    //if (this.spinnerObj == null) {
    var target = document.getElementById(argID);
    this.spinnerObj = new Spinner(this.spinnerOpt).spin(target);
    target.appendChild(this.spinnerObj.el);
    //}

    if (mode) {
        $("#" + argID).show();
    } else {
        $("#" + argID).hide();
        //this.spinnerObj.stop();
    }
};

/**
 * Ajax 호출함수..
 */
function jqueryAjax(){}
jqueryAjax.prototype.method = "POST"; // "POST" or "GET"
jqueryAjax.prototype.async = false;
jqueryAjax.prototype.url = "";
jqueryAjax.prototype.dataType = "json"; //전송받을 데이터 타입 : xml, html, script, json, jsonp, text ( 미지정시 자동판단 )
jqueryAjax.prototype.formName = "";
jqueryAjax.prototype.contentType = "application/x-www-form-urlencoded; charset=UTF-8";
jqueryAjax.prototype.resultData;
jqueryAjax.prototype.isCallback = true; 
jqueryAjax.prototype.callback = "";  
jqueryAjax.prototype.callbackMethod = "AJAX_CALLBACK(objInfo.jqueryAjax.callback, objInfo.jqueryAjax.resultData);";

jqueryAjax.prototype.init = function () {
	this.method = "POST"; // "POST" or "GET"
	this.async = false;
	this.url = "";
	this.dataType = "json"; //전송받을 데이터 타입 : xml, html, script, json, jsonp, text ( 미지정시 자동판단 )
	this.formName = "";
	this.contentType = "application/x-www-form-urlencoded; charset=UTF-8";
	this.resultData;
	this.isCallback = true; 
	this.callback = "";  
	this.callbackMethod = "AJAX_CALLBACK(objInfo.jqueryAjax.callback, objInfo.jqueryAjax.resultData);";
};

//설정된 값을 이용하여, 통신을 한다.
jqueryAjax.prototype.send = function ( method ) {
	this.method = method;
	this.isCallback = (this.callback == "" ? false : true);
	
	var url = this.url;
	var async = this.async;
	var dataType = this.dataType;
	var formName = this.formName;
	var contentType = this.contentType;
	
	switch(method){
		case "MULTIPART": 
			$("#"+formName+"").ajaxForm(
					{url:url
				    ,async:async
					//,dataType: dataType
					,contentType:contentType
					
					//통신을 시작할때 처리
					,beforeSend:function(){
						objInfo.jqueryAjax.result("beforeSend");
					}
					//통신성공시 처리
					,success:function(args){
						objInfo.jqueryAjax.result("success", args );
					}
					//통신이 완료된 후 처리
					,complete:function(){
						objInfo.jqueryAjax.result("complete");
					}
					//통신에러발생시 처리
					,error:function(request,status,error){
						objInfo.jqueryAjax.result("error", error );
					}
				}
			);
			var frm = $("#"+formName+"");
			frm.attr('action', url);
			frm.submit();
			break;
		case "GET":
			$.ajax(
					{url:url
					,type:method
				    ,async: async
					,dataType: "text"
					,data: formName //formName.serialize()
					,contentType:contentType //"application/x-www-form-urlencoded; charset=UTF-8"
	
					//통신을 시작할때 처리
					,beforeSend:function(){
						objInfo.jqueryAjax.result("beforeSend");
					}
					//통신성공시 처리
					,success:function(args){
						objInfo.jqueryAjax.result("success", args );
					}
					//통신이 완료된 후 처리
					,complete:function(){
						objInfo.jqueryAjax.result("complete");
					}
					//통신에러발생시 처리
					,error:function(request,status,error){
						objInfo.jqueryAjax.result("error", error );
					}
				}
			);
			break;
		case "POST":
			$.post( url
				   ,formName //formName.serialize()
				   ,function(data){
						objInfo.jqueryAjax.result("success", data );
					}
					//,dataType
			);
			break;
	} 

	return false;
};
//통신완료된 데이터를 처리하는 부문
jqueryAjax.prototype.result = function(trans, args) {
    if (args == null) return;
    //if (args == "undefined") return;

    switch (trans) {
        case "beforeSend": break;
        case "complete": break;
        case "success": 
            if ("json" == this.dataType) {
                this.parseJSON(args);
            } else if ("xml" == this.dataType) {
                this.parseXML(args);
            } else {
                /*-- HEAD data S--*/
                var rphead = new Array();
                rphead[0] = new Array();
                rphead[0]["error"] = false;
                /*-- HEAD data E--*/

                /*-- RESULT data S--*/
                var rpdata = args;
                /*-- RESULT data E--*/

                this.resultData = new Array();
                this.resultData[0] = rphead;
                this.resultData[1] = rpdata;

                //if (this.isCallback) AJAX_CALLBACK(this.callback, this.resultData);
                if (this.isCallback)  $.globalEval(this.callbackMethod);
            }
            break;
        case "error":
            alert("error:" + args);
            //this.resultData = args;
            break;
    }
};
//통신완료된 데이터가 JSON일 경우 데이터를 재가공하여, 리턴한다.
jqueryAjax.prototype.parseJSON = function(jsonDoc) {
    var json_rdata = eval(jsonDoc);

    /*-- HEAD data S--*/
    var rphead = new Array();
    rphead[0] = new Array();
    rphead[0]["error"] = false;
    /*-- HEAD data E--*/

    /*-- RESULT data S--*/
    var rpdata;
    if (json_rdata == null) {
        rpdata = new Array();
    } else {
        if (json_rdata.length == null) {
            rpdata = new Array();
            rpdata[0] = new Array();
            rpdata[0] = json_rdata;
        } else {
            rpdata = json_rdata;
        }
    }
    /*-- RESULT data E--*/

    this.resultData = new Array();
    this.resultData[0] = rphead;
    this.resultData[1] = rpdata;

    //if (this.isCallback) AJAX_CALLBACK(this.callback, this.resultData);
    if (this.isCallback)  $.globalEval(this.callbackMethod);
};
//통신완료된 데이터가 XML일 경우 데이터를 재가공하여, 리턴한다.
jqueryAjax.prototype.parseXML = function(xmldata) {
    /*-- HEAD data S--*/
    var rphead = new Array();
    rphead[0] = new Array();
    rphead[0]["error"] = $(xmldata).find("HEAD").find("error").text();
    rphead[0]["message"] = $(xmldata).find("HEAD").find("message").text();
    /*-- HEAD data E--*/

    /*-- RESULT data S--*/
    var rpdata = new Array();
    {
        $(xmldata).find("RECORD").each(function(index) {
            rpdata[index] = new Array();
            $(this).children().each(function(j){
                rpdata[index][this.tagName] = $(this).text();
            });
        });
    }
    /*-- RESULT data E--*/

    this.resultData = new Array();
    this.resultData[0] = rphead;
    this.resultData[1] = rpdata;

    //if (this.isCallback) AJAX_CALLBACK(this.callback, this.resultData);
    if (this.isCallback)  $.globalEval(this.callbackMethod);
}

/**
 * 검색로딩 관련함수
 */
function jqueryLoading(){}
jqueryLoading.prototype.search = function (v_mode) {
	switch(v_mode)
	{
		case true:
			$("#id_loading_comm").show();
			$("#id_loading_comm_dimm").show();
			
			$('body').addClass('bodyHide');
			var winH =  $(window).height()
			var lyLoadH = $("#id_loading_comm").height();
			if(lyLoadH > winH){
				$("#id_loading_comm").addClass('poTop');
			}
			else{
				$("#id_loading_comm").removeClass('poTop');
			}
			/* animate : 1회 or 무한루프 미정 / 작업시점에서 확인요망 */
			this.realtimeAnimate();
			//$("#" + v_layer_id + " .progress .ico_plane" ).animate({left: "100%"},{duration:10000, easing:"easeInOutQuart"});
			//$("#" + v_layer_id + " .progress .ing" ).animate({width: "100%"},{duration:10000, easing:"easeInOutQuart"});
			break;
		case false:
			$("#id_loading_comm").hide();
			$("#id_loading_comm_dimm").hide();

			$('body').removeClass('bodyHide');
			$("#id_loading_comm").removeClass('poTop');
			break;
	}
};
jqueryLoading.prototype.realtimeAnimate = function (){
	$("#id_loading_comm .progress .ico_plane").attr("style","left:0%");
	$("#id_loading_comm .progress .ing").attr("style","left:0%");
	
	$("#id_loading_comm .progress .ico_plane" ).animate({left: "100%"}, 5000, 'linear', function(){
		objInfo.jqueryLoading.realtimeAnimate();
    });
	$("#id_loading_comm .ing" ).animate({width: "100%"}, 5000, 'linear', function(){
		objInfo.jqueryLoading.realtimeAnimate();
    });
};

/**
 * 웹스토리지 관련함수
 *   - 도메인마다 따로 생성된다.
 *   - local : 영구적, session : 윈도우객체와 동일
 *   - 메소드 
 *        length, key(index), getItem(key), setItem(key,data), removeItem(key), clear()
 *   - KEY => 채널코드 + "_" + 구분코드(FA,RSV)
 *   - VAL => json 구조체로 생성
 */
function webStorage() { }
webStorage.prototype.mode = "local"; //로컬:local, 세션:session
webStorage.prototype.isSupported = function() {
	return window.Storage?true:false;
};
webStorage.prototype.setCookie = function(v_channel, v_gubun, v_value) {
	if(!this.isSupported()) return;

	var v_key = v_channel+"_"+v_gubun;
	switch(this.mode)
	{
		case "local":
			localStorage[v_key] = v_value;
			break;
		case "session":
			sessionStorage[v_key] = v_value;
			break;
	}
};
webStorage.prototype.getCookie = function(v_channel, v_gubun) {
	if(!this.isSupported()) return;

	var v_key = v_channel+"_"+v_gubun;
	var v_value = "";
	
	switch(this.mode)
	{
		case "local":
			v_value = localStorage[v_key];
			break;
		case "session":
			v_value = sessionStorage[v_key];
			break;
	}
	return v_value == null ? "" : v_value;
};

/**
 * bPopup 호출
 */
function jqueryPopup(){}
jqueryPopup.prototype.open = function (loadUrl, options) {
	$('.layerWrapLoad').bPopup({
		content:'ajax',
		contentContainer:'.layerWrapLoad',
		loadUrl:loadUrl,
		follow:[false, true],
		modalClose: false
	});
};