console.log("script.js loaded");
let startingPosition;
let currentPosition;
let swipedRight = false;
let swipedLeft = false;

// VALUES
const bookWidth = screen.width > 991 ? 50 : (screen.width > 600 ? 70 : 90);

const shrinkValue = bookWidth * .9;
const rotateValue = 30;

const leftSwipeCutoffPoint = screen.width / 5;
const rightSwipeCutoffPoint = screen.width / (5 / 4);
const horizontalSwipeCutoffPoint = screen.width / 5;
const downSwipeCutoffPoint = screen.height / 7;
let bookshelfMoveValue = screen.width > 991 ? 400 : (screen.width > 600 ? 300 : 100);


//FUNCTIONS
function swipedLeftAnimation() {
    $('.draggable').animate({left: -1000}, 300)
        .css({'transform': 'rotate(-20deg)'})
        .hide("fade", {percent: 0}, 150);
}

function swipedRightAnimation() {
    $('.draggable').animate({left: 1000}, 300)
        .css({'transform': 'rotate(20deg)'})
        .hide("fade", {percent: 0}, 150);
}

function swipedDownAnimation() {
    $('.draggable').hide("scale", {percent: 0}, 150);
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
            .css('width', shrinkValue + '%')
            .css('opacity', 1 - Math.abs(currentPosition.left / 700))

        ;

        //WHEN SWIPING, MAKE SURE IT DOESN'T SNAP BACK
        // console.log(screen.width, currentPosition.left)
        if (currentPosition.left > horizontalSwipeCutoffPoint) {
            swipedRight = true;
            console.log("swipe right");
            $('.draggable').draggable("option", "revert", false);


        } else if (currentPosition.left < -1 * horizontalSwipeCutoffPoint) {
            // console.log("swipe left");
            $('.draggable').draggable("option", "revert", false);
        } else if (currentPosition.top > downSwipeCutoffPoint) {
            // console.log("swipe down");
            $('.draggable').draggable("option", "revert", false);
        }

    },
    stop: function (e, ui) {
        // RESET ROTATION
        $('.top-of-stack').css('transform', 'rotate(0deg)')
            .css('width', bookWidth + '%')
            .css('opacity', 100)
        ;


        // LISTENERS FOR SWIPING ACTION
        if (currentPosition.left > horizontalSwipeCutoffPoint) {
            $('.top-of-stack').css('width', shrinkValue + '%');
            swipedRightAnimation();
        } else if (currentPosition.left < -1 * horizontalSwipeCutoffPoint) {
            $('.top-of-stack').css('width', shrinkValue + '%');
            swipedLeftAnimation()
        } else if (currentPosition.top > downSwipeCutoffPoint) {
            $('.top-of-stack').css('width', shrinkValue + '%');
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