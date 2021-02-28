const input = document.querySelector('input#rating'),
spans = document.querySelectorAll('span.comment-star');


function fillStars(value) {
    for (let i=0; i<value; i++) {
        spans[i].classList.add('glyphicon-star');
        spans[i].classList.remove('glyphicon-star-empty');
    }
    for (let i=0; i<5-value; i++) {
        span = spans[4-i];
        console.log('fill')
        if (span.classList.contains('glyphicon-star')) {
            span.classList.add('glyphicon-star-empty');
            span.classList.remove('glyphicon-star');
        }
    }
    console.log('fill2')
}


function getRatingValue() {
    spans.forEach(span => span.addEventListener('click', function() {
        const rating = span.dataset.rating;
        input.value = rating;
        fillStars(rating);
        console.log(rating);
    }))
}


function init() {
    getRatingValue();
}

init();


