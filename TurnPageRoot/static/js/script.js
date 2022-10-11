console.log("https://github.com/gcivil-nyu-org/team-3-inperson")

let startingPosition;
let currentPosition;
let swipedRight = false;
let swipedLeft = false;

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
            if (currentPosition.left > 300) {
                swipedRight = true;
                console.log("swipe right");
                $('.draggable').draggable("option","revert", false);


            }
            else if (currentPosition.left < -300) {
                console.log("swipe left");
                $('.draggable').draggable("option","revert", false);
            }
            else if (currentPosition.top > 300) {
                console.log("swipe down");
                $('.draggable').draggable("option","revert", false);
            }

    },
    stop: function(e, ui) {
        if(currentPosition.left > 300){
            $('.draggable').animate({left: 1000}, 300).css(
                {'transform': 'rotate(20deg)'}
            );
        }
        else if (currentPosition.left < -300){
            $('.draggable').animate({left: -1000}, 300).css(
                {'transform': 'rotate(-20deg)'}
            );
        }
        else if(currentPosition.top > 300){
            $('.draggable').hide("scale", {percent: 0}, 150);
        }

    },
    revert: true,
    cursor: "grabbing",

    revertDuration: 50,
});
