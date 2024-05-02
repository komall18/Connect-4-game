document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('connect4-board');
    const resetBtn = document.getElementById('reset-btn');
    let currentPlayer = 1; // Player 1 starts the game
    let gameWon = false;

    // Initialize the board
    for (let row = 0; row < 6; row++) {
        for (let col = 0; col < 7; col++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = row;
            cell.dataset.col = col;
            board.appendChild(cell);
        }
    }

    // Reset the game
    resetBtn.addEventListener('click', () => {
        document.querySelectorAll('.cell').forEach(cell => {
            cell.style.backgroundColor = '#ecf0f1';
        });
        gameWon = false; // Reset game status
        currentPlayer = 1; // Reset to Player 1
    });

    // Add event listener for player moves
    board.addEventListener('click', (event) => {
        if (!gameWon) { // If game is not won
            const clickedCell = event.target;
            if (clickedCell.classList.contains('cell')) {
                const col = parseInt(clickedCell.dataset.col);
                const row = getLowestEmptyRow(col);

                if (row !== -1) {
                    const pieceColor = currentPlayer === 1 ? 'red' : 'yellow';
                    dropPiece(row, col, pieceColor);
                    if (checkWin(row, col)) { // Check for win after each move
                        gameWon = true;
                        const winner = currentPlayer === 1 ? 'Player 1' : 'Player 2';
                        alert(`${winner} wins the game!`);
                    } else {
                        currentPlayer = currentPlayer === 1 ? 2 : 1; // Toggle between players
                    }
                }
            }
        }
    });

    // Function to drop a piece into the board
    function dropPiece(row, col, color) {
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        cell.style.backgroundColor = color;
    }

    // Function to find the lowest empty row in a column
    function getLowestEmptyRow(col) {
        const cellsInCol = document.querySelectorAll(`[data-col="${col}"]`);
        for (let i = cellsInCol.length - 1; i >= 0; i--) {
            if (cellsInCol[i].style.backgroundColor === 'rgb(236, 240, 241)' || cellsInCol[i].style.backgroundColor === '') {
                return parseInt(cellsInCol[i].dataset.row);
            }
        }
        return -1; // Column is full
    }

    // Function to check for winning conditions
    function checkWin(row, col) {
        const color = currentPlayer === 1 ? 'red' : 'yellow';

        // Check horizontally
        let count = 0;
        for (let c = 0; c < 7; c++) {
            if (board.querySelector(`[data-row="${row}"][data-col="${c}"]`).style.backgroundColor === color) {
                count++;
                if (count === 4) return true;
            } else {
                count = 0;
            }
        }

        // Check vertically
        count = 0;
        for (let r = 0; r < 6; r++) {
            if (board.querySelector(`[data-row="${r}"][data-col="${col}"]`).style.backgroundColor === color) {
                count++;
                if (count === 4) return true;
            } else {
                count = 0;
            }
        }

        // Check diagonally (/)
        count = 0;
        let r = row - Math.min(row, col);
        let c = col - Math.min(row, col);
        while (r < 6 && c < 7) {
            if (board.querySelector(`[data-row="${r}"][data-col="${c}"]`).style.backgroundColor === color) {
                count++;
                if (count === 4) return true;
            } else {
                count = 0;
            }
            r++;
            c++;
        }

        // Check diagonally (\)
        count = 0;
        r = row - Math.min(row, 6 - col);
        c = col + Math.min(row, 6 - col);
        while (r < 6 && c >= 0) {
            if (board.querySelector(`[data-row="${r}"][data-col="${c}"]`).style.backgroundColor === color) {
                count++;
                if (count === 4) return true;
            } else {
                count = 0;
            }
            r++;
            c--;
        }

        return false; // No win condition found
    }
});
