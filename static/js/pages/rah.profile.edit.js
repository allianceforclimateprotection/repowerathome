/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["libs/jquery.ui", "libs/jquery.validation", "mods/facebook"], 
    function (ui, validate, facebook) {
        $("#profile_edit_tabs").bind("tabsselect", function (event, ui) {
            $("form", this).attr("action", $(ui.tab).attr("href"));
        });
        // Validate the registration form
        $("#profile_edit_form").validate({
            rules: {
                zipcode:    { required: false, remote: { url: "/validate/", type: "post" } },
                email:      { required: true, email: true, remote: { url: "/validate/", type: "post" } },
                first_name: { required: true, minlength: 2 },
                password1:  { required: false, minlength: 5 },
                password2:  { required: false, minlength: 5, equalTo: "#id_password1" }
            },
            messages: {
                email: { remote: "That email is already registered" },
                zipcode: { remote: "We couldn't locate this zipcode" }
            }
        });
        $(".selector").click(function () {
            var selector = $(this);
            var checked = selector.hasClass("select_all");
            $("input[type='checkbox']", selector.parents(".form_row")).attr("checked", checked);
            return false;
        });
        $("#team_selectors").removeClass("hidden");
        $("#link_with_facebook").click(facebook.authorize);
    });
