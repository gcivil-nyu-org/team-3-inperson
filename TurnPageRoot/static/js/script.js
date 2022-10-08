console.log("https://github.com/gcivil-nyu-org/team-3-inperson")
$('.draggable').draggable({
    // axis: 'x',
    cursor: "grabbing"
}).addEventListener('dragstart', (e) => {
    e.preventDefault();
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