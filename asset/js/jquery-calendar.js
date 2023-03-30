/*********************************************************************************************************************************
* 파일명: jquery-calendar.js
* 기  능: 달력작성
* 만든이: 김승환
* 날  짜: 2015-11-17
 *********************************************************************************************************************************/
// 기본 오브젝트 변수
var objCal = new Object();

objCal.arr_week = new Array("일", "월", "화", "수", "목", "금", "토");			// 요일


/**
 * Type 별 달력 인스턴스를 생성한다.
 */
objCal.getCalendar = function(calendarType) {
	if(calendarType == 1) {
		return new calendarType_1();
		
	} else if(calendarType == 2) {
		return new calendarType_2();
		
	} else if(calendarType == 3) {
		return new calendarType_3();
	}

	return null;
}

/**
 * 날짜 오브젝트를 리턴한다.
 */
objCal.getDateObj = function(p_yyyymmdd) {
    var yyyy = p_yyyymmdd.substring(0, 4);
    var mm = p_yyyymmdd.substring(4, 6);
    var dd = p_yyyymmdd.substring(6, 8);
    
    return new Date(yyyy, mm - 1, dd);
};

/**
 * 날짜 오브젝트로 스트링을 리턴한다.
 */
objCal.getDateString = function(p_date, format) {
    if(p_date==null) return null;

	var p_yyyy = p_date.getFullYear();
	var p_mm = Number(p_date.getMonth() + 1);
	p_mm = p_mm < 10 ? "0" + p_mm : p_mm;
	var p_dd = p_date.getDate();
	p_dd = p_dd < 10 ? "0" + p_dd : p_dd;

	var ret_value;
	switch(format) {
	    case "yyyymm": ret_value = p_yyyy + "" + p_mm; break;
	    case "yyyymmdd": ret_value = p_yyyy + "" + p_mm + "" + p_dd; break;
		case "yyyy-mm-dd": ret_value = p_yyyy + "-" + p_mm + "-" + p_dd; break;
	}
	return ret_value;
};

/**
 * 날짜의 요일을 리턴한다.
 */
objCal.getWeek = function(p_yyyymmdd) {
    return this.arr_week[this.getDateObj(p_yyyymmdd).getDay()];
};

/**
 * n 문자열이 digits 자리수보다 작은 경우 앞에 0 을 채운다.
 */
objCal.fillZeros = function(n, digits) {
	  var zero = "";
	  n = n.toString();
	  
	  if (n.length < digits) {
	    for (i = 0; i < digits - n.length; i++) {
	      zero += "0";
	    }
	  }
	  
	  return zero + n;
}


/*********************************************************************************************************************************
 * 타입 1 달력 (GNB 검색 영역)
 *********************************************************************************************************************************/
/**
 * 생성자
 */
function calendarType_1() {};

calendarType_1.prototype.positionId;																							// 달력이 삽입될 id 명
calendarType_1.prototype.instanceName;																						// 해당 인스턴스의 변수 명
calendarType_1.prototype.callback;																								// 날짜 선택, 해제시 콜백 함수

calendarType_1.prototype.arr_month;																							// 월별 일수
calendarType_1.prototype.arr_selected_date;																					// 선택된 날짜

calendarType_1.prototype.maxSelectableCount = 5;																		// 선택 가능한 최대 개수
calendarType_1.prototype.selectableClass;																						// 선택, 해제 가능한 일자 css 명
calendarType_1.prototype.disabledClass = "disa";																			// 선택 불가 일자 css 명
calendarType_1.prototype.enabledClass = "";																					// 선택 가능 일자 css 명
calendarType_1.prototype.selectedClass = "on onfrst onlast";															// 선택된 일자 css 명
calendarType_1.prototype.todayClass = "today";																			// 오늘 일자 css 명


/**
 * 달력 초기화 함수
 * 
 * @parameter 달력이 삽입될 id 명
 * @parameter 해당 인스턴스의 변수 명
 * @parameter 날짜 선택, 해제시 콜백 함수
 */
