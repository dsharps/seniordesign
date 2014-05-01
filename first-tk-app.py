from Tkinter import *

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="black")   
         
        self.parent = parent
        
        self.initUI()
    
    def initUI(self):
      
        self.parent.title("Joytone UI")
        self.pack(fill=BOTH, expand=1)

        

def main():
  
    root = Tk()
    root.geometry("320x240+0+50")
    #root.wm_overrideredirect(True)
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  