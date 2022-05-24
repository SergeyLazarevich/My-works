$(document).on("click", "ul a", function (e) {
    e.preventDefault();
    let id = $(this).attr('href');
    let top = $(id).offset().top;
    $('body, html').animate({
        scrollTop: top
    }, 500);
});

$(document).on("click", ".go_to_top", function (e) {
    e.preventDefault();
    $('body, html').animate({
        scrollTop: 0
    }, 500);
});

