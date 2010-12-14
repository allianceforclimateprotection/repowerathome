/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["libs/jquery", "libs/webfont", "libs/jquery.ui", "libs/jquery.form", "mods/feedback", "mods/messages", "mods/facebook"],
    function (jquery, webfont, ui, form, feedback, messages, facebook) {
        // Setup TypeKit for non IE browsers
        var browser = $.browser;
        if (!browser.msie && !(browser.mozilla && browser.version.substr(0, 5) === "1.9.0")) {
            WebFont.load({ typekit: { id: 'vbg1eri'}});
        }
        
        // setup buttons
        $("button, input:submit, a.button, input.button").button();
        $(".buttonset").buttonset();
        
        // Setup datepicker
        $(".datepicker").datepicker();
        
        // setup tabs
        $(".tabs").tabs();

        // Highlight the right nav option if specified
        var rah_nav_select = RAH.ENV.nav_select;
        if (typeof(rah_nav_select) !== 'undefined' && rah_nav_select !== '') {
            $("#" + rah_nav_select).addClass("selected");
        }
        $("#nav a").text("");

        // style some submit buttons as links
        $(".as_link[type='submit']").each(function () {
            var button = $(this);
            var link = $("<a/>")
                .text(button.val())
                .attr("href", "#")
                .click(function () {
                    button.parents("form").submit();
                    return false;
                });
            button.replaceWith(link);
        });
        
        $.ajaxSetup({
            error: function (XMLHttpRequest, textStatus) { 
                var error_msg = $("<ul/>")
                    .attr({"class": "plain_list shadow"})
                    .append("<li/>")
                        .attr({"class": "messages error sticky"})
                        .text(textStatus)
                        .append("<a/>")
                            .attr({"href": "#", "class": "dismiss"})
                            .text("close");
                messages.add_message(error_msg);
            }
        });

        $.validator.setDefaults({
            submitHandler: function (form) {
                form.submit();
            }
        });

        $(".chart_link").click(function () {
            $.getScript($(this).attr("href"));
            return false;
        });

        messages.setup();
        feedback.setup();
        facebook.setup();
    });
