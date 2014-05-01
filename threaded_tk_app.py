from Tkinter import *
import time, sys, thread

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


def appthread():
    main()

try:
    thread.start_new_thread(appthread, ())
except:
    print "Failed to start appthread: %s" % repr(sys.exc_info())
    
exit = raw_input("Press Enter to exit\n")
exit = 1
time.sleep(1)

'''if __name__ == '__main__':
    main()  '''