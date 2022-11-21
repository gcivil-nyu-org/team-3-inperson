console.log('bookshelf.js loaded');

function loadDescriptionOfFirstBook() {
    try {

        let description = $('#book-on-shelf:nth-child(3)').attr("data-book-description");
        $('.on-first-load').append('<p>' + description + '</p>');
    } catch (err) {
        console.log(err + " - Error with loading initial description. See javascript.");
    }
}

loadDescriptionOfFirstBook();


// console.log('first load description: ' + description);
$('.my-bookshelf').flipster(
    {
        style: 'coverflow',
        start: 2,
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
            let description = $('.active').attr("data-book-description");
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