calendarType_1.prototype.init = function(positionId, instanceName, selectedDates, callback) {
	this.positionId = $("#" + positionId);
	this.instanceName = instanceName;
	this.callback = callback;
	
	this.selectableClass = positionId + "_selectable";

	this.arr_month = new Array(0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	this.arr_selected_date = new Array();
	
	if(selectedDates != null && selectedDates != "") {
		var arrSelectedDate = selectedDates.split(",");
		for(var i = 0; i < arrSelectedDate.length; i++) {
			this.arr_selected_date.push(arrSelectedDate[i]);
		}
	}
	
	this.excute();
}

/**
 * 달력을 실행한다.
 */
calendarType_1.prototype.excute = function() {
	// 현재 년월
    var to_date = new Date();
    var to_yyyy = to_date.getFullYear();
    var to_mm = to_date.getMonth() + 1;
    // ----------
    
    this.displayCalender(to_yyyy, to_mm);
}

/**
 * 해당 월을 기준으로 달력을 출력한다.
 */
calendarType_1.prototype.displayCalender = function(p_yyyy, p_mm) {
	
	// 첫번째 달력 구성
	var cal1Html = this.makeCalender(1, p_yyyy, p_mm);

	// 두번째 달력 구성
	var nextCalDate = new Date(p_yyyy, p_mm, 1);
	var cal2Html = this.makeCalender(2, nextCalDate.getFullYear(), nextCalDate.getMonth() + 1);
	
	// 전체 달력 화면 출력
    var __html__ = "";
    __html__ += "<p class=\"tit\">출발날짜<span class=\"abR\">출발일은 5개까지 선택 가능합니다.</span></p>";
    __html__ += "<div class=\"clear\">";
    
    __html__ += cal1Html;
    __html__ += cal2Html;

    __html__ += "</div>";	 
    
    this.positionId.html("");
    this.positionId.html(__html__);
    
    // 날짜 클릭시 선택, 해제 등의 이벤트를 등록한다.
    this.addEvent(this);
}

/**
 * 해당 월의 달력 화면을 만든다.
 */
calendarType_1.prototype.makeCalender = function(order, p_yyyy, p_mm) {
	// 2월 윤달인 경우 일 수 변경
    if ((p_yyyy % 4 == 0 && p_yyyy % 100) != 0 || p_yyyy % 400 == 0) { 
    	this.arr_month[2] = 29; 
    } else {
    	this.arr_month[2] = 28; 
	}

    // 해당 월 1일의 요일 정보(0:일, 1:월, 2:화, 3:수, 4:목, 5:금, 6:토)를 가져온다.
    var p_date = new Date(p_yyyy, p_mm - 1, 1);
    var p_week = p_date.getDay();

    // 달력 날짜 영역의 HTML 을 만든다.
    var dayHtml = "";									// 달력 날짜 영역 HTML 
    var increase = 0; 										// 주 단위 증가값
    var dd = 1;												// 일 단위 증가값
    
    var __html__ = "";
    __html__ += "<div class=\"dev " + (order == 1 ? "fl" : "fr") + "\">";
    __html__ += "<div class=\"unit_calender\">";
    __html__ += "	<div class=\"headerW\">";

    // 이전 버튼 표시
    if(order == 1) {
        var pre_date = new Date(p_date.getFullYear(), p_date.getMonth() - 1, 1);
        var pre_yyyy = pre_date.getFullYear();
        var pre_mm = pre_date.getMonth() + 1;

    	__html__ += "		<a href=\"#none\" class=\"btnLeft\" onclick=\"" + this.instanceName + ".displayCalender(" + pre_yyyy + "," + pre_mm + "); return false;\"><img src=\"/images/contents/util_calender2_btn_left.png\" alt=\"\"></a>";
    }
    
    // 년월 표시
    __html__ += "		<span class=\"list\">" +  p_yyyy + "." + p_mm + "</span>";
    
    // 다음 버튼 표시
    if(order == 2) {
    	var next_date = new Date(p_date.getFullYear(), p_date.getMonth(), 1);
        var next_yyyy = next_date.getFullYear();
        var next_mm = next_date.getMonth() + 1;
        
    	__html__ += "    	<a href=\"#\" class=\"btnRight\" onclick=\"" + this.instanceName + ".displayCalender(" + next_yyyy + "," + next_mm + "); return false;\"><img src=\"/images/contents/util_calender2_btn_right.png\" alt=\"\"></a>";
    }
    
    __html__ += "	</div>";
    __html__ += "	<table class=\"tbl_cal\">";
    __html__ += "		<caption>달력</caption>";
    __html__ += "		<thead>";
    __html__ += "		<tr>";
    __html__ += "			<th scope=\"col\" class=\"sun\">SUN</th>";
    __html__ += "			<th scope=\"col\">MON</th>";
    __html__ += "			<th scope=\"col\">TUE</th>";
    __html__ += "			<th scope=\"col\">WED</th>";
    __html__ += "			<th scope=\"col\">THU</th>";
    __html__ += "			<th scope=\"col\">FRI</th>";
    __html__ += "			<th scope=\"col\" class=\"sat\">SAT</th>";
    __html__ += "		</tr>";
    __html__ += "		</thead>";
    __html__ += "		<tbody>";
    
    for (var i = 0; i < 7 * 6; i++) {
    	// 달력 한줄 시작
    	dayHtml += (increase % 7 == 0) ? "<tr>" : "";

    	// 달력에서 이전달 또는 다음달의 날짜인 경우 공백 처리
        if (i < p_week || dd > this.arr_month[p_mm]) {
        	dayHtml += "<td>&nbsp;</td>";
        	
        // 해당 월의 달력 날짜 처리
        } else {
            var p_yyyymmdd = p_yyyy + objCal.fillZeros(p_mm, 2) + objCal.fillZeros(dd, 2);

            var curDate = new Date();																						
            var cDateTime = objCal.getDateObj(objCal.getDateString(curDate, "yyyymmdd")).getTime();			// 현재날짜
            var pDateTime = objCal.getDateObj(p_yyyymmdd).getTime();														// 달력날짜

            // 선택 가능한 날짜인지 여부
            var isEnabled = (pDateTime > cDateTime) ? true : false;
            
            // 선택 가능 또는 불가능 표시 
            var class_name = isEnabled ? this.enabledClass : this.disabledClass;
            
            // 토,일요일 표시
            if(isEnabled && increase % 7 == 0) {
            	class_name = "sun";
            } else if(isEnabled && increase % 7 == 6) {
            	class_name = "sat";
            }
            
            // 달력의 날짜가 오늘인 경우 표시
            class_name = (p_yyyymmdd == objCal.getDateString(curDate, "yyyymmdd")) ? this.todayClass : class_name;
            	
            // 선택된 날짜인 경우 처리
            var idx = $.inArray(p_yyyymmdd, this.arr_selected_date);
            if(idx >= 0) {
            	if(isEnabled == false) {
            		// 선택 불가능한 날짜인 경우 선택된 날짜 목록에서 삭제 (For 선택후 자정이 지난 경우 처리)
            		this.arr_selected_date.splice(idx, 1);
            	} else {
            		// 선택된 상태로 표시
                	class_name = this.selectedClass;
            	}
            }

            // 선택 가능한 날짜인 경우 링크 테그 추가
            if(isEnabled) {
            	dayHtml += "<td class=\"" + class_name + " " + this.selectableClass + "\" date=\"" + p_yyyymmdd + "\"><a href=\"#none\">" +  objCal.fillZeros(dd, 2) + "</a></td>";
            } else {
            	dayHtml += "<td class=\"" + class_name + "\" date=\"" + p_yyyymmdd + "\"><a href=\"#none\">" + objCal.fillZeros(dd, 2) + "</a></td>";
            }            
            
            // 다음 날짜로 이동
            dd++;				
        }

        // 달력 한줄 종료 (다음주로 이동)
        dayHtml += (increase % 7 == 6) ? "</tr>" : "";					
        increase++;
    }

    __html__ += dayHtml;
    
    __html__ += "			</tbody>";
    __html__ += "		</table>";	
    __html__ += "	</div>";	
    __html__ += "</div>";	    
    return __html__;
}

/**
 * 날짜 클릭시 선택, 해제 등의 이벤트 처리
 */
calendarType_1.prototype.addEvent = function(p) {
	$("." + p.selectableClass).click(function() {
	    var selectDate = $(this).attr("date");
	    var bSelected = false; 
	    	
	    if (selectDate != null) {
	    	var idx = $.inArray(selectDate, p.arr_selected_date);
	    	if(idx >= 0) {
	    		// 날짜 선택 해제 처리
	    		p.arr_selected_date.splice(idx, 1);
	    		if(selectDate == objCal.getDateString(new Date(), "yyyymmdd")) {
	    			// 날짜가 오늘인 경우 별도 표시
	    			$(this).attr("class", p.todayClass + " " + p.selectableClass);
	    		} else {
	    			$(this).attr("class", p.enabledClass + " " + p.selectableClass);
	    		}
	    	} else {
	    		if(p.arr_selected_date.length >= p.maxSelectableCount) {
	    			// 최대 선택 가능한 개수를 초과하는 경우 메시지 출력
	    			alert("출발일은 " + p.arr_selected_date.length + "개 까지 선택 가능합니다.");
	    			return;
	    		} else {
		    		// 날짜 선택 처리
		    		bSelected = true;
		    		
		    		p.arr_selected_date.push(selectDate);
		    		$(this).attr("class", p.selectedClass + " " + p.selectableClass); 
	    		}
	    	}
	    }
	    
		// 콜백 함수를 호출한다.
		if(p.callback != null) {
			p.callback(selectDate, bSelected);
		}
	});
}

/**
 * 선택된 날짜들의 배열을 조회한다.
 */
calendarType_1.prototype.getSelectedDate = function() {
	return this.arr_selected_date;
}











/*********************************************************************************************************************************
 * 타입 2 달력 (출발상품 검색 영역)
 *********************************************************************************************************************************/
/**
 * 생성자
 */
function calendarType_2() {}

calendarType_2.prototype.positionId;																							// 달력이 삽입될 id 명
calendarType_2.prototype.instanceName;																						// 해당 인스턴스의 변수 명
calendarType_2.prototype.curDate;																								// 현재 날짜 (yyyyMMdd)
calendarType_2.prototype.arrYm = new Array();																				// 표시할 모든 년월 배열
calendarType_2.prototype.dayCallback;																							// 날짜 선택, 해제시 콜백 함수
calendarType_2.prototype.monthCallback;																					// 달 선택시 콜백 함수

calendarType_2.prototype.arr_month;																							// 월별 일수
calendarType_2.prototype.arr_selected_date;																					// 선택된 날짜들
calendarType_2.prototype.selectedYearMonth;																				// 선택된 년월
calendarType_2.prototype.navMonthIdx = 0;																					// 네비게이션 첫 년월의 인덱스 번호 

calendarType_2.prototype.maxSelectableCount = 3;																		// 선택 가능한 최대 개수
calendarType_2.prototype.selectableClass;																						// 선택, 해제 가능한 일자 css 명
calendarType_2.prototype.disabledClass = "disa";																			// 선택 불가 일자 css 명
calendarType_2.prototype.enabledClass = "";																					// 선택 가능 일자 css 명
calendarType_2.prototype.selectedClass = "on onfrst onlast";															// 선택된 일자 css 명
calendarType_2.prototype.todayClass = "today";																			// 오늘 일자 css 명


/**
 * 달력 초기화 함수
 * 
 * @parameter positionId 달력이 삽입될 id 명
 * @parameter instanceName 해당 인스턴스의 변수 명
 * @parameter curDate 현재 날짜(yyyyMMdd)
 * @parameter ymList 표시할 모든 년월 목록 스트링 (yyyyMM,yyyyMM ...)
 * @parameter dayCallback 날짜 선택, 해제시 콜백 함수
 * @parameter monthCallback 달 선택시 콜백 함수
 */
calendarType_2.prototype.init = function(positionId, instanceName, curDate, ymList, dayCallback, monthCallback) {
	this.positionId = $("#" + positionId);
	this.instanceName = instanceName;
	this.curDate = objCal.getDateObj(curDate);
	this.arrYm = ymList.split(",");
	this.dayCallback = dayCallback;
	this.monthCallback = monthCallback;
	
	this.selectableClass = positionId + "_selectable";
	
	this.arr_month = new Array(0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	this.arr_selected_date = new Array();
	this.selectedYearMonth = "";
	
	this.excute();
}

/**
 * 달력을 실행한다.
 */
calendarType_2.prototype.excute = function() {
	// 가장 빠른 출발 년월
    var to_yyyy = Number(this.arrYm[0].substring(0, 4)); 
    var to_mm = Number(this.arrYm[0].substring(4, 6)); 
    
    // 선택된 년월
    this.selectedYearMonth = this.arrYm[0];
    
    this.displayCalender(to_yyyy, to_mm, 0, false);
}

/**
 * 해당 월을 기준으로 달력을 출력한다.
 * 
 * @parameter p_yyyy 하단 달력의 년도
 * @parameter p_mm 하단 달력의 월
 * @parameter c_yyyy 상단 년월 네비게이션의 첫번째 년도
 * @parameter c_yyyy 상단 년월 네비게이션의 첫번째 월
 * @parameter bClearSelectDays 선택된 날짜들을 초기화할지 여부
 */
calendarType_2.prototype.displayCalender = function(p_yyyy, p_mm, monthIdx, bClearSelectDays) {
	
	// 이동된 네비게이션 첫 년월의 인덱스
	this.navMonthIdx = monthIdx;
	
	// 네비게이션의 달을 선택한 경우 
	if(bClearSelectDays) {
		// 기 선택된 날짜들을 초기화
		this.arr_selected_date = new Array();
		
	    // 선택된 년월
	    this.selectedYearMonth = p_yyyy + objCal.fillZeros(p_mm, 2);
	    
		// callback 함수를 호출
		if(this.monthCallback != null) {
			this.monthCallback(p_yyyy + objCal.fillZeros(p_mm, 2));
		}
	}
	
	// 전체 달력 구성
	var calHtml = this.makeCalender(p_yyyy, p_mm);

    this.positionId.html("");
    this.positionId.html(calHtml);
    
    // 날짜 클릭시 선택, 해제 등의 이벤트를 등록한다.
    this.addEvent(this);
}

/**
 * 해당 월을 기준으로 달력 화면을 만든다.
 */
calendarType_2.prototype.makeCalender = function(p_yyyy, p_mm, monthIdx) {
	// 2월 윤달인 경우 일 수 변경
    if ((p_yyyy % 4 == 0 && p_yyyy % 100) != 0 || p_yyyy % 400 == 0) { 
    	this.arr_month[2] = 29; 
    } else {
    	this.arr_month[2] = 28; 
	}

    // 해당 월 1일의 요일 정보(0:일, 1:월, 2:화, 3:수, 4:목, 5:금, 6:토)를 가져온다.
    var p_date = new Date(p_yyyy, p_mm - 1, 1);
    var p_week = p_date.getDay();

    // 달력 전체 HTML 을 만든다.
    var __html__ = "";
    
    // 오늘 날짜
    __html__ += "<p class=\"today\">" + this.curDate.getFullYear() + "년 " + objCal.fillZeros("" + (this.curDate.getMonth() + 1), 2)+ "월 " + objCal.fillZeros("" +this.curDate.getDate(), 2)+ "일(" + objCal.arr_week[this.curDate.getDay()] + ")</p>";

    // 월 영역 표시
    __html__ += "<div class=\"month\">";

    // 이전달 버튼 표시 
    if(this.navMonthIdx > 0) {
    	__html__ += "    	<a href=\"#none\" class=\"btn btn_prev txtImg\" onclick=\"" + this.instanceName + ".displayCalender(" + p_yyyy + "," + p_mm + "," + (this.navMonthIdx - 1) + ", false); return false;\">이전달</a>";
    }
    
    // 년월 표시
    __html__ += "<ul>";
    for(var i = 0; i < 6 && (this.navMonthIdx + i <= this.arrYm.length - 1); i++) {
    	var linkDate = this.arrYm[this.navMonthIdx + i];
        var linkYYYY = linkDate.substring(0, 4);
        var linkMM = linkDate.substring(4, 6);

        if(Number(linkYYYY) == p_yyyy && Number(linkMM) == p_mm) {
        	__html__ += "    <li><a href=\"#none\" class=\"on\" onclick=\"return false;\"><span>" +  linkMM + "월</span>" + linkYYYY + "년</a></li>";
        } else {
        	__html__ += "    <li><a href=\"#none\" onclick=\"" + this.instanceName + ".displayCalender(" + Number(linkYYYY) + "," + Number(linkMM) + "," + this.navMonthIdx + ", true); return false;\"><span>" +  linkMM + "월</span>" + linkYYYY + "년</a></li>";
        }
	}
    __html__ += "</ul>";
    
    // 다음 버튼 표시
    if(this.navMonthIdx + 6 < this.arrYm.length) {
    	__html__ += "    	<a href=\"#none\" class=\"btn btn_next txtImg\" onclick=\"" + this.instanceName + ".displayCalender(" + p_yyyy + "," + p_mm + "," + (this.navMonthIdx + 1) + ", false); return false;\">다음달</a>";
    }
    
    __html__ += "</div> ";
    
    __html__ += "<div class=\"comment\">※ 출발일은 <span class=\"fc_red1 bd\">3개까지 선택</span>할 수 있습니다.(원하시는 날짜를 클릭하면 선택 또는 취소됩니다.)</div>";
    
    // 달력 요일과 날짜 영역의 HTML 을 만든다.
    var weekHtml = "";															// 달력 요일 영역 HTML
    var dayHtml = "";															// 달력 날짜 영역 HTML 
    var dd = 1;																		// 일 단위 증가값
    
    // 요일 영역 HTML
    for (var i = 0; i < this.arr_month[Number(p_mm)]; i++) {
    	var idxWeek = (p_week++) % 7;
    	if(idxWeek == 0) {
    		weekHtml += "<th scope=\"col\" class=\"sun\">";
    	} else if(idxWeek == 6) {
    		weekHtml += "<th scope=\"col\" class=\"sat\">";
    	} else {
    		weekHtml += "<th scope=\"col\">";
    	}
    	weekHtml += objCal.arr_week[idxWeek] + "</th>"
    }
    weekHtml += "<th scope=\"col\">&nbsp;</th>";
    
    // 날짜 영역 HTML
    for (var i = 0; i < this.arr_month[Number(p_mm)]; i++) {    
        var p_yyyymmdd = p_yyyy + objCal.fillZeros(p_mm, 2) + objCal.fillZeros(dd, 2);
																				
        var cDateTime = objCal.getDateObj(objCal.getDateString(this.curDate, "yyyymmdd")).getTime();			// 현재날짜
        var pDateTime = objCal.getDateObj(p_yyyymmdd).getTime();															// 달력날짜

        // 선택 가능한 날짜인지 여부
        var isEnabled = (pDateTime > cDateTime) ? true : false;
        
        // 선택 가능 또는 불가능 표시 
        var class_name = isEnabled ? this.enabledClass : this.disabledClass;
        
        // 달력의 날짜가 오늘인 경우 표시
        class_name = (p_yyyymmdd == objCal.getDateString(this.curDate, "yyyymmdd")) ? this.todayClass : class_name;
        	
        // 선택된 날짜인 경우 처리
        var idx = $.inArray(p_yyyymmdd, this.arr_selected_date);
        if(idx >= 0) {
    		// 선택된 상태로 표시
        	class_name = this.selectedClass;
        }

        // 선택 가능한 날짜인 경우 링크 테그 추가
        if(isEnabled) {
        	dayHtml += "<td class=\"" + class_name + " " + this.selectableClass + "\" date=\"" + p_yyyymmdd + "\"><a href=\"#none\">" + dd + "</a></td>";
        } else {
        	dayHtml += "<td class=\"" + class_name + "\" date=\"" + p_yyyymmdd + "\"><a href=\"#none\">" + dd + "</a></td>";
        }

        // 다음 날짜로 이동
        dd++;

    }
    dayHtml += "<td class=\"disa\"><span>&nbsp;</span></td>";

    // 달력 요일, 날짜 표시
    __html__ += "<div class=\"day\">";
    __html__ += "	<table class=\"tbl_cal_dayWide\">";
    __html__ += "		<caption>달력</caption>";
    __html__ += "		<thead>";
    __html__ += "			<tr>";
    __html__ += weekHtml;
    __html__ += "			</tr>";
    __html__ += "		</thead>";
    __html__ += "		<tbody>";
    __html__ += "			<tr>";   
    __html__ += dayHtml;
    __html__ += "			</tr>";       
    __html__ += "		</tbody>";    
    __html__ += "	</table>";
    __html__ += "</div> ";

    return __html__;
}


/**
 * 날짜 클릭시 선택, 해제 등의 이벤트 처리
 */
calendarType_2.prototype.addEvent = function(p) {
	$("." + p.selectableClass).click(function() {
	    var selectDate = $(this).attr("date");
	    var bSelected = false; 
	    	
	    if (selectDate != null) {
	    	var idx = $.inArray(selectDate, p.arr_selected_date);
	    	if(idx >= 0) {
	    		// 날짜 선택 해제 처리
	    		p.arr_selected_date.splice(idx, 1);
	    		if(selectDate == objCal.getDateString(p.curDate, "yyyymmdd")) {
	    			// 날짜가 오늘인 경우 별도 표시
	    			$(this).attr("class", p.todayClass + " " + p.selectableClass);
	    		} else {
	    			$(this).attr("class", p.enabledClass + " " + p.selectableClass);
	    		}
	    	} else {
	    		if(p.arr_selected_date.length >= p.maxSelectableCount) {
	    			// 최대 선택 가능한 개수를 초과하는 경우 메시지 출력
	    			alert("출발일은 " + p.arr_selected_date.length + "개 까지 선택 가능합니다.");
	    			return;
	    		} else {
		    		// 날짜 선택 처리
		    		bSelected = true;
		    		
		    		p.arr_selected_date.push(selectDate);
		    		$(this).attr("class", p.selectedClass + " " + p.selectableClass); 
	    		}
	    	}
	    }
	    
		// 콜백 함수를 호출한다.
		if(p.dayCallback != null) {
			p.dayCallback(selectDate, bSelected);
		}
	});
}

/**
 * 선택된 날짜들의 배열을 조회한다.
 */
calendarType_2.prototype.getSelectedDates = function() {
	var selectedDates = "";
	for(var i = 0; i < this.arr_selected_date.length; i++) {
		selectedDates += (i == 0) ? this.arr_selected_date[i] : "," + this.arr_selected_date[i];
	}
	return selectedDates;
}

/**
 * 선택된 년월을 조회한다.
 */
calendarType_2.prototype.getSelectedYearMonth = function() {
	return this.selectedYearMonth;
}







/*********************************************************************************************************************************
 * 타입 3 달력  (긴급 모객/확정 테마 검색 영역)
 *********************************************************************************************************************************/
/**
 * 생성자
 */
function calendarType_3() {}

calendarType_3.prototype.positionId;																							// 달력이 삽입될 id 명
calendarType_3.prototype.instanceName;																						// 해당 인스턴스의 변수 명
calendarType_3.prototype.curDate;																								// 현재 날짜 (yyyyMMdd)
calendarType_3.prototype.selectedDate;																						// 선택된 날짜 (yyyyMMdd)
calendarType_3.prototype.holidayList;																							// 휴일 전체 목록
calendarType_3.prototype.isSelectableFromToday;																			// 오늘부터 선택가능한지 여부
calendarType_3.prototype.callback;																								// 날짜 선택시 콜백 함수

calendarType_3.prototype.selectableClass;																						// 선택, 해제 가능한 일자 css 명
calendarType_3.prototype.disabledClass = "disa";																			// 선택 불가 일자 css 명
calendarType_3.prototype.enabledClass = "";																					// 선택 가능 일자 css 명
calendarType_3.prototype.selectedClass = "on onfrst onlast";															// 선택된 일자 css 명
calendarType_3.prototype.todayClass = "today";																			// 오늘 일자 css 명

calendarType_3.prototype.arr_month;																							// 월별 일수


/**
 * 달력 초기화 함수
 * 
 * @parameter 달력이 삽입될 id 명
 * @parameter 해당 인스턴스의 변수 명
 * @parameter 현재 날짜
 * @parameter 선택된 날짜
 * @parameter 휴일 전체 목록 
 * @parameter 날짜 선택, 해제시 콜백 함수
 */
calendarType_3.prototype.init = function(positionId, instanceName, curDate, selectedDate, holidayList, isSelectableFromToday, callback) {
	this.positionId = $("#" + positionId);
	this.instanceName = instanceName;
	this.curDate = objCal.getDateObj(curDate);
	this.selectedDate = selectedDate;
	this.holidayList = holidayList;
	this.isSelectableFromToday = isSelectableFromToday;		
	this.callback = callback;
	
	this.selectableClass = positionId + "_selectable";

	this.arr_month = new Array(0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	
	this.positionId.hide();
	
	this.excute();
}

/**
 * 달력을 실행한다.
 */
calendarType_3.prototype.excute = function() {
	// 현재 년월
    var to_yyyy = this.curDate.getFullYear();
    var to_mm = this.curDate.getMonth() + 1;
    
    // 선택된 날짜가 있는 경우 현재 년월을 대체
    if(this.selectedDate != "") {
        to_yyyy = Number(this.selectedDate.substring(0, 4));
        to_mm = Number(this.selectedDate.substring(4, 6));
    }
    
    this.displayCalender(to_yyyy, to_mm);
}

/**
 * 해당 월을 기준으로 달력을 출력한다.
 * 
 * @parameter p_yyyy 네비게이션에서 선택한 달력의 년도
 * @parameter p_mm 네비게이션에서 선택한 달력의 월
 */
calendarType_3.prototype.displayCalender = function(p_yyyy, p_mm) {
	// 전체 달력 구성
	var calHtml = this.makeCalender(p_yyyy, p_mm);

    this.positionId.html("");
    this.positionId.html(calHtml);

    // 날짜 클릭시 선택 이벤트를 등록한다.
    this.addEvent(this);
}

/**
 * 달을 이동한다.
 * 
 * @parameter yyyy 네비게이션에서 선택한 달력의 년도
 * @parameter mm 네비게이션에서 선택한 달력의 월
 */
calendarType_3.prototype.moveMonth = function(yyyy, mm) {
	if(yyyy != null && mm != null) {
		this.displayCalender(yyyy, mm);
	}
}

/**
 * 해당 월의 달력 화면을 만든다.
 */
calendarType_3.prototype.makeCalender = function(p_yyyy, p_mm) {
	// 2월 윤달인 경우 일 수 변경
    if ((p_yyyy % 4 == 0 && p_yyyy % 100) != 0 || p_yyyy % 400 == 0) { 
    	this.arr_month[2] = 29; 
    } else {
    	this.arr_month[2] = 28; 
	}


    // 해당 월 1일의 요일 정보(0:일, 1:월, 2:화, 3:수, 4:목, 5:금, 6:토)를 가져온다.
    var p_date = new Date(p_yyyy, p_mm - 1, 1);
    var p_week = p_date.getDay();

    // 달력 전체 HTML 을 만든다.
    var __html__ = "";
    
    __html__ +="<div class=\"bdWrap\">";
    __html__ +="	<div class=\"unit_calender\">";    
    __html__ +="		<div class=\"innerbdWrap\">";
    __html__ += "			<div class=\"headerW\">";

    // 이전 버튼 표시
    var pre_date = new Date(p_date.getFullYear(), p_date.getMonth() - 1, 1);
    var pre_yyyy = pre_date.getFullYear();
    var pre_mm = pre_date.getMonth() + 1;
    
    // 네비게이션 첫 달이 현재 달이 아닌 경우 이전 버튼 활성화
    if(p_yyyy != this.curDate.getFullYear() || p_mm != this.curDate.getMonth() + 1) {
    	__html__ += "    			<a href=\"#none\" yyyy=\"" + pre_yyyy + "\" mm=\"" + pre_mm + "\" class=\"btnLeft\">";
    } else {
    	__html__ += "    			<a href=\"#none\" class=\"btnLeft\">";
    }
    __html__ += "<img src=\"/images/contents/util_calender_btn_left.png\" alt=\"\" close=\"no\"></a>";
   
   // 년월 표시
    __html__ += "				<a href=\"#none\" class=\"list\">" + p_yyyy + ". " + objCal.fillZeros(p_mm) + "</a>";
    
    // 다음 버튼 표시
    var next_date = new Date(p_date.getFullYear(), p_date.getMonth() + 1, 1);
    var next_yyyy = next_date.getFullYear();
    var next_mm = next_date.getMonth() + 1;
    
    var navLastDate = new Date(this.curDate.getFullYear(), this.curDate.getMonth() + 11, 1);
    var navLastYYYY = navLastDate.getFullYear();
    var navLastMM = navLastDate.getMonth() + 1;
    
    // 선택한 년월이 (현재 년월 + 12개월) 미만인 경우 다음 버튼 활성화
    if(navLastYYYY > p_yyyy || (navLastYYYY == p_yyyy && navLastMM > p_mm)) {
    	__html__ += "    			<a href=\"#none\" yyyy=\"" + next_yyyy + "\" mm=\"" + next_mm + "\" class=\"btnRight\">";
    } else {
    	__html__ += "    			<a href=\"#none\" class=\"btnRight\">";
    }
    __html__ += "<img src=\"/images/contents/util_calender_btn_right.png\" alt=\"\" close=\"no\"></a>";

    // 년월 표시
    __html__ += "				<div class=\"listCont\" style=\"display:none;\">";
    __html__ += "					<a href=\"#none\" class=\"close txtImg\">close</a>";
    __html__ += "					<ul>";
   
    for(var i = 0; i < 12; i++) {
    	var linkDate = new Date(this.curDate.getFullYear(), this.curDate.getMonth() + i, 1);
        var linkYYYY = linkDate.getFullYear();
        var linkMM = linkDate.getMonth() + 1;    
        
    	__html__ += "						<li><a href=\"#none\" yyyy=\"" + linkYYYY + "\" mm=\"" + linkMM + "\" class=\"monthLink\" close=\"no\">" + linkYYYY + "." + objCal.fillZeros(linkMM, 2) + "</a></li>";
	}
    __html__ += "					</ul>";
    __html__ += "				</div>";

    __html__ += "			</div>";
    
    __html__ += "			<table class=\"tbl_cal\">";    
    __html__ += "				<caption>달력</caption>";
    
    // 달력 요일 표시
    __html__ += "				<thead>";    
    __html__ += "					<tr>";    
    __html__ += "	    				<th scope=\"col\" class=\"sun\">SUN</th><th scope=\"col\">MON</th><th scope=\"col\">TUE</th><th scope=\"col\">WED</th><th scope=\"col\">THU</th><th scope=\"col\">FRI</th><th scope=\"col\" class=\"sat\">SAT</th>";    
    __html__ += "					</tr>";    
    __html__ += "				</thead>";    
    
    // 달력 날짜 영역의 HTML 을 만든다.
    var dayHtml = "";									// 달력 날짜 영역 HTML 
    var increase = 0; 										// 주 단위 증가값
    var dd = 1;												// 일 단위 증가값
    
    for (var i = 0; i < 7 * 6; i++) {
    	// 달력 한줄 시작
    	dayHtml += (increase % 7 == 0) ? "<tr>" : "";						

    	// 달력에서 이전달 또는 다음달의 날짜인 경우 공백 처리
        if (i < p_week || dd > this.arr_month[p_mm]) {
        	dayHtml += "<td>&nbsp;</td>";
        	
        // 해당 월의 달력 날짜 처리
        } else {
            var p_yyyymmdd = p_yyyy + objCal.fillZeros(p_mm, 2) + objCal.fillZeros(dd, 2);
																			
            var cDateTime = objCal.getDateObj(objCal.getDateString(this.curDate, "yyyymmdd")).getTime();			// 현재날짜
            var pDateTime = objCal.getDateObj(p_yyyymmdd).getTime();															// 달력날짜

            // 선택 가능한 날짜인지 여부
            var isEnabled = (pDateTime > cDateTime) ? true : false;
            
            // 오늘부터 선택 가능한 경우 선택 가능한 날짜인지 여부
            if(this.isSelectableFromToday) {
            	isEnabled = (pDateTime >= cDateTime) ? true : false;
            }
            
            // 선택 가능 또는 불가능 표시 
            var class_name = isEnabled ? this.enabledClass : this.disabledClass;
            
            // 토,일요일 표시
            if(isEnabled && increase % 7 == 0) {
            	class_name = "sun";
            } else if(isEnabled && increase % 7 == 6) {
            	class_name = "sat";
            }
            
            // 달력의 날짜가 오늘인 경우 표시
            class_name = (p_yyyymmdd == objCal.getDateString(this.curDate, "yyyymmdd")) ? this.todayClass : class_name;

            // 선택된 날짜인 경우 처리
            if(this.selectedDate == p_yyyymmdd) {
        		// 선택된 상태로 표시
            	class_name = this.selectedClass;
            }
            
            // 선택 가능한 날짜인 경우 링크 테그 추가
            if(isEnabled) {
            	dayHtml += "<td class=\"" + class_name + " " + this.selectableClass + "\" date=\"" + p_yyyymmdd + "\"><a href=\"#none\">" + objCal.fillZeros(dd, 2) + "</a></td>";
            } else {
            	dayHtml += "<td class=\"" + class_name + "\" date=\"" + p_yyyymmdd + "\"><a href=\"#none\">" + objCal.fillZeros(dd, 2) + "</a></li>";
            }

            // 다음 날짜로 이동
            dd++;				
        }

        // 달력 한줄 종료 (다음주로 이동)
        if(increase % 7 == 6) {
        	dayHtml += "</tr>";
        	
        	// 더이상 날짜가 없는 경우 날짜 출력 종료
        	if(dd > this.arr_month[p_mm]) {
        		break;
        	}
        }
        
        increase++;
    }
 
    // 달력 날짜 영역 표시
    __html__ += "				<tbody>";
    __html__ += dayHtml;
    __html__ += "				</tbody> ";
    
    __html__ += "			</table> ";
    __html__ += "		</div> ";
    
    // 휴일 목록
    __html__ += "		<ul class=\"footList\">";
    
    var p_yyyymm = p_yyyy + objCal.fillZeros(p_mm, 2);
    var arrHoliday = this.holidayList.split(",");
    
    for(var i = 0; i < arrHoliday.length; i++) {
    	var info = arrHoliday[i].split("|");
    	var yyyymmdd =  info[0];
    	var dayName =  info[1];
    	
    	if(yyyymmdd.indexOf(p_yyyymm) == 0) {
    	    __html__ += "			<li><em>" + yyyymmdd.substring(6) + "일 </em>" + dayName + "</li>";    
    	}
    }
    __html__ += "		</ul>";        
    
    __html__ += "	</div>";   
    __html__ += "</div>";   
    
    return __html__;
}

/**
 * 클릭시 선택 이벤트 처리
 */
calendarType_3.prototype.addEvent = function(p) {
	// 달력 년월 펼침	
	p.positionId.find(".unit_calender .headerW .list").click(function(){
		$(this).parent().find('.listCont').slideDown('fast');			
	});
	p.positionId.find(".unit_calender .listCont .close").click(function(){
		$(this).parent().slideUp();			
	});		
	
	// 달력 년월 선택
	p.positionId.find(".monthLink").click(function() {
		p.moveMonth($(this).attr("yyyy"), $(this).attr("mm"));
	});
	
	// 날짜 클릭
	p.positionId.find("." + p.selectableClass).click(function() {
	    var selectDate = $(this).attr("date");
	    var bSelected = false; 
	    	
	    if (selectDate != null) {
			// 콜백 함수를 호출한 후, 팝업 레이어를 닫는다.
			if(p.callback != null) {
				p.selectedDate = selectDate;
				
				// 콜백 함수 호출
				p.callback(selectDate);
				
				// 달력 refresh
				p.displayCalender(Number(selectDate.substring(0,4)), Number(selectDate.substring(4,6)));
				
				// 닫기
				p.positionId.hide();
			}
			// ----------
	    }
	});

	// 이전 버튼 클릭
	p.positionId.find(".btnLeft").click(function() {
		p.moveMonth($(this).attr("yyyy"), $(this).attr("mm"));
	});
	
	// 다음 버튼 클릭
	p.positionId.find(".btnRight").click(function() {
		p.moveMonth($(this).attr("yyyy"), $(this).attr("mm"));
	});
}