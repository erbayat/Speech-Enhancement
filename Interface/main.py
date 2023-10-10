import pygame
import soundfile as sf
import numpy as np
import tkinter as tk
import tkfilebrowser
import scipy.signal as signal
import os
class App:
        def __init__(self, window):
            pygame.mixer.init()
            self.radioButtonVariable = tk.StringVar()
            self.radioButtonVariable.set(1)
            tk.Label(window, text="Noise Reduction Interface", font=("Courier", 18)).pack()
            tk.Label(window, text="Designed by A.U. Kaypak, M. Basturk, E. Erbayat", font=("Courier", 10)).pack()
            self.channelLabel = tk.Label(window, text="Please Select Channel Type", font=("Courier", 10))
            self.singleButton = tk.Radiobutton(window, text="Single Channel", variable=self.radioButtonVariable, value=1)
            self.dualButton = tk.Radiobutton(window, text="Dual Channel", variable=self.radioButtonVariable, value=2)
            self.selectionButton = tk.Button(window, text="Select", command=self.channelButton)
            self.channelLabel.place(x=30, y=80)
            self.singleButton.place(x=250, y=80)
            self.dualButton.place(x=360, y=80)
            self.selectionButton.place(x=460, y=80)
            self.channelType = 0
            self.waitLabel = tk.Label(window, text="... Please Wait ...", font=("Courier", 10))
            self.noisySpeechButton = tk.Button(window, text="Select Noisy Speech File", command=self.getSpeechPath)
            self.noiseButton = tk.Button(window, text="Select Noise File", command=self.getNoisePath)
            self.desiredOutputButton = tk.Button(window, text="Select Desired Output Path", command=self.getOutputPath)
            self.speechPath = ""
            self.noisePath = ""
            self.outputPath = ""
            self.executeButton = tk.Button(window, text="Execute", command=self.executeButtonFunc, state = "disable")
            self.clearButton = tk.Button(window, text="Clear", command=self.clearButtonFunc)
            self.variableLabel = tk.Label(window, text="Type required variables  \u03BC: \t Order:", font=("Courier", 10))
            self.warningLabel = tk.Label(window, text="All paths and variables must be given to execute", font=("Courier", 10))
            self.muValueFloat = 0.0
            self.orderValueInt = 0
            self.betaValueFloat = 0.0
            self.muBox = tk.Entry(window, width=6)
            self.orderBox = tk.Entry(window, width=6)
            self.betaBox = tk.Entry(window, width=6)
            self.setVariableButton = tk.Button(window, text="Set", command=self.setVariableButtonFunc)
            self.filenameBox = tk.Entry(window, width=12)
            self.filenameLabel = tk.Label(window, text="Type desired file name without extension:", font=("Courier", 10))
            self.setOutputFilenameButton = tk.Button(window, text="Set", command=self.setOutputFilenameFunc)
            self.speechLabel = tk.Label(window, text="Input Speech:", font=("Courier", 10))
            self.outputLabel = tk.Label(window, text="Output Speech:", font=("Courier", 10))
            self.isVariablesSet = False
            self.isFilenameSet = False
            self.outputFilename = ""
            self.duration = 0.0

            self.sliderValueInput = tk.DoubleVar(value=0)
            self.sliderInput = tk.Scale()
            self.sliderValueOutput = tk.DoubleVar(value=0)
            self.sliderOutput = tk.Scale()

            self.bounImage = tk.PhotoImage(file = "boun.png")
            self.pauseImage = tk.PhotoImage(file = "pause.png")
            self.playImage = tk.PhotoImage(file="play.png")
            self.stopImage = tk.PhotoImage(file="stop.png")
            self.bounLabel = tk.Label(window, image = self.bounImage).place(x=6, rely=1, anchor=tk.SW)

            self.playSpeechButton = tk.Button(window, text="Play", command=self.playSpeechFunc, image = self.playImage)
            self.playOutputButton = tk.Button(window, text="Play", command=self.playOutputFunc, image = self.playImage)
            self.stopSpeechButton = tk.Button(window, text="Stop", command=self.stopSpeechFunc, image = self.stopImage)
            self.stopOutputButton = tk.Button(window, text="stop", command=self.stopOutputFunc, image = self.stopImage)
            self.speechPlaytime = 0
            self.outputPlaytime = 0
            self.loadedSound = 0

        def stopSpeechFunc(self):
            self.playSpeechButton["text"] = "Play"
            self.playSpeechButton["image"] = self.playImage
            self.loadedSound = 0
            self.sliderValueInput.set(0)
            pygame.mixer.music.stop()

        def stopOutputFunc(self):
            self.playOutputButton["text"] = "Play"
            self.playOutputButton["image"] = self.playImage
            self.loadedSound = 0
            self.sliderValueOutput.set(0)
            pygame.mixer.music.stop()

        def playSpeechFunc(self):
            if self.playSpeechButton["text"] == "Play":
                if self.loadedSound != 1:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.unload()
                    pygame.mixer.music.load(self.speechPath)
                    self.loadedSound = 1
                    pygame.mixer.music.play()
                    self.playOutputButton["text"] = "Play"
                    self.playOutputButton["image"] = self.playImage
                else:
                        pygame.mixer.music.unpause()
                self.playSpeechButton["text"] = "Pause"
                self.playSpeechButton["image"] = self.pauseImage
                self.TrackPlay(channel=1)
            else:
                self.playSpeechButton["text"] = "Play"
                self.playSpeechButton["image"] = self.playImage
                pygame.mixer.music.pause()

        def playOutputFunc(self):
            if self.playOutputButton["text"] == "Play":
                if self.loadedSound != 2:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.unload()
                        self.playSpeechButton["text"] = "Play"
                        self.playSpeechButton["image"] = self.playImage
                    pygame.mixer.music.load(self.outputFullPath)
                    self.loadedSound = 2
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.unpause()
                self.playOutputButton["text"] = "Pause"
                self.playOutputButton["image"] = self.pauseImage
                self.TrackPlay(channel=2)
            else:
                self.playOutputButton["text"] = "Play"
                self.playOutputButton["image"] = self.playImage
                pygame.mixer.music.pause()

        def checkAllPathsAreGiven(self):
            if self.speechPath != '' and (self.noisePath != '' or self.channelType == 1) and self.outputPath != '' and self.isVariablesSet and self.isFilenameSet:
                self.executeButton["state"] = "active"
                self.warningLabel.place_forget()

        def getSpeechPath(self):
            self.speechPath = tkfilebrowser.askopenfilename(filetypes=(("wav Files", "*.wav"), ("All Files", "*.*")), title = "Select Noisy Speech File", okbuttontext = "Select", foldercreation = False)
            self.checkAllPathsAreGiven()

        def getNoisePath(self):
            self.noisePath = tkfilebrowser.askopenfilename(filetypes=(("wav Files", "*.wav"), ("All Files", "*.*")), title = "Select Noise File", okbuttontext = "Select", foldercreation = False)
            self.checkAllPathsAreGiven()

        def getOutputPath(self):
            self.outputPath = tkfilebrowser.askopendirname(title = "Select Desired Output Path", okbuttontext = "Select", foldercreation = False)
            self.checkAllPathsAreGiven()

        def clearButtonFunc(self):
            self.showSettings()
            self.clearButton.place_forget()

        def TrackPlay(self, channel = 1):
                if pygame.mixer.music.get_busy():
                    current = pygame.mixer.music.get_pos()
                    if channel == 1 and self.playSpeechButton["text"] != "Play":
                        self.sliderValueInput.set(current / 1000)
                    elif channel == 2 and self.playOutputButton["text"] != "Play":
                        self.sliderValueOutput.set(current / 1000)
                    window.after(100, lambda: self.TrackPlay(channel=channel))
                else:
                    if channel == 1 and self.playSpeechButton["text"] != "Play":
                        self.stopSpeechFunc()
                    elif channel == 2 and self.playOutputButton["text"] != "Play":
                        self.stopOutputFunc()

        def executeButtonFunc(self):
            self.executeButton.place_forget()
            self.waitLabel.place(relx=0.5, y=245, anchor=tk.CENTER)
            self.outputFullPath = self.outputPath + "\\" + self.outputFilename + ".wav"
            f = sf.SoundFile(self.speechPath)
            self.duration = f.frames / f.samplerate
            window.after(10, lambda: self.chooseMethod())

        def chooseMethod(self):
            if self.channelType == 1:
                spectral_substraction(self.speechPath, self.outputFullPath, self.betaValueFloat)
            else:
                adaptive_filtering(self.speechPath, self.noisePath, self.outputFullPath, self.muValueFloat, self.orderValueInt)
            self.showSounds()

        def setVariableButtonFunc(self):
            self.isVariablesSet = True
            if self.channelType == 1:
                try:
                    self.betaValueFloat = float(self.betaBox.get())
                except ValueError:
                    tk.messagebox.showerror(title="Error", message="\u03B2 must be a decimal number")
                    self.isVariablesSet = False
                    self.betaBox.delete(0, tk.END)
            else:
                try:
                    self.muValueFloat = float(self.muBox.get())
                except ValueError:
                    tk.messagebox.showerror(title="Error", message="\u03BC must be a decimal number")
                    self.isVariablesSet = False
                    self.muBox.delete(0, tk.END)
                try:
                    self.orderValueInt = int(self.orderBox.get())
                except ValueError:
                    tk.messagebox.showerror(title="Error", message="Order must be an integer")
                    self.isVariablesSet = False
                    self.orderBox.delete(0, tk.END)
            self.checkAllPathsAreGiven()

        def setOutputFilenameFunc(self):
            self.outputFilename = self.filenameBox.get()
            self.isFilenameSet = True
            self.checkAllPathsAreGiven()

        def showSounds(self):
            self.waitLabel.place_forget()
            self.noisySpeechButton.place_forget()
            self.desiredOutputButton.place_forget()
            self.filenameBox.place_forget()
            self.filenameLabel.place_forget()
            self.setOutputFilenameButton.place_forget()
            self.noiseButton.place_forget()
            self.variableLabel.place_forget()
            self.betaBox.place_forget()
            self.muBox.place_forget()
            self.orderBox.place_forget()
            self.setVariableButton.place_forget()
            self.warningLabel.place_forget()
            self.channelLabel.place_forget()
            self.singleButton.place_forget()
            self.dualButton.place_forget()
            self.selectionButton.place_forget()
            self.clearButton.place(relx=0.5, y=245, anchor=tk.CENTER)
            self.speechLabel.place(x=30, y=60)
            self.playSpeechButton.place(x=30, y=95)
            self.outputLabel.place(x=30, y=150)
            self.playOutputButton.place(x=30, y=185)
            self.inputSpeech = pygame.mixer.Sound(self.speechPath)
            self.outputSpeech = pygame.mixer.Sound(self.outputFullPath)
            self.stopSpeechButton.place(x=60, y=95)
            self.stopOutputButton.place(x=60, y=185)
            self.sliderInput = tk.Scale(to=self.duration, orient=tk.HORIZONTAL, length=400, resolution=1,
                                        showvalue=True, tickinterval=self.duration / 20, variable=self.sliderValueInput,
                                        state="disable")
            self.sliderInput.place(x=100, y=80)
            self.sliderOutput = tk.Scale(to=self.duration, orient=tk.HORIZONTAL, length=400, resolution=1,
                                         showvalue=True, tickinterval=self.duration / 20,
                                         variable=self.sliderValueOutput,
                                         state="disable")
            self.sliderOutput.place(x=100, y=170)

        def showSettings(self):
            self.sliderValueInput.set(0)
            self.sliderValueOutput.set(0)
            self.channelLabel.place(x=30, y=80)
            self.singleButton.place(x=250, y=80)
            self.dualButton.place(x=360, y=80)
            self.selectionButton.place(x=460, y=80)
            self.speechLabel.place_forget()
            self.outputLabel.place_forget()
            self.playSpeechButton.place_forget()
            self.playOutputButton.place_forget()
            self.stopSpeechButton.place_forget()
            self.stopOutputButton.place_forget()
            self.sliderOutput.place_forget()
            self.sliderInput.place_forget()

        def channelButton(self):
                self.noisySpeechButton.place(x=110, y=120)
                self.desiredOutputButton.place(x=350, y=120)
                self.executeButton.place(relx=0.5, y= 245, anchor=tk.CENTER)
                self.speechPath = ""
                self.noisePath = ""
                self.outputPath = ""
                self.isVariablesSet = False
                self.isFilenameSet = False
                self.executeButton["state"] = "disable"
                self.filenameBox.place(x=415, y=165, anchor=tk.CENTER)
                self.filenameLabel.place(relx=0.35, y=165, anchor=tk.CENTER)
                self.setOutputFilenameButton.place(x=470, y=165, anchor=tk.CENTER)
                self.muBox.delete(0,tk.END)
                self.betaBox.delete(0,tk.END)
                self.orderBox.delete(0,tk.END)
                self.filenameBox.delete(0,tk.END)
                if self.radioButtonVariable.get() == '1':
                        self.noiseButton.place_forget()
                        self.channelType = 1
                        self.variableLabel["text"] = "Type required variable  \u03B2:"
                        self.variableLabel.place(relx=0.45, y=190, anchor=tk.CENTER)
                        self.betaBox.place(x=398, y=190, anchor=tk.CENTER)
                        self.muBox.place_forget()
                        self.orderBox.place_forget()
                        self.setVariableButton.place(x=470, y=190, anchor=tk.CENTER)
                else:
                        self.noiseButton.place(x=250, y=120)
                        self.channelType = 2
                        self.variableLabel["text"] = "Type required variables  \u03BC: \t Order:"
                        self.betaBox.place_forget()
                        self.variableLabel.place(relx=0.40, y=190, anchor=tk.CENTER)
                        self.muBox.place(x=322, y=190, anchor=tk.CENTER)
                        self.orderBox.place(x=420, y=190, anchor=tk.CENTER)
                        self.setVariableButton.place(x=470, y=190, anchor=tk.CENTER)
                        self.warningLabel["text"] = "All paths and variables must be given to execute"
                self.warningLabel.place(relx=0.5, y= 215, anchor=tk.CENTER)

