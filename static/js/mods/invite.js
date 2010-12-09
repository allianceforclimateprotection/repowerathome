/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
define(["libs/jquery.validate", "libs/jquery.ui", "mods/messages"],
    function (validate, ui, messages) {
        // Add a validator method for checking the comma separated email list
        $.validator.addMethod("multiemail", function (value, element) {
            // return true on optional element
            if (this.optional(element)) {
                return true;
            }
            var emails = value.split(new RegExp("\\s*,\\s*", "gi"));
            var valid = true;
            
            for (var i = 0; i < emails.length; i = i + 1) {
                valid = $.validator.methods.email.call(this, emails[i], element);
            }
            return valid;
        }, "The format for one or more emails doesn't look right.");
        return {
            setup: function () {
                // Setup invite friend form, link, and dialog
                $('.invite_form_submit').remove();
                $("#invite_form").validate({ rules: { emails: { required: true, multiemail: true }}});
                $('.invite_friend_link').click(function () { 
                    $('#invite_friend_dialog').dialog('open'); 
                    return false; 
                });
                $('#invite_friend_dialog').dialog({
                    title: 'Invite a friend', 
                    modal: true,
                    autoOpen: false, 
                    resizable: false, 
                    draggable: false, 
                    width: 360,
                    buttons: { 
                        "Send Invitation": function () {
                            if (!$("#invite_form").valid()) {
                                return;
                            }
                            $("#invite_form").ajaxSubmit({
                                success: function (messages_html) {
                                    $("#invite_friend_dialog").dialog("close");
                                    messages.init(messages_html);
                                    $("#id_emails, #id_note").val("");
                                }
                            });
                        }
                    }
                });
            }
        };
    });
