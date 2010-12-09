define(["libs/jquery.validation", "libs/jquery.cookie", "mods/messages", "libs/jquery.ui"],
    function (validate, cookies, messages, ui) {
        return {
            submit_setup: function () {
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
                                    this.advance_slide();
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
        }
});
