console.log("https://github.com/gcivil-nyu-org/team-3-inperson")

let startingPosition;
let currentPosition;
let swipedRight = false;
let swipedLeft = false;

// VALUES
let shrinkValue = 45;
let rotateValue = 30;


$('.draggable').draggable({
    data: {
        startingPosition: startingPosition,
        currentPosition: currentPosition,
    },

    drag: function (e, ui) {
        startingPosition = ui.originalPosition;
        currentPosition = ui.position;
        // console.log(currentPosition);
        // TODO screen width calculation

        // BOOK ROTATES TOWARDS POSITION
        $('.book-cover-img').css('transform', 'rotate(' + currentPosition.left / rotateValue + 'deg)')
            .css('width', shrinkValue + '%')
            .css('opacity', 1 - Math.abs(currentPosition.left / 700))

        ;


        //WHEN SWIPING, MAKE SURE IT DOESN'T SNAP BACK
        if (currentPosition.left > 300) {
            swipedRight = true;
            console.log("swipe right");
            $('.draggable').draggable("option", "revert", false);


        } else if (currentPosition.left < -300) {
            console.log("swipe left");
            $('.draggable').draggable("option", "revert", false);
        } else if (currentPosition.top > 300) {
            console.log("swipe down");
            $('.draggable').draggable("option", "revert", false);
        }

    },
    stop: function (e, ui) {
        // RESET ROTATION
        $('.book-cover-img').css('transform', 'rotate(0deg)')
            .css('width', '50%')
            .css('opacity', 100)
        ;


        // LISTENERS FOR SWIPING ACTION
        if (currentPosition.left > 300) {
            $('.book-cover-img').css('width', shrinkValue + '%');
            $('.draggable').animate({left: 1000}, 300)
                .css({'transform': 'rotate(20deg)'})
                .hide("fade", {percent: 0}, 150);
        } else if (currentPosition.left < -300) {
            $('.book-cover-img').css('width', shrinkValue + '%');
            $('.draggable').animate({left: -1000}, 300)
                .css({'transform': 'rotate(-20deg)'})
                .hide("fade", {percent: 0}, 150);
        } else if (currentPosition.top > 300) {
            $('.book-cover-img').css('width', shrinkValue + '%');
            $('.draggable').hide("scale", {percent: 0}, 150);
        }

    },
    revert: true,
    cursor: "grabbing",

    revertDuration: 50,
});
