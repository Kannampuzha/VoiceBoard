from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import Scale
import pyscreenshot as ImageGrab
from speech_recogniser import audio_to_text
from recorder import record_to_file
import multiprocessing
import subprocess
import os

class main:
    def __init__(self, master):
        self.root = master
        self.root.title("WHITEBOARD"
                        )
        self.root.geometry("1300x700")
        self.color_fg = 'black'#Colour of pen
        self.color_bg = 'white'#Background colour
        self.root.configure(background='white')
        self.root.resizable(0,0)
        self.color_frame=LabelFrame(self.root,relief=RIDGE,bg='white')
        self.color_frame.place(x=0,y=0,width=40,height=210)
        self.state=0
        self.clicked=0
        self.clicked1=0

        #making colour buttons

        colors=['blue','black','red','#00a5f9','#682cbf','#009888']
        i=7
        j=0
        for color in colors:
            if color=='blue':
                Button(self.color_frame,bd=3,bg=color,relief=RIDGE,width=1,command=self.change_colorblue).grid(row=i,column=j)
            elif color=='black':
                Button(self.color_frame, bd=3, bg=color, relief=RIDGE, width=1, command=self.change_colorblack).grid(
                    row=i, column=j)
            elif color=='red':
                Button(self.color_frame, bd=3, bg=color, relief=RIDGE, width=1, command=self.change_colorred).grid(
                    row=i, column=j)
            elif color=='#00a5f9':
                Button(self.color_frame, bd=3, bg=color, relief=RIDGE, width=1, command=self.change_colora).grid(
                    row=i, column=j)
            elif color=='#682cbf':
                Button(self.color_frame, bd=3, bg=color, relief=RIDGE, width=1, command=self.change_colorb).grid(
                    row=i, column=j)
            elif color=='#009888':
                Button(self.color_frame, bd=3, bg=color, relief=RIDGE, width=1, command=self.change_colorc).grid(
                    row=i, column=j)
            i=i+1

        #making other buttons and placing them in apprprite place

        self.erazer_button=Button(self.root,text='ERAZE',font=('calibri',10),bd=0, bg= 'white' , command=self.eraze, width=8,relief=RIDGE)
        self.erazer_button.place(x=0,y=215)

        self.clear_button = Button(self.root, text='CLEAR', bd=0, bg='white', command=self.clear, width=8, relief=RIDGE)
        self.clear_button.place(x=0, y=245)

        self.save_button = Button(self.root, text='SAVE', bd=0, bg='white', command=self.save, width=8, relief=RIDGE)
        self.save_button.place(x=0, y=275)

        #A 'Listen' button is herby added
        self.recognise_button = Button(self.root,text = 'Listen' , bd=0 , bg = 'white' , command = self.recogniser, width = 8 , relief=RIDGE)
        self.recognise_button.place(x=0,y=650)

        #this is regarding the pen
        self.pen_size_scale_frame=LabelFrame(self.root,text='SIZE',bd=0,bg='white',font=('arial',8,'bold'),relief=RIDGE)
        self.pen_size_scale_frame.place(x=0,y=310,height=200,width=40)
        self.pen_size=Scale(self.pen_size_scale_frame,orient=VERTICAL,from_=0,to=25,command=self.changeW,length=170)
        self.pen_size.set(1)
        self.pen_size.grid(row=0,column=1,padx=9)

        #making the canvas and making it recognise movements of the mouse
        self.canvas=Canvas(self.root,bg='white',bd=0,relief=GROOVE,height=680,width=1200)
        self.canvas.place(x=92,y=7)
        self.old_x = None
        self.old_y = None
        self.penwidth = 3

        #Binding the mouse , its motion and everything it does along with key press to some below defined functcions
        self.canvas.bind('<B1-Motion>', self.paint)  # drawing  line
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind("<Button-1>", self.set_cursor)
        self.canvas.bind("<Key>", self.handle_key)

    #All functions are defined below

    def r_callback(self,event):
        #Note : The text processing and recognition stuff happens here
        self.ax = event.x
        self.ay = event.y
        print("clicked at", event.x, event.y)
        self.canvas.unbind('<Button-1>')
        self.canvas.bind("<Button-1>", self.set_cursor)
        self.recognise_button['text']='Listening..'#Change the name to 'listening'
        self.recognise_button['state']='disabled'
        p1 = multiprocessing.Process(target=record_to_file, args=('speech.wav', ))
        p1.start()
        while True :
            if p1.is_alive() == False:
                #Change the font to change font of the text that comes after recognition
                self.canvas.create_text(self.ax, self.ay,anchor=NW,fill=self.color_fg,font="Arial 15", text=audio_to_text(),)
                self.recognise_button['state']='normal'
                self.recognise_button['bg']='white'
                self.recognise_button['text'] = 'Listen'
                break
            else:
                #print(p1.is_alive())
                self.canvas.update()
                continue

                
    def paint(self, e):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, e.x, e.y, width=self.penwidth, fill=self.color_fg,
                               capstyle=ROUND, smooth=True)
        self.old_x = e.x
        self.old_y = e.y
    def reset(self, e):  # resetting or cleaning the canvas
        self.old_x = None
        self.old_y = None

    def changeW(self, e):  # change Width of pen through slider
        self.penwidth = e

    def clear(self):      #clears the canvas
        self.canvas.delete(ALL)

