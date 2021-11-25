/* document.querySelector('#room-name-input').focus();
document.querySelector('#room-name-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#room-name-submit').click();
    }
};*/

document.getElementById('option1').checked = true


document.getElementById('white').onclick = function(e) {
    console.log('checked White')
    document.getElementById('option2').checked = false;
    document.getElementById('option1').checked = true;
}

document.getElementById('black').onclick = function(e) {
    console.log('checked Black')
    document.getElementById('option1').checked = false;
    document.getElementById('option2').checked = true;
}