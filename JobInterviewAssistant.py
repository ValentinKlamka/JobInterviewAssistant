from tkinter import *
import tkinter as tk
import pyaudio
import wave
import threading
from os.path import join, dirname
from openai import OpenAI
import configparser


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
WAVE_OUTPUT_FILENAME = "output"
FILEINDEX = 0
memory=[]
frames=[]
recording = False

#create items consiting of model name, cost and description
class Model:
    def __init__(self, name,  hint,cost):
        self.name = name
        self.hint = hint
        self.cost = cost


Modellist = []
Modellist.append(Model("gpt-3.5-turbo"," (Recommended)", "$0.002 / 1K tokens"))
Modellist.append(Model("gpt-4-1106-preview","", "$0.03 / 1K tokens"))

client = OpenAI()

class recordThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      print ("Starting " + self.name)
      record()
      print ("Exiting " + self.name)

# thread to transcribe the recorded audio file

class transcribeThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):  
        print ("Starting " + self.name)
        transcribe()
        print ("Exiting " + self.name)

#thread to get response from gpt-3 with argument transcript

class getResponseThread (threading.Thread):
    def __init__(self,transcript):
        threading.Thread.__init__(self)
        self.transcript = transcript
    def run(self):  
        print ("Starting " + self.name)
        getResponse(self.transcript)
        print ("Exiting " + self.name)

#on enter start recording
def on_enter(e):
    
    
    button['background'] = 'green'
    button['text'] = 'Recording'
    button['fg'] = 'black'

    print("* recording")
    global recording
    recording=True
    thread_r = recordThread()
    thread_r.start()

def record():

    global recording
    while recording:

        data = stream.read(CHUNK)
        frames.append(data)


    return
    
def on_leave(e):
    
    button['background'] = 'red'
    button['text'] = 'Record'
    button['fg'] = 'white'
    global recording
    recording=False
    print("* done recording")
    
    global FILEINDEX
    wf = wave.open(WAVE_OUTPUT_FILENAME+str(FILEINDEX)+".wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("wav saved")
    frames.clear()
    thread_t = transcribeThread()
    thread_t.start()
   

def transcribe():
    global FILEINDEX
    audio_file= open(WAVE_OUTPUT_FILENAME+str(FILEINDEX)+".wav", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text"
    )
    if len(transcript) <= 4:
        print("No transcript found")
        return
    #append transcript to log.txt file
    f = open("log.txt", "a")
    f.write(transcript)
    f.write("\n")
    f.close()

    #append transcript to text box
    text_box.configure(state='normal')
    text_box.insert(END,transcript)
    text_box.configure(state='disabled')
    #scroll to bottom
    text_box.see(END)
    
    FILEINDEX+=1
    #start response thread
    thread_g = getResponseThread(transcript)
    thread_g.start()
    return

def getResponse(transcript):
    global memory 
    #read config.ini file to get gpt-version
    config = configparser.ConfigParser()
    config.read('config.ini')

    #open and read cv_summary.md file
    f = open("cv_summary.md", "r")
    cv_summary = f.read()
    f.close()
    if len(cv_summary) > 0:
        cv_summary_prompt= {"role": "assistant", "content": "Summary of the CV of the interviewed person: "+cv_summary}
    else:
        cv_summary_prompt= {"role": "assistant", "content": ""}

    #open and read job_description.md file
    f = open("job_description_summary.md", "r")
    job_description = f.read()
    f.close()
    if len(job_description) > 0:
        job_description_prompt= {"role": "assistant", "content": "Job description summary: "+job_description}
    else:
        job_description_prompt= {"role": "assistant", "content": ""}
    #get gpt-version from config.ini file
    gpt_version = config["GPT-Version"]["gpt-version"]
    response = client.chat.completions.create(
        model=gpt_version,
        messages=[
            {"role": "system", "content": "Please help to guide me through my job interview. Answer the questions from the perspective of the interviewed person."},
            cv_summary_prompt,
            job_description_prompt,
            {"role": "assistant", "content": ''.join(memory)},
            {"role": "user", "content": transcript}
        ],
        stream=True
        )
    collected_messages = []
    text_box.tag_config('blue', foreground="blue")
    for chunk in response:
        chunk_message = chunk.choices[0].delta.content
        if chunk_message:
            collected_messages.append(chunk_message)
            text_box.configure(state='normal')
            #insert the chunk_message into the text box in blue color
            text_box.insert(END,chunk_message,'blue')
            text_box.configure(state='disabled')
            text_box.see(END)
    full_reply_content = ''.join(collected_messages)
    f = open("log.txt", "a")
    f.write(full_reply_content)
    f.write("\n")
    f.close()
    memory.append(transcript)
    memory.append(full_reply_content)
    return

def on_closing():
    global recording
    recording=False

    stream.stop_stream()
    stream.close()
    p.terminate()
    window.destroy()

def select(option):
    #change config.ini file to change gpt-version
    config = configparser.ConfigParser()
    config.read('config.ini')
    config['GPT-Version']['gpt-version'] = option
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    changebold()
    return

def changebold():
    #value of gpt-version in config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    for index in range(file_menu.index("end")):
        if config["GPT-Version"]["gpt-version"] ==Modellist[index].name:

            file_menu.entryconfig(index, font=('TkDefaultFont', 10, 'bold'))
            add_checkmark(file_menu, index)

        else:
            file_menu.entryconfig(index, font=('TkDefaultFont', 10))
            remove_checkmark(file_menu, index)
    return

def add_checkmark(menu, index,checkmark='\u2713'):

    label = menu.entrycget(index, "label")
    if checkmark not in label:
        label += f" {checkmark}"
        menu.entryconfig(index, label=label)

def remove_checkmark(menu, index,checkmark='\u2713'):
    label = menu.entrycget(index, "label")
    if checkmark in label:
        label = label.replace(checkmark, "").strip()
        menu.entryconfig(index, label=label)

    
    return

def send_message(event=None):
    message = entry_box.get()
    if message.strip() != "":
        text_box.config(state=tk.NORMAL)
        text_box.insert(tk.END, f"\n{message}\n")
        f = open("log.txt", "a")
        f.write(message)
        f.write("\n")
        f.close()
        text_box.config(state=tk.DISABLED)
        text_box.see(tk.END)
        entry_box.delete(0, tk.END)
        #start response thread
        thread_g = getResponseThread(message+"\n")
        thread_g.start()
    return 





p = pyaudio.PyAudio()


stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                input_device_index =2,
                frames_per_buffer = CHUNK)

