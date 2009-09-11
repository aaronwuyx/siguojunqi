try:
    #python 2.x
    from Tkinter import *
except:
    #python 3.x
    from tkinter import *

def askyesno(title,msg):
    def retyes():
        nonlocal ret,t
        ret = True
        t.destroy()
    def retno():
        nonlocal t
        t.destroy()
    t = Toplevel()
    ret = False
    t.title(title)
    Label(t,text=msg+'\n').pack(side=TOP,expand=YES,fill=X)
    Button(t,text='Yes',width=5,command=retyes).pack(side=LEFT)
    Button(t,text='No',width=5,command=retno).pack(side=RIGHT)
    t.focus_set()
    t.grab_set()
    t.wait_window()
    return ret

if __name__=='__main__':
    Tk().withdraw()
    print(askyesno('Warning','continue?'))