def spectral_substraction(input_path, output_path, beta = 1):
    input, fs = sf.read(input_path)
    window_size = int(25e-3 * fs)
    total_window_number = int(np.size(input) / window_size *2-1)
    shift = int(window_size/2)
    output = np.zeros(np.size(input))
    reference = input[0:window_size]
    my_window = np.hamming(window_size)
    Wn = 2500/(fs/2)
    sos = signal.butter(4, Wn, 'Low', output='sos')
    for i in range(total_window_number):
        windowed_input = my_window* input[shift*i: window_size+shift*i ]
        windowed_input_fft_abs = np.fft.fft(windowed_input)
        windowed_input_fft_phase = np.angle(windowed_input_fft_abs)
        windowed_input_fft_abs = np.abs(windowed_input_fft_abs)
        reference_fft_abs = np.abs(np.fft.fft(reference))
        dummy = windowed_input_fft_abs **2 - beta*reference_fft_abs ** 2
        dummy = np.maximum(dummy, 0)
        windowed_output_fft = dummy ** (1 / 2) * np.exp(1j * windowed_input_fft_phase)
        windowed_output = np.real(np.fft.ifft(windowed_output_fft))
        windowed_output = signal.sosfilt(sos,windowed_output)
        output[shift*i: window_size+shift*i] = output[shift*i: window_size+shift*i] + windowed_output
    if os.path.exists(output_path):
        os.remove(output_path)
    sf.write(output_path, output, fs)
    return input, output, fs

