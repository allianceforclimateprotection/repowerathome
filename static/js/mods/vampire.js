/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
define(function () {
    return {
        skip_to_next_sheet: function (worksheet, delay, scroller) {
            var offset = 1;
            worksheet.nextAll().each(function () {
                if ($(this).find(".vampire_slayer:checked").length === 0) {
                    return false;
                }
                /* increment the offset, as we want to skip ahead and find
                a worksheet that hasn't been filled out */
                offset = offset + 1; 
            });
            setTimeout(function () {
                scroller.move(offset);
            }, delay);
        }
    };
});
