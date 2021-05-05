from tkinter import *
from tkinter import filedialog
import pygame
import tkinter.ttk as ttk
from mutagen.mp3 import MP3
import time



root = Tk()
root.title("MP3 Player")
root.geometry("500x400")
root.config(bg="gray")
# define pygame music initialization
pygame.mixer.init()


def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos()/1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/Home/PycharmProjects/MP3_PLAYER/songs/{song}.mp3'
    song_mut = MP3(song)
    global song_length
    song_length= song_mut.info.length

    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    if int(song_slider.get()) == int(song_length):
        stop_song()

    elif paused:
        pass

    else:
        next_time = int(song_slider.get())+1
        song_slider.config(to=song_length, value= next_time)
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')


    if current_time > 0:
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')

    status_bar.after(1000, play_time)

def add_song():
    song = filedialog.askopenfilename(initialdir='songs/',title="Choose A song", filetypes=(("mp3 files", "*.mp3"), ))
    song = song.replace("C:/Users/Home/PycharmProjects/MP3_PLAYER/songs/", "")
    song = song.replace(".mp3", "")
    playlist_box.insert(END, song)

def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='songs/',title="Choose songs ", filetypes=(("mp3 files", "*.mp3"), ))
    for song in songs:
        song = song.replace("C:/Users/Home/PycharmProjects/MP3_PLAYER/songs/", "")
        song = song.replace(".mp3", "")
        playlist_box.insert(END, song)

def delete_song():
    playlist_box.delete(ANCHOR)


def delete_all_song():
    playlist_box.delete(0, END)


def previous_song():

    status_bar.config(text="")
    song_slider.config(value=0)

    next_one = playlist_box.curselection()
    next_one = next_one[0] - 1

    playlist_box.selection_clear(0, END)
    playlist_box.activate(next_one)
    play_song()
    playlist_box.selection_set(next_one, last=None)


def next_song():
    status_bar.config(text="")
    song_slider.config(value=0)
    next_one = playlist_box.curselection()
    next_one = next_one[0]+1
    playlist_box.selection_clear(0, END)
    playlist_box.activate(next_one)
    play_song()
    playlist_box.selection_set(next_one, last=None)



global paused

paused=False


def pause_song(is_pause):
    global paused
    paused = is_pause

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True



def play_song():
    global stopped
    stopped = False

    song =playlist_box.get(ACTIVE)
    song = f'C:/Users/Home/PycharmProjects/MP3_PLAYER/songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()


global stopped
stopped = False


def stop_song():
    pygame.mixer.music.stop()
    playlist_box.selection_clear(ACTIVE)

    status_bar.config(text='')
    song_slider.config(value=0)
    global stopped
    stopped = True

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


def slide(x):
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/Home/PycharmProjects/MP3_PLAYER/songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start= song_slider.get())

# creating main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)

# volume slider frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

# create volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient = VERTICAL, length=125, value=1, command=volume)
volume_slider.pack(pady=10)

# create song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)



# create buttons images

back_btn_img = PhotoImage(file='images_button/back.png')
forward_btn_img = PhotoImage(file='images_button/forward.png')
pause_btn_img = PhotoImage(file='images_button/pause.png')
play_btn_img = PhotoImage(file='images_button/play.png')
stop_btn_img = PhotoImage(file='images_button/stop.png')

# create Buttons

control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song).grid(row=0, column=0, padx=10)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song).grid(row=0, column=1, padx=10)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda:pause_song(paused)).grid(row=0, column=3, padx=10)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play_song).grid(row=0, column=2, padx=10)
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop_song).grid(row=0, column=4, padx=10)

# create menu

my_menu=Menu(root)
root.config(menu=my_menu)

# Create add song meny dropdowns

add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add songs", menu=add_song_menu)

# add one song menu
add_song_menu.add_cascade(label="Add one song to Playlist",command=add_song)
add_song_menu.add_cascade(label="Add many song to Playlist",command=add_many_song)

# delete song menu dropdowns

delete_song_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Delete songs", menu=delete_song_menu)

delete_song_menu.add_cascade(label="Delete a selected song", command=delete_song)
delete_song_menu.add_cascade(label="Delete all songs", command=delete_all_song)

# Status Bar

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# temporary label

my_label=Label(root, text="",bg="gray").pack(pady=20)

root.mainloop()