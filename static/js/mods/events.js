define(["libs/jquery.qtip", "libs/jquery.editable", "libs/jquery.ui", "mods/messages"], function () {
    return {
        date: function () {
             $(".future_date_warning").change(function () {
                var now = new Date();
                var when = new Date(this.value);
                if (when - now < 0) {
                    if (!confirm("Has this event really already taken place?")) {
                        this.value = "";
                    }
                }
            });
            $(".form_row:has(.datepicker)").change(function () {
                var row = $(this);
                if ($(".datepicker", row).val() !== "") {
                    $("label.inside", row).removeClass("inside");
                } else {
                    $("label:first", row).addClass("inside");
                }
            });
        },
        guests: function () {
            var namespace = this;
            var editables = $(".editable");
            editables.each(function(idx, elem) { this.make_editable(elem); });
            editables.delegate(".guest_icon", "mouseover", function () {
                $(this).addClass("ui-icon-circle-triangle-s");
                $(this).removeClass("ui-icon-triangle-1-s");
            }).delegate(".guest_icon", "mouseover", function () {
                $(this).addClass("ui-icon-triangle-1-s");
                $(this).removeClass("ui-icon-circle-triangle-s");
            });
            $("#guest_list .tooltip").qtip({
                position: {
                    corner: {
                        target: 'rightMiddle',
                        tooltip: 'leftMiddle'
                    }
                },
                style: {
                    name: 'green',
                    tip: 'leftMiddle',
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
            $(".guests_add_link, #event_hosts_link").each(function () {
                var link = $(this);
                var container = $("<div class='hidden'></div>");
                $("body").append(container);
                container.load(link.attr("href"), function () {
                    $("button, input:submit, a.button, input.button", container).button();
                    $("form", container).attr("action", link.attr("href"));
                    container.dialog({ 
                        autoOpen: false,
                        modal: true,
                        height: 575,
                        width: 360
                    });
                });
                link.click(function () {
                    container.dialog("open");
                    return false;
                });
            });
        },
        make_editable: function (elem) {
            var args = {
                placeholder: '<span class="event_inline_placeholder">click to add</span>',
                cancel: 'Cancel',
                submit: '<br/><button type="submit">Ok</button>'
            };
            if (elem.hasClass("rsvp_select")) {
                args.type = "select";
                args.loadurl = "/events/rsvp_statuses/";
            }
            elem.editable(function (value, settings) {
                $.post(elem.attr("id"), {"value": value}, function (data) {
                    messages.add_message(data["message_html"]);
                    elem.html(data["guest_status"]);
                    // added editable event back to element
                }, "json");
                return value;
            }, args);
        }
    }
});
