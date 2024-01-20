
import socket
import random


def count_neighbor(board, x, y):
    directions = [(dx, dy) for dx in [-1, 0, 1]
                  for dy in [-1, 0, 1] if not dx == dy == 0]
    count = 0
    size = len(board)
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < size and 0 <= new_y < size and board[new_x][new_y] == 'X':
            count += 1
    return count


def generate_board(size, num_mines):
    board = [['0' for _ in range(size)] for _ in range(size)]
    for _ in range(num_mines):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        board[x][y] = 'X'
    for i in range(size):
        for j in range(size):
            if board[i][j] != 'X':
                board[i][j] = count_neighbor(board, i, j)
    return board


def write_msg(conn, client_board):
    message = ''
    for row in client_board:
        row = map(lambda a: str(a), row)
        message += ''.join(row) + '\n'
    conn.send(str.encode(message))



def read_client(conn):
    data = conn.recv(3)
#    print("data:", data)
    data = data.decode("utf-8")
    return int(data[0]), int(data[2])


def main_gaem_ig(conn, server):
    size = 5
    bomb_count = 8
    board = generate_board(size, bomb_count)
    client_board = [['_' for _ in range(size)] for _ in range(size)]
    checked = 0
    conn.send(str.encode(str(size)))
    while checked < size*size-bomb_count:
        x,y = read_client(conn)
        if board[x][y] != 'X':
            client_board[x][y] = board[x][y]
            write_msg(conn, client_board)
            checked += 1
        elif board[x][y]=='X':
            conn.send(str.encode("GAME OVER!"))
            break
    conn.send(str.encode("BYE!"))
    conn.close()
    server.close()
    exit(0)


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print("w8ing connection...")
    conn, addr = server.accept()
    print('Connected by', addr)
    main_gaem_ig(conn, server)


start_server("127.0.0.1", 9999)


# if __name__ == '__main__':
#     start_server('localhost', 5000)
