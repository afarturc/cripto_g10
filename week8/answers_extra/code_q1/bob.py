from shared import receive_data, send_data, loadKeys, HOST, PORT
import socket

encryption_key, authentication_key = loadKeys()
print(f"Encryption: \b{encryption_key}, Authentication: \b{authentication_key}")

msg2 = "Hello Alice"
msg4 = "Me too. Same time, same place?"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(f"Connected by address: {addr}")
    
    send_seq = 0
    recv_seq = 0
    
    message = receive_data(conn, encryption_key, authentication_key, recv_seq)
    recv_seq += 1
    print(f"Alice: {message.decode()}")
    
    send_data(conn, msg2.encode(), encryption_key, authentication_key, send_seq)
    send_seq += 1
    print(f"Me: {msg2}")
    
    message = receive_data(conn, encryption_key, authentication_key, recv_seq)
    recv_seq += 1
    print(f"Alice: {message.decode()}")
    
    send_data(conn, msg4.encode(), encryption_key, authentication_key, send_seq)
    send_seq += 1
    print(f"Me: {msg4}")
    
    message = receive_data(conn, encryption_key, authentication_key, recv_seq)
    recv_seq += 1
    print(f"Alice: {message.decode()}")
    
    
    
    
    