/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["mods/pledge", "mods/invite", "libs/jquery.validate", "libs/jquery.ui", "mods/commitments"],
    function (pledge, invite, validate, ui, commitments) {
        pledge.submit_setup();
        invite.setup();
         // Setup twitter update form, link, and dialog
        $("#twitter_status_form").validate({ rules: { status: { required: true }}});
        $('#twitter_status_link').click(function () {
            $('#twitter_post_dialog').dialog('open'); 
            return false;
        });
        
        // Create an object for the buttons
        var buttons = { };
        if ($('#twitter_status_form').length) {
            buttons["Update status"] = function () { 
                $('#twitter_status_form').submit(); 
            };
        }
        
        $('#twitter_post_dialog').dialog({
            title: 'Tell your tweeps about us', 
            modal: true, 
            autoOpen: false,
            buttons: buttons
        });
        
        // Setup the commitment card open link
        commitments.card_setup();
    });
