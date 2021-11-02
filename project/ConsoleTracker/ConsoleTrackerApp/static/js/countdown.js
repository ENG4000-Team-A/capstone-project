//global
var timer
var remainingTime

//runs countdown() every 1000 millis
function startCountdown(id ,then){

	timer = setInterval(function(){countdown(id, then)}, 1000);
	
}

// // unused
// function pause(){
// 	clearInterval(timer);
// }


function countdown(id, then){

	// unix time in seconds
	var now = Math.floor(Date.now() / 1000);

	remainingTime = then - now;

	var hour = Math.floor(remainingTime / (60 * 60) );
	var min = Math.floor((remainingTime / 60) % 60 );
	var sec = Math.floor(remainingTime % 60);

	if (remainingTime < 0){
		hour = 0;
		min = 0;
		sec = 0;
	}


	var result = hour +':'+ min +':'+ sec;
	document.getElementById(id).innerHTML = result;
}

