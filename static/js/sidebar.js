const ul = document.querySelector('nav#sidebar ul.navigation');
const navs = ul.querySelectorAll('li');


function activateNav(nav_id) {
    navs.forEach(li => {
        if (li.dataset.id === nav_id) {
            li.classList.add('active');
        }
    })
}


function highlightNav() {
    if (location.pathname.split('/')[1] === 'book') {
        activateNav('library');
    } else if (location.pathname.split('/')[1] === 'search') {
        activateNav('search');
    } else if (location.pathname.split('/')[1] === 'archive') {
        if (location.pathname.split('/')[2] === 'marks') {
            activateNav('marked_books');
        } else {
            activateNav('book_archive');
        }
    } else {
        activateNav('dashboard');
    }
}


function init() {
    highlightNav();
}


init();
