import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
from pygame import mixer
import random

if __name__ == '__main__':
    root = Tk()
    root.geometry("340x520")
    root.title("MUSIC")
    root.iconbitmap(r"Images/Music_Player.ico")
    root.resizable(False, False)
    # root.minsize


    # root.attributes("-alpha",0.92)

    class MusicPlayer:

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
        starGif = PhotoImage(file="Images/Stars.gif")

        # _________________Variables_________________

        songsName = []
        # songLoader = []
        songsLoc = []
        myIndex = 0
        shuffleStatus = 0
        repeatStatus = 0
        prevIndex = 0
        backupVolume = 60
        initialiseWindow = 1

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

            self.frameCover = Frame(root, bg="YELLOW", height=350)
            self.frameCover.pack(fill=BOTH, expand=TRUE)

            self.lbl_coverPic = Label(self.frameCover, image=self.coverImg)
            self.lbl_coverPic.pack()

            self.frameTitle = Frame(root, bg="AQUA", height=30)
            self.frameTitle.pack(fill=BOTH, expand=TRUE)

            self.frameArtist = Frame(root, bg="BLACK", height=20)
            self.frameArtist.pack(fill=BOTH, expand=TRUE)

            self.frameScrubbar = Frame(root, bg="GREEN", height=30)
            self.frameScrubbar.pack(fill=BOTH, expand=TRUE)


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
                                   command=self.nextSong)
            self.btn_next.grid(row=0, column=3)

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

                os.chdir(self.songsLoc[self.myIndex])
                try:
                    self.lstbx_library.itemconfig(self.prevIndex, bg="WHITE")
                    self.lstbx_library.itemconfig(self.myIndex, bg="YELLOW")
                except:
                    pass
                mixer.init()
                mixer.music.load(self.songsName[self.myIndex])

                mixer.music.play()
                self.resumeSong()
                # self.btn_play_pause.config(image=self.pauseImg, command=self.pauseSong)

        def pauseSong(self):
            mixer.music.pause()
            self.btn_play_pause.config(image=self.playImg, command=self.resumeSong)

        def resumeSong(self):
            mixer.music.unpause()
            self.btn_play_pause.config(image=self.pauseImg, command=self.pauseSong)

        # _________________Next Methods_________________

        def nextSong(self):
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
            self.btn_repeat.config(image=self.repeatOneImg, command=self.repeatAll)

        def repeatAll(self):
            self.btn_repeat.config(image=self.repeatAllImg, command=self.repeatNorm)

        def repeatNorm(self):
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
                        self.songsLoc.append(directory)
                if(len(self.songsName) == 0):
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
            self.lstbx_library.itemconfig(self.myIndex, bg="YELLOW")

        def invokeSong(self, event):
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

        # _________________Search Methods_________________

        def searchAndPlay(self, event=None):
            getIndex = self.entry_search.get()
            try:
                if (getIndex == ""):
                    return
                else:
                    temp = int(getIndex)
                    if (0 < temp <= len(self.songsName)):
                        self.myIndex = temp - 1
                        self.playSong()
                    else:
                        messagebox.showerror("OUT OF RANGE!", "MUSIC NOT FOUND!")
            except:
                messagebox.showwarning("INVALID INDEX!", "Index must be integer.")


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

    root.mainloop()
