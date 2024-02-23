import json
from tkinter import *
import pyaudio
from vosk import Model, KaldiRecognizer
import threading
from datetime import datetime
import pyperclip
from subprocess  import run
from sys import executable

current_datetime = datetime.now()
text = None
clipboard_data = ''
print('Loading model...')
model = Model('small_model')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()
print('\nModel loaded successfully!\n' + str(current_datetime))
with open('log.txt', 'a') as log_file:
	log_file.write('\n\n*** ' + str(current_datetime) + '\n\n')
	log_file.close()


def listen():				# Line in
	while True:
		data = stream.read(4000, exception_on_overflow=False)
		if (rec.AcceptWaveform(data)) and (len(data) > 0):
			answer = json.loads(rec.Result())
			if answer['text']:
				yield answer['text']


def record():
	global text
	global label
	global clipboard_data
	for text in listen():
		print(text.capitalize())
		clipboard_data = (clipboard_data + text.capitalize() + '. ')
		with open('log.txt', 'a') as log_file:
			log_file.write(text.capitalize() + '. \n')
			log_file.close()
		text_field.insert(END, (text.capitalize() + '. \n'))
		label_last_string.config(text=text.capitalize() + '.')
		text_field.yview(END)


def terminate_program():
	global stream
	stream = None
	root.destroy() 
	quit()


def paper_clip():
	pyperclip.copy(clipboard_data)


def open_log():
	run('notepad.exe C:\VOSK\log.txt')


def clear_log():
	with open('log.txt', 'w') as log_clear:
			log_clear.write('')
			log_clear.close()
			label_last_string.config(text='Cleared')
			text_field.delete(1.0, END)

def about_window():
	about = Tk()
	about.title('About program')
	about.geometry('400x165')
	about.resizable(False, False)
	label_about = Label(about, background='black', height=10, foreground='green', font=('Arial', 10), text='VOSK API transcribator\
		\n\nVersion: 1.0 alpha\n\n(c) Constantine Shvorak\n\n2024')
	label_about.pack(fill=BOTH)


root = Tk()
root.title('VOSK')
root.geometry('600x400')
mainmenu = Menu(root)
root.configure(background='grey', menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Copy to clipboard", command=paper_clip)
filemenu.add_command(label="Open log", command=open_log)
filemenu.add_command(label="Clear log", command=clear_log)
filemenu.add_command(label="Exit", command=terminate_program)
helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="About...", command=about_window)

mainmenu.add_cascade(label="File", menu=filemenu)
mainmenu.add_cascade(label="Help", menu=helpmenu)

label_datetime = Label(root, height=2, background='black', foreground='green', font=('Arial', 10),
	text=('Transcribation started: ' + str(current_datetime) + '\nLast string:'))
label_datetime.pack(fill=X)

label_last_string = Label(root, height=1, background='black', foreground='red', font=('Arial', 10))
label_last_string.pack(fill=X)

button_paperclip = Button(root, height=2, text='Copy to clipboard', state='normal', command=paper_clip)
button_paperclip.pack(fill=X)

text_field = Text(width=200, height=70, background='white', foreground='black', font=('Arial', 10))
scroll = Scrollbar(command=text_field.yview)
scroll.pack(side=RIGHT, fill=Y)
text_field.pack(fill=BOTH)
text_field.config(yscrollcommand=scroll.set)

thread = threading.Thread(target=record)
thread.start()

root.protocol("WM_DELETE_WINDOW", terminate_program)
root.mainloop()
