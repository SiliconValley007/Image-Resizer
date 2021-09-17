import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image
from os import path

#Class to show Tooltip on hover over a widget
class CreateToolTip(object):
        def __init__(self, widget, width, height, text='widget info'):
            self.waittime = 500
            self.wraplength = 180 
            self.widget = widget
            self.text = text
            self.width = width
            self.height = height
            self.widget.bind("<Enter>", self.enter)
            self.widget.bind("<Leave>", self.leave)
            self.widget.bind("<ButtonPress>", self.leave)
            self.id = None
            self.tw = None

        def enter(self, event=None):
            self.widget.configure(background="gray85")
            self.schedule()

        def leave(self, event=None):
            self.widget.configure(background="SystemButtonFace")
            self.unschedule()
            self.hidetip()

        def schedule(self):
            self.unschedule()
            self.id = self.widget.after(self.waittime, self.showtip)

        def unschedule(self):
            id = self.id
            self.id = None
            if id:
                self.widget.after_cancel(id)

        def showtip(self, event=None):
            x = y = 0
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + self.width
            y += self.widget.winfo_rooty() + self.height
            self.tw = tk.Toplevel(self.widget)
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry("+%d+%d" % (x, y))
            label = ttk.Label(self.tw, text=self.text, justify='left',
                           background="#ffffff", relief='solid', borderwidth=1,
                           wraplength = self.wraplength, foreground="red")
            label.pack(ipadx=1)

        def hidetip(self):
            tw = self.tw
            self.tw= None
            if tw:
                tw.destroy()

#Function to select a file from the file system
def selectfile():
    try:
        filename = fd.askopenfilename(initialdir="/", title="Select a File", filetypes=(("All", "*.*"), ("PNG", "*.png*"), ("JPG", "*.jpg*"), ("JPEG", "*.jpeg*"), ("Bitmap", "*.bmp*")))
        select_image_entry.delete(0, "end")
        select_image_entry.insert(0, filename)
        file_location = select_image_entry.get()
        image = Image.open(file_location)
        current_width, current_height = image.size
        current_image_width_value_label.config(text = current_width)
        current_image_height_value_label.config(text = current_height)
    except AttributeError:
        pass
    
    
#Function to resize the image on the click of a button
def resizeImage():
    num = 0
    file_location = select_image_entry.get()
    if is_checked.get():
        fixed_height = int(image_height_entry.get())
        image = Image.open(file_location)
        height_percent = (fixed_height / float(image.size[1]))
        width_size = int((float(image.size[0])*float(height_percent)))
        new_image = image.resize((width_size, fixed_height), Image.NEAREST)
    else:
        width = int(image_width_entry.get())
        height = int(image_height_entry.get())
        image = Image.open(file_location)
        new_image = image.resize((width,height), Image.ANTIALIAS)
    new_filename = file_location[:-4]+"_resized"+file_location[-4:]
    while path.exists(new_filename):
        new_filename = file_location[:-4]+"_resized"+"_"+str(num)+file_location[-4:]
        num += 1
    new_image.save(new_filename)

root = tk.Tk()
root.title('Image Resizer')
root.resizable(False, False)
root.geometry('330x350')
root.configure(bg="#ffffff")

s = ttk.Style()
s.configure('TLabel', background='#ffffff')

select_image_label = ttk.Label(root, text="Image Resizer", padding=10, font=('Helvetica', 24), style="TLabel")
select_image_label.grid(column=0, row=0, columnspan = 3)
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

select_image_label = ttk.Label(root, text="Select a File  ", padding=10, style="TLabel")
select_image_label.grid(column=0, row=1, sticky=tk.W)

select_image_entry = ttk.Entry(root)
select_image_entry.grid(column = 1, row = 1, sticky=tk.W)

select_image_button = ttk.Button(root, text = "Select Image", command=selectfile, cursor="hand2")
select_image_button.grid(column = 2, row = 1, sticky=tk.W, padx=(10,10))

current_image_width_label = ttk.Label(root, text="Current Width : ", padding=10, style="TLabel")
current_image_width_label.grid(column=0, row=2, sticky=tk.W)

current_image_width_value_label = ttk.Label(root, text="0", padding=10, style="TLabel")
current_image_width_value_label.grid(column=1, row=2, sticky=tk.W)

current_image_height_label = ttk.Label(root, text="Current Height : ", padding=10, style="TLabel")
current_image_height_label.grid(column=0, row=3, sticky=tk.W)

current_image_height_value_label = ttk.Label(root, text="0", padding=10, style="TLabel")
current_image_height_value_label.grid(column=1, row=3, sticky=tk.W)

enter_image_width_label = ttk.Label(root, text="Enter Width  ", padding=10, style="TLabel")
enter_image_width_label.grid(column=0, row=4, sticky=tk.W)
image_width_entry = ttk.Entry(root)
image_width_entry.grid(column = 1, row = 4, sticky=tk.W)

enter_image_height_label = ttk.Label(root, text="Enter Height  ", padding=10, style="TLabel")
enter_image_height_label.grid(column=0, row=5, sticky=tk.W)
image_height_entry = ttk.Entry(root)
image_height_entry.grid(column = 1, row = 5, sticky=tk.W)

is_checked = tk.IntVar()
aspect_ratio_check = tk.Checkbutton(root, text = "Maintain Aspect Ratio", onvalue=1, offvalue=0, variable=is_checked, cursor="hand2")
aspect_ratio_check.grid(column = 0, row = 6, columnspan = 2, sticky=tk.W, padx=10, pady=(0,6))
CreateToolTip(aspect_ratio_check, 30, 26, "To maintain the aspect ratio of the image, the image width has to be adjusted. Therefore the new resized image might not have the same width as the width you entered.")


resize_image_button = ttk.Button(root, text = "Resize", command=resizeImage, cursor="hand2")
resize_image_button.grid(column = 2, row = 6, sticky=tk.W, padx=(10,0), pady=(0,10))

root.mainloop()
