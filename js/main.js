const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
document.getElementById("key").value = urlParams.get('key');
printBoard();

var newGame = (key)=>{
    // instantiate a headers object
    var myHeaders = new Headers();
    // add content type header to object
    myHeaders.append("Content-Type", "application/json");
    // using built in JSON utility package turn object to string and store in a variable
    var raw = JSON.stringify({"key":key}, null, 2);
    // create a JSON object with parameters for API call and store in a variable
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    // Update UI
    document.getElementById("call").innerHTML = "POST /newGame<br/><pre>" + raw + "</pre>";
    document.getElementById("response").innerHTML = "";
    document.getElementById("game_id").value = "";
    document.getElementById("guess").value = "";
    var json_data;
    // make API call with parameters and use promises to get response
    fetch("https://MY_API.execute-api.us-east-1.amazonaws.com/dev", requestOptions)
    .then(response => response.text())
    .then(data => json_data = data)
    .then(() => printResults(json_data))
    .catch(error => console.log('error', error));
    }

var submitGuess = (key, game_id, guess)=>{
    // instantiate a headers object
    var myHeaders = new Headers();
    // add content type header to object
    myHeaders.append("Content-Type", "application/json");
    // using built in JSON utility package turn object to string and store in a variable
    var raw = JSON.stringify({"key":key, "game_id":game_id, "guess":guess}, null, 2);
    // create a JSON object with parameters for API call and store in a variable
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    document.getElementById("call").innerHTML = "POST /submitGuess<br/><pre>" + raw + "</pre>";
    document.getElementById("guess").value = "";
    document.getElementById("response").innerHTML = "";
    var json_data;
    // make API call with parameters and use promises to get response
    fetch("https://MY_API.execute-api.us-east-1.amazonaws.com/dev", requestOptions)
    .then(response => response.text())
    .then(data => json_data = data)
    .then(() => printResults(json_data))
    .catch(error => console.log('error', error));
}

function printResults (json_data) {
    var o = JSON.parse(json_data)
    document.getElementById("response").innerHTML = "<pre>" + JSON.stringify(o, null, 2) + "</pre>"
    if (o.body.game_id != null) {
        document.getElementById("game_id").value = o.body.game_id;
        document.getElementById("guess").focus();
    }
    printBoard (json_data);
}

function printBoard (json_data = '{"body":""}'){
    g = JSON.parse(json_data).body.guesses;
    c = JSON.parse(json_data).body.checks;

    const gameBoard = document.getElementById("board");
    gameBoard.innerHTML = "";
    var rowCounter = 0;
    var correct = [];
    var misplaced = [];
    var incorrect = [];
    if (g) {
        for (var i = 0; i < g.length; i++) {
        let row = document.createElement("div");
        row.classList.add("row");
        gameBoard.appendChild(row)
        str = g[i];
        chk = c[i];
        rowCounter++;
        for (var j = 0; j < str.length; j++) {
            let tile = document.createElement("div");
            tile.classList.add("tile");
            tile.innerHTML = str.charAt(j);
            row.appendChild(tile);
            if (chk[j] == 1) {
                tile.classList.add("correct");
                correct.push(str.charAt(j));
            }
            else if (chk[j] == 2) {
                tile.classList.add("misplaced");
                misplaced.push(str.charAt(j));
            }
            else incorrect.push(str.charAt(j));    
            }
        }
    }
    for (rowCounter; rowCounter < 6; rowCounter++) {
        let row = document.createElement("div");
        row.classList.add("row");
        gameBoard.appendChild(row)

        for (var i = 0; i < 5; i++) {
            let tile = document.createElement("div");
            tile.classList.add("tile");
            row.appendChild(tile);
        }
    }
    let keyboard = [];
    keyboard[0] = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'];
    keyboard[1] = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'];
    keyboard[2] = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
    
    for (rowCounter = 0; rowCounter < 3; rowCounter++) {
        let row = document.createElement("div");
        row.classList.add("keyboard-row");
        gameBoard.appendChild(row)

        for (var i = 0; i < keyboard[rowCounter].length; i++) {
            let tile = document.createElement("div");
            tile.innerHTML = keyboard[rowCounter][i];
            tile.classList.add("keyboard-tile");
            if(correct.includes(keyboard[rowCounter][i])) {
                tile.classList.add("correct");
            }
            else if(misplaced.includes(keyboard[rowCounter][i])) {
                tile.classList.add("misplaced");
            }
            else if(incorrect.includes(keyboard[rowCounter][i])) {
                tile.classList.add("incorrect");
            }
            row.appendChild(tile);
        }
    }  
}