def adaptive_filtering(input_path, noise_path, output_path, mu = 0.01, order = 400):
    input, fs_input = sf.read(input_path)
    reference, fs_reference = sf.read(noise_path)
    if fs_input != fs_reference:
        my_list = input_path.split("/")
        in_path = '/'.join(my_list[0: len(my_list) - 1])
        file = open(in_path +"error_log.txt", "w")
        file.write('Error: Sampling rate of input and reference signals are different\n')
        file.close()
        exit(-1)
    else:
        fs = fs_input
    if len(input) > len(reference):
        my_list = input_path.split("/")
        in_path = '/'.join(my_list[0: len(my_list) - 1])
        file = open(in_path+"error_log.txt", "w")
        file.write('Error: Input length is greater than reference length\n')
        file.close()
        exit(-1)
    else:
        reference = reference[0:len((input))]
    ## Filter Parameters ##
    n = np.arange(len(input))
    window_size = int(25e-3 * fs)
    delayed = np.zeros([1, order])
    h = np.zeros([1, order])
    output = np.zeros(len(input))
    total_window_number = int(np.size(input) / window_size)
    windowed_input = np.zeros(window_size)
    windowed_output = np.zeros(window_size)
    for i in range(total_window_number):
        windowed_input = input[(i) * window_size: (i + 1) * window_size]
        my_reference = reference[(i) * window_size: (i + 1) * window_size]
        for k in range(window_size):
            delayed[:, 0] = my_reference[k]
            estimated_noise = np.matmul(delayed, np.transpose(h))
            windowed_output[k] = windowed_input[k] - estimated_noise
            h = h + 2 * mu * windowed_output[k] * delayed
            delayed[:, 1: order] = delayed[:, 0: order - 1]
        output[(i) * window_size: (i + 1) * window_size] = windowed_output
    if os.path.exists(output_path):
        os.remove(output_path)
    sf.write(output_path, output, fs)
    return input, output, fs

if __name__ == "__main__":

        window = tk.Tk()
        window.geometry("600x360")
        window.resizable(False, False)
        window.title("Noise Reduction")
        app = App(window)
        window.mainloop()