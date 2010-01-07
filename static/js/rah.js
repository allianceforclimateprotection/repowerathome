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
            // Funnel step 1: Start on registration page
            _gaq.push(['_trackPageview', '/reg/start']);
            
            // Set up a dialog window for opening later
            $('#dialog').dialog({ 
                buttons: {
                    "Finish Registration": function() { 
                        // Funnel step 3: Post registration questions submitted
                        _gaq.push(['_trackPageview', '/reg/questions']);
                        
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
                                // (idea from Eric: Replace form with new form markup from django that inlcudes the errors)
                                alert(response['errors']);
                                return;
                            } else {
                                // Set the action of the profile form with the freshly minted user id
                                $("#profile_form").attr("action", "/user/edit/" + response['userid'] + "/");
                                
                                // Show the dialog with profile form
                                $('#dialog').dialog('open');
                                
                                // Funnel step 2: Post registration questions popped up
                                _gaq.push(['_trackPageview', '/reg/questions']);
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
            
            var sin = [], cos = [];
            for (var i = 0; i < 14; i += 0.5) {
                sin.push([i, Math.sin(i)]);
                cos.push([i, Math.cos(i)]);
            }
            
            var userData = [
                [1261575504000, 0],
                [1262434528000, 10],
                [1262736000000, 25],
                [1262736000000, 30],
            ];
            
            var tips = [
                ["You joined Repower@Home"],
                ["Install the shower head"],
                ["Buy a low-flow shower head"],
                ["Size your water heater" + "Buy a low-flow shower head"],
            ];

            var plot = $.plot($("#placeholder"),
                   [ { data: userData }], {
                       series: {
                           lines: { show: true },
                           points: { show: true, radius: 10 },
                           shadowSize: 5,
                       },
                       grid: { hoverable: true, clickable: true, backgroundColor: { colors: ["#DDD", "#FFF"] } },
                       legend: {show: false},
                       xaxis: {mode: "time", max: 1262982147000}
                     });

            function showTooltip(x, y, index) {
                console.log(index);
                $('<div id="tooltip">' + tips[index] + '</div>').css( {
                    position: 'absolute',
                    display: 'none',
                    width: 200,
                    top: y - 18,
                    left: x + 25 ,
                    border: '2px solid #000',
                    padding: '5px',
                    'background-color': '#fee',
                }).appendTo("body").fadeIn(300);
            }

            // var previousPoint = null;
            $("#placeholder").bind("plothover", function (event, pos, item) {
                // console.log(item.toSource());
                if (item) {
                    // if (previousPoint != item.datapoint) {
                    //     previousPoint = item.datapoint;

                        // $("#tooltip").remove();
                        
                    // }
                    showTooltip(item.pageX, item.pageY, item.dataIndex);
                }
                else {
                    $("#tooltip").remove();
                    previousPoint = null;            
                }
            });


            
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
            $("#house_party_form").validate({
                rules: {
                    phone_number: { required: true, },
                },
            });
            $('.house_party').click(function(){ $('#house_party_dialog').dialog('open'); return false; });
        },
        
        create_dialog: function(){
            $('#house_party_dialog').dialog({
                title: 'House Parties',
                buttons: {
                    "Give me a call": function() {
                        $('#house_party_form').submit();
                    },
                },
                modal: true,
                resizable: false,
                draggable: false,
                autoOpen: false, 
            });
        },
        
    },
}