$(document).ready(function () {
    $(".toggle-full-content").click(function(event) {
        event.preventDefault();
        let full_content_div = $(this).parent("div").prev().children(".full-content");
        if ($(this).text() === "VIEW FULL ARTICLE") {
            $(full_content_div).slideDown(1500);
            $(this).text("HIDE ARTICLE");
        } else {
            $(full_content_div).slideUp(1500);
            $(this).text("VIEW FULL ARTICLE");
        }
    });
});