var access_key = 'bd6cf312bc7800bc1b82f66cbed78ebc';

function PhoneChange(val) {
	$.ajax({
		type : "POST",
		url: 'http://apilayer.net/api/validate?access_key=' + access_key + 
		'&number=' + val + 
		'&country_code=IN'+
		'&line_type=' +'mobile',
		success : PhoneChange2,
		failure : function(data) {
			console.log(json);
		}
	})
}
function PhoneChange2(val) {
	$.ajax({
		type : "POST",
		url : '/phone/check',
		data : val,
		success : function(json){
			console.log('ssssssssssssssssssssss');
		},
		failure : function(data) {
		}
	})
}