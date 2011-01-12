/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["libs/jquery.validation", "libs/jquery.slimbox2"], function () {
    $("#media_widget_upload_form").validate({
        rules: {
            name: { required: true },
            image: { required: true },
            email: { required: true, email: true }
        }
    });
    $("#registration_form").validate({
        rules: {
            first_name: { required: true },
            last_name: { required: true },
            address: { required: true },
            state: { required: true },
            city: { required: true },
            zipcode: { required: true },
            image: { required: true },
            email: { required: true, email: true }
        }
    });
    $("a.lightbox").slimbox({}, null, function(el) {
        return (this == el) || ((this.rel.length > 0) && (this.rel == el.rel));
    });
});
