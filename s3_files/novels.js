var API_ENDPOINT = "https://k2vit8e9o3.execute-api.us-east-1.amazonaws.com/dev"


document.getElementById("updateButton").onclick = function(){
	document.getElementById("status").textContent="Update in Progress";
	var inputData = {
		"voice": "Brian",
	};

	$.ajax({
	      url: API_ENDPOINT,
	      type: 'PUT',
	      data:  JSON.stringify(inputData)  ,
	      contentType: 'application/json; charset=utf-8',
	      success: function (response) {
					document.getElementById("status").textContent=response;
	      },
	      error: function () {
	          alert("error");
	      }
	  });
}

function deleteRecord(id){
	document.getElementById("status").textContent="Delete in Progress.";
	var postId = id

	var inputData = {
		"postId": postId
	};
	$.ajax({
	      url: API_ENDPOINT ,
	      data:  JSON.stringify(inputData)  ,
	      type: 'DELETE',
	      contentType: 'application/json; charset=utf-8',
	      success: function (response) {
					document.getElementById("status").textContent="Success! Please list again to see results.";
	      },
	      error: function () {
	          alert("Error");
	      }
	  });
}


function searchButton() {
	document.getElementById("status").textContent="Getting Chapters...";
	var postId = "*";
	var index = 0;

	$.ajax({
				url: API_ENDPOINT + '?postId='+postId,
				type: 'GET',
				success: function (response) {
					$('#posts tr').slice(1).remove();
			console.log(response)
			response.sort((a,b) => (a.id > b.id) ? 1 : ((b.id > a.id) ? -1 : 0)); 
	        jQuery.each(response, function(i,data) {

						var player = "<audio controls><source src='" + data['url'] + "' type='audio/mpeg'></audio>"
						var deleteB = "<input type=\"submit\" ontouchstart=\"deleteRecord(\'" + data['id'] + "\')\" onclick=\"deleteRecord(\'" + data['id'] + "\')\" class=\"buttons\" value=Delete id=\"deleteButton\">" 
						if (typeof data['url'] === "undefined") {
	    					var player = ""
						}
						if ((typeof data['text'] === "undefined")) {
	    					data['text'] = ""
						}

						$("#posts").append("<tr> \
								<td>" + data['id'] + "</td> \
								<td>" + data['voice'] + "</td> \
								<td>" + data['text'].substring(0,30) + "</td> \
								<td>" + data['status'] + "</td> \
								<td>" + player + "</td> \
								<td>" + deleteB + "</td> \
								</tr>");
						index += 1;
	        });
	    	if (index == 0){
	    		alert("No results for search query.");
	    	}
				},
				error: function () {
						alert("error");
				}
		});
}

document.getElementById("searchButton").onclick = function(){
	searchButton();
	document.getElementById("status").textContent="Listing done.";
}

