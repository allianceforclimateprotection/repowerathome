/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, FB: false, rah_name: false, WebFont: false, rah_nav_select: false, jQuery: false, window: false, google: false */

function dump(arr,level) {
	var dumped_text = "";
	if(!level) level = 0;

	//The padding given at the beginning of the line.
	var level_padding = "";
	for(var j=0;j<level+1;j++) level_padding += "    ";

	if(typeof(arr) == 'object') { //Array/Hashes/Objects 
		for(var item in arr) {
			var value = arr[item];

			if(typeof(value) == 'object') { //If it is an array,
				dumped_text += level_padding + "'" + item + "' ...\n";
				dumped_text += dump(value,level+1);
			} else {
				dumped_text += level_padding + "'" + item + "' => \"" + value + "\"\n";
			}
		}
	} else { //Stings/Chars/Numbers etc.
		dumped_text = "===>"+arr+"<===("+typeof(arr)+")";
	}
	return dumped_text;
}

function show_ticket(ticket_id){
    // Return if we're trying to go out of range
    if (jQuery.inArray(ticket_id, RAH_TESTING_TICKETS) === -1) {
        return;
    };
    $(".ticket_active").hide();
    $("#ticket_id__" + ticket_id).show();
    $("#ticket_id__" + ticket_id).addClass("ticket_active");
    
    // Figure out the index for this ticket
    for (var i=0; i < RAH_TESTING_TICKETS.length; i++) {
        if (ticket_id == RAH_TESTING_TICKETS[i]) {
            RAH_TICKET_INDEX = i;
            break;
        }
    };
    $("#ticket_index").text(RAH_TICKET_INDEX+1);
}

function ticket_received_state(form) {
    $(".form_row", form).slideUp();
    $(".ticket_more_feedback", form).slideDown();
    try {
        $(".ticket_submit", form).button( "option", "disabled", true );
        $(".ticket_submit span", form).html("Feedback received!");        
    } catch (err) {
        $(".ticket_submit", form).html("Feedback received!");
        $(".ticket_submit", form).attr("disabled", true);
    }
}

function ticket_ready_state(form) {
    $(".form_row", form).slideDown();
    $(".ticket_more_feedback", form).slideUp();
    try {
        $(".ticket_submit span", form).html("Submit");
        $(".ticket_submit", form).button( "option", "disabled", false );
    } catch (err) {
        $(".ticket_submit", form).html("Submit");
        $(".ticket_submit", form).attr("disabled", false);
    }
}

$(document).ready(function() {    
    // RAH_TESTING_TICKETS is an array of ticket IDs. It's defined in _testing_widget.html
    // RAH_TICKET_INDEX points to the current ticket in RAH_TESTING_TICKETS. It's also defined in _testing_widget.html
    show_ticket(RAH_TESTING_TICKETS[RAH_TICKET_INDEX])
    
    $(".testing_widget_tab").click(function () {
        var link = $(this);
        link.hide().siblings().show();
        $("#testing_feedback_form_container").toggle();
        $.post(link.attr("href"));
        return false;
    });
    $("#prev_ticket_control").live("click", function () {
        show_ticket(RAH_TESTING_TICKETS[RAH_TICKET_INDEX-1]);
        return false;
    });
    $("#next_ticket_control").live("click", function () {
        show_ticket(RAH_TESTING_TICKETS[RAH_TICKET_INDEX+1]);
        return false;
    });
    $(".ticket_more_feedback").live("click", function() {
        ticket_ready_state($(this).parents("form"));
        return false;
    });
    $(".testing_feedback_form").live("submit", function () {
        var form = $(this);
        var submit = $(".ticket_submit", form);
        $("#id_ticket_id", form).val(RAH_TESTING_TICKETS[RAH_TICKET_INDEX]);
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
            beforeSend: function () {
                try {
                    submit.button("option", "disabled", true );
                    $("span", submit).html($("#testing_spinner").html());
                } catch (err) {
                    submit.attr("disabled", true);
                    submit.html($("#testing_spinner").html());
                }
            },
            success: function (data) {
                if (data['valid']) {
                    ticket_received_state(form);
                    show_ticket(RAH_TESTING_TICKETS[RAH_TICKET_INDEX + 1]);
                } else {
                    alert(dump(data['errors']));
                    try {
                        submit.button( "option", "disabled", false );
                        $("span", submit).html("Submit");
                    } catch (err) {
                        submit.attr("disabled", false);
                        submit.html("Submit");
                    }
                }
            }
        }, "json");
        return false;
    });
});