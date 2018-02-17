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
    let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    let lang_dict = $(res).find("option").eq(index).text();
    let formData = [];
    formData.push({"name": "csrfmiddlewaretoken", "value": csrf_token});
    formData.push({"name": "question_id", "value": qid});
    formData.push({"name": "language", "value" : lang_dict});
    $.ajax({
        'url': "/parse_lang/",
        'type': "POST",
        'dataType': "json",
        'data': formData,
        beforeSend: function () {
            M.toast({html: "Parsing Data..."});
        }, success: function (response) {
            if(response.id === 200) {
                let className1 = ".content-details-" + qid;
                let className2 = ".summary-" + qid;
                $(className1).html(response.content);
                $(className2).html(response.summary);
            }
        }, error: function (xhr, textStatus, errorThrown) {
            console.log("Please report this error: " + errorThrown + " " + xhr.status);
            res = false;
        } 
    });
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