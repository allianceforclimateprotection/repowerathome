define(function() {
    return {
        setup: function () {
            $("#message_box").delegate(".dismiss", "click", function () {
                $(this).parents(".messages").slideUp(400, function () {
                    $(this).remove();
                });
                return false;
            });
            this.auto_remove_messages();
        },
        auto_remove_messages: function () {
            $(".messages:not(.sticky)").each(function () {
                var elem = $(this);
                elem.delay(5000).slideUp(400, function () {
                    elem.remove();
                });
            });
        },
        add_message: function (html) {
            if (html) {
                $("#message_box").hide.append(html).slideDown();
            }
            this.auto_remove_messages();
        }
    }
});
