$(document).ready(function() {
    rah.base.init();

    // Page templates that require additional js should add an object within the rah object. 
    // then define rahClass to be the name of the object within rah.
    if(undefined !== window.rah_name){
        try{
            rah[rah_name].init();
        }catch(err){}
    }
});

// Object containing all javascript necessary for Repower at Home
var rah = {    
    /**
    * Base contains code that needs to be excecuted with every 
    * page request. e.g., navigation with drop down menus
    **/
    base: {
        init: function(){
            // Setup TypeKit
            try{Typekit.load();}catch(e){}
            
            // setup buttons
            $("button, input:submit, a.button").button();
            rah.mod_overset.init();
            
            // Hide the nav text content
            $(".nav a").text("");
            
            // Setup Feedback dialog
            $("#feedback_dialog").dialog({
                modal:true,
                buttons: {
                    "Submit Feedback": function() { 
                        $("#feedback_form").ajaxSubmit({
                            success: function(messages_html) {
                                $("#feedback_dialog").dialog("close");
                                rah.mod_messages.init(messages_html);
                            }
                        });
                    }
                },
                title: "Feedback",
                autoOpen: false,
                width: 400
            });
            // Attach functionality to feedback links
            $(".feedback_link").click(function(){
                $("#feedback_dialog").load("/feedback/", function(){ // Load the feedback form via ajax
                    $("#loading").hide();
                    $("#feedback_submit").hide(); // We don't need this button when viewed inside dialog
                    $("#id_url").val(location.href); // Set the url to the current url
                    $("#feedback_dialog").dialog("open"); // Open the dialog with feedback form
                });
                return false;
            });
            rah.mod_messages.init();
            rah.mod_ajax_setup.init();
            rah.mod_validate_setup.init();
        }
    },
    
    /**
    * setup all of the overset inputs
    **/
    mod_overset: {
        init: function(){
            $(".overset input, .overset textarea").blur(function(){
               var field = $(this);
               var label = field.prev("label");
               if(field.val() == "") {
                   label.addClass("inside");
               } else {
                   label.removeClass("inside");
               }
            }).blur();
            $(".overset input, .overset textarea").focus(function(){
               $(this).prev("label").removeClass("inside");
            });
        }
    },
    
    /**
    * Registration page
    **/
    page_register: {
        init: function(){
            // Validate the registration form
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
            $("#login_form").validate({
                rules: {
                    email:      { required: true, email: true },
                    password:  { required: true, minlength: 5 }
                }
            });
        }
    },
    
    /**
    * Profile page
    **/
    page_profile: {
        init: function(){
            rah.mod_action_nugget.init();
            
            // Setup the chart
            if (!chart_data['point_data'].length) {
                $("#chart").html('<img src="' + media_url + 'images/theme/chart_demo.png" alt="sample chart"/>');
            } else {
                // Add an additional datapoint at the beginning to represent 0 points
                yesterday = chart_data['point_data'][0][0] - (60*60*24*1000*1);
                chart_data['point_data'].unshift([yesterday, 0]);
                chart_data["tooltips"].unshift("");
                                
                var plot = $.plot($("#chart"), [ { data: chart_data['point_data'] }], {
                    series: {
                        lines: { show: true },
                        points: { show: true, radius: 10 },
                        shadowSize: 5
                    },
                    grid: { hoverable: true, clickable: true, backgroundColor: { colors: ["#DDD", "#FFF"] } },
                    legend: {show: false},
                    xaxis: {mode: "time",autoscaleMargin: 0.1,  minTickSize: [1, "day"]},
                    yaxis: {min: 0, tickDecimals: 0, autoscaleMargin: 0.6}
                });
                $("#chart").bind("plothover", function (event, pos, item) {
                    if (item) {
                        showTooltip(item.pageX, item.pageY, item.dataIndex);
                    }
                    else {
                        $(".chart_tooltip").remove();
                    }
                });
                function showTooltip(x, y, index) {
                    // The first datapoint is an artificial point representing zero points, so it doesn't need a tooltip
                    if (index == 0){
                        return;
                    }
                    $('<div class="chart_tooltip">' + chart_data["tooltips"][index] + '</div>').css( {
                        position: 'absolute',
                        display: 'none',
                        top: y - 18,
                        left: x + 5
                    }).appendTo("body").fadeIn(300);
                }
            }
            
            // Setup house party form, link, and dialog
            $("#house_party_form").validate({rules: {phone_number: { required: true }}});
            $('#house_party_link').click(function(){ $('#house_party_dialog').dialog('open'); return false; });
            $('#house_party_dialog').dialog({
                title: 'House Party', modal: true, resizable: false, draggable: false, autoOpen: false, 
                buttons: { "Give me a call": function() { $('#house_party_form').submit(); }}
            });
            
            rah.mod_invite_friend.init();
            
            // Setup twitter update form, link, and dialog
            $("#twitter_post_dialog").validate({ rules: {status: { required: true }}});
            $('.twitter_status').click(function(){ $('#twitter_post_dialog').dialog('open'); return false; });
            var form = $('#twitter_status_form');
            $('#twitter_post_dialog').dialog({
                title: 'Tell your tweeps about us', modal: true, autoOpen: false,
                buttons: (form.size() > 0 ? { "Update status": function() { form.submit(); } } : { })
            });
        }
    },
    
    /**
    * Profile Edit Page
    **/
    page_profile_edit: {
        init: function(){
            $("#profile_edit_tabs").tabs();
            $("#profile_edit_tabs").bind("tabsselect", function(event, ui){
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
                },
            });
            var global_group_notifications = $("#id_global_group_notifications");
            global_group_notifications.change(function() {
                rah.page_profile_edit.toggle_group_notifications(this);
            });
            rah.page_profile_edit.toggle_group_notifications(global_group_notifications);
        },
        toggle_group_notifications: function(toggle_switch) {
            var global_on = $(toggle_switch).attr("checked");
            $("#group_notifications_form ul").each(function() {
                if(global_on) {
                    $(this).parent().hide();
                } else {
                    $(this).parent().show();
                }
            });
        }
    },
    
    /**
    * Action Detail page
    **/
    page_action_detail: {
        init: function(){
            var checkboxes = $(".action_task_submitter :checkbox");
            checkboxes.parents('form').find(':submit').remove();
            rah.set_task_completion_submission.init(checkboxes);
            rah.mod_comment_form.init();
            
            // $("#house_party_form").validate({rules: {phone_number: { required: true }}});
            $(".date_commit_field").parent().hide();
            $(".commit_trigger").click(function(){
                $("#commit_widget").dialog("open");
                return false;
            });
            $(".undo_trigger").click(function(){
                $(".action_undo_form").submit();
            })
            $("#commit_widget").dialog({
                title: "Make a Commitment", modal: true, resizable: false, 
                    draggable: false, autoOpen: false, 
                width: 550,
                height: 450,
                open: function(){
                    var widget = $(this);
                    widget.find(".commit_calendar").datepicker({
                        dateFormat: 'yy-mm-dd', 
                        maxDate: '+2y', 
                        minDate: '0', 
                        numberOfMonths: 2, 
                        onSelect: function(dateText, inst) { 
                            $(".date_commit_field").val(dateText);
                        }
                    });
                },
                buttons: { 
                    "Commit": function() {
                        $("#commit_widget").dialog("close");
                        var form = $(".action_commit_form:first");
                        form.submit();
                    }
                }
            });
            if(undefined !== window.rich_action_name){
                try{
                    rah["rich_actions"][rich_action_name].init();
                }catch(err){}
            }
        }
    },
    
    rich_actions: {
        vampire_power: {
            init: function(){
                var scroller = $("#vampire_worksheet").scrollable({ 
                    size: 1, 
                    clickable: false,
                    item: "* .worksheet",
                    api: true
                });
                $("#vampire_worksheet").navigator({
                    navi: ".vampire_worksheet_wizard_nav",
                    naviItem: "a"
                });
                var nav = $("ul.vampire_worksheet_wizard_nav");
                $("#get_started").click(function(){
                    nav.slideDown("fast", function(){
                        scroller.nextPage();
                    });
                    return false;
                });
                if(!(typeof(vampire_worksheet_started) == "undefined") && vampire_worksheet_started) {
                    nav.show();
                    scroller.end(0);
                }
                $(".vampire_slayer").click(function(){
                    var form = $(this).parents("form");
                    /* save the worksheet data */
                    $.post(form.attr("action"), form.serialize(), function(data){
                        $("#vampire_savings_total").text(data["total_savings"]);
                    }, "json");
                    
                    /* set the slay method in the plan sheet */
                    var input_selected = $(this);
                    var plan_value = $("." + input_selected.attr("name") + " .slay_method");
                    plan_value.text(input_selected.parent().text());
                    
                    /* skip to the next incomplete worksheet */
                    $("." + input_selected.attr("name") + " .slay_link").show();
                    var worksheet = input_selected.parents(".worksheet");
                    var offset = 1;
                    worksheet.nextAll().each(function(){
                        if($(this).find(".vampire_slayer:checked").length == 0) {
                            return false;
                        }
                        /* increment the offset, as we want to skip ahead and find
                        a worksheet that hasn't been filled out */
                        offset++; 
                    });
                    setTimeout(function() {
                        scroller.move(offset);
                    }, 500);
                });
                
                $(".slay_link a").click(function(){
                    page = $(this).attr("href");
                    nav.find("a[href='" + page + "']").click();
                    return false;
                });
                
            }
        }
    },
    
    /**
    * Action Show page
    **/
    page_action_show: {
        init: function(){
            rah.mod_action_nugget.init();
        }
    },
    
    /**
    * Post (Blog) Detail page
    **/
    page_post_detail: {
        init: function(){
            rah.mod_comment_form.init();
        }
    },
    
    /**
    * Action Nugget
    */
    mod_action_nugget: {
        init: function(){
            this.set_tasks_list_toggle();
            rah.set_task_completion_submission.init($('.action_task_submitter :checkbox'));
        },
        
        set_tasks_list_toggle: function(){
            $('.action_nugget .tasks_link').click(function(){
                $(this).parents('.action_nugget').find('.task_list').slideToggle();
                return false;
            });
        }
    },
   
    set_task_completion_submission: {
        init: function(checkboxes){
            checkboxes.click(function(){
                var form = $(this).parents('form');
                $.post(form.attr('action'), form.serialize(), function(data){
                    rah.mod_messages.init(data['message_html']);
                    try{
                        form.parents('.action_nugget').find('.user_completes').text(data['completed_tasks']);
                    } catch(err){}
                    var box = form.find(':checkbox');
                    box.attr('checked', !box.attr('checked'));
                }, 'json');
                return false;
            });
        }
    },
    
    mod_comment_form: {
        init: function() {
            $(".comment_form").validate({
                rules: {
                    comment:    { required: true, maxlength: 3000 }
                },
                messages: {
                    comment: { maxlength: "comment must be less than 3000 characters" }
                }
            });
            rah.mod_is_helpful_widget.init();
            rah.mod_flag.init();
        }
    },
    
    /**
    * mod_messages: call this method to attach message html, if no html is passed it will just set a timer on any existing messages
    **/
    mod_messages: {
        init: function(html) {
            if(html) { $('#message_box').append(html); }
            $(".messages:not(.sticky)").each(function() {
                var elem = $(this).parents("ul");
                setTimeout(function() {
                    elem.slideUp(400, function(){ elem.remove(); });
                }, 5000);
            });
            $("#message_box .dismiss").live("click", function(){ $(this).parents("ul").remove(); });
        }
    },
    
    page_password_change: {
        init: function(){            
            // Validate the password form
            $("#password_change_form").validate({
                rules: {
                    old_password: { required: true },
                    new_password1: { required: true, minlength: 5 },
                    new_password2: { required: true, minlength: 5, equalTo: "#id_new_password1" }
                }
            });
        }
    },
    
    page_password_reset_confirm: {
        init: function(){            
            // Validate the password form
            $("#password_reset_confirm").validate({
                rules: {
                    new_password1: { required: true, minlength: 5 },
                    new_password2: { required: true, minlength: 5, equalTo: "#id_new_password1" }
                }
            });
        }
    },
    
    mod_ajax_setup: {
        init: function() {
            $.ajaxSetup({
                beforeSend: function() { $("#loading").show(); },
                complete: function() { $("#loading").hide(); },
                error: function(XMLHttpRequest, textStatus) { 
                    var error_html = "<ul class='messages'><li class='messages error sticky'>" + textStatus;
                    error_html += "<a href='#' class='dismiss'>close</a></li></ul>";
                    rah.mod_messages.init(error_html);
                }
            });
        }
    },
    
    page_group_create: {
        init: function() {
            $("#id_slug").change(function() {
                $(this).data("changed", true);
            });

            $("#id_name").keyup(function() {
                var slug = $("#id_slug");
                if(!slug.data("changed")) {
                    slug.focus();
                    slug.val(URLify($(this).val(), 50));
                    slug.blur();
                    $(this).focus();
                }
            });
            
            $("#group_create_form").validate({
                rules: {
                    name: { required: true },
                    slug: { required: true },
                    description: { required: true }
                }
            });
        }
    },
    
    page_group_detail: {
        init: function() {
            $("table").tablesorter();
            rah.mod_invite_friend.init();
        }
    },
    
    page_group_list: {
        init: function() {
            rah.mod_search_widget.init();
        }
    },
    
    mod_invite_friend: {
        init: function(){
            // Setup invite friend form, link, and dialog
            $('#invite_friend_form_submit').hide();
            $("#invite_friend_form").validate({rules: {to_email: { required: true, email: true }}});
            $('#invite_friend_link').click(function(){ $('#invite_friend_dialog').dialog('open'); return false; });
            $('#invite_friend_dialog').dialog({
                title: 'Invite a friend', modal: true, autoOpen: false, 
                buttons: { "Send Invitation": function() { $('#invite_friend_form_submit').click();}}
            });
        }
    },
    
    mod_search_widget: {
        init: function() {
            $(".search_widget").submit(function() {
                var form = $(this);
                $.ajax({
                    url: form.attr("action"),
                    type: form.attr("method"),
                    data: form.serialize(),
                    success: function(data) {
                        data = jQuery.trim(data)
                        if(data.length > 0) {
                            $(".search_results").removeClass("hidden");
                            $(".search_results", form).html(data);
                        } else {
                            $(".search_results").addClass("hidden");
                        }
                    }
                });
                return false;
            });
            $(".search_more").live("click", function() {
                var link = $(this);
                var form = link.parents("form");
                $.get(link.attr("href"), function(data) {
                    link.replaceWith(data);
                });
                return false;
            });
        }
    },
    
    page_group_edit: {
        init: function() {
            $("#group_edit_tabs").tabs();
            $("#group_edit_tabs").bind("tabsselect", function(event, ui){
                $("form", this).attr("action", $(ui.tab).attr("href"));
            });
            $("#delete_group_form").submit(function(){
                return confirm("Are you sure you delete? This cannot be undone.");
            });
        }
    },
    
    mod_is_helpful_widget: {
        init: function() {
            $(".rateable_rate_form [name='next']").remove();
            $(".rateable_rate_form :submit").click(function() {
               var submit = $(this);
               var form = submit.parents("form");
               form.append("<input type='hidden' name='" + submit.val() + "' />");
               $.ajax({
                   url: form.attr("action"),
                   type: form.attr("method"),
                   data: form.serialize(),
                   success: function(data) {
                       form.parent("div").html(data);
                   }
               });
               return false;
            });
        }
    },
    
    mod_flag: {
        init: function() {
            $(".flagged_flag_form [name='next']").remove();
            $(".flagged_flag_form :submit").each(function() {
                var button = $(this);
                button.replaceWith("<a class='flag_submit_link' href='#'>" + button.val() + "</a>");
            });
            $(".flag_submit_link").click(function() {
                var form = $(this).parents("form");
                $.ajax({
                    url: form.attr("action"),
                    type: form.attr("method"),
                    data: form.serialize(),
                    success: function(data) {
                        form.html(data);
                    }
                });
                return false;
            });
        }
    },
    
    mod_validate_setup: {
        init: function() {
            $.validator.setDefaults({
                submitHandler: function(form) { form.submit(); }
            });
        }
    }
}