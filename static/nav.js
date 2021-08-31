const hamburgerBars = document.getElementsByClassName("hamburger")[0];
const closeHamburgerBox = document.getElementsByClassName("close-hamburger")[0];
const topBar = document.getElementsByClassName("top")[0]
const middleBar = document.getElementsByClassName("middle")[0]
const bottomBar = document.getElementsByClassName("bottom")[0]
const nav = document.getElementsByClassName('nav')[0]

hamburgerBars.addEventListener("click", (e) => handleDropDown(e));
closeHamburgerBox.addEventListener('click', closeDropDown);

function handleDropDown(e) {
    if (hamburgerBars.classList.contains('bars')) {
        nav.classList = 'nav'
        hamburgerBars.classList = 'hamburger cross';
        closeHamburgerBox.style.visibility = 'visible';

        topBar.classList = 'top bar cross-top'
        middleBar.classList = 'middle bar cross-middle'
        bottomBar.classList = 'bottom bar cross-bottom'
    } else {
        closeDropDown()
    }
}

function closeDropDown() {
    nav.classList = 'nav closed'
    hamburgerBars.classList = 'hamburger bars'
    closeHamburgerBox.style.visibility = 'hidden'
    
    topBar.classList = 'top bar'
    middleBar.classList = 'middle bar'
    bottomBar.classList = 'bottom bar'
}