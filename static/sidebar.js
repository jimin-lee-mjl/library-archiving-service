// function handleNavClick() {
//     const ul = document.querySelector('nav#sidebar ul');
//     const navs = ul.querySelectorAll('li');
//     navs.forEach(nav => nav.addEventListener('click', function() {
//         navs.forEach(_nav => {
//             if (_nav.classList.contains('active')) {
//                 _nav.classList.remove('active');
//             }
//         })
//         nav.classList.add('active');
//     }))
// }

// function init() {
//     handleNavClick();
// }

// init();

$(function() {
    const $ul = $('nav#sidebar ul');
    const $navs = $ul.find('li');

    const nav_id = localStorage.getItem('nav-id');
    if (nav_id) {
        $navs.find('#'+nav_id).addClass('active');
    }
    
    $navs.on('click', function() {
        $navs.find('.active').removeClass('active');
        $(this).addClass('active');
        const $id = $(this).attr('id');
        localStorage.setItem('nav-id', $id);
    })
});