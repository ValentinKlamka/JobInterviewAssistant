from tkinter import *
import tkinter as tk
import pyaudio
import wave
import threading
from os.path import join, dirname
from openai import OpenAI


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
WAVE_OUTPUT_FILENAME = "output"
FILEINDEX = 0
memory=[]
frames=[]
recording = False

client = OpenAI()

class recordThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      print ("Starting " + self.name)
      record()
      print ("Exiting " + self.name)



class transcribeThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):  
        print ("Starting " + self.name)
        transcribe()
        print ("Exiting " + self.name)

#on enter start recording
def on_enter(e):
    
    
    button['background'] = 'green'
    button['text'] = 'Recording'
    button['fg'] = 'black'
    button['width'] = 20
    button['height'] = 20

    print("* recording")
    global recording
    recording=True
    thread_r = recordThread()
    thread_r.start()

def record():

    global recording
    print("BLA")
    while recording:

        data = stream.read(CHUNK)
        frames.append(data)


    return
    
def on_leave(e):
    
    button['background'] = 'red'
    button['text'] = 'Record'
    button['fg'] = 'white'
    button['width'] = 20
    button['height'] = 20
    global recording
    recording=False
    print(len(frames))
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
    print (transcript)
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

    getResponse(transcript)
    return

def getResponse(transcript):
    global memory 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Please help to guide me through my job interview."},
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

    print("Closing")
    global recording
    recording=False

    stream.stop_stream()
    stream.close()
    p.terminate()
    window.destroy()



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
window.geometry('2000x200')
window.configure(background='white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
button = tk.Button(mainframe, text='Record', width=20, height=10, bg='red', fg='white')
#button always top left
button.pack(side=LEFT, anchor=NW)
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)
# to the right side of the button create a scrollable text box
text_box = tk.Text(mainframe, height=10, width=200)
text_box.pack(side=RIGHT, anchor=NW)


# make it scrollable
scroll = tk.Scrollbar(mainframe, command=text_box.yview)
scroll.pack(side=RIGHT, fill=Y)
text_box.config(yscrollcommand=scroll.set)
#make it non editable
text_box.configure(state='disabled')




window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()





