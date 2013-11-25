$(function() {

    if(Modernizr.history){

    var newHash      = "",
        $mainContent = $("#main-content"),
        $container    = $("#container"),
        baseHeight   = 0,
        $el;
        
    $container.height($container.height());
    baseHeight = $container.height() - $mainContent.height();
    
    $("#urlform").submit(function(event) {
        _link = $("#urlinput").val();
        //history.pushState(null, null, _link);
        loadContent(_link);
        event.preventDefault();
    });

    function loadContent(href){
        if (!href) { return; } // went to /, no query
        alert(href);
        $mainContent
                .find("#guts")
                .fadeOut(200, function() {
                    $mainContent.hide().load('/' + href + " #guts", function() {
                        $mainContent.fadeIn(200, function() {
                            $container.animate({
                                height: baseHeight + $mainContent.height() + "px"
                            });
                        });
                        //$("nav a").removeClass("current");
                        console.log(href);
                        //$("nav a[href$="+href+"]").addClass("current");
                    });
                });

        $('html, body').animate({
            scrollTop: $("#guts").offset().top
            }, 2000);
    }
    
    $(window).bind('popstate', function(){
       _link = location.pathname.replace(/^.*[\\\/]/, ''); //get filename only
       loadContent(_link);
    });

} // otherwise, history is not supported, so nothing fancy here.

    
});