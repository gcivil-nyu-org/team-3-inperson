console.log('bookshelf.js loaded');
$('.my-bookshelf').flipster(
    {
        style: 'coverflow',
        pauseOnHover: true,
        touch: true,
        buttons: true,
        fadeIn: 300,
        scrollwheel: false,
        // nav: true,
        onItemSwitch: function (currentItem, previousItem) {
            console.log(currentItem);
            $(currentItem).addClass('active');
            $(previousItem).removeClass('active');
            $('.description-of-book').empty()
            let description = $('.active').attr("data-book-description");
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