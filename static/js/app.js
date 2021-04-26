$("#timeSelect").on("change", function() {
	let timeSpan = $(this).val();
	switch(timeSpan) {
	case "Season":
		$("#seasonCol").show();
		$("#fillerCol").hide();
		$("#timeStartCol").hide();
		$("#timeEndCol").css('visibility', 'hidden');
		break;
	case "Time Period":
		$("#seasonCol").hide();
		$("#fillerCol").hide();
		$("#timeStartCol").show();
		$("#timeEndCol").css('visibility', 'visible');
		break;
	case "Career":
		$("#seasonCol").hide();
		$("#fillerCol").show();
		$("#timeStartCol").hide();
		$("#timeEndCol").css('visibility', 'hidden');
		break;
	default:
		return;
	};
});

function filterShot(shotsData) {
	let selectedQuarters = [];
	$('input[name="quarter"]:checked').each(function() {
	   selectedQuarters.push(parseInt(this.value));
	});
	if (selectedQuarters.indexOf(5) >= 0) {
		selectedQuarters.push(6, 7, 8, 9, 10);
	}

	let selectedRange = [];
	$('input[name="range"]:checked').each(function() {
	    switch(this.value) {
	    case "Paint":
	   		selectedRange.push("Restricted Area", "In The Paint (Non-RA)");
	   		break
	   	case "Midrange":
	   		selectedRange.push("Mid-Range");
	   		break
	   	case "Three":
	   		selectedRange.push("Right Corner 3", "Left Corner 3", "Above the Break 3", "Backcourt");
	   		break
	   }
	});
	
	let filtered = shotsData.filter((e) => { return selectedQuarters.indexOf(e[7]) >= 0; })
							.filter((e) => { return selectedRange.indexOf(e[13]) >= 0; });

	return filtered;
}

$(function() {
	$("#seasonCol").show();
	$("#fillerCol").hide();
	$("#timeStartCol").hide();
	$("#timeEndCol").css('visibility', 'hidden');
});