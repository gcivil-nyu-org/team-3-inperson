console.log('bookshelf.js loaded');

function loadDescriptionOfFirstBook() {
    let description = $('#book-on-shelf').attr("data-book-description");
    $('.on-first-load').append('<p>' + description + '</p>');
}
loadDescriptionOfFirstBook();


// console.log('first load description: ' + description);
$('.my-bookshelf').flipster(
    {
        style: 'coverflow',
        start: 'center',
        pauseOnHover: true,
        touch: true,
        buttons: true,
        fadeIn: 300,
        scrollwheel: false,
        // nav: 'after',
        onItemSwitch: function (currentItem, previousItem) {
            $(currentItem).addClass('active');
            $(previousItem).removeClass('active');
            $('.description-of-book').empty()
            description = $('.active').attr("data-book-description");
            console.log(description)
            $('.description-of-book').append('<p>' + description + '</p>');


        }
    }
);

const liked_books = JSON.parse(JSON.parse(document.getElementById('liked_books').textContent));
const bookImageElements = document.getElementsByClassName('book-cover-img');


//

// $('#card').flip({
//     trigger: 'manual',
// })
//
// $('#description-1').click(function () {
//     $('#card').flip('toggle');
// });