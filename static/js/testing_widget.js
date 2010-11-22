/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, FB: false, rah_name: false, WebFont: false, rah_nav_select: false, jQuery: false, window: false, google: false */

function move_ticket(offset) {
    // this only works with 3 values right now, +1, 0 or -1
    if (offset > 1 || offset < -1) {
        return;
    }
    var current = $(".active", $("#tickets"));
    var next = current;
    if (offset > 0) {
        next = current.next();
    } else if (offset < 0) {
        next = current.prev();
    } else {
        return;
    }
    if (next.length > 0) {
        var idx = $("#ticket_index");
        idx.text(parseInt(idx.text(), 10) + offset);
        current.addClass("hidden");
        current.removeClass("active");
        next.addClass("active");
        next.removeClass("hidden");
        $("#id_ticket_id").val($(".ticket_id", next).text());
    }
}
$(document).ready(function() {
    $(".testing_widget_tab").click(function () {
        var link = $(this);
        link.hide().siblings().show();
        $("#testing_feedback_form_container").toggle();
        $.post(link.attr("href"));
        return false;
    });
    $("#prev_ticket_control").live("click", function () {
        move_ticket(-1);
        return false;
    });
    $("#next_ticket_control").live("click", function () {
        move_ticket(1);
        return false;
    });
    $("#testing_feedback_form").live("submit", function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
            success: function (data) {
                var container = $("#testing_feedback_form_container");
                container.html(data["form_html"]);
                $("input:submit", container).button();
            }
        }, "json");
        return false;
    });
});