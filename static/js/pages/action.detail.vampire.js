/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["pages/action.detail", "libs/jquery.tools.scrollable", "libs/jquery.tools.scrollable.navigator", "libs/jquery.ui", "libs/jquery.qtip", "mods/vampire"],
    function (action, scrollable, navigator, ui, qtip, vampire) {
        var scroller = $("#vampire_worksheet").scrollable({ 
            size: 1, 
            clickable: false,
            item: "* .worksheet",
            api: true
        });
        $("#vampire_worksheet").navigator({
            navi: "#vampire_worksheet_wizard_nav",
            naviItem: "li"
        });
        var nav = $("#vampire_worksheet_wizard_nav");
        $(".frame_shifter").click(function () {
            var worksheet = $(this).parents(".worksheet");
            vampire.skip_to_next_sheet(worksheet, 0, scroller);
            nav.slideDown("fast");
            return false;
        });
        if (undefined !== RAH.vampire_worksheet_started && RAH.vampire_worksheet_started) {
            nav.show();
            scroller.end(0);
        }
        $(".vampire_slayer").click(function () {
            var form = $(this).parents("form");
            /* save the worksheet data */
            $.ajax({
                url: form.attr("action"),
                type: form.attr("method"),
                data: form.serialize(),
                success: function (data) {},
                error: function () {},
                dataType: "json"
            });
            
            /* set the slay method in the plan sheet */
            var input_selected = $(this);
            var device = input_selected.parents("form").find(".device_label").val();
            if (input_selected.val() === "y") {
                $("#my_vampire_list").append("<li>" + device + "</li>");
            } else {
                $("#my_vampire_list li:contains('" + device + "')").remove();
            }
            $("#my_vampire_count").text($("#my_vampire_list li").length);
            
            /* skip to the next incomplete worksheet */
            var worksheet = input_selected.parents(".worksheet");
            vampire.skip_to_next_sheet(worksheet, 500, scroller);
        });
        
        $(".slay_link a").click(function () {
            var page = $(this).attr("href");
            nav.find("a[href='" + page + "']").click();
            return false;
        });
        $(".slayer_help").button("destroy");
        $("#vampire_worksheet a.tooltip").each(function () {
            var link = $(this);
            var location = link.attr("href");
            link.qtip({
                content: {
                    url: location
                },
                position: {
                    corner: {
                        target: "rightMiddle",
                        tooltip: "leftTop"
                    }
                },
                style: {
                    name: "green",
                    tip: "leftTop",
                    background: "#E3EC9F",
                    color: "#00AAD8",
                    border: {
                        width: 3,
                        radius: 2,
                        color: "#92C139"
                    }
                },
                show: "mouseover",
                hide: "mouseout"
            });
            link.click(function () { 
                return false; 
            });
        });
    });
