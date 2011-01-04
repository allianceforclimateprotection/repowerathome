/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["libs/jquery.validation"], function () {
    // Validate the password form
    $("#password_reset_confirm").validate({
        rules: {
            new_password1: { required: true, minlength: 5 },
            new_password2: { required: true, minlength: 5, equalTo: "#id_new_password1" }
        }
    });
});
