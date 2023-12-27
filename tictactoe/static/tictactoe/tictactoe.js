const x = 'X';
const o = 'O';
var my_turn = true;
var player_as;
// Tic Tac Toe game board; two dimenstional array
let two_d_arr = [['','',''],['','',''],['','','']];


document.addEventListener('DOMContentLoaded', () => {
    player_as = document.getElementById('plyr').value;
    let ai_turn = document.getElementById('ai_turn');

        if (player_as === o){
            let move = minimax(two_d_arr);
            change(move);
            my_turn = true;
        }
        // Adding event listener to all game board boxes for clicking the user
        document.querySelectorAll('.child').forEach(item => {
            // Those cells which are not filled yet, need to be clicked
            item.addEventListener('click', event => {
                if (my_turn){
                    if (event.target.textContent.trim() === ''){
                        // Handle click
                        let id = event.target.id;
                        let my_array = id.split("");
                        let row = parseInt(my_array[0]);
                        let column = parseInt(my_array[1]);
                        
                        two_d_arr[row][column] = player_as;
                        event.target.innerHTML = player_as;
                        
                        my_turn = false;
                        // Check for the winner after user made a move, before AI moves
                        if (!terminate(two_d_arr)){
                            ai_turn.innerHTML = "Computer thinking...";
                            setTimeout(function(){
                                // Now it's time for AI move
                                let move = minimax(two_d_arr);
                                if (move){
                                    change(move);
                                }
                                // Check for termination
                                terminate(two_d_arr);
                                my_turn = true;
                                ai_turn.innerHTML = "";
                            }, 2000);
                        }
   
                    } else {
                        alert("This move is already made.");
                    }
                } else {
                    alert("Please wait, it's not your turn.");
                }
                
            })
        })
})

function change(move){
    let ai_row = move[0];
    let ai_column = move[1];
    let cell_id = ai_row.toString() + ai_column.toString();
    let cell = document.getElementById(cell_id);

    two_d_arr = result(two_d_arr, move);

    if (player_as === x){
        cell.innerHTML = o;
    } else {
        cell.innerHTML = x;
    }
}


function terminate(board){
    if (winner(board)){
        if (winner(board) === player_as){
            alert("Game over, congratulations you won.");
        } else {
            alert("Sorry, you lost");
        }
        window.location = window.location;
        return true;
    }

    if (terminal(board)){
        alert("Game over, tie");
        window.location = window.location;
        return true;
    }

    return false;
}


function player(board){
    let num_of_o = 0;
    let num_of_x = 0;

    for (let i=0; i<board.length; i++){
        for (let j=0; j<board.length; j++){
            if (board[i][j] === x){
                num_of_x += 1;
            } 
            if (board[i][j] === o){
                num_of_o += 1;
            }
        }
    }

    if (num_of_o > num_of_x){
        return x;
    } else if (num_of_o < num_of_x){
        return o;
    } else {
        return x;
    }
}

// Needs changes Achtung
function actions(board){
    var acts = [];
    for (let i=0; i<board.length; i++){
        for (let j=0; j<board.length; j++){
            if (board[i][j] === ""){
                acts.push([i, j]);
            }
        }
    }

    return acts;
}

function result(board, action){
    let new_board = JSON.parse(JSON.stringify(board)); 

    if (board[action[0]][action[1]]){
        throw new Error('Invalid action');
    }

    let turn = player(board);
    new_board[action[0]][action[1]] = turn;
    
    return new_board;
}


function terminal(board){
    if (winner(board)){
        return true;
    }

    let num = 0;
    for (let i=0; i<board.length; i++){
        for (let j=0; j<board.length; j++){
            if (board[i][j]){
                num += 1;
            }
        }
    }

    if (num === 9){
        return true;
    }else {
        return false;
    }
}


function winner(tictactoe){
    let x_winner = ['X','X','X'];
    let o_winner = ['O', 'O', 'O'];
    
    let temp3 = [];

    for (let i=0; i < tictactoe.length; i++){
        let temp1 = [];
        let temp2 = [];
        for (let j=0; j < tictactoe.length; j++){
            temp1.push(tictactoe[i][j]);
            temp2.push(tictactoe[j][i]);
            if (i === j){
                temp3.push(tictactoe[i][j]);
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

    return false;
} 

function utility(board){
    if (winner(board) === x){
        return 1;
    } else if (winner(board) === o){
        return -1;
    }
    else {
        return 0;
    }

}

function minimax(board){
    // First check for terminal
    if (terminal(board)){
        return null;
    }

    // Check who's turn it is
    var trn = player(board);
    
    var results_list = [];
    var actions_list = [];

    if (trn === x){
        for (let a of actions(board)){
            actions_list.push(a);
            let return_result = min_val(result(board, a));
            results_list.push(return_result);
        
            if (return_result === 1){
                break;
            }
        }
        
        let max_of_results = Math.max(...results_list);

        let index_of_max = results_list.indexOf(max_of_results);

        let move = actions_list[index_of_max];
        return move;
    } else {
        for (let a of actions(board)){
            actions_list.push(a);
            let return_result = max_val(result(board, a));
            results_list.push(return_result);
        
            if (return_result === -1){
                break;
            }
        }
        
        let min_of_results = Math.min(...results_list);

        let index_of_min = results_list.indexOf(min_of_results);

        let move = actions_list[index_of_min];
        return move;
    }
}

function max_val(board){
    if (terminal(board)){
        return utility(board);
    }

    let v = -Infinity;

    for (let a of actions(board)){
        v = Math.max(v, min_val(result(board, a)));

        if (v === 1){
            break;
        }
    }
    return v;
}

function min_val(board){
    if (terminal(board)){
        return utility(board);
    }

    let v = +Infinity;

    for (let a of actions(board)){
        v = Math.min(v, max_val(result(board, a)));
        if (v === -1){
            break;
        }
    }
    return v;
}





