// validate note, if success - send it to the server
function validateNote() {
    // not 'let' or 'const', because once I have used 'let'
    // as a result my site broke down on mobile devices
    var text = $("#noteTextarea").val();

    // check if there is any non-space char
    if (text.trim() === "") {
        showAlert("#alertError");
    } else {
        addNote(text);
    }
}

// send note text to the server
function addNote(text) {
    $.ajax({
        url: "/api/notes",
        method: "POST",
        data: {
            text: text
        }
	}).done(function(msg) {
	    showAlert("#alertSuccess");
	}).fail(function(err, textStatus){
	    showAlert("#alertWrong");
	});

    $("#noteTextarea").val('');
}

function deleteNotes() {
    $.ajax({
        url: "/api/notes",
        method: "DELETE",
	}).done(function(msg) {
	    $("#notesData").html('');
	});
}


// show pretty alert for 2 seconds
function showAlert(id) {
	$(id).slideDown("slow");
	setTimeout(function() {
    	$(id).slideUp("slow");
    }, 2000);
}