#Below are the colorcahnging functions
    def change_colorblue(self):
        self.color_fg='blue'
    def change_colorblack(self):
        self.color_fg='black'
    def change_colorred(self):
        self.color_fg='red'
    def change_colora(self):
        self.color_fg='#00a5f9'
    def change_colorb(self):
        self.color_fg='#682cbf'
    def change_colorc(self):
        self.color_fg='#009888'
    def eraze(self):   #erazing stuff simply by changing colour of the brush to white
        self.color_fg='white'


    def save(self):
        # Making values for a screenshort
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        screenshort = ImageGrab.grab().crop((x, y, x1, y1))

        #Asking format
        filename: str = asksaveasfilename(initialdir="/home", title="Select file", filetypes=(
        ('JPEG', ('*.jpg', '*.jpeg', '*.jpe', '*.jfif')), ('PNG', '*.png'), ('PS','*.ps'),('BMP', ('*.bmp', '*.jdib')),
        ('GIF', '*.gif'),('PDF','*.pdf'),))
        print(filename)
        if filename.endswith('.ps'):
            #Saving a postscript file
            try:
                self.canvas.postscript(file=filename, colormode='color')
                messagebox.showinfo('File saved : ', str(filename))
            except:
                print('No file saved')

        elif filename.endswith('.pdf'):#This is the process that makes a pdf
            in_filename=filename.replace('.pdf','.ps')
            self.canvas.postscript(file=in_filename, colormode='color')
            process = subprocess.Popen(["ps2pdf", in_filename, filename])
            process.wait()
            os.remove(in_filename)
            #
            messagebox.showinfo('File saved : ', str(filename))

        else :
            try:
                screenshort.save(filename)
                messagebox.showinfo('File saved : ', str(filename))
            except:
                print('No file saved')


    def recogniser(self):
            self.recognise_button['bg']='#f0f0f0'
            self.canvas.bind('<Button-1>', self.r_callback)




#########################Following code deals with making the canvas text editable .
    def highlight(self, item):
        # mark focused item.  note that this code recreates the
        # rectangle for each update, but that's fast enough for
        # this case.
        bbox = self.canvas.bbox(item)
        self.canvas.delete("highlight")
        if bbox:
            i = self.canvas.create_rectangle(
                bbox, fill="white",
                tag="highlight"
                )
            self.canvas.lower(i, item)

    def has_focus(self):
        return self.canvas.focus()

    def has_selection(self):
        # hack to work around bug in Tkinter 1.101 (Python 1.5.1)
        return self.canvas.tk.call(self.canvas._w, 'select', 'item')

    def set_cursor(self, event):
        if self.canvas.type(CURRENT) != "text":
            self.canvas.focus_set()
            self.canvas.focus("")
            self.canvas.delete("highlight")
            return

        self.highlight(CURRENT)

        # move focus to item
        self.canvas.focus_set() # move focus to canvas
        self.canvas.focus(CURRENT) # set focus to text item
        self.canvas.select_from(CURRENT, 0)
        self.canvas.select_to(CURRENT, END)
        # move insertion cursor
        item = self.has_focus()
        if not item:
            return # or do something else

        # translate to the canvas coordinate system
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        self.canvas.icursor(item, "@%d,%d" % (x, y))
        self.canvas.select_clear()

    def handle_key(self, event):
        # widget-wide key dispatcher
        item = self.has_focus()
        if not item:
            return

        insert = self.canvas.index(item, INSERT)

        if event.char >= " ":
            # printable character
            if self.has_selection():
                self.canvas.dchars(item, SEL_FIRST, SEL_LAST)
                self.canvas.select_clear()
            self.canvas.insert(item, "insert", event.char)
            self.highlight(item)

        elif event.keysym == "BackSpace":
            if self.has_selection():
                self.canvas.dchars(item, SEL_FIRST, SEL_LAST)
                self.canvas.select_clear()
            else:
                if insert > 0:
                    self.canvas.dchars(item, insert-1, insert)
            self.highlight(item)

        # navigation
        elif event.keysym == "Home":
            self.canvas.icursor(item, 0)
            self.canvas.select_clear()
        elif event.keysym == "End":
            self.canvas.icursor(item, END)
            self.canvas.select_clear()
        elif event.keysym == "Right":
            self.canvas.icursor(item, insert+1)
            self.canvas.select_clear()
        elif event.keysym == "Left":
            self.canvas.icursor(item, insert-1)
            self.canvas.select_clear()
        else:
            pass # print event.keysym
###################################################

if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('BOARD')
    root.mainloop()




