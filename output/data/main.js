//code copy
$(function() {
    $("pre").append("<button>copy</button>");
});
$(function(){
    const copybtn = $("pre button");
    copybtn.click(function(){
        const code = $(this).parent().find("code").text();
        navigator.clipboard.writeText(code);
    });
});