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
}