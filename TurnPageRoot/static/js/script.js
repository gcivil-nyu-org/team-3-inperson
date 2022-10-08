console.log("https://github.com/gcivil-nyu-org/team-3-inperson")
// CLASSES
class BookStack{
    bookStack = [];
    addBook(book){
        this.bookStack.push(book);
    }
    removeBook(book){
        this.bookStack.remove(book);
    }
}

class Book{
    constructor({
                    imageUrl,
                    onDismiss,
                    onLike,
                    onDislike
                }) {
        this.imageUrl = imageUrl;
        this.onDismiss = onDismiss;
        this.onLike = onLike;
        this.onDislike = onDislike;
        this.#init();
    }
    #startPoint;
    #offsetX;
    #offsetY;

    #isTouchDevice = () => {
        return (('ontouchstart' in window) ||
            (navigator.maxTouchPoints > 0) ||
            (navigator.msMaxTouchPoints > 0));
    }

    #init = () => {
        const card = document.createElement('div');
        card.classList.add('card');
        const img = document.createElement('img');
        img.src = this.imageUrl;
        card.append(img);
        this.element = card;
        if (this.#isTouchDevice()) {
            this.#listenToTouchEvents();
        } else {
            this.#listenToMouseEvents();
        }
    }

    #listenToTouchEvents = () => {
        this.element.addEventListener('touchstart', (e) => {
            const touch = e.changedTouches[0];
            if (!touch) return;
            const {clientX, clientY} = touch;
            this.#startPoint = {x: clientX, y: clientY}
            document.addEventListener('touchmove', this.#handleTouchMove);
            this.element.style.transition = 'transform 0s';
        });

        document.addEventListener('touchend', this.#handleTouchEnd);
        document.addEventListener('cancel', this.#handleTouchEnd);
    }

    #listenToMouseEvents = () => {
        this.element.addEventListener('mousedown', (e) => {
            const {clientX, clientY} = e;
            this.#startPoint = {x: clientX, y: clientY}
            document.addEventListener('mousemove', this.#handleMouseMove);
            this.element.style.transition = 'transform 0s';
        });

        document.addEventListener('mouseup', this.#handleMoveUp);

        // prevent card from being dragged
        this.element.addEventListener('dragstart', (e) => {
            e.preventDefault();
        });
    }

    #handleMove = (x, y) => {
        this.#offsetX = x - this.#startPoint.x;
        this.#offsetY = y - this.#startPoint.y;
        const rotate = this.#offsetX * 0.1;
        this.element.style.transform = `translate(${this.#offsetX}px, ${this.#offsetY}px) rotate(${rotate}deg)`;
        // dismiss card
        if (Math.abs(this.#offsetX) > this.element.clientWidth * 0.7) {
            this.dismiss(this.#offsetX > 0 ? 1 : -1);
        }
    }
    // mouse event handlers
    #handleMouseMove = (e) => {
        e.preventDefault();
        if (!this.#startPoint) return;
        const {clientX, clientY} = e;
        this.#handleMove(clientX, clientY);
    }

    #handleMoveUp = () => {
        this.#startPoint = null;
        document.removeEventListener('mousemove', this.#handleMouseMove);
        this.element.style.transform = '';
    }

    // touch event handlers
    #handleTouchMove = (e) => {
        if (!this.#startPoint) return;
        const touch = e.changedTouches[0];
        if (!touch) return;
        const {clientX, clientY} = touch;
        this.#handleMove(clientX, clientY);
    }

    #handleTouchEnd = () => {
        this.#startPoint = null;
        document.removeEventListener('touchmove', this.#handleTouchMove);
        this.element.style.transform = '';
    }

    dismiss = (direction) => {
        this.#startPoint = null;
        document.removeEventListener('mouseup', this.#handleMoveUp);
        document.removeEventListener('mousemove', this.#handleMouseMove);
        document.removeEventListener('touchend', this.#handleTouchEnd);
        document.removeEventListener('touchmove', this.#handleTouchMove);
        this.element.style.transition = 'transform .5s';
        this.element.style.transform = `translate(${direction * window.innerWidth + 200}px, ${this.#offsetY}px) rotate(${45 * direction}deg)`;
        this.element.classList.add('dismissing');
        setTimeout(() => {
            this.element.remove();
        }, 1000);
        if (typeof this.onDismiss === 'function') {
            this.onDismiss();
        }
        if (typeof this.onLike === 'function' && direction === 1) {
            this.onLike();
        }
        if (typeof this.onDislike === 'function' && direction === -1) {
            this.onDislike();
        }
    }
}


// DOM
const swiper = document.querySelector('#swiper');
const like = document.querySelector('#like');
const dislike = document.querySelector('#dislike');

// constants for test books
const img1 = new Image().src = 'static/js/book_covers/american-psycho-670x1024.jpg';
const img2 = new Image().src = 'static/js/book_covers/gatsby-original2.jpg';
const img3 = new Image().src = 'static/js/book_covers/image.jpg';
const img4 = new Image().src = 'static/js/book_covers/image-1.jpg';
const img5 = new Image().src = 'static/js/book_covers/jurrasic.jpg';

const images = [
    img1,
    img2,
    img3,
    img4,
    img5
]

// variables
let cardCount = 0;
let book = null;
let bookStack = new BookStack();

function appendNewCard() {
    book = new Book({
        imageUrl: images[cardCount % 5],
        onDismiss: appendNewCard,
        onLike: () => {
            like.style.animationPlayState = 'running';
            like.classList.toggle('trigger');
        },
        onDislike: () => {
            dislike.style.animationPlayState = 'running';
            dislike.classList.toggle('trigger');
        }
    });
    swiper.append(book.element);
    bookStack.addBook(book);
    cardCount++;

    //ensures that we are talking about only the cards in the stack that are NOT the swiped book
    const cards = swiper.querySelectorAll('.card:not(.dismissing)');
    //this makes the next item in the stack come up to the top
    cards.forEach((card, index) => {
        card.style.setProperty('--i', index);
    });
}


// first 5 cards
for (let i = 0; i < 5; i++) {
    appendNewCard();
}
like.addEventListener('click', () => {
    like.style.animationPlayState = 'running';
    like.classList.toggle('trigger');
    console.log(bookStack)
    bookStack.removeBook(book);
});

dislike.addEventListener('click', () => {
    dislike.style.animationPlayState = 'running';
    dislike.classList.toggle('trigger');
});

document.onmousemove = function(e){
    let pageCoords = "( " + e.pageX + ", " + e.pageY + " )";
    console.log(pageCoords);
}