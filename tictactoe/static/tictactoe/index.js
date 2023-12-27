const x = 'X';
const o = 'O';
var player_as;
var my_turn = true;
// Tic Tac Toe game board; two dimenstional array
let two_d_arr = [['','',''],['','',''],['','','']];
var connection = true;

document.addEventListener('DOMContentLoaded', () => {
    
    // Accessing different elements for detecting different page
    let about_page = document.getElementById('about_contact');
    let cha_pass_div = document.getElementById('change_pass_div');
    let input = document.getElementById('join_input');
    let enter_game = document.getElementById('enter_div');
    let page_player = document.getElementById('player-container');
    let board = document.getElementById('game_board');
    let generated_room = document.getElementById('wait_to_join');
    let index_page = document.getElementById("index_page");

    if (input || index_page || enter_game || about_page || cha_pass_div){
        // Delete the previous connections for this user, if existed.
        fetch('delete_current_connection')
        .then(respnse => respnse.json())
        .then(result => {console.log(result.message)})
    }

    if (input){
      
        var submit = document.getElementById('join_submit');
        submit.disabled = true;

        // When the user types in the input field, make abled the button
        input.addEventListener('keyup', () => {
            if (input.value.length > 0){
                submit.disabled = false;
            }else{
                submit.disabled = true;
            }
        })
    }

    if (enter_game){

        let create_btn = document.getElementById('create');
        let join_btn = document.getElementById('join');

        create_btn.onclick = () => {
            if (confirm("Are you sure to create the room?")){
                window.location = 'http://127.0.0.1:8000/create_room';
            }
        }

        join_btn.onclick = () => {
            window.location = 'http://127.0.0.1:8000/join_room';
        }
    
    }

    if (generated_room){
        // Check every 2 seconds if another user joined the room or not
        setInterval(checkForJoining, 2000);
    }

    
    if (board){
        var usr_id;
        var usr_name;
        
        // Check if another player already made a move
        // check_move();

        // Fetching the current user
        fetch('cur_usr')
        .then(response => response.json())
        .then(user => {
            usr_id = user.id;
            usr_name = user.name;
        })


        const room_code = document.getElementById('hidden_input').value;

        const socket_url = `ws://${window.location.host}/ws/playing/${room_code}/`;

        const matchSocket = new WebSocket(socket_url);

        matchSocket.onmessage = (e) => {
            const data = JSON.parse(e.data);

            // Check if any player lefts the game match first
            if (data.row === 'none' && data.column === 'none' && data.id === 'none'){
                alert("If one of the players refreshes the game or lefts the game the current game will be terminated.");
                matchSocket.close();
            }

            // Since the id of board cells are the rows and colums, we make the id back
            let cell_id = data.row + data.column;
            let cell = document.getElementById(cell_id);

            // Access to the row and column of clicked cell accordingly
            let row = parseInt(data.row);
            let column = parseInt(data.column);
            
            // Check the data for playing game move
            if (data.id === usr_id){
                // Fill the two dimenstional array accordingly
                two_d_arr[row][column] = x;

                // Change the turn to another user
                my_turn = false;

                // Fill the tictactoe board cell accordingly
                cell.innerHTML = player_as;
            } else {
                // Fill the two dimenstional array accordingly
                two_d_arr[row][column] = o;

                // Change the turn to me
                my_turn = true;

                if (player_as === x){
                    cell.innerHTML = o;
                } else {
                    cell.innerHTML = x;
                }
            }

            // Every time the players move, check for winner, looser or tie.
            let result = tie(two_d_arr);
            

            if (result){
                if (result === "Tie"){
                    alert('Tie, Game Over.');
                } else if (result === x){
                    alert(`Congrutulations, You Won.`);
                } else {
                    alert("Sorry, you lost");
                }

                // window.location = 'http://127.0.0.1:8000/room';
                reset_game();
            }      

        }

        matchSocket.onclose = (e) => {
            console.error("Match socket closed unexpectedly. ", e);
            // Every time the connection closes, reset the game board
            window.location = 'http://127.0.0.1:8000/room';
        }

            
        // If the user lefts the page or refreshes the page, disconnect the current game connection.
        window.onbeforeunload = function() {
            matchSocket.send(JSON.stringify({
                'row': 'none',
                'column': 'none',
                'id': 'none'
            }));
        };
    


        // Adding event listener to all game board boxes for clicking the user
        document.querySelectorAll('.child').forEach(item => {
            // Those cells which are not filled yet, need to be clicked
            item.addEventListener('click', event => {
                
                // Check that it should be the user's turn 
                if (my_turn){
                    // Check if the cell is moved already
                    if (event.target.textContent.trim() === ''){
                        // Handle click
                        let id = event.target.id;
                        let my_array = id.split("");
                        let row = my_array[0];
                        let column = my_array[1];
                                                                                                                            
                        matchSocket.send(JSON.stringify({
                            'row': row,
                            'column': column,
                            'id': usr_id
                        }))
                    } else {
                        alert("This move is already made.");
                    }
                } else {
                    alert("It is not your turn. Please wait!");
                }
                
            })
        })

        board.style.display = 'none';
        let button1 = document.getElementById('as_x');
        let button2 = document.getElementById('as_o');

        button1.onclick = () => {
            if (confirm('You will play as X.')){
                // TODO 
                player_as = x;
                board.style.display = 'grid';
                page_player.style.display = 'none';
                check_move();
            }
        
        }

        button2.onclick = () => {
            if (confirm('You will play as O.')){
                // TODO 
                player_as = o;
                board.style.display = 'grid';
                page_player.style.display = 'none';
                check_move();
            }
        }
    }
})


