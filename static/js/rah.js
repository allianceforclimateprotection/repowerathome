$(document).ready(function() {
    rah.base.init();

    // Page templates that require additional js should add an object within the rah object. 
    // then define rahClass to be the name of the object within rah.
    if(undefined !== window.rah_name){
        try{
            rah[rah_name].init();
        }catch(err){
            if(typeof(console) !== 'undefined' && console != null) {
                console.log("No page specific javascript was run.");
            }
        }
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
            // Setup TypeKit for non IE browsers
            if (!$.browser.msie) {
                WebFont.load({typekit: {id: 'vbg1eri'}});
            }
            
            // setup buttons
            $("button, input:submit, a.button, input.button").button();
            $(".buttonset").buttonset();
            $(".datepicker").datepicker();
            
            // setup tabs
            $(".tabs").tabs();
            
            // Highlight the right nav option if specified
            if(typeof(rah_nav_select) !== 'undefined' && rah_nav_select != '') {
                $("#" + rah_nav_select).addClass("selected");
            }
            
            // style some submit buttons as links
            $(".as_link[type='submit']").each(function(){
                var button = $(this);
                var form = button.parents("form");
                button.hide();
                var link = $("<a></a>");
                link.text(button.val());
                link.attr("href", "#");
                link.click(function(){ 
                    form.submit();
                    return false;
                });
                button.replaceWith(link);
            });
            
            // Hide the nav text content
            $("#nav a").text("");
            
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
            rah.mod_facebook_connect.init();
            rah.mod_ajax_setup.init();
            rah.mod_validate_setup.init();
            rah.mod_chart_dialog.init();
        }
    },
    
    mod_facebook_connect: {
        init: function() {
            $("#fb-login").click(function(){
                FB.login(function(response) {
                    if (response.session) {
                        next_elem = $("input[type='hidden'][name='next']");
                        next = next_elem ? next_elem.val() : window.location;
                        window.location = "/facebook/login/?next=" + next;
                    }
                }, {perms:"email,publish_stream,offline_access"});
            });
        },
        authorize: function() {
            FB.login(function(response) {
                if (response.session) {
                    next_elem = $("input[type='hidden'][name='next']");
                    next = next_elem.length ? next_elem.val() : window.location;
                    window.location = "/facebook/authorize/?next=" + next;
                }
            }, {perms:"email,publish_stream,offline_access"});
            return false;
        }
    },
    
    mod_ask_to_share: {
        init: function(url) {
            $.get(url, function(data) {
                rah.mod_ask_to_share.build_dialog(data);
            });
        },
        build_dialog: function(data) {
            var container = $("<div />");
            container.html(data);
            container.dialog({autoOpen: false, modal: true, height: 312, width: 386,
                title: "Repower at Home &hearts; Facebook"});
            $("input:submit, .button, button", container).button();
            // $(".buttonset", container).buttonset();
            $("#ask_to_share").submit(function() {
                var form = $(this);
                if(!($("#id_has_facebook_access", form).val() == "True")) {
                    FB.login(function(response) {
                        if (response.session) {
                            $.get("/facebook/authorize/", function(data) {
                                rah.mod_ask_to_share.share(form);
                            });   
                        }
                    }, {perms:"email,publish_stream,offline_access"});
                } else {
                    rah.mod_ask_to_share.share(form);
                }
                container.dialog("close");
                return false;
            });
            $("#ask_to_share_cancel", container).click(function() {
                container.dialog("close");
                return false;
            });
            $("#id_dont_ask", container).click(function() {
                $(this).parents("form").submit();
            });
            container.dialog("open");
        },
        share: function(form) {
            $.ajax({
                url: form.attr("action"),
                type: form.attr("method"),
                data: form.serialize(),
                success: function(data) {
                    if($(".messages", data).size() > 0){
                        rah.mod_messages.init(data);
                    } else {
                        rah.mod_ask_to_share.build_dialog(data);
                    }
                },
                dataType: "html"
            });
        }
    },
    
    /**
    * Registration page
    **/
    page_register: {
        init: function(){
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
        }
    },
    
    /**
    * Log in page
    **/
    page_login: {
        init: function(){
            $("#login_form").validate({
                rules: {
                    email:      { required: true, email: true },
                    password:  { required: true, minlength: 5 }
                }
            });
        }
    },    
    /**
    * Logged in Home Page
    **/
    page_home_logged_in: {
        init: function(){
            rah.mod_action_nugget.init();
            rah.mod_invite_friend.init();
            
            // Setup twitter update form, link, and dialog
            $("#twitter_status_form").validate({ rules: {status: { required: true }}});
            $('#twitter_status_link').click(function(){ $('#twitter_post_dialog').dialog('open'); return false; });
            $('#twitter_post_dialog').dialog({
                title: 'Tell your tweeps about us', modal: true, autoOpen: false,
                buttons: ($('#twitter_status_form').size() > 0 ? { "Update status": function() { $('#twitter_status_form').submit(); } } : { })
            });
        }
    },
        
    mod_chart_dialog: {
        init: function() {
            $(".chart_link").click(function(){
                $.getScript($(this).attr("href"));
                return false;
            });
        }
    },
    
    /**
    * Profile Edit Page
    **/
    page_profile_edit: {
        init: function(){
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
                }
            });
            $(".selector").click(function(){
                var selector = $(this);
                var checked = selector.hasClass("select_all");
                $("input[type='checkbox']", selector.parents(".form_row")).attr("checked", checked);
                return false;
            });
            $("#team_selectors").removeClass("hidden");
            $("#link_with_facebook").click(rah.mod_facebook_connect.authorize);
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
            });
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
                        var form = $(".action_commit_form");
                        form.submit();
                    }
                }
            });
            $(".commit_cancel").click(function(){
                if(confirm("Are you sure you want to cancel your commitment?")) {
                    $(".action_cancel_form").submit();
                }
               return false; 
            });
            if(undefined !== window.rich_action_name){
                try{
                    rah["rich_actions"][rich_action_name].init();
                }catch(err){
                    console.error(err);
                }
            }
            $(".action_forms .tooltip").qtip({
                position: {
                    corner: {
                        target: 'bottomMiddle',
                        tooltip: 'topMiddle'
                    }
                },
                style: {
                    name: 'green',
                    tip: 'topMiddle',
                    background: '#E3EC9F',
                    color: '#00AAD8',
                    border: {
                        width: 3,
                        radius: 2,
                        color: '#92C139'
                    }
                },
                show: 'mouseover',
                hide: 'mouseout'
            });
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
                    navi: "#vampire_worksheet_wizard_nav",
                    naviItem: "li"
                });
                var nav = $("#vampire_worksheet_wizard_nav");
                $(".frame_shifter").click(function(){
                    var worksheet = $(this).parents(".worksheet");
                    rah.rich_actions.vampire_power.skip_to_next_sheet(worksheet, 0, scroller);
                    nav.slideDown("fast");
                    return false;
                });
                if(!(typeof(vampire_worksheet_started) == "undefined") && vampire_worksheet_started) {
                    nav.show();
                    scroller.end(0);
                }
                $(".vampire_slayer").click(function(){
                    var form = $(this).parents("form");
                    /* save the worksheet data */
                    $.ajax({
                        url: form.attr("action"),
                        type: form.attr("method"),
                        data: form.serialize(),
                        success: function(data) {
                            $("#vampire_savings_total").text(data["total_savings"]);
                        },
                        error: function() {},
                        dataType: "json"
                    });
                    
                    /* set the slay method in the plan sheet */
                    var input_selected = $(this);
                    var plan_value = $("." + input_selected.attr("name") + " .slay_method");
                    plan_value.text(input_selected.parent().find("label").text());
                    $("." + input_selected.attr("name") + " .slay_link").show();
                    
                    /* skip to the next incomplete worksheet */
                    var worksheet = input_selected.parents(".worksheet");
                    rah.rich_actions.vampire_power.skip_to_next_sheet(worksheet, 500, scroller);
                });
                
                $(".slay_link a").click(function(){
                    page = $(this).attr("href");
                    nav.find("a[href='" + page + "']").click();
                    return false;
                });
                $(".slayer_help").button("destroy");
                $("#vampire_worksheet a.tooltip").each(function(){
                    var link = $(this);
                    var location = link.attr("href");
                    link.qtip({
                        content: {
                            url: location
                        },
                        position: {
                            corner: {
                                target: 'rightMiddle',
                                tooltip: 'leftTop'
                            }
                        },
                        style: {
                            name: 'green',
                            tip: 'leftTop',
                            background: '#E3EC9F',
                            color: '#00AAD8',
                            border: {
                                width: 3,
                                radius: 2,
                                color: '#92C139'
                            }
                        },
                        show: 'mouseover',
                        hide: 'mouseout'
                    });
                    link.click(function(){ return false; });
                });
            },
            skip_to_next_sheet: function(worksheet, delay, scroller){
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
                }, delay);
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
            $("#comment_form").validate({
                rules: {
                    comment:    { required: true, maxlength: 3000 }
                },
                messages: {
                    comment: { maxlength: "comment must be less than 3000 characters" }
                }
            });
            rah.mod_thumbs_radio_widget.init();
            rah.mod_flag.init();
            $("#comments .tooltip").qtip({
                position: {
                    corner: {
                        target: 'topMiddle',
                        tooltip: 'bottomMiddle'
                    }
                },
                style: {
                    name: 'green',
                    tip: 'bottomMiddle',
                    background: '#E3EC9F',
                    color: '#00AAD8',
                    border: {
                        width: 3,
                        radius: 2,
                        color: '#92C139'
                    }
                },
                show: 'mouseover',
                hide: 'mouseout'
            });
        }
    },
    
    /**
    * mod_messages: call this method to attach message html, if no html is passed it will just set a timer on any existing messages
    **/
    mod_messages: {
        init: function(html) {
            if(html) { 
                $('#message_box').hide().append(html).slideDown();
            }
            $(".messages .dismiss").live("click", function(){ 
                $(this).parents(".messages").slideUp(400, function(){
                    $(this).remove();
                });
            });
            $(".messages:not(.sticky)").each(function() {
                var elem = $(this);
                setTimeout(function() {
                    elem.slideUp(400, function(){ elem.remove(); });
                }, 5000);
            });
        }
    },
    
    page_password_change: {
        init: function() {
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
                beforeSend: function() { },
                complete: function() { },
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
            $("#id_slug").prepopulate($("#id_name"), 32);
            $("#id_name").focus(function(){
                $("#group_slug_address label.inside").removeClass("inside");
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
            $('.invite_form_submit').remove();
            $("#invite_form").validate({rules: {email: { required: true, email: true }}});
            $('.invite_friend_link').click(function(){ $('#invite_friend_dialog').dialog('open'); return false; });
            $('#invite_friend_dialog').dialog({
                title: 'Invite a friend', modal: true, autoOpen: false, 
                buttons: { "Send Invitation": function() { $("#invite_form").submit(); }}
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
                        data = jQuery.trim(data);
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
                $.get(link.attr("href"), function(data) {
                    link.replaceWith(data);
                });
                return false;
            });
        }
    },
    
    page_group_edit: {
        init: function() {
            $("#group_edit_tabs").bind("tabsselect", function(event, ui){
                $("form", this).attr("action", $(ui.tab).attr("href"));
            });
            $("#delete_group_form").submit(function(){
                return confirm("Are you sure you delete? This cannot be undone.");
            });
        }
    },
    
    mod_thumbs_radio_widget: {
        init: function() {
            $(".rateable_rate_form [type='submit']").remove();
            $(".rateable_rate_form [name='next']").remove();
            $(".rateable_rate_form .score_radio").change(function() {
               var form = $(this).parents("form");
               $.ajax({
                   url: form.attr("action"),
                   type: form.attr("method"),
                   data: form.serialize(),
                   dataType: "json",
                   success: function(data) {
                       var container = form.parent("div");
                       // rah.mod_messages.init(data["messages"]);
                       $(".users_voted_stats", container).html(data["users_voted_stats"]).effect(
                           "highlight", {"backgroundColor": "#B0D8F2"}, 1500);
                   }
               });
               return false;
            });
        }
    },
    
    mod_flag: {
        init: function() {
            $(".flagged_flag_form [name='next']").remove();
            $(".flagged_flag_form .flag_box").click(function() {
                var box = $(this);
                var form = box.parents("form");
                $.ajax({
                    url: form.attr("action"),
                    type: form.attr("method"),
                    data: form.serialize(),
                    success: function(data) {
                        rah.mod_messages.init(data);
                        box.button("disable");
                    }
                });
                return false;
            });
        }
    },
    
    mod_validate_setup: {
        init: function() {
            $.validator.setDefaults({
                submitHandler: function(form) { 
                    form.submit(); 
                }
            });
        }
    },
    
    mod_event_tabs: {
        init: function(tab_number) {
            $("#event_tabs").tabs({
                select: function(event, ui) {
                    var url = $.data(ui.tab, "load.tabs");
                    if( url ) {
                        window.location.href = url;
                        return false;
                    }
                    return true;
                },
                selected: tab_number
            });
        }
    },
    
    page_event_list: {
        init: function() {
            $("#house_party_form").validate({rules: {phone_number: { required: true }}});
            $('#house_party_link').click(function(){ $('#house_party_dialog').dialog('open'); return false; });
            $('#house_party_dialog').dialog({
                title: 'Energy meeting contact', modal: true, resizable: false, draggable: false, autoOpen: false, 
                buttons: { "Give me a call": function() { $('#house_party_form').submit(); }}
            });
        }
    },
    
    page_event_show: {
        init: function() {
            rah.mod_comment_form.init();
            rah.mod_event_tabs.init(0);
            var address = $("#event_address").text();
            var location = $("#event_location").text();
            geocoder = new google.maps.Geocoder();
            var myOptions = {
              zoom: 9,
              mapTypeId: google.maps.MapTypeId.ROADMAP,
              scrollwheel: false
            };
            var map = new google.maps.Map(document.getElementById("event_map"), myOptions);
            if(geocoder) {
                geocoder.geocode( { 'address': address+" "+location}, function(results, status) {
                    if (status == google.maps.GeocoderStatus.OK) {
                        map.setCenter(results[0].geometry.location);
                        var marker = new google.maps.Marker({
                            map: map, 
                            position: results[0].geometry.location
                        });
                        var infowindow = new google.maps.InfoWindow({
                            content: "<h4>" + address + "</h4><h6>" + location + "</h6>"
                        });
                        google.maps.event.addListener(marker, 'click', function() {
                            infowindow.open(map,marker);
                        });
                    }
                });
            }
        }
    },
    
    mod_event_date: {
        init: function() {
            $(".future_date_warning").change(function(){
                var now = new Date();
                var when = new Date(this.value);
                if(when-now < 0) {
                    if(!confirm("Has this event really already taken place?")){
                        this.value = "";
                    }
                }
            });
            $(".form_row:has(.datepicker)").change(function() {
                var row = $(this);
                if($(".datepicker", row).val() != "") {
                    $("label.inside", row).removeClass("inside");
                } else {
                    $("label:first", row).addClass("inside");
                }
            });
        }
    },
    
    page_event_create: {
        init: function() {
            rah.mod_event_date.init();
        }
    },
    
    page_event_edit: {
        init: function() {
            rah.mod_event_date.init();
        }
    },
    
    page_event_guests: {
        init: function() {
            rah.mod_event_tabs.init(1);
            rah.mod_comment_form.init();
            var table = $("#event_guests_table");
            $(".selector").click(function(){
                var checked = $(this).hasClass("select_all");
                $("input[type='checkbox']", table).attr("checked", checked);
                return false;
            });
            rah.page_event_guests.submit_on_select();
            $("#event_guests_selectors").removeClass("hidden");
            var namespace = this;
            var editables = $(".editable");
            editables.each(rah.page_event_guests.make_editable);
            editables.live("mouseover", function(){
                $(this).addClass("editable_highlight");
            }).live("mouseout", function(){
                $(this).removeClass("editable_highlight");
            });
            $("#event_guests_table .tooltip").qtip({
                position: {
                    corner: {
                        target: 'rightMiddle',
                        tooltip: 'leftMiddle'
                    }
                },
                style: {
                    name: 'green',
                    tip: 'leftMiddle',
                    background: '#E3EC9F',
                    color: '#00AAD8',
                    border: {
                        width: 3,
                        radius: 2,
                        color: '#92C139'
                    }
                },
                show: 'mouseover',
                hide: 'mouseout'
            });
            var guests_add_link = $("#guests_add_link");
            var guests_add_container = $("#guests_add_container");
            guests_add_container.load(guests_add_link.attr("href"), function() {
                $(".tabs", guests_add_container).tabs();
                $("button, input:submit, a.button, input.button", guests_add_container).button();
                rah.page_guest_add.init();
                guests_add_container.dialog({ 
                    autoOpen: false,
                    modal: true,
                    height: 650,
                    width: 500
                });
            });
            guests_add_link.click(function() {
                guests_add_container.dialog("open");
                return false;
            });
        },
        make_editable: function() {
            var element = $(this);
            var args = {
                placeholder: '<span class="event_inline_placeholder">click to add</span>',
                cancel: 'Cancel',
                submit: '<br/><button type="submit">Ok</button>'
            }
            if(element.hasClass("rsvp_select")) {
                args.type = "select";
                args.loadurl = "/events/rsvp_statuses/";
            }
            element.editable(function(value, settings) {
                $.post(element.attr("id"), {"value": value}, function(data) {
                    rah.mod_messages.init(data["message_html"]);
                    var row = element.parents("tr");
                    row.html(data["guest_row"]).effect(
                           "highlight", {"backgroundColor": "#FFF"}, 1500);
                    $(".editable", row).each(rah.page_event_guests.make_editable);
                }, "json");
                return value;
            }, args);
        },
        submit_on_select: function() {
            var form = $("#guest_edit_form");
            $("#id_action").change(function(){
                var select = $(this);
                if(!select.val().trim()) {
                    return;
                }
                if($("input[type='checkbox']", form).is(":checked")) {
                    form.submit();
                } else {
                    alert("Please select at least one guest.");
                    return;
                }
            });
        }
    },
    
    page_guest_add: {
        init: function() {
            $("#guests_add .tab").each(function() {
                var tab = $(this);
                $("form", tab).each(function() {
                    var form = $(this);
                    form.attr("action", form.attr("action") + "#" + tab.attr("id"));
                });
            });
        }
    },
    
    page_event_commitments: {
        init: function() {
            rah.mod_event_tabs.init(2);
            $("#ui-tabs-2").removeClass("ui-tabs-hide");
            rah.mod_comment_form.init();
        }
    }
};