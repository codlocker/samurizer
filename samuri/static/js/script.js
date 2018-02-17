$(document).ready(function () {
    $('select').select();
    $('.modal').modal();
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

function get_selected_lan(res) {
    let qid = $(res).attr("id").split("_")[1];
    let index = res.selectedIndex;
    console.log(qid);
    console.log(index);
}

function add_data(image, score) {
    let image_loc = "/static/images/" + image + ".png";
    let get_modal = $("#chart");
    console.log(get_modal);
    let image_div = $(get_modal).find("#news-image");
    $(image_div).attr("src", image_loc);
    $(image_div).attr("Word Cloud Image");
    let view_analysis = M.Modal.getInstance(get_modal);
    view_analysis.open();
}