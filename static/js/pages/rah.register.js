/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["libs/jquery", "libs/jquery.validate"], function () {
    $("#registration_form").validate({
        rules: {
            zipcode:        { required: false, remote: { url: "/validate/", type: "post" } },
            email: { required: true, email: true, remote: { url: "/validate/", type: "post" } },
            first_name:     { required: true, minlength: 2 },
            password1:      { required: true, minlength: 5 },
            password2:      { required: true, minlength: 5, equalTo: "#id_password1" }
        },
        messages: {
            email: { remote: "That email is already registered" },
            zipcode: { remote: "We couldn't locate this zipcode" }
        }
    });
});