window=tk.Tk()
mainframe=tk.Frame(window,bg='white')
mainframe.pack(fill=BOTH, expand=1)
window.title('Job Interview Assistant')  
screen_width = window.winfo_screenwidth()
window.geometry(str(screen_width)+ 'x200')
#it should open on the top of the screen
window.geometry("+0+0")

window.configure(background='white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

menu_bar = Menu(window)
file_menu = Menu(menu_bar, tearoff=0)
for model in Modellist:
    file_menu.add_command(label=model.name+model.hint + " "+model.cost, command=lambda m=model.name: select(m))

file_menu.add_command(label="Quit", command=on_closing) 
menu_bar.add_cascade(label="File", menu=file_menu)
window.config(menu=menu_bar)
changebold()

button = tk.Button(mainframe, text='Record', width=20, height=10, bg='red', fg='white')
button.pack(side=LEFT, anchor=SW)
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

# to the right side of the button create a scrollable text box
text_box = tk.Text(mainframe, height=10, width=200)

# make it scrollable
scroll = tk.Scrollbar(mainframe, command=text_box.yview)
scroll.pack(side=RIGHT, fill=Y)
text_box.config(yscrollcommand=scroll.set)
#make it non editable
text_box.configure(state='disabled')

entry_frame = tk.Frame(mainframe, bg='white')
entry_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5)
text_box.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, expand=True)

entry_box = tk.Text(entry_frame,height=2,width=200) 
entry_box.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
#make entry box scrollable
scroll = tk.Scrollbar(entry_frame, command=entry_box.yview)
scroll.grid(row=0, column=1, sticky="ns")
entry_box.config(yscrollcommand=scroll.set)

#bind enter key to send message
entry_box.bind("<Return>", send_message)


send_button = tk.Button(entry_frame, text="Send", command=send_message)
send_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")


entry_frame.columnconfigure(0, weight=1)  # Make entry_box expandable
entry_frame.columnconfigure(1, minsize=50)  # Set a minimum size for the Send button




window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()





