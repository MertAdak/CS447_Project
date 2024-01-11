import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = 'X'
        self.you = None
        self.opponent = None
        self.winner = None
        self.game_over = False
        self.send_move = None
        
        self.counter = 0
        
        
    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        
        # Receive the mark from the server
        self.you = client.recv(1024).decode('utf-8')
        self.opponent = 'X' if self.you == 'O' else 'O'
        
        if self.you == 'X' : print("You are X, let's start the game!")
        if self.you == 'O' : print("You are O, let's start the game!")
        
        threading.Thread(target=self.handle_connection, args=(client,)).start()
    
    def handle_connection(self, client):
        while not self.game_over:
            # If it is the turn of the user
            if self.turn == self.you:
                # If it is the first move of the game, print the board for the user
                if self.you == 'X' and self.counter == 0:
                    self.print_board()
                    
                # Get the move from the user from the console
                move = input("Enter (row, column) type of move : ")
                
                # Check if the move is valid, if it is send it to the server with 
                # the game_over flag for closing the socket purposes
                if self.check_valid_move(move.split(',')):
                    self.send_move = move + ',' + str(self.game_over)
                    self.apply_move(move.split(','), self.you, client)
                    self.turn = self.opponent
                    client.send(self.send_move.encode('utf-8'))
                else:
                    # If the move is not valid, print an error message and ask for a new move
                    print("Invalid move, try again. Format: row,column")
                    
            else:
                # If it is the turn of the opponent, receive the 
                # move of the opponent from the server 
                data = client.recv(1024)
                if not data:
                    break
                else:
                    # If the move is succesfully received, apply it to 
                    # the board and give the turn to the user
                    self.apply_move(data.decode('utf-8').split(','), self.opponent, client)
                    self.turn = self.you
                     
        # If the game is over, close the socket   
        client.close()
            
    def apply_move(self, move, player,client):
        if self.game_over:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        
        if self.check_if_won():
            if self.winner == self.you:
                print("You won!")
            elif self.winner == self.opponent:
                print("You lost!")
            
            temp = self.send_move.split(',')
            temp[2] = "True"
            self.send_move = ','.join(temp)
            client.send(self.send_move.encode('utf-8'))
            exit()
            
        else:
            if self.counter == 9:
                print("Tie!")
                temp = self.send_move.split(',')
                temp[2] = "True"
                self.send_move = ','.join(temp)
                client.send(self.send_move.encode('utf-8'))
                exit()
                
    def check_valid_move(self, move):
        # Check if the move has the form of a,b
        if len(move) != 2:
            return False
        
        # Check if the move is a number
        try :
            int(move[0])
            int(move[1])
        except ValueError:
            return False
        
        
        return (int(move[0]) < 3 and int(move[1]) < 3 and self.board[int(move[0])][int(move[1])] == " ")
    
    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
            
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True
            
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            self.game_over = True
            return True
        
        return False
    
    def print_board(self):
        print("**************************************")
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("-------------")
                
        print()
                
if __name__ == "__main__":
    game = TicTacToe()
    game.connect_to_game('51.20.93.151', 5005)
    
        