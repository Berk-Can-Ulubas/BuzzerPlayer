from serial import *
from tkinter import *
from tkinter import filedialog as fd
import serial.tools.list_ports
import time


ser = None
filename = None
window = Tk()

def get_com_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def connect_b_action():
    global ser
    try:
        port = selected_port.get()
        ser = Serial(port, 9600)
        text.insert('1.0', f'Connected to {port}\n')
    except Exception as e:
        text.insert('1.0', f'Error: {e}\n')

def disconnect_b_action():
    global ser
    if ser and ser.is_open:
        ser.close()
        text.insert('1.0', 'Disconnected\n')

def load_file_b_action():
    global filename
    filename = fd.askopenfilename()
    if filename.endswith('.wav'):
        text.insert('1.0', filename + ' file loaded\n')
    else:
        text.insert('1.0', 'No wav file found\n')
    
def start_b_action():
    if filename:
        if ser and ser.is_open:
            try:
                with open(filename, 'rb') as file:
                    while True:
                        byte = file.read(1)
                        if not byte:
                            break  

                        ser.write(byte)  
                        
                        
                        response = b''
                        timeout = time.time() + 2 
                        while time.time() < timeout:
                            if ser.in_waiting:
                                response = ser.read(1)
                                break
                            time.sleep(0.001)  
                        
                        if not response:
                            text.insert('1.0', 'Timeout waiting for response!\n')
                            break 

                    text.insert('1.0', 'File sent with handshake per byte.\n')

            except Exception as e:
                text.insert('1.0', f'Error: {e}\n')
        else:
            text.insert('1.0', 'Serial port not connected.\n')
    else:
        text.insert('1.0', 'No file loaded.\n')

selected_port = StringVar()
available_ports = get_com_ports()
if available_ports:
    selected_port.set(available_ports[0]) 
else:
    selected_port.set("No Ports Found")

button_frame = Frame(window)
button_frame.pack(pady=10)

button_style = {'font': ('Arial', 10), 'width': 12, 'height': 2}

load_file_button = Button(button_frame, text='Load File', command=load_file_b_action, **button_style)
connect_button = Button(button_frame, text='Connect', command=connect_b_action, **button_style)
start_button = Button(button_frame, text='Start', command=start_b_action, **button_style)
disconnect_button = Button(button_frame, text='Disconnect', command=disconnect_b_action, **button_style)
text = Text(window, width=60, height=15)

load_file_button.pack(side=LEFT, padx=5)
connect_button.pack(side=LEFT, padx=5)
start_button.pack(side=LEFT, padx=5)
disconnect_button.pack(side=LEFT, padx=5)

window.geometry("500x400")
window.title("BuzzerPlayer GUI")
text.pack(pady=10)
text.insert('1.0', 'welcome to the BuzzerPlayer for wav files!\n')

port_menu_label = Label(window, text="Select COM Port:", font=("Arial", 10))
port_menu_label.pack()
port_menu = OptionMenu(window, selected_port, *available_ports)
port_menu.config(font=("Arial", 10))
port_menu.pack(pady=5)


