	/**
	 *	함수명 : gn_ArrayOfDay(), gv_date_check()
	 *	내  용 : 입력값이 올바른 날짜 포맷인지를 체크
	 *			 BOOLEAN return
	 *
	 */
	function gn_ArrayOfDay(l_sLeapYear) {
		this[0]=0;  // <- 아무런 의미가 없는 것임. 무시해도 좋음.
		this[1]=31;
		this[2]=28;
		if (l_sLeapYear) // 윤달이 아니면...
			this[2]=29;
		this[3]=31;
		this[4]=30;
		this[5]=31;
		this[6]=30;
		this[7]=31;
		this[8]=31;
		this[9]=30;
		this[10]=31;
		this[11]=30;
		this[12]=31;
	}
	function gv_date_check(l_sDate) {	// "19991231" 이런 형식`으로 반드시 넘겨줄것
										// "1999/12/31" 이런 형식은 절대 안됨
		if (l_sDate == "") return false;

		if (l_sDate.length != 8) {		// 처음엔 자리수부터 Check 한다.
			return false;
		}

		/*************************************************
		* text Box 의 입력된 자료 Check
		*************************************************/
		var l_iYear  = parseInt(l_sDate.substring(0,4), 10);
		var l_iMonth = parseInt(l_sDate.substring(4,6), 10);
		var l_iDay   = parseInt(l_sDate.substring(6,8), 10);


		/******************************************************************
		* 윤달 Check!
		******************************************************************/
		var l_sLeapYear = (((l_iYear%4 == 0) && (l_iYear%100 != 0)) || (l_iYear%400 == 0));
		var monthDays  = new gn_ArrayOfDay(l_sLeapYear);

		if (l_iYear < 1900) {
			return false;
		} else if (l_iMonth > 12) {		// 달수가 12월 보다 크면...
			return false;
		} else if((parseInt(l_iDay) < 1) || (l_iDay > monthDays[l_iMonth])) {	// 그 달의 마지막 날 보다 크다면...
			return false;
		}

		return true;
	}	
	

	/**
	 *	함수명 : getCookie(), setCookie()
	 *	내  용 : 입력값이 올바른 날짜 포맷인지를 체크
	 */
	   function setCookie(cName, cValue, cDay){
	        var expire = new Date();
	        expire.setDate(expire.getDate() + cDay);
	        cookies = cName + '=' + escape(cValue) + '; path=/ '; 
	        if(typeof cDay != 'undefined') cookies += ';expires=' + expire.toGMTString() + ';';
	        document.cookie = cookies;
	    }
	 
	    // 쿠키 가져오기
	    function getCookie(cName) {
	        cName = cName + '=';
	        var cookieData = document.cookie;
	        var start = cookieData.indexOf(cName);
	        var cValue = '';
	        if(start != -1){
	            start += cName.length;
	            var end = cookieData.indexOf(';', start);
	            if(end == -1)end = cookieData.length;
	            cValue = cookieData.substring(start, end);
	        }
	        return unescape(cValue);
	    }
	