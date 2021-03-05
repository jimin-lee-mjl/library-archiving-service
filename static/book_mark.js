const URL = '/mark/';
const mark = document.querySelector('.heart-mark');


function handleHeartMark() {
    const book_id = mark.dataset.id;

    if (mark.classList.contains('glyphicon-heart-empty')) {
        const option = {
            method: "POST",
            body: JSON.stringify({
                book_id: book_id,
            }),
            headers: {
                "Content-Type": "application/json",
            },
        };

        fetch(URL, option)
        .then(function(type) {
            return type.json();
        })
        .then(function(result) {
            console.log(result);
        })
        mark.classList.remove('glyphicon-heart-empty');
        mark.classList.add('glyphicon-heart')
    } else {
        const option = {
            method: "DELETE",
            body: JSON.stringify({
                book_id: book_id,
            }),
            headers: {
                "Content-Type": "application/json",
            },
        };
        fetch(URL, option)
        .then(function(type) {
            return type.json();
        })
        .then(function(result) {
            console.log(result);
        })
        mark.classList.remove('glyphicon-heart');
        mark.classList.add('glyphicon-heart-empty')
    }
}


function init() {
    mark.addEventListener('click', handleHeartMark);
}

init();