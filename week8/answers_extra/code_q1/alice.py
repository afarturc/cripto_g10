from shared import receive_data, send_data, loadKeys, HOST, PORT
import socket


encryption_key, authentication_key = loadKeys()
print(f"Encryption: \b{encryption_key}, Authentication: \b{authentication_key}")

msg1 = "Hello, Bob"
msg3 = "I would like to have dinner"
msg5 = "Sure!"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    send_seq = 0
    recv_seq = 0
    
    send_data(s, msg1.encode(), encryption_key, authentication_key, send_seq)
    send_seq += 1
    print(f"Me: {msg1}")
    
    message = receive_data(s, encryption_key, authentication_key, recv_seq)
    recv_seq += 1
    print(f"Bob: {message.decode()}")
    
    send_data(s, msg3.encode(), encryption_key, authentication_key, send_seq)
    send_seq += 1
    print(f"Me: {msg3}")
    
    message = receive_data(s, encryption_key, authentication_key, recv_seq)
    recv_seq += 1
    print(f"Bob: {message.decode()}")
    
    send_data(s, msg5.encode(), encryption_key, authentication_key, send_seq)
    send_seq += 1
    print(f"Me: {msg5}")
    