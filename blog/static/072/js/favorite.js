/*********************************************
* 파일명: favorite.js
* 기  능: 최근본상품관련 유틸리티
* 만든이: 이진환
* 날  짜: 2016-03-16
**********************************************/
// 0. 기본 오브젝트 변수
var favoriteObjInfo	= new Object();
favoriteObjInfo.favorite = new favorite();

/**
 * 최근본상품 관련함수
 */
function favorite(){}
favorite.prototype.channel = "";
favorite.prototype.mode = "FA"; //FA:최근본상품
favorite.prototype.newdata = {
			prod_id:"",title:"",price:"",img_url:"http://",link_url:"http://",regdate:""
		  , etc1:"" //상품:5~6일, 호텔:등급
	      , etc2:""
};

//1.최근본상품 데이터를 적재한다.
favorite.prototype.push = function () 
{
	var arr_json = new Array();

	//기 등록된 목록을 가져온다.
	var arr_tmp_json = this.list();
	
	try
	{
		//data push!
		$.each(arr_tmp_json, function(i, data){
			if(data.prod_id==favoriteObjInfo.favorite.newdata.prod_id){
				//기등록되어있으면, 패스!
			}else{
				arr_json.push(data);
			}
		});
		arr_json.push(favoriteObjInfo.favorite.newdata);
			
		//generation json data
		var v_json_data = JSON.stringify(arr_json);
		
		//cookie setting!
		objInfo.webStorage.setCookie(this.channel,this.mode, v_json_data);
		
	}catch(e){}
};

//2.최근본상품 목록을 리턴한다.
favorite.prototype.list = function () 
{
	var arr_json = new Array();
	try
	{
		var v_json_str = objInfo.webStorage.getCookie(this.channel,this.mode);
		if(""==v_json_str) return arr_json;
		
		var json_obj = $.parseJSON(v_json_str);
		var incrase = 1;
		$.each(json_obj.slice().reverse(), function(i, data){
			if(parseInt(favoriteObjInfo.favorite.getDateString()) <= parseInt(data.regdate) && incrase < 100)
			{
				arr_json.push(data);
			}else{
				//날짜가 지난것은 버린다.
			}
			
			incrase++;
		});
	}catch(e){}
	return arr_json;
};
//3.모든채널의 상품목록을 리턴한다.
favorite.prototype.listAll = function () 
{
	var arr_json = new Array();
	{
		arr_json = this.getArrayList("10", arr_json); //땡처리항공
		arr_json = this.getArrayList("20", arr_json); //항공+호텔
		arr_json = this.getArrayList("30", arr_json); //해외호텔
		arr_json = this.getArrayList("40", arr_json); //패키지
		arr_json = this.getArrayList("50", arr_json); //자유여행
		arr_json = this.getArrayList("60", arr_json); //패스&투어
		arr_json = this.getArrayList("70", arr_json); //국내호텔
		arr_json = this.getArrayList("80", arr_json); //렌터카
		arr_json = this.getArrayList("90", arr_json); //골프
	}
	return arr_json.sort(this.sortRegDate);
};
favorite.prototype.getArrayList = function (v_channel_code, arr_json) 
{
	var v_json_str = objInfo.webStorage.getCookie(v_channel_code,this.mode);
	if(""!=v_json_str){
		try{
			json_obj = $.parseJSON(v_json_str);
			$.each(json_obj.slice().reverse(), function(i, data){
				data.channel_code=v_channel_code;
				arr_json.push(data);
			});
		}catch(e){}
	}
	return arr_json;
};
favorite.prototype.sortRegDate = function (a, b) 
{
	var aRegDate = a.regdate;
	var bRegDate = b.regdate; 
	return ((aRegDate > bRegDate) ? -1 : ((aRegDate < bRegDate) ? 1 : 0));
};

//날짜오브젝트로 스트링을 리턴한다.
favorite.prototype.getDateString = function() {
	var p_date = new Date();
	
	var p_yyyy = p_date.getFullYear();
	var p_mm = Number(p_date.getMonth() + 1);
	p_mm = p_mm < 10 ? "0" + p_mm : p_mm;
	var p_dd = p_date.getDate();
	p_dd = p_dd < 10 ? "0" + p_dd : p_dd;

	return p_yyyy + "" + p_mm + "" + p_dd;
};