/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["libs/jquery.cookie", "mods/pledge"], function (cookies, pledge) {
    if ($.cookie("repowerathomepledge")) {
        pledge.advance_slide();
    } else {
        pledge.setup();
    }
});
