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
                            success: function(){
                                $("#feedback_dialog").dialog("close");
                            }
                        });
                    },
                },
                title: "Feedback",
                autoOpen: false,
                width: 350,
            });
            // Attach functionality to feedback links
            $(".feedback_link").click(function(){
                $("#feedback_dialog").load("/feedback/", function(){ // Load the feedback form via ajax
                    $("#feedback_submit").hide(); // We don't need this button when viewed inside dialog
                    $("#id_url").val(location.href); // Set the url to the current url
                    $("#feedback_dialog").dialog("open"); // Open the dialog with feedback form
                });
                return false;
            });
        },
    },
    
    /**
    * Registration page
    **/
    page_register: {
        init: function(){
            // Set up a dialog window for opening later
            $('#dialog').dialog({ 
                buttons: {
                    "Finish Registration": function() { 
                        $("#profile_form").submit();
                    },
                    "Skip": function() { 
                        window.location = "/"
                    },
                },
                modal: true,
                resizable: false,
                draggable: false,
                autoOpen: false,
                title: "Almost done...",
            });
            
            // Validate the registration form
            $("#registration_form").validate({
                rules: {
                    email: {
                        required: true,
                        email: true,
                        remote: {
                            url: "/validate/",
                            type: "post",
                        }
                    },
                    password1: {
        				required: true,
        				minlength: 5
        			},
        			password2: {
        				required: true,
        				minlength: 5,
        				equalTo: "#id_password1"
        			},
                },
                messages: {
                    email: {
                        remote: "That email is already registered",
                    },
                },
                submitHandler: function(form) {
                    $(form).ajaxSubmit({
                        dataType: "json",
                        success: function(response, status){
                            if(response['valid'] != true){
                                // TODO Get these errors inline insead of in an alert
                                alert(response['errors']);
                                return;
                            } else {
                                // Set the action of the profile form with the freshly minted user id
                                $("#profile_form").attr("action", "/user/edit/" + response['userid'] + "/");
                                
                                // Show the dialog with profile form
                                $('#dialog').dialog('open');                                
                            }
                        }
                    });
                }
            });
            // Validate the post registration questions form
            $("#profile_form").validate({
                rules: {
                    zipcode: {
                        remote: {
                            url: "/validate/",
                            type: "post",
                        }
                    },
                },
                messages: {
                    zipcode: {
                        remote: "Please enter a valid 5 digit zipcode",
                    },
                },
            });
        },
    },
    
    /**
    * Home Logged In page
    **/
    page_home_logged_in: {
        init: function(){
            rah.mod_action_nugget.init();
            rah.mod_house_party.init();
        },
    },
    
    /**
    * Action Detail page
    **/
    page_action_detail: {
        init: function(){
            var checkboxes = $(".action_task_submitter :checkbox");
            checkboxes.parents('form').find(':submit').remove();
            rah.set_task_completion_submission.init(checkboxes);
        },
    },
    
    /**
    * Action Show page
    **/
    page_action_show: {
        init: function(){
            rah.mod_action_nugget.init();
        },
    },
    
    /**
    * Profile page
    **/
    page_profile: {
        init: function(){
            rah.mod_action_nugget.init();
        },
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
        },
    },
    
    set_task_completion_submission: {
        init: function(checkboxes){
            checkboxes.click(function(){
                var form = $(this).parents('form');
                $.post(form.attr('action'), form.serialize(), function(completed_tasks){
                    try{
                        form.parents('.action_nugget').find('.user_completes').text(completed_tasks);
                    } catch(err){}
                    var box = form.find(':checkbox');
                    box.attr('checked', !box.attr('checked'));
                });
                return false;
            });
        }
    },
    
    mod_house_party: {
        init: function(){
            this.create_dialog();
            $('.house_party').click(function(){ $('#house_party_dialog').dialog('open'); return false; });
        },
        
        create_dialog: function(){
            $('#house_party_dialog').dialog({
                title: 'House Parties',
                buttons: {
                    "Give me a call": function() {
                        $(this).find('form').submit();
                    },
                },
                modal: true,
                resizable: false,
                draggable: false,
                autoOpen: false, 
            });
        }
        
    },
}