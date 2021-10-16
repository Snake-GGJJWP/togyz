const color = JSON.parse(document.getElementById('color').textContent);
if (color == "white") {
    var board_ind = [1,2,3,4,5,6,7,8,9];
}
else if (color == "black") {
    var board_ind = [10,11,12,13,14,15,16,17,18]
}

function set_fields_onclick (field, arr_i, arr) {
    let index = field.getAttribute('name');
    console.log(index);
    if (board_ind.includes(parseInt(index))) {
        console.log(field);
        field.onclick = function(e) {
            if (parseInt(field.getAttribute('kum')) > 0) {
                let field_i = parseInt(field.getAttribute('name'));
                let kum = parseInt(field.getAttribute('kum'));
                var endField = (field_i + kum)
                while (endField > 18) {
                    endField = endField%19 + Math.floor(endField/19);
                }
                chatSocket.send(JSON.stringify({
                    'msgType': "move",
                    'message': color + "has made a move",
                    'startField': field_i,
                    'endField': endField
                }))
            }
        };
    }
};

document.querySelectorAll('[class="square"]').forEach(set_fields_onclick);