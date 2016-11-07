jQuery(document).ready(function(){
    $('a.scroll_effect').on('click', function(e){
        target_element = $(this).attr('href');
        scroll_to = $(target_element).offset().top;
        if($(window).scrollTop() != scroll_to && target_element !== undefined){
            // Chrome scroll to calculation and other browser scroll to calculation is different.
            if($.templatemo_is_chrome){
                body_scroll_target = scroll_to;
            }else{
                body_scroll_target = $("body").scrollTop()+scroll_to;
            }
            $('html,body').animate({scrollTop:body_scroll_target},1000);
        }
        // If menu is visible hide the nav.
        $('nav:visible').templateMoMenuHide();
        return false;
    });
    // Javascropt parallax effect config for different browser.
    // Chrome broswer setting
    if($.templatemo_is_chrome){
        $("html").attr("style","overflow:auto;");
        $("body").attr("style","overflow:auto;height:auto;");
        $('#templatemo_home').parallax("50%", 0.1);
        $('#templatemo_contact').parallax("50%", 0.1);
    // Non IE broswer setting
    }else if(!$.templatemo_is_ie){
        $("html").attr("style","overflow: auto;");
        $("body").attr("style","background: #455a64;overflow: auto;height: auto;");
        $('#templatemo_home').parallax("50%", 0.1);
        $('#templatemo_contact').parallax("50%", 0.1);
    // IE broswer setting
    }else{
        $('#templatemo_home').parallax("50%", 0.5);
        $('#templatemo_contact').parallax("50%", 0.5);
    }
});