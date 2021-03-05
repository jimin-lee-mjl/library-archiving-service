const input = document.querySelector('input#rating'),
spans = document.querySelectorAll('span.comment-star'),
update_btn = document.querySelector('#update_btn');


// 별점 주기
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


// comment 업데이트 
function handleUpdateBtn(event) {
    const update_field = document.querySelector('.comment_field-wrapper');
    const cancel_btn = document.querySelector('#cancel_btn');
    event.preventDefault();
    update_field.classList.remove('invisible');
    cancel_btn.addEventListener('click', function(event) {
        event.preventDefault();
        update_field.classList.add('invisible');
    })
}


function init() {
    getRatingValue();
    update_btn.addEventListener('click', handleUpdateBtn);
}


init();


