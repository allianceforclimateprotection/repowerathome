/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
define(["libs/jquery", "libs/jquery.ui", "libs/jquery.form", "mods/messages"],
    function (jquery, ui, form, messages) {
        return {
            setup: function () {
                // Setup Feedback dialog
                $("#feedback_dialog").dialog({
                    modal: true,
                    buttons: {
                        "Submit Feedback": function () { 
                            $("#feedback_form").ajaxSubmit({
                                success: function (messages_html) {
                                    $("#feedback_dialog").dialog("close");
                                    messages.add_message(messages_html);
                                }
                            });
                        }
                    },
                    title: "Feedback",
                    autoOpen: false,
                    width: 400
                });
                // Attach functionality to feedback links
                $(".feedback_link").click(function () {
                    $("#feedback_dialog").load("/feedback/", function () { // Load the feedback form via ajax
                        $("#loading").hide();
                        $("#feedback_submit").hide(); // We don't need this button when viewed inside dialog
                        $("#id_url").val(location.href); // Set the url to the current url
                        $("#feedback_dialog").dialog("open"); // Open the dialog with feedback form
                    });
                    return false;
                });
            }
        };
    });
