#!/usr/bin/env python3
import socket
import time
import select

def try_answer(answer):
    print(f"\n{'='*60}")
    print(f"Trying: {answer}")
    print(f"{'='*60}\n")
    
    try:
        # Connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('tethys.picoctf.net', 59853))
        
        # Receive initial banner
        time.sleep(1)
        banner = sock.recv(4096).decode()
        
        # Send password
        sock.sendall(b'My_Passw@rd_@1234\n')
        time.sleep(1)
        sock.recv(4096)
        
        # Send conference answer
        sock.sendall(b'DEFCON\n')
        time.sleep(1)
        sock.recv(4096)
        
        # Send hacker answer
        sock.sendall(answer.encode() + b'\n')
        time.sleep(2)
        
        # Try to receive response
        response = sock.recv(4096).decode()
        print(f"Response: '{response}'")
        
        if '$' in response or 'player@' in response:
            print(f"\n*** SUCCESS WITH: {answer} ***\n")
            return True
        elif 'good try' in response or 'try again' in response:
            print(f"Wrong answer: {answer}")
            return False
        elif response.strip() == '':
            print(f"Empty response - might be correct, connection closing")
            # Try to send a command
            try:
                sock.sendall(b'whoami\n')
                time.sleep(1)
                cmd_response = sock.recv(4096).decode()
                print(f"Command response: '{cmd_response}'")
                if cmd_response.strip():
                    return True
            except:
                pass
            return None
        else:
            print(f"Unknown response")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        try:
            sock.close()
        except:
            pass
    
    time.sleep(1)

# List of possible answers
answers = [
    "John Draper",
    "Joe Engressia",
    "Joybubbles",
    "Kevin Mitnick",
    "phreaker",
    "Captain Crunch",
    "Draper",
    "Engressia",
]

for ans in answers:
    result = try_answer(ans)
    if result == True:
        print(f"\n\n*** FOUND CORRECT ANSWER: {ans} ***\n\n")
        break
