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
        },
    },
    
    /**
    * Registration page
    **/
    page_register: {
        init: function(){
            // Validate the form
            $("#registration_form").validate({
                rules: {
                    email: {
                        required: true,
                        // email: true
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
                submitHandler: function(form) {
                    $(form).ajaxSubmit({
                        success: function(responseText, statusText){
                            console.log(responseText);
                        }
                    });
                }
            });
            // Submit the form with an AJAX request
            // On successful valid submission, display post reg questions
        },
    },
    
    /**
    * Home Logged In page
    **/
    page_home_logged_in: {
        init: function(){
            rah.mod_action_nugget.init();
        },
    },
    
    /**
    * Action Nugget
    */
    mod_action_nugget: {
        init: function(){
            rah.mod_action_nugget.set_tasks_list_toggle();
            rah.mod_action_nugget.set_task_completion_submission();
        },
        
        set_tasks_list_toggle: function(){
            $('.action_nugget .tasks_link').click(function(){
                $(this).parents('.action_nugget').find('.task_list').slideToggle();
                return false;
            });
        },
        
        set_task_completion_submission: function(){
            $('.action_nugget .task_list :checkbox').click(function(){
                var form = $(this).parents('form');
                $.post(form.attr('action'), form.serialize(), function(completed_tasks){
                    form.parents('.action_nugget').find('.user_completes').text(completed_tasks);
                    var box = form.find(':checkbox');
                    box.attr('checked', !box.attr('checked'));
                });
                return false;
            });
        },
    },
}