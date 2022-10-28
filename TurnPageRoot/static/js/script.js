console.log("script.js loaded");
let startingPosition;
let currentPosition;
let swipedRight = false;
let swipedLeft = false;

// VALUES
const bookMinHeight = screen.width > 550 ? '100%' : '60vw';

const bookShrinkMinHeight = screen.width > 550 ? '80%' : '40vw';
const rotateValue = 30;

const leftSwipeCutoffPoint = screen.width / 5;
const rightSwipeCutoffPoint = screen.width / (5 / 4);
const horizontalSwipeCutoffPoint = screen.width / 4;
const downSwipeCutoffPoint = screen.height / 7;
let bookshelfMoveValue = screen.width > 991 ? 400 : (screen.width > 600 ? 300 : 100);


//FUNCTIONS
function swipedLeftAnimation() {
    $('.draggable').animate({left: -1000}, 300)
        .css({'transform': 'rotate(-20deg)'})
        .css('opacity', .5)
        .hide("fade", {percent: 0}, 150);
}

function swipedRightAnimation() {
    $('.draggable').animate({left: 1000}, 300)
        .css({'transform': 'rotate(20deg)'})
        .css('opacity', .5)
        .hide("fade", {percent: 0}, 150);
}

function swipedDownAnimation() {
    $('.draggable')
    .css('opacity', .5)
    .hide("fade", {percent: 0}, 150);
}

function flipCard(){
   var card = document.getElementById('card');
document.getElementById('flip').addEventListener('click', function() {
    card.classList.toggle('flipped');
}, false);
}

$('.draggable').draggable({
    data: {
        startingPosition: startingPosition,
        currentPosition: currentPosition,
    },

    drag: function (e, ui) {
        startingPosition = ui.originalPosition;
        currentPosition = ui.position;

        // BOOK ROTATES TOWARDS POSITION
        $('.top-of-stack').css('transform', 'rotate(' + currentPosition.left / rotateValue + 'deg)')
            .css('min-height', bookShrinkMinHeight)
            .css('opacity', 1 - Math.max(Math.abs(currentPosition.left / 1000), Math.abs(currentPosition.top / 1000)))
        ;

        //WHEN SWIPING, MAKE SURE IT DOESN'T SNAP BACK
        // console.log(screen.width, currentPosition.left)
        if (currentPosition.left > horizontalSwipeCutoffPoint) {
            swipedRight = true;
            console.log("swipe right");
            $('.draggable').draggable("option", "revert", false);


        } else if (currentPosition.left < -1 * horizontalSwipeCutoffPoint) {
            $('.draggable').draggable("option", "revert", false);
        } else if (currentPosition.top > downSwipeCutoffPoint) {
            $('.draggable').draggable("option", "revert", false);
        }

    },
    stop: function (e, ui) {
        // RESET ROTATION
        $('.top-of-stack').css('transform', 'rotate(0deg)')
            .css('min-height', bookMinHeight)
            .css('opacity', 100)
        ;


        // LISTENERS FOR SWIPING ACTION
        if (currentPosition.left > horizontalSwipeCutoffPoint) {
            $('.top-of-stack').css('min-height', bookShrinkMinHeight);
            swipedRightAnimation();
        } else if (currentPosition.left < -1 * horizontalSwipeCutoffPoint) {
            $('.top-of-stack').css('min-height', bookShrinkMinHeight);
            swipedLeftAnimation()
        } else if (currentPosition.top > downSwipeCutoffPoint) {
            $('.top-of-stack').css('min-height', bookShrinkMinHeight);
            swipedDownAnimation();
        }

    },
    revert: true,
    cursor: "grabbing",

    revertDuration: 50,
});


$('#swipe-right-btn').click(function () {
    swipedRightAnimation();
});

$('#swipe-left-btn').click(function () {
    swipedLeftAnimation();
});


$('#bookshelf-btn').click(function () {
    $('.draggable').animate({top:bookshelfMoveValue + 'px'}, 200)
    swipedDownAnimation();
});