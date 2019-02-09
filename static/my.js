console.log("banana pancakes")
$(document).ready(function(){
    $(".btn").click(function(){
        pattern_name = $(this)[0].id;
        url = "/pattern/".concat(pattern_name);
        $.get(url);
    });

});
