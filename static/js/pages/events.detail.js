/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["mods/comments", "mods/events", "mods/commitments"],
    function (comments, events, commitments) {
        require.ready(function () {
            comments.setup();
            events.guests();
            commitments.card_setup();
        });
    });
