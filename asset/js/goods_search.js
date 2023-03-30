	/**
	 * 출발지를 선택한다.
	 * @param posClass 출발지 정보를 포함한 class 명
	 * @param event 이벤트가 발생한 tag
	 */
	function selectDepartureCity(posClass, event) {
		var code = event.attr("code");
		
		$("." + posClass + " .departure_city a").each(function() {
			if($(this).attr("code") == code) {
				$(this).attr("class", "on");
			} else {
				$(this).attr("class", "");
			}
		});
	}

	
	/**
	 * 선택한 카테고리에 대한 하위 카테고리 정보를 가져온다.
	 * @param posClass 카테고리 정보를 포함한 상위 class 명
	 * @param searchKind 조회 또는 선택한 카테고리 종류 (1:국가-도시, 2:도시, 3:도시선택)
	 * @param event 이벤트가 발생한 tag
	 */
	function selectCategoryInfo(posClass, searchKind, event) {
		var code = event.attr("code");
		
		var selectedCategoryKind = " .major_category_list";
		if(searchKind == 2) {
			selectedCategoryKind = " .nat_list";
		} else if(searchKind == 3) {
			selectedCategoryKind = " .city_list";
		}

		$("." + posClass + selectedCategoryKind +" a").each(function() {
			if($(this).attr("code") == code) {
				$(this).attr("class", "on");
			} else {
				$(this).attr("class", "");
			}
		});
		
		if(searchKind == 1 || searchKind == 2) {
			var param = 
				"searchKind=" +searchKind +
				"&searchCode=" + code +
				"&salesGbnFlag=T";
			
			$.ajax({
				type : "GET",
				url : "/product/common/getCategoryInfo.do",
				data : param,
				dataType:"JSON",
				success : function(data) {
					// 카테고리 영역을 새로운 데이터로 그린다.
					printCategoryInfo(posClass, searchKind, data);
				},
				error : function(xhr, status, error) {
					alert("잠시 후 다시 이용해 주세요.");
				},
				complete : function(data) {
				}
			});
			
		} else if(searchKind == 3) {
			
		}
	}
	

	/**
	 * 카테고리 영역을 새로운 데이터로 그린다.
	 * @param posClass 카테고리 정보를 포함한 상위 class 명
	 * @param searchKind 조회할 카테고리 종류 (1:국가-도시, 2:도시)
	 * @param event 이벤트가 발생한 tag
	 */
	function printCategoryInfo(posClass, searchKind, data) {
		if(searchKind == 1) {
			var natList = "";
			for(var i = 0; i < data.categoryInfo.natList.length; i++) {
				natList += "<li><a href=\"#none\"" + ((i == 0) ? "class=\"on\"" : "") + " code=\"" +  data.categoryInfo.natList[i].categoryCd + "\" onclick=\"selectCategoryInfo('" + posClass + "', 2, $(this))\">" +  data.categoryInfo.natList[i].categoryName + "</a></li>";
			}
		
			$("." + posClass + " .nat_list").html(natList);
		}
		
		var cityList = "";
		for(var i = 0; i <  data.categoryInfo.cityList.length; i++) {
			cityList += "<li><a href=\"#none\"" + ((i == 0) ? "class=\"on\"" : "") + " code=\"" +  data.categoryInfo.cityList[i].categoryCd + "\" onclick=\"selectCategoryInfo('" + posClass + "', 3, $(this))\">" +  data.categoryInfo.cityList[i].categoryName + "</a></li>";
		}
	
		$("." + posClass + " .city_list").html(cityList);
	}
	
	
	/**
	 * 리스트에서 선택된 코드를 조회한다.
	 * @param posClass 코드 정보를 포함한 상위 class 명
	 */
	function getCodeInList(posClass, targetCss) {
		var code = "";
		
		$("." + posClass + " ." + targetCss + " a").each(function() {
			if($(this).attr("class") == "on") {
				code = $(this).attr("code");
			}
		});
		
		return code;
	}
	
	