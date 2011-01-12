/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["libs/jquery.ui"], function () {
    $("#group_edit_tabs").bind("tabsselect", function (event, ui) {
        $("form", this).attr("action", $(ui.tab).attr("href"));
    });
    $("#delete_group_form").submit(function () {
        return confirm("Are you sure you delete? This cannot be undone.");
    });
});
