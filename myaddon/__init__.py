from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from aqt.gui_hooks import browser_will_show_context_menu

def merge_selected_notes(browser):
    #choose the notes that are selected
    selected_notes = browser.selectedNotes()

    #if its not two, stop
    if len(selected_notes) != 2:
        showInfo("Please select exactly TWO cards to merge.")
        return

    #actually fetch the notes/data in the notes
    note1 = mw.col.getNote(selected_notes[0])
    note2 = mw.col.getNote(selected_notes[1])

    #combine the two words into my preferred layout that ive always been using
    if "Front" in note1 and "Front" in note2:
        # Appends the text and adds the specific imperfect/perfect tag
        note1["Front"] = f"{note1['Front'].strip()} / {note2['Front'].strip()} (imperf,perf)"

    #merge the other fields
    fields_to_merge = ["Back", "Sentence", "Audio"]

    for field in fields_to_merge:
        if field in note1 and field in note2:
            val1 = note1[field].strip()
            val2 = note2[field].strip()

            #append the data if note 2 isnt the exact copy of ntoe 1
            if val2 and val1 != val2:
                #newline for audio, html for text fields
                separator = "\n" if field == "Audio" else "<br><br>"
                if val1:
                    note1[field] = f"{val1}{separator}{val2}"
                else:
                    note1[field] = val2

    #save the first nore
    note1.flush()

    #delete the second one since i dont need it anymore, its in teh first note
    try:
        #anki api 2.1.45 and above
        mw.col.remove_notes([note2.id])
    except AttributeError:
        #if its an older version this wont work
        mw.col.remNotes([note2.id])

    #refresh the window
    browser.model.reset()

    showInfo("Cards successfully merged!")


def add_context_menu_action(browser, menu):
    #adding the action to the right click window
    action = menu.addAction("Merge 2 Cards (Imperf/Perf)")
    action.triggered.connect(lambda _, b=browser: merge_selected_notes(b))

#adding the method to the context menu
browser_will_show_context_menu.append(add_context_menu_action)