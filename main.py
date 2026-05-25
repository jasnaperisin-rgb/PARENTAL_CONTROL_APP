import tkinter as tk
from tkinter import messagebox,simpledialog, ttk
import json
import datetime
import threading
import time
import os
import sys

CONFIG_FILE = "config.json"
ADMIN_PIN = "1234"



# ==========   CONFIG  ==========

def load_config():
    if not os.path.exists (CONFIG_FILE):
        return {"allowed_times": []}
    with open (CONFIG_FILE, "r") as f:
        return json.load(f)
    

def save_config(config):
    with open (CONFIG_FILE,"w") as f:
        json.dump(config,f, indent=4)


# ==========  TIME CHECK ==========

def is_allowed():
    config = load_config()
    now = datetime.datetime.now()

    for slot in config["allowed_times"]:
        start = datetime.datetime.strptime(slot["start"], "%Y-%m-%d %H:%M")
        end = datetime.datetime.strptime(slot["end"], "%Y-%m-%d %H:%M")

        if start <= now <= end:
            return True
    
    return False


#  ==========  LOCK  SCREEN  ==========

class LockScreen:
    def __init__(self,root):
        self.win = tk.Toplevel(root)
        self.win.attibutes("-fullscreen", True)
        self.win.configure(bg="black")

        label = tk.Label(self.win, text="Računalo zaključano\nPokušaj kasnije.",
                         fg="white",
                         bg="black",
                         font=("Arial" , 40))
        label.pack(expand=True)



        self.win.protocol("WM_DELETE_WINDOW", lambda:None)
        self.win.bind("<Alt-F4>", lambda e: "break")



#  ========== ADMIN  GUI  ==========

class AdminGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Parental Control -Admin")
        self.root.geometry("500x400")

        tk.Label(self.root, text="Start (YYYY-MM-DD HH:MM)").pack()
        self.start_entry = tk.Entry(self.root)
        self.start_entry.pack()

        tk.Label(self.root, text="End (YYYY-MM-DD HH:MM)").pack()
        self.end_entry = tk.Entry(self.root)
        self.end_entry.pack()

        tk.Button(self.root, text="Dodaj raspored", command=self.add_schedule).pack(pady=5)

        tk.Button(self.root, text="Obriši odabrani", command=self.delete_selected).pack(pady=5)

        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("start", "end")
        self.tree.heading("#0", text="ID")
        self.tree.heading("start", text="Start")
        self.tree.heading("end", text="End")
        self.tree.pack(expand=True, fill="both")

        self.refresh_list()

    def add_schedule(self):
        start = self.start_entry.get()
        end = self.end_entry.get()

        try:
            datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
            datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")
        except:
            messagebox.showerror("Greška", "Neispravan format!")
            return
        
        config = load_config()
        config["allowed_times"].append({"start": start, "end": end})
        save_config(config)

        self.refresh_list()
        messagebox.showinfo("OK", "Dodano!")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

            config = load_config()
            for i, slot in enumerate(config["allowed_times"]):
                self.tree.insert("","end", iid=i,text=str(i),
                                 values=(slot["start"], slot["end"]))
                
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        index = int(selected[0])

        config = load_config()
        config["allowed_times"].pop(index)
        save_config(config)

        self.refresh_list()


    def run(self):
        self.root.mainloop()


 #  ============  MONITOR ============

def monitor(root):
    lock_screen = None

    while True:
        if not is_allowed():
            if lock_screen is None:
                root.after(0, lambda: LockScreen(root))
                lock_screen = True
        else:
            lock_screen = None

        time.sleep(10)


 #  =============   PIN   =============


def ask_pin():
    r = tk.Tk()
    r.withdraw()

    pin = simpledialog.askstring("PIN", "Unesi admin PIN:", show="*")

    print("Uneseni PIN:", pin)   # DEBUG

    if pin is None:
        return False

    return pin.strip() == ADMIN_PIN
        

 # ================MAIN  ===============


       
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "admin":
            print("ADMIN mode pokrenut")

            if ask_pin():
                print("PIN OK")
                app = AdminGUI()
                app.run()
            else:
                print("Pogrešan PIN")
        else:
            print("CLIENT mode pokrenut")

            root = tk.Tk()
            root.withdraw()

            threading.Thread(target=monitor, args=(root,), daemon=True).start()
            root.mainloop()

    except Exception as e:
        print("GREŠKA:", e)
        input("Press Enter...")

    

        
                    
                
                
                
    