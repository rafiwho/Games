import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        # Color scheme
        self.bg_color = '#2C3E50'  # Dark blue background
        self.frame_color = '#34495E'  # Slightly lighter blue for frame
        self.button_color = '#ECF0F1'  # Light gray for buttons
        self.text_color = '#ECF0F1'  # Light text color
        self.x_color = '#3498DB'  # Bright blue for X
        self.o_color = '#E74C3C'  # Bright red for O
        self.win_color = '#2ECC71'  # Green for winning line
        
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.configure(bg=self.bg_color)
        self.window.minsize(400, 500)  # Set minimum window size
        
        # Game state
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        
        # Create and configure the main container
        self.main_frame = tk.Frame(self.window, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Create title with custom font and styling
        self.title_label = tk.Label(
            self.main_frame,
            text="Tic Tac Toe",
            font=('Helvetica', 36, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.pack(pady=20)
        
        # Create status label with improved styling
        self.status_label = tk.Label(
            self.main_frame,
            text="Next player: X",
            font=('Helvetica', 16),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.status_label.pack(pady=15)
        
        # Create game board with improved styling
        self.board_frame = tk.Frame(
            self.main_frame,
            bg=self.frame_color,
            padx=10,
            pady=10
        )
        self.board_frame.pack(pady=20)
        
        # Create buttons with improved styling
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=('Helvetica', 24, 'bold'),
                    width=3,
                    height=1,
                    bg=self.button_color,
                    activebackground='#BDC3C7',  # Slightly darker when clicked
                    relief=tk.FLAT,  # Flat appearance
                    command=lambda row=i, col=j: self.handle_click(row, col)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)
        
        # Create reset button with improved styling
        self.reset_button = tk.Button(
            self.main_frame,
            text="New Game",
            font=('Helvetica', 14),
            bg='#27AE60',  # Green color
            fg='white',
            activebackground='#219A52',  # Darker green when clicked
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.reset_game
        )
        self.reset_button.pack(pady=25)
        
    def handle_click(self, row, col):
        index = row * 3 + col
        if self.board[index] == "" and not self.game_over:
            self.board[index] = self.current_player
            color = self.x_color if self.current_player == 'X' else self.o_color
            self.buttons[index].config(
                text=self.current_player,
                fg=color,
                disabledforeground=color  # Keep color when disabled
            )
            self.buttons[index].config(state='disabled')  # Disable clicked button
            
            if self.check_winner():
                self.game_over = True
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins! 🎉")
            elif "" not in self.board:
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a draw! 🤝")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                next_color = self.o_color if self.current_player == "O" else self.x_color
                self.status_label.config(
                    text=f"Next player: {self.current_player}",
                    fg=next_color
                )
    
    def check_winner(self):
        # Winning combinations
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for line in lines:
            if (self.board[line[0]] == self.board[line[1]] == 
                self.board[line[2]] != ""):
                # Highlight winning line
                for index in line:
                    self.buttons[index].config(bg=self.win_color)
                return True
        return False
    
    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.status_label.config(text="Next player: X", fg=self.text_color)
        for button in self.buttons:
            button.config(
                text="",
                bg=self.button_color,
                fg=self.text_color,
                state='normal'  # Re-enable buttons
            )
    
    def run(self):
        # Center the window on the screen
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run() 