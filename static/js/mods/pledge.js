/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
define(["libs/jquery", "libs/jquery.validation", "libs/jquery.form", "libs/jquery.cookie", "mods/messages", "libs/jquery.ui"],
    function (jquery, validate, form, cookies, messages, ui) {
        return {
            submit_setup: function () {
                var pledge_mod = this;
                $("#pledge_card_form").validate({
                    rules: {
                        zipcode:    { required: false, minlength: 5, digits: true },
                        email:      { required: true, email: true },
                        first_name: { required: true, minlength: 2 }
                    },
                    submitHandler: function (form) {
                        $(form).ajaxSubmit({
                            dataType: "json",
                            success: function (rsp) {
                                messages.add_message(rsp.msg);
                                if (rsp.errors === false) {
                                    pledge_mod.advance_slide();
                                    $.cookie('repowerathomepledge', true);
                                } else {
                                    var form = $("#pledge_card_form");
                                    form.html(rsp.payload);
                                    $("button", form).button();
                                }
                            }
                        });
                        return false;
                    }
                });
            },
            advance_slide: function () {
                $("#home_pledge_slide").fadeOut(200, function () {
                    $("#home_pledge_actions_slide").fadeIn(200);
                });
            }
        };
    });
