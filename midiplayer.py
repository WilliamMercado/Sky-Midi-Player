import tkinter as tk
from tkinter import filedialog as fd


import keyboard
import mido
import pywinauto as pwa


class SkyMidiPlayer():
    """The Wigit for a Sky Midi Player
    """
    def __init__(self, master:tk.Tk) -> None:
        self.convertion_table = {
            58:"y", 59:"y", 60:"y",
            61:"u", 62:"u",
            63:"i", 64:"i",
            65:"o",
            66:"p", 67:"p",
            68:"h", 69:"h",
            70:"j", 71:"j",
            72:"k",
            73:"l", 74:"l",
            75:";", 76:";",
            77:"n",
            78:"m", 79:"m",
            80:",", 81:",",
            82:".", 83:".",
            84:"/", 85:"/", 86:"/"
        }
        self.midi_file = ""
        self.offset    = 8
        self.track_no  = 4
        self.track_no2 = 4


        # Window and event setup
        self._master = master
        self._master.title("Sky Midi Player")
        self._master.geometry("500x300")

        # File select and file
        file_control = tk.Frame(padx=20)
        file_control.pack(fill="x")
        self.file_name_label = tk.Label(master=file_control,text="{No File Selected}",width=15)
        self.file_name_label.pack(side="left",expand=1)
        tk.Button(
            master=file_control,
            text="Select File",
            command=self.prompt_select_midi
        ).pack(side="left")

        # Play button
        tk.Button(
            master = master,
            text = "Play Midi",
            command = self.play_midi
        ).pack()

    def prompt_select_midi(self) -> None:
        """Promts the user to select a midi file 
        """
        self.midi_file = fd.askopenfilename(
            defaultextension="*.mid",
            filetypes=[("Midi Files", "*.mid")]
        )
        if self.midi_file:
            self.file_name_label.configure(text = self.midi_file)
        else:
            self.file_name_label.configure(text = "{No File Selected}")

    def play_midi(self) -> None:
        """Play the midi
        """
        handle = pwa.findwindows.find_window(title="Sky") # Sky path here
        window = pwa.Application().connect(handle=handle)["Sky"]
        window.set_focus()
        mid = mido.MidiFile(self.midi_file)
        for msg in mid.play():
            # sleep(0.1)

            if (msg.type[0] == "n" and (msg.note + self.offset) in self.convertion_table
                and (msg.channel == self.track_no or msg.channel == self.track_no2)):

                if msg.type == 'note_on':
                    keyboard.press(self.convertion_table[msg.note + self.offset])
                else:
                    keyboard.release(self.convertion_table[msg.note + self.offset])

            if keyboard.is_pressed("v"):
                break

if __name__ == '__main__':
    root = tk.Tk()
    SkyMidiPlayer(root)
    root.mainloop()
