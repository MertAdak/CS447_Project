import socket
import threading

class TicTacToe:
    def __init__(self):
        self.client1 = None
        self.client2 = None
        self.server = None
        self.game_over = False
        
    def host_game(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        
        # Listen for 2 connections and start a thread for each
        self.server.listen(2)
        print("Waiting for connections...")
        self.client1, addr = self.server.accept()
        print("Player 1 connected")
        self.client2, addr = self.server.accept()
        print("Player 2 connected")
        
        # Send the mark to the clients
        self.client1.send('X'.encode('utf-8'))
        self.client2.send('O'.encode('utf-8'))
        
        threading.Thread(target=self.handle_connection, args=(self.client1,)).start()
        threading.Thread(target=self.handle_connection, args=(self.client2,)).start()
        
        # Close the connections for further connections
        self.server.close()
        print("The game has ended, new session started")
        
        
        
    def handle_connection(self, client):
        # if the game is not over and a client says something run while loop
        while not self.game_over:
            data = client.recv(1024)
            if not data:
                continue
            else:
                # if the client says something
                # split the data into which has form a,b,c 
                # where a is the row, b is the column, and c is the game_over flag
                data = data.decode('utf-8').split(',')
                print(data)
                # if the game is over
                if data[2] == 'True':
                    print("Game over")
                    self.game_over = True
                    
                    if client == self.client1:
                        send_data = data[0] + ',' + data[1]
                        self.client2.send(send_data.encode('utf-8'))
                    else:
                        send_data = data[0] + ',' + data[1]
                        self.client1.send(send_data.encode('utf-8'))
                    
                    # close the connections
                    exit()           
                             
                # if the game is not over
                else:
                    # send the data to the other client
                    if client == self.client1:
                        send_data = data[0] + ',' + data[1]
                        self.client2.send(send_data.encode('utf-8'))
                    else:
                        send_data = data[0] + ',' + data[1]
                        self.client1.send(send_data.encode('utf-8'))
                
   
if __name__ == "__main__":
    game = TicTacToe()
    game.host_game("localhost", 5005)
    
        