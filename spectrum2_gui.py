# Author: Hugues Ripoche
# Copyright (c) 2002-2011
# License: BSD Style.
# python version: 2.6

import Tkinter, tkFileDialog, tkMessageBox, spectrum2

class Application(Tkinter.Frame):

    def get_ascii_file(self):
        self.ascii_file_value = tkFileDialog.askopenfilename()
        return self.ascii_file_value

    def get_output_file(self):
        self.output_file_value = tkFileDialog.asksaveasfilename()
        return self.output_file_value

    def get_log_file(self):
        self.log_file_value = tkFileDialog.asksaveasfilename()
        return self.log_file_value

    def get_img_file(self):
        self.img_file_value = tkFileDialog.asksaveasfilename()
        return self.img_file_value

    def run(self):
        hashtable = {}
        try:
            hashtable["ascii_file"] = self.ascii_file_value.encode('ascii')
            hashtable["output_file"] = self.output_file_value.encode('ascii')
            hashtable["log_file"] = self.log_file_value.encode('ascii')
            hashtable["img_file"] = self.img_file_value.encode('ascii')
            hashtable["delta"] = float(self.delta_StringVar.get())
            hashtable["parental_mass"] = float(self.parental_mass_StringVar.get())
            hashtable["theoretical_fragment_masses"] = map(float,self.theoretical_mass_text.get('1.0',Tkinter.END).encode('ascii').split())
        except ValueError:
            tkMessageBox.showerror("ValueError", "Bad input format")

        mode_text = ""
        tuple = self.mode_listbox.curselection()
        print "tuple=",tuple
        if tuple == ():
            tkMessageBox.showerror("TclError: bad listbox index", "Select mode")
        else:
            mode_text = self.mode_listbox.get(tuple)
            print "mode_text=",mode_text
            try:
                log_file = open(hashtable["log_file"],"w")
                print >>log_file, "ascii_file\t" + hashtable["ascii_file"]
                print >>log_file, "output_file\t" + hashtable["output_file"]
                print >>log_file, "log_file\t" + hashtable["log_file"]
                print >>log_file, "img_file\t" + hashtable["img_file"]
                print >>log_file, "delta\t" + str(hashtable["delta"])
                print >>log_file, "parental_mass\t" + str(hashtable["parental_mass"])
                print >>log_file, "theoretical_fragment_masses\t" + " ".join(map(str,hashtable["theoretical_fragment_masses"]))
                log_file.close()
                delta = 0
                delta = hashtable["delta"]
                fragments = spectrum2.Fragments(hashtable["ascii_file"],hashtable["parental_mass"],hashtable["theoretical_fragment_masses"],delta,mode_text)
                fragments.print_get_lines(hashtable["output_file"])
                fragments.plot_lines(hashtable["img_file"],mode_text)
            except IOError:
                tkMessageBox.showerror("IOError", "Bad filename or Input/Output problem")
        return

    def initVars(self):
        self.ascii_file_value = ""
        self.output_file_value = ""
        self.log_file_value = ""
        self.img_file_value = ""

    def createWidgets(self):

        buttons_frame = Tkinter.Frame(self,borderwidth=1)
        self.ascii_file_button = Tkinter.Button(buttons_frame, text="Ascii file", command=self.get_ascii_file)
        self.ascii_file_button.pack(side=Tkinter.LEFT)
        self.output_file_button = Tkinter.Button(buttons_frame, text="Output file", command=self.get_output_file)
        self.output_file_button.pack(side=Tkinter.LEFT)
        self.log_file_button = Tkinter.Button(buttons_frame, text="Log file", command=self.get_log_file)
        self.log_file_button.pack(side=Tkinter.LEFT)
        self.img_file_button = Tkinter.Button(buttons_frame, text="Image file (pdf)", command=self.get_img_file)
        self.img_file_button.pack(side=Tkinter.LEFT)
        self.run_button = Tkinter.Button(buttons_frame, text="Run", command=self.run)
        self.run_button.pack(side=Tkinter.LEFT)
        self.quit_button = Tkinter.Button(buttons_frame)
        self.quit_button["text"] = "Quit"
        self.quit_button["fg"] = "black"
        self.quit_button["command"] = self.quit
        self.quit_button.pack({"side" : "left"})
        buttons_frame.pack()

        delta_frame = Tkinter.Frame(self,borderwidth=1)
        self.delta_label = Tkinter.Label(delta_frame, text="Delta")
        self.delta_label.pack(side=Tkinter.LEFT)
        self.delta_StringVar = Tkinter.StringVar()
        self.delta_StringVar.set(0.1)
        self.delta_entry = Tkinter.Entry(delta_frame,textvariable=self.delta_StringVar)
        self.delta_entry.pack(side=Tkinter.LEFT)
        delta_frame.pack()

        parental_mass_frame = Tkinter.Frame(self,borderwidth=1)
        self.parental_mass_label = Tkinter.Label(parental_mass_frame, text="Parental Mass")
        self.parental_mass_label.pack(side=Tkinter.LEFT)
        self.parental_mass_StringVar = Tkinter.StringVar()
        self.parental_mass_entry = Tkinter.Entry(parental_mass_frame,textvariable=self.parental_mass_StringVar)
        self.parental_mass_entry.pack(side=Tkinter.LEFT)
        parental_mass_frame.pack()

        mode_frame = Tkinter.Frame(self,borderwidth=1)
        self.mode_label = Tkinter.Label(mode_frame, text="Mode")
        self.mode_label.pack(side=Tkinter.LEFT)
        self.mode_listbox = Tkinter.Listbox(mode_frame, selectmode = Tkinter.BROWSE)
        self.mode_listbox.insert(0,spectrum2.FILTER_MODE[0])
        self.mode_listbox.insert(1,spectrum2.FILTER_MODE[1])
        self.mode_listbox.selection_set(first=1) # default = FILTER_MODE[1]
        self.mode_listbox.pack(side=Tkinter.LEFT)
        mode_frame.pack()

        theoretical_mass_frame = Tkinter.Frame(self,borderwidth=1)
        self.theoretical_mass_label = Tkinter.Label(theoretical_mass_frame, text="Theoretical Masses")
        self.theoretical_mass_label.pack(side=Tkinter.LEFT)
        self.theoretical_mass_text = Tkinter.Text(theoretical_mass_frame)
        self.theoretical_mass_text.pack(side=Tkinter.LEFT)
        theoretical_mass_frame.pack()
        
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self,master)
        self.pack()
        self.initVars()
        self.createWidgets()
 
root = Tkinter.Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
