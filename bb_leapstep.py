import socket
from bb_pystepper import Stepper
from bb_pystepper import Solenoid

def run_motor(s, step, sol):
    s.listen(1)
    conn, addr = s.accept()
    while(True):
        data = conn.recv(1)
        if not data:
            break
        elif data == 'r':
            step.rotate(1.8, 15)
        #    print("right")
        elif data == 'l':
            step.rotate(-1.8, 15)
        #    print("left")
        elif data == 's':
            sol.shoot()
            print("BOOM!")
    conn.close

def main():
    # create Stepper
    mystepper = Stepper(200, ["P8_13", "P8_14", "P8_15", "P8_16"])

    # set up a pin for shooting the solenoid
    mysolenoid = Solenoid()

    # connect to server
    HOST = ''
    PORT = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    # get data and run motor
    run_motor(s, mystepper, mysolenoid)

if __name__ == "__main__":
    main()
