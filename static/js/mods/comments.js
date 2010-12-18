/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
define(["libs/jquery.qtip", "mods/messages"], function (qtip, messages) {
    return {
        setup: function () {
            $("#comment_form").validate({
                rules: {
                    comment:    { required: true, maxlength: 3000 }
                },
                messages: {
                    comment: { maxlength: "comment must be less than 3000 characters" }
                }
            });
            this.thumbs_radio_widget();
            this.flag_widget();
            $("#comments .tooltip").qtip({
                position: {
                    corner: {
                        target: 'topMiddle',
                        tooltip: 'bottomMiddle'
                    }
                },
                style: {
                    name: 'green',
                    tip: 'bottomMiddle',
                    background: '#E3EC9F',
                    color: '#00AAD8',
                    border: {
                        width: 3,
                        radius: 2,
                        color: '#92C139'
                    }
                },
                show: 'mouseover',
                hide: 'mouseout'
            });
        },
        thumbs_radio_widget: function () {
            $(".rateable_rate_form input[type='submit']").remove();
            $(".rateable_rate_form input[name='next']").remove();
            $(".rateable_rate_form .score_radio").change(function () {
                var form = $(this).parents("form");
                $.ajax({
                    url: form.attr("action"),
                    type: form.attr("method"),
                    data: form.serialize(),
                    dataType: "json",
                    success: function (data) {
                        var container = form.parent("div");
                        $(".users_voted_stats", container).html(data["users_voted_stats"]).effect("highlight", {"backgroundColor": "#B0D8F2"}, 1500);
                    }
                });
                return false;
            });
        },
        flag_widget: function () {
            $(".flagged_flag_form input[name='next']").remove();
            $(".flagged_flag_form .flag_box").click(function () {
                var box = $(this);
                var form = box.parents("form");
                $.ajax({
                    url: form.attr("action"),
                    type: form.attr("method"),
                    data: form.serialize(),
                    success: function (data) {
                        messages.add_messages(data);
                        box.button("disable");
                    }
                });
                return false;
            });
        }
    };
});
