console.log("https://github.com/gcivil-nyu-org/team-3-inperson")
$(function () {
    $('.draggable').draggable({
        // axis: 'x',
        cursor: "grabbing"
    });
});

// $(document).ready(function () {
//     $('.fade-out-btn').click(function () {
//         $('.draggable').animate(
//             {deg: 70},
//             {duration: 700,
//             step: function(now){
//                 $(this).css({
//                     transform:'rotate('+now+'deg)'
//                 })
//             }}
//         ).fadeOut(700).promise();
//
//     });
//
// });


// document.addEventListener('mousemove', (event) => {
//     console.log(`(${event.clientX}, ${event.clientY})`);
// });