/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
define(function () {
    return {
        setup: function () {
            $(".search_widget").submit(function () {
                var form = $(this);
                $.ajax({
                    url: form.attr("action"),
                    type: form.attr("method"),
                    data: form.serialize(),
                    success: function (data) {
                        data = jQuery.trim(data);
                        if (data.length > 0) {
                            $(".search_results").removeClass("hidden");
                            $(".search_results", form).html(data);
                        } else {
                            $(".search_results").addClass("hidden");
                        }
                    }
                });
                return false;
            });
            $(".search_more").live("click", function () {
                var link = $(this);
                $.get(link.attr("href"), function (data) {
                    link.replaceWith(data);
                });
                return false;
            });
        }
    };
});
