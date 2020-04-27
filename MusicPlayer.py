import os, sys
from io import *
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
from pygame import mixer
from pygame import time
from mutagen.id3 import *
from mutagen.mp3 import *
from mutagen.easyid3 import EasyID3
from tkinter.ttk import Progressbar
import random
import threading
import time as myt
import stagger
from PIL import Image, ImageTk, ImageSequence



timer = 0


if __name__ == '__main__':
    root = Tk()
    root.geometry("340x532")
    root.title("MUSIC")
    root.iconbitmap(r"Images/Music_Player.ico")
    root.resizable(False, False)


    # root.minsize

    # root.attributes("-alpha",0.92)

    class MusicPlayer():

        # _________________Image Files_________________

        playImg = PhotoImage(file="Images/Play.png")
        pauseImg = PhotoImage(file="Images/Pause.png")
        previousImg = PhotoImage(file="Images/Previous.png")
        nextImg = PhotoImage(file="Images/Next.png")
        repeatNormImg = PhotoImage(file="Images/Repeat.png")
        repeatOneImg = PhotoImage(file="Images/Repeat_One.png")
        repeatAllImg = PhotoImage(file="Images/Repeat_All.png")
        shuffleOnImg = PhotoImage(file="Images/Shuffle_On.png")
        shuffleOffImg = PhotoImage(file="Images/Shuffle_Off.png")
        coverImg = PhotoImage(file="Images/Headphone.png")
        openFolderImg = PhotoImage(file="Images/Open_Folder.png")
        libraryImg = PhotoImage(file="Images/Library.png")
        volumeHighImg = PhotoImage(file="Images/Volume_High.png")
        volumeMidImg = PhotoImage(file="Images/Volume_Mid.png")
        volumeLowImg = PhotoImage(file="Images/Volume_Low.png")
        volumeOffImg = PhotoImage(file="Images/Volume_Off.png")
        selectVolumeImg = PhotoImage(file="Images/Select_Volume.png")
        searchImg = PhotoImage(file="Images/Search.png")
        # giffy = PhotoImage(file="Images/spec.gif")
        # starGif = PhotoImage(file="Images/Stars.gif")

        # _________________Variables_________________

        songsName = []
        # songLoader = []
        songsLoc = []
        # songTitle = []
        # songArtist = []
        myIndex = 0
        shuffleStatus = 0
        repeatStatus = 0
        prevIndex = 0
        backupVolume = 60
        initialiseWindow = 1
        songsLength = 0
        haltMusic = 0
        prog = 0
        exitStatus = 0
        cur_Val = 0
        isPaused = 0
        juststarted = 1

        global timer

        # insertIndex = 0
        # initialiseVolume = 1

        # _________________Volume Window_________________

        def VolumeWindow(self, root, color, height):
            self.frameVolume = Frame(root, bg=color, height=height)
            self.frameVolume.pack(fill=BOTH, expand=TRUE)

            self.btn_volume = Button(self.frameVolume, image=self.volumeHighImg, relief=FLAT, command=self.volumeOff)
            self.btn_volume.pack(side=LEFT)

            self.scl_volume = Scale(self.frameVolume, bg="white", bd=0, relief=FLAT, activebackground="GREEN",
                                    orient=HORIZONTAL, fr=0, to=100,
                                    command=self.setVolume)
            self.scl_volume.pack(ipadx=100)
            mixer.init()
            mixer.music.set_volume(0.6)
            self.scl_volume.set(60)

        # _________________Volume Methods_________________

        def setVolume(self, volume_value):
            volume = int(volume_value) / 100
            mixer.music.set_volume(volume)
            if (volume > 0.8):
                self.scl_volume.config(activebackground="RED")
            elif (volume > 0.6):
                self.scl_volume.config(activebackground="ORANGE")
            elif (volume > 0):
                self.scl_volume.config(activebackground="LIGHT GREEN")
            if (volume > 0.7):
                self.btn_volume.config(image=self.volumeHighImg, command=self.volumeOff)
            elif (volume > 0.3):
                self.btn_volume.config(image=self.volumeMidImg, command=self.volumeOff)
            elif (volume > 0):
                self.btn_volume.config(image=self.volumeLowImg, command=self.volumeOff)
            else:
                self.btn_volume.config(image=self.volumeOffImg, command=self.volumeOn)

        def volumeOff(self):
            self.backupVolume = self.scl_volume.get()
            # print(self.backupVolume)
            self.scl_volume.set(0)
            mixer.init()
            mixer.music.set_volume(0)
            self.btn_volume.config(image=self.volumeOffImg, command=self.volumeOn)

        def volumeOn(self):
            getVolume = self.backupVolume
            mixer.init()
            if (getVolume > 70):
                self.scl_volume.set(getVolume)
                mixer.music.set_volume(getVolume / 100)
                self.btn_volume.config(image=self.volumeHighImg, command=self.volumeOff)
            elif (getVolume > 30):
                self.scl_volume.set(getVolume)
                mixer.music.set_volume(getVolume / 100)
                self.btn_volume.config(image=self.volumeMidImg, command=self.volumeOff)
            else:
                self.scl_volume.set(getVolume)
                mixer.music.set_volume(getVolume / 100)
                self.btn_volume.config(image=self.volumeLowImg, command=self.volumeOff)

        # def Frames(self, root, color, height):
        #     self.frame = Frame(root, bg=color, height=height)
        #     self.frame.pack(fill=BOTH, expand=TRUE)

        # _________________Cover Window_________________

        # def CoverWindow(self, root, color, height):
        #     self.frameCover = Frame(root, bg=color, height=height)
        #     self.frameCover.pack(fill=BOTH, expand=TRUE)
        #
        #     self.lbl_coverPic = Label(self.frameCover, image=self.coverImg)
        #     self.lbl_coverPic.pack()

        # _________________Control Window_________________

        def ControlWindow(self, root):

            self.frameCover = Frame(root, bg="GREY", height=350)
            self.frameCover.pack(fill=BOTH, expand=TRUE)

            self.lbl_coverPic = Label(self.frameCover, image=self.coverImg)
            self.lbl_coverPic.pack()

            self.frameTitleArtist = Frame(root, bg="AQUA", height=30)
            self.frameTitleArtist.pack(fill=BOTH, expand=TRUE)

            self.lbl_TitleArtist = Label(self.frameTitleArtist, text="Name\nArtist\nAlbum", relief=RIDGE)
            self.lbl_TitleArtist.pack(fill=BOTH, expand=TRUE)

            # self.frameAlbum = Frame(root, bg="BLACK", height=20)
            # self.frameAlbum.pack(fill=BOTH, expand=TRUE)
            #
            # self.lbl_Album = Label(self.frameAlbum, text="", relief=FLAT)
            # self.lbl_Album.pack(fill=BOTH, expand=TRUE)

            self.frameScrubbar = Frame(root, bg="BLACK", height=30)
            self.frameScrubbar.pack(fill=BOTH, expand=TRUE)

            self.prgBar = Progressbar(self.frameScrubbar, length=340, orient=HORIZONTAL,
                                      maximum=100,
                                      value=0)
            self.prgBar.grid(row=0, column=0, columnspan=3)

            # self.prgBar.bind("<Button-1>", self.seek)

            # self.canvas = Canvas(self.frameScrubbar, width=236, height=18)
            # self.canvas.grid(row=1, column=1)

            self.lbl_prgTime = Label(self.frameScrubbar, text="--:--:--")
            self.lbl_prgTime.grid(row=1, column=0, sticky=W)

            self.lbl_totalTime = Label(self.frameScrubbar, text="--:--:--")
            self.lbl_totalTime.grid(row=1, column=2, sticky=E)

            self.frameControl = Frame(root, bg="INDIGO", height=100)
            self.frameControl.pack(fill=BOTH, expand=TRUE)

            self.btn_shuffle = Button(self.frameControl, text="SHUF", image=self.shuffleOffImg, relief=FLAT, height=50,
                                      width=62,
                                      command=self.shuffleOn)
            self.btn_shuffle.grid(row=0, column=0)

            self.btn_previous = Button(self.frameControl, text="PREV", image=self.previousImg, relief=FLAT, height=50,
                                       width=62,
                                       command=self.previousSong)
            self.btn_previous.grid(row=0, column=1)

            self.btn_play_pause = Button(self.frameControl, text="PLAY", image=self.playImg, relief=FLAT, height=50,
                                         width=62,
                                         command=self.playSong)
            self.btn_play_pause.grid(row=0, column=2)

            self.btn_next = Button(self.frameControl, text="NEXT", image=self.nextImg, relief=FLAT, height=50, width=62,
                                   command=lambda : self.nextSong(1))
            self.btn_next.grid(row=0, column=3)
            # self.btn_next.bind("<Button-1>", lambda x : self.nextSong(1))

            self.btn_repeat = Button(self.frameControl, text="REAP", image=self.repeatNormImg, relief=FLAT, height=50,
                                     width=62,
                                     command=self.repeatOne)
            self.btn_repeat.grid(row=0, column=4)

            self.frm_openFolder = Frame(root, bg="WHITE", width=50, height=50)
            self.frm_openFolder.place(relx=0.07, rely=0.12, anchor=CENTER)

            self.btn_openFolder = Button(self.frm_openFolder, image=self.openFolderImg, relief=FLAT,
                                         command=self.openFolder)
            self.btn_openFolder.pack()

            self.frm_library = Frame(root, bg="WHITE", width=50, height=50)
            self.frm_library.place(relx=0.93, rely=0.12, anchor=CENTER)

            self.btn_library = Button(self.frm_library, image=self.libraryImg, relief=FLAT, command=self.myLibrary)
            self.btn_library.pack()

            self.frm_search = Frame(root, width=200, height=25)
            self.frm_search.place(relx=0.5, rely=0.11, anchor=CENTER)
            # self.frm_search.__setattr__('-alpha', 0.9)

            self.entry_search = Entry(self.frm_search, relief=FLAT, command=None)
            self.entry_search.pack(side=LEFT, ipadx=10)
            self.entry_search.bind('<Return>', self.searchAndPlay)

            self.btn_Search = Button(self.frm_search, image=self.searchImg, relief=FLAT, command=self.searchAndPlay)
            self.btn_Search.pack()


        # _________________Progress Bar Methods_________________

        def seek(self, event):
            self.exitStatus = 1
            myt.sleep(1)
            temp = (event.x / 830) * 100
            cur_pos = int((temp * round(MP3(self.songsName[self.myIndex]).info.length)) / 100)
            self.cur_Val = int((cur_pos * round(MP3(self.songsName[self.myIndex]).info.length)) / 100) + ((2*cur_pos)/100)
            self.prog = self.cur_Val
            mixer.init()
            mixer.music.stop()
            mixer.music.load(self.songsName[self.myIndex])
            mixer.music.play(loops=0, start=self.prog)
            self.prgBar.config(value=(self.prog / round(MP3(self.songsName[self.myIndex]).info.length)) * 100)
            self.exitStatus = 0
            self.progressTimer = threading.Timer(0, self.progressInc)
            self.progressTimer.start()


            # self.exitStatus = 1
            # self.prgBar.config(value=(self.prog / round(MP3(self.songsName[self.myIndex]).info.length)) * 100)
            # # self.progressStop()
            # temp = (event.x / 830)*100
            # print(temp)
            # cur_pos = int((temp * round(MP3(self.songsName[self.myIndex]).info.length))/100)
            # print(self.cur_Val)
            # self.cur_Val = int((cur_pos * round(MP3(self.songsName[self.myIndex]).info.length))/100)
            # self.prog = self.cur_Val
            # self.progressTimer = threading.Timer(0, self.progressInc)
            # self.progressTimer.start()
            # self.songLength = (float(round(MP3(self.songsName[self.myIndex]).info.length)) - self.prog) + 2
            # self.timer = threading.Timer(self.songLength, self.nextSong)
            # self.timer.start()
            # self.exitStatus = 1



        # def myGIf(self):
        #     self.canvas = Canvas(root, width=250, height=18)
        #     self.canvas.place(relx=0.5, rely=0.875, anchor=CENTER)#grid(row=1, column=1)
        #     self.sequence = [ImageTk.PhotoImage(img.resize((236,18), Image.ANTIALIAS))
        #                      for img in ImageSequence.Iterator(Image.open("Images/Specturm.gif"))]
        #     self.image = self.canvas.create_image(118, 9, image=self.sequence[0])
        #     self.animate(1)
        #
        # def animate(self, counter):
        #     self.canvas.itemconfig(self.image, image=self.sequence[counter])
        #     root.after(30, lambda: self.animate((counter+1) % len(self.sequence)))
        #
        # def destroy_myGif(self):
        #     self.canvas.destroy()

        def progressInc(self):
            # if(self.isPaused == 0):
            #     self.myGIf()
            # else:
            #     self.destroy_myGif()
            try:
                songLen = round(MP3(self.songsName[self.myIndex]).info.length)
                # h_time = str(songLen // 3600)
                # m_time = str((songLen % 3600) // 60)
                # s_time = str(songLen % 60)
                t_m_time, t_s_time = divmod(songLen, 60)
                t_h_time, t_m_time = divmod(t_m_time, 60)
                total_t_format = '{:02d}:{:02d}:{:02d}'.format(t_h_time, t_m_time, t_s_time)
                self.lbl_totalTime.config(text=total_t_format)
                while (self.prog <= songLen):
                    if(self.exitStatus):
                        return
                    else:
                        self.prgBar.config(value=(self.prog / songLen) * 100)
                        c_m_time, c_s_time = divmod(self.prog, 60)
                        c_h_time, c_m_time = divmod(c_m_time, 60)
                        cur_time_format = '{:02d}:{:02d}:{:02d}'.format(c_h_time, c_m_time, c_s_time)
                        self.lbl_prgTime.config(text=cur_time_format)
                        self.prog += 1
                        myt.sleep(1)
                self.btn_play_pause.config(image=self.playImg)
                # if(self.myIndex == len(self.songsName)-1):
                #     self.myIndex = 0
            except:
                pass

        def progressStop(self):
            self.exitStatus = 1
            self.cur_Val = self.prog
            self.prgBar.config(value=(self.prog/round(MP3(self.songsName[self.myIndex]).info.length))*100)

        def progressResume(self):
            self.exitStatus = 0
            self.prog = self.cur_Val
            self.progressTimer = threading.Timer(0, self.progressInc)
            self.progressTimer.start()
            # print("Hey")

        # _________________Shuffle Methods_________________

        def shuffleOn(self):
            self.shuffleStatus = 1
            # self.lstbx_library.itemconfig(self.myIndex,bg="WHITE")
            self.prevIndex = self.myIndex
            self.myIndex = random.randint(0, len(self.songsName) - 1)
            # self.playSong()
            self.btn_shuffle.config(image=self.shuffleOnImg, command=self.shuffleOff)

        def shuffleOff(self):
            self.shuffleStatus = 0
            self.btn_shuffle.config(image=self.shuffleOffImg, command=self.shuffleOn)

        # _________________Previous Methods_________________

        def previousSong(self):
            if(self.prog > 6):
                self.exitStatus = 1
                myt.sleep(1)
                self.exitStatus = 0
                self.prgBar.config(value=0)
                self.prog = 0
                self.playSong()
                return

            self.exitStatus = 1
            myt.sleep(1)
            self.exitStatus = 0
            self.prgBar.config(value=0)
            self.prog = 0
            if (self.shuffleStatus == 0):
                self.prevIndex = self.myIndex
                try:
                    self.lstbx_library.itemconfig(self.myIndex, bg="WHITE")
                except:
                    pass
                if (self.myIndex == 0):
                    self.myIndex = len(self.songsName) - 1
                else:
                    self.myIndex -= 1
                self.playSong()
            elif (self.shuffleStatus == 1):
                try:
                    self.lstbx_library.itemconfig(self.myIndex, bg="WHITE")
                except:
                    pass
                self.myIndex = self.prevIndex
                self.prevIndex = random.randint(0, len(self.songsName) - 1)
                self.playSong()

        # _________________Play Song Methods_________________

        def playSong(self):
            if (len(self.songsName) == 0):  # or len(self.songsLoc) == 0):
                self.openFolder()
            else:
                # self.myIndex = self.songsName.index(self.lstbx_library.get(ACTIVE))
                # mySongLoc = "\\".join(self.songsLoc[self.myIndex].split("\\")[:-1])
                # os.chdir(mySongLoc)
                # self.btn_play_pause.config(image=self.pauseImg, command=self.pauseSong)
                # mixer.init()
                # mixer.music.load(self.songsLoc[self.myIndex])
                # mixer.music.play()
                # event.config(image=self.pauseImg, command=self.pauseSong)
                # print(self.myIndex)
                # self.lstbx_library.curselection()
                # songN = self.lstbx_library.get(self.lstbx_library.curselection()[0])
                # print(songN)
                # print(self.songsLoc)
                # print(self.songsName)
                # mixer.music.load(self.songLoader[self.myIndex])
                # if(self.initialiseVolume == 1):
                #     self.initialiseVolume=0
                #     mixer.music.set_volume(0.6)
                # if(self.initialiseWindow):
                #     self.initialiseWindow = 0
                #     self.myLibrary()
                #     self.destroy_Lstbx()
                try:
                    self.timer.cancel()
                except:
                    pass
                # try:
                #     mixer.music.stop()
                # except:
                #     pass

                os.chdir(self.songsLoc[self.myIndex])
                try:
                    # print(self.prevIndex)
                    self.lstbx_library.itemconfig(self.prevIndex, bg="WHITE")
                    self.lstbx_library.itemconfig(self.myIndex, bg="YELLOW")
                except:
                    pass
                mixer.init()
                mixer.music.load(self.songsName[self.myIndex])
                mixer.music.play()
                # mixer.music.set_endevent()

                # def invokeNextSong():
                #     self.nextSong()

                # self.myGIf()  # Error

                self.songLength = float(round(MP3(self.songsName[self.myIndex]).info.length)) + 2
                self.timer = threading.Timer(self.songLength, self.nextSong)
                self.timer.start()

                # self.prgBar = Progressbar(self.frameScrubbar, length=320, orient=HORIZONTAL,
                #                           maximum=100,
                #                           value=0)
                # self.prgBar.pack()

                # self.prog = 0
                self.progressTimer = threading.Timer(0, self.progressInc)
                self.progressTimer.start()
                # self.progressTimer.setDaemon(TRUE)

                self.currentSongTitleArtist()
                self.juststarted = 0
                self.btn_play_pause.config(image=self.pauseImg, command=self.pauseSong)

                # self.resumeSong()
                # self.progress()

                # print(mixer.music.get_busy())
                # self.btn_play_pause.config(image=self.pauseImg, command=self.pauseSong)


        def invokePlayNext(self):
            if(self.myIndex != len(self.songsName)-1):
                self.songLength = (float(round(MP3(self.songsName[self.myIndex]).info.length)) - self.prog) + 2
                self.timer = threading.Timer(self.songLength, self.nextSong)
                self.timer.start()

        def pauseSong(self):
            mixer.music.pause()
            self.isPaused = 1
            # self.haltMusic = mixer.music.get_pos() / 100
            # self.timer.cancel()
            self.btn_play_pause.config(image=self.playImg, command=self.resumeSong)
            self.progressStop()

            # while mixer.music.get_busy():
            #     continue
            # self.nextSong()

        def resumeSong(self):
            # print(mixer.music.get_pos())
            self.isPaused = 0
            mixer.music.unpause()
            self.progressResume()
            self.invokePlayNext()

            # print(self.songLength-self.haltMusic)
            # try:
            #     self.timer = threading.Timer(self.songLength-self.haltMusic, self.nextSong)
            #     self.timer.start()
            # except:
            #     pass

            # self.progress()
            self.btn_play_pause.config(image=self.pauseImg, command=self.pauseSong)

        # _________________Next Methods_________________

        def nextSong(self, arg = None):

            # self.prgBar.destroy()
            # print(self.isPaused)
            # print(arg)

            # Prevent from unnecessary threading invoke
            if(self.isPaused == 1 and arg != 1):
                # print("1")
                self.progressTimer.cancel()
                return

            if(self.shuffleStatus == 1):
                if (self.isPaused == 0 and self.prog < round(
                        MP3(self.songsName[self.prevIndex]).info.length) and arg != 1):
                    # print(self.isPaused, self.prog, round(MP3(self.songsName[self.myIndex]).info.length))
                    # print("invoked")
                    # print("2")
                    return
            else:
                if(self.isPaused == 0 and self.prog < round(MP3(self.songsName[self.myIndex]).info.length) and arg != 1):
                    # print(self.isPaused, self.prog, round(MP3(self.songsName[self.myIndex]).info.length))
                    # print("invoked")
                    # print("3")
                    return
            # print(self.prog)

            self.exitStatus = 1
            myt.sleep(1)
            self.exitStatus = 0
            self.prgBar.config(value=0)
            self.prog = 0


            # if self.timer == 1:
            #     self.timer.cancel()
            # print(self.repeatStatus)
            if (self.repeatStatus == 0 and self.myIndex == len(self.songsName) - 1):
                mixer.music.stop()
            elif (self.repeatStatus == 1):
                self.playSong()
            else:
                if (self.shuffleStatus == 0):
                    try:
                        self.lstbx_library.itemconfig(self.prevIndex, bg="WHITE")
                    except:
                        pass
                    self.prevIndex = self.myIndex
                    try:
                        self.lstbx_library.itemconfig(self.myIndex, bg="WHITE")
                    except:
                        pass
                    if (self.myIndex == len(self.songsName) - 1):
                        self.myIndex = 0
                    else:
                        self.myIndex += 1
                    self.playSong()
                elif (self.shuffleStatus == 1):
                    try:
                        self.lstbx_library.itemconfig(self.prevIndex, bg="WHITE")
                        self.lstbx_library.itemconfig(self.myIndex, bg="WHITE")
                    except:
                        pass
                    self.shuffleOn()
                    self.playSong()

        # _________________Repeat Methods_________________

        def repeatOne(self):
            self.repeatStatus = 1
            self.btn_repeat.config(image=self.repeatOneImg, command=self.repeatAll)

        def repeatAll(self):
            self.repeatStatus = 2
            self.btn_repeat.config(image=self.repeatAllImg, command=self.repeatNorm)

        def repeatNorm(self):
            self.repeatStatus = 0
            self.btn_repeat.config(image=self.repeatNormImg, command=self.repeatOne)

        # _________________Open Folder Methods_________________

        def openFolder(self):
            try:
                directory = askdirectory()
                os.chdir(directory)
                # self.songsName=[]
                for files in os.listdir(directory):
                    if (files.endswith(".mp3")):
                        # print(files)
                        self.songsName.append(files)
                        # try:
                        #     self.songTitle.append(str(ID3(files)['TIT2'].text[0]))
                        #     # self.songArtist.append(str(ID3(files)['TPE1'].text[0]))
                        # except:
                        #     self.songTitle.append("Unknown")
                        # self.songArtist.append(str("Unknown"))
                        self.songsLoc.append(directory)
                if (len(self.songsName) == 0):
                    messagebox.showwarning("EMPTY FOLDER", "Music not found in this folder."
                                                           "\nPlease select a folder containing mp3 files.")

                # for root, dirs, files in os.walk("."):
                #     for filename in files:
                #         if(filename.endswith(".mp3")):
                #             self.songsName.append(str(filename))
                #             # print(os.path.abspath(filename))
                #             self.songLoader.append(os.path.abspath(filename))
                #             temp = "/".join(os.path.abspath(filename).split("\\")[:-1])
                #             self.songsLoc.append(temp)

            except:
                messagebox.showinfo("Oops!", "Folder could not select properly")

        # _________________Library Methods_________________

        def myLibrary(self):
            try:
                if(len(self.songsName)==0):
                    self.openFolder()
            except:
                pass
            self.frm_libraryWindow = Frame(root, bg="WHITE")
            self.frm_libraryWindow.place(relx=0.5, rely=0.44, anchor=CENTER)

            self.lstbx_library = Listbox(self.frm_libraryWindow, width=50, height=17)
            self.lstbx_library.grid(row=0, column=0)  # pack(side=LEFT, fill=Y)
            self.lstbx_library.bind('<Double-1>', self.invokeSong)

            self.vscrl_lstbx_library = Scrollbar(self.frm_libraryWindow, orient=VERTICAL)
            self.vscrl_lstbx_library.config(command=self.lstbx_library.yview)
            self.vscrl_lstbx_library.grid(row=0, column=1, ipady=112)  # pack(side=RIGHT, fill=Y)
            self.lstbx_library.config(bd=2, yscrollcommand=self.vscrl_lstbx_library.set)

            self.hscrl_lstbx_library = Scrollbar(self.frm_libraryWindow, orient=HORIZONTAL)
            self.hscrl_lstbx_library.config(command=self.lstbx_library.xview)
            self.hscrl_lstbx_library.grid(row=1, column=0, columnspan=2, ipadx=135)  # pack(fill=X)
            self.lstbx_library.config(bd=2, xscrollcommand=self.hscrl_lstbx_library.set)

            for i in range(len(self.songsName)):
                self.lstbx_library.insert(END, str(i + 1) + ". " + self.songsName[i])
                self.lstbx_library.itemconfig(i, bg="WHITE")
            self.btn_library.config(command=self.destroy_Lstbx)
            try:
                self.lstbx_library.itemconfig(self.myIndex, bg="YELLOW")
            except:
                pass

        def invokeSong(self, event):
            self.exitStatus = 1
            myt.sleep(1)
            self.exitStatus = 0
            self.prgBar.config(value=0)
            self.prog = 0
            self.lstbx_library.itemconfig(self.prevIndex, bg="WHITE")
            self.lstbx_library.itemconfig(self.myIndex, bg="WHITE")
            filterSongName = self.lstbx_library.get(ACTIVE)
            filterSongName = filterSongName[filterSongName.find(" ") + 1:]
            self.myIndex = self.songsName.index(filterSongName)
            self.prevIndex = self.myIndex
            # print(self.myIndex)
            self.playSong()

        def destroy_Lstbx(self):
            self.frm_libraryWindow.destroy()
            self.btn_library.config(command=self.myLibrary)

        # _________________Title Methods_________________
        def currentCover(self):
            try:
                my_mp3 = stagger.read_tag(self.songsName[self.myIndex])
                cover_data = BytesIO(my_mp3[stagger.id3.APIC][0].data)
                cover_image = Image.open(cover_data)
                # basewidth = 340
                # wpercent = (basewidth / float(cover_image.size[0]))
                # hsize = int((float(cover_image.size[1]) * float(wpercent)))
                img = cover_image.resize((340,340), Image.ANTIALIAS)
                # img.save('temp.jpg')
                cur_photo = ImageTk.PhotoImage(img)
                self.lbl_coverPic.config(image=cur_photo)
                self.lbl_coverPic.image = cur_photo
            except:
                self.lbl_coverPic.config(image=self.coverImg)


        def currentSongTitleArtist(self):
            self.currentCover()
            try:
                tag = EasyID3(self.songsName[self.myIndex])
                # songTitle = str(ID3(self.songsName[self.myIndex])['TIT2'].text[0]) \
                #             + "\n" + str(ID3(self.songsName[self.myIndex])['TPE1'].text[0])
                songTitle = str(self.myIndex+1)+". "+str(tag['title'][0])+"\nArtist: "+str(tag['artist'][0])+"\nAlbum: "+str(tag['album'][0])
            except:
                songTitle = str(self.myIndex+1)+". "+str(self.songsName[self.myIndex]) + "\nArtist: Unknown\nAlbum: Unknown"
            self.lbl_TitleArtist.config(text=songTitle)

        # _________________Search Methods_________________

        def searchAndPlay(self, event=None):
            getIndex = self.entry_search.get().strip()
            try:
                if (getIndex == ""):
                    return
                else:
                    temp = int(getIndex)
                    if (0 < temp <= len(self.songsName)):
                        self.exitStatus = 1
                        myt.sleep(1)
                        self.exitStatus = 0
                        self.prgBar.config(value=0)
                        self.prog = 0
                        self.prevIndex = self.myIndex
                        self.myIndex = temp - 1
                        self.playSong()
                    else:
                        messagebox.showerror("OUT OF RANGE!", "MUSIC NOT FOUND!")
            except:
                messagebox.showwarning("INVALID INDEX!", "Index must be integer.")

        def keyInvoke(self, event):
            # print(ord(event.char))
            try:
                if (event.char == " " and self.juststarted==1 ):
                    # print("PLAY")
                    self.playSong()
                elif (event.char == " " and self.isPaused == 1):
                    # self.isPaused = 0
                    # print("space play")
                    self.resumeSong()
                elif (event.char == " " and self.isPaused == 0):
                    # print("space paused")
                    # self.isPaused = 1
                    self.pauseSong()
            except:
                pass




    volume = MusicPlayer()
    volume.VolumeWindow(root, "BLUE", 40)

    # cover = MusicPlayer()
    # cover.CoverWindow(root, "YELLOW", 350)

    # title = MusicPlayer()
    # title.Frames(root, "AQUA", 30)
    #
    # artist = MusicPlayer()
    # artist.Frames(root, "BLACK", 20)
    #
    # scrubBar = MusicPlayer()
    # scrubBar.Frames(root, "GREEN", 30)

    controls = MusicPlayer()
    controls.ControlWindow(root)

    # def pr():
    #     print("Function")

    # root.bind("<Key>", controls.keyInvoke)
    root.bind("<Key>", lambda x: controls.keyInvoke(x))





    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            mixer.music.stop()
            try:
                controls.timer.cancel()
                controls.timer.join()
            except:
                pass
            root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
