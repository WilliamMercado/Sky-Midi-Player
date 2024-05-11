import mido
from pywinauto.application import Application
import time
import warnings
import keyboard


warnings.simplefilter('ignore', category=UserWarning)


allNotes = [0 for _ in range(128)]
notes = []

pianoConverter = {
    58:"y",
    59:"y",
    60:"y",
    61:"u",
    62:"u",
    63:"i",
    64:"i",
    65:"o",
    66:"p",
    67:"p",
    68:"h",
    69:"h",
    70:"j",
    71:"j",
    72:"k",
    73:"l",
    74:"l",
    75:";",
    76:";",
    77:"n",
    78:"m",
    79:"m",
    80:",",
    81:",",
    82:".",
    83:".",
    84:"/",
    85:"/",
    86:"/"
}
# ---------------- Load midis here ---------------
# mid = mido.MidiFile("Test Midis/Undertale_-_Megalovania.mid")
# mid = mido.MidiFile("Test Midis\Everything Stays │ Adventure Time.mid")
# mid = mido.MidiFile("Test Midis\Suzume no Tojimari.mid.mid")
# mid = mido.MidiFile("Test Midis\Kataomoi.mid.mid")
mid = mido.MidiFile(r"Test Midis\birdhouse_in_your_soul.mid")
# -------------------------------------------------

mid.print_tracks(True)
# scan mid
for msg in mid:
    if msg.type == 'note_on' and msg.channel == 5:
        allNotes[msg.note] += 1
        if not msg.note in notes:
            notes.append(msg.note)
    # if msg.type == 'note_off' and msg.channel == 0:
    #     allNotes[msg.note] -= 1

notes.sort()
print(allNotes)
print(notes)

app = Application().connect(path=r"") # Sky path here

window = app["Sky"]
window.set_focus()
time.sleep(1)

NOTE_OFFSET = 0
for msg in mid.play():
    # sleep(0.1)
    
    if msg.type[0] == "n" and (msg.note + NOTE_OFFSET) in pianoConverter and msg.channel == 0:
        
        if msg.type == 'note_on':
            # send_keys("{" + pianoConverter[msg.note + NOTE_OFFSET] + " down}")
            keyboard.press(pianoConverter[msg.note + NOTE_OFFSET])
            # print(pianoConverter[msg.note] + " down")
            # send_keys(pianoConverter[msg.note])
        # elif msg.type == 'note_on':
        #     print(f"Missed Note: {msg.note}")
        else:
            # send_keys("{" + pianoConverter[msg.note + NOTE_OFFSET] + " up}")
            keyboard.release(pianoConverter[msg.note + NOTE_OFFSET])
            # print(pianoConverter[msg.note] + " up")

    if keyboard.is_pressed("v"):
        break
