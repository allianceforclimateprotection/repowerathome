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
                    zipcode:    { required: false, remote: { url: "/validate/", type: "post" } },
                    email:      { required: true, email: true, remote: { url: "/validate/", type: "post" } },
                    first_name: { required: true, minlength: 2 },
                    password1:  { required: true, minlength: 5 },
        			password2:  { required: true, minlength: 5, equalTo: "#id_password1" }
                },
                messages: {
                    email: { remote: "That email is already registered" },
                    zipcode: { remote: "We couldn't locate this zipcode" }
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
                    yaxis: {min: 0, tickDecimals: 0, autoscaleMargin: 0.6,}
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
            
            // Setup invite friend form, link, and dialog
            $("#invite_friend_form").validate({rules: {to_email: { required: true, email: true }}});
            $('#invite_friend_link').click(function(){ $('#invite_friend_dialog').dialog('open'); return false; });
            $('#invite_friend_dialog').dialog({
                title: 'Invite a friend', modal: true, autoOpen: false, 
                buttons: { "Send Invitation": function() { $('#invite_friend_form').submit(); }}
            });
            
            // Setup twitter update form, link, and dialog
            $("#twitter_post_dialog").validate({ rules: {status: { required: true, }}});
            $('.twitter_status').click(function(){ $('#twitter_post_dialog').dialog('open'); return false; });
            var form = $('#twitter_status_form');
            $('#twitter_post_dialog').dialog({
                title: 'Tell your tweeps about us', modal: true, autoOpen: false,
                buttons: (form.size() > 0 ? { "Update status": function() { form.submit(); } } : { })
            });
        },
    },
    
    /**
    * Profile Edit Page
    **/
    page_profile_edit: {
        init: function(){
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
            
            $('.commit_link').click(function(){ $('#commit_dialog').dialog('open'); return false; });
            $('.commit_cancel_link').click(function(){
                $("#id_cancel_commitment").attr("checked", "checked");
                $('#commit_form').submit();
                return false;
            });
            $('#commit_dialog').dialog({
                title: 'Make a Commitment', modal: true, resizable: false, draggable: false, autoOpen: false, 
                width: 550,
                height: 450,
                open: function(){
                    $("#commit_form").hide();
                    $("#commit_calendar").datepicker({
                        dateFormat: 'yy-mm-dd', 
                        maxDate: '+2y', 
                        minDate: '0', 
                        numberOfMonths: 2, 
                        onSelect: function(dateText, inst) { 
                            $("#id_date_committed").val(dateText);
                        }
                    });
                },
                buttons: { 
                    "Commit": function() {
                        $('#commit_form').submit(); 
                        $('#commit_dialog').dialog('close');
                    }
                }
            });
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
                    name: { required: true }
                }
            });
            $(".rateable_rate_form [name='next']").remove();
            $('.rateable_rate_form :submit').click(function(){
                submit = $(this);
                form = submit.parents('form');
                form.append("<input type='hidden' name='" + submit.val() + "' value='" + submit.val() + "' />");
                $.post(form.attr('action'), form.serialize(), function(data){
                    rah.mod_messages.init(data);
                });
               return false; 
            });
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
                }, 3000);
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
                    slug.val(URLify($(this).val(), 50));
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
        }
    },
    
    page_group_list: {
        init: function() {
            rah.mod_search_widget.init();
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
                        $(".search_results", form).html(data);
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
                return confirm("Are you sure you delete, this can not be undone?");
            })
        }
    }
}