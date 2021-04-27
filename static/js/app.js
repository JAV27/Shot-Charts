$("#timeSelect").on("change", function() {
	let timeSpan = $(this).val();
	switch(timeSpan) {
	case "Season":
		$("#seasonCol").show();
		$("#timeStartCol").hide();
		$("#timeEndCol").css('visibility', 'hidden');
		break;
	case "Time Period":
		$("#seasonCol").hide();
		$("#timeStartCol").show();
		$("#timeEndCol").css('visibility', 'visible');
		break;
	default:
		return;
	};
});

function filterShot(shotsData) {
	let selectedSuccess = [];
	$('input[name="success"]:checked').each(function() {
	    switch(this.value) {
	    case "made":
	   		selectedSuccess.push("Made Shot");
	   		break;
	   	case "missed":
	   		selectedSuccess.push("Missed Shot");
	   		break;
	   }
	});

	let selectedQuarters = [];
	$('input[name="quarter"]:checked').each(function() {
	   selectedQuarters.push(parseInt(this.value));
	});
	if (selectedQuarters.indexOf(5) >= 0) {
		selectedQuarters.push(6, 7, 8, 9, 10);
	}

	let selectedRanges = [];
	$('input[name="range"]:checked').each(function() {
	    switch(this.value) {
	    case "Paint":
	   		selectedRanges.push("Restricted Area", "In The Paint (Non-RA)");
	   		break;
	   	case "Midrange":
	   		selectedRanges.push("Mid-Range");
	   		break;
	   	case "Three":
	   		selectedRanges.push("Right Corner 3", "Left Corner 3", "Above the Break 3", "Backcourt");
	   		break;
	   }
	});

	let filtered = shotsData.filter((e) => { return selectedSuccess.indexOf(e[10]) >= 0; })
							.filter((e) => { return selectedQuarters.indexOf(e[7]) >= 0; })
							.filter((e) => { return selectedRanges.indexOf(e[13]) >= 0; });

	return filtered;
}

$(function() {
	$("#seasonCol").show();
	$("#timeStartCol").hide();
	$("#timeEndCol").css('visibility', 'hidden');
});