function tie(tictactoe){
    let x_winner = ['X','X','X'];
    let o_winner = ['O', 'O', 'O'];
    let temp3 = [];
    let num = 0;
    for (let i=0; i < tictactoe.length; i++){
        let temp1 = [];
        let temp2 = [];
        for (let j=0; j < tictactoe.length; j++){
            temp1.push(tictactoe[i][j]);
            temp2.push(tictactoe[j][i]);
            if (i === j){
                temp3.push(tictactoe[i][j]);
            }

            if (tictactoe[i][j]){
                num += 1;
            }
        }
        if (temp1.toString() === x_winner.toString() || temp1.toString() === o_winner.toString()){
            return temp1[0];
        }
        if (temp2.toString() === x_winner.toString() || temp2.toString() === o_winner.toString()){
            return temp2[0];
        }
    }

    if (temp3.toString() === x_winner.toString() || temp3.toString() === o_winner.toString()){
            return temp3[0];
        }

    temp3 = [tictactoe[0][2], tictactoe[1][1], tictactoe[2][0]];
    if (temp3.toString() === x_winner.toString() || temp3.toString() === o_winner.toString()){
            return temp3[0];
        }

    if (num === 9){
        return 'Tie';
    }
    return false;
}


function checkForJoining(){
    fetch('is_joined')
    .then(respnse => respnse.json())
    .then(result => {
        if (result.connected){
            window.location = 'http://127.0.0.1:8000/room';
        }
    })
}


function reset_game(){
    // Reset the two dimenstional array
    two_d_arr = [['','',''],['','',''],['','','']];
    // Make my turn to true
    my_turn = true

    // Now remove all moves from tic tac toe game board
    document.querySelectorAll('.child').forEach(item => {
        item.innerHTML = '';
    })
}

function check_move(){
    console.log('check funckon is called.');
    // Loop throug board if another player has already a move
    document.querySelectorAll('.child').forEach(item => {
        if (item.innerHTML === player_as){
            console.log("Item is equal to my selection.");
            if (player_as === x){
                item.innerHTML = o;
            } else {
                item.innerHTML = x;
            }
        }
    })
}