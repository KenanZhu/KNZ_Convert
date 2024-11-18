# @ File           : KNZ_Convert.py
#
# @ Brief          : GUI main functions.
#
# Copyright (c) 2024 - 2024 KenanZhu. All Right Reserved.
#
# @ Author         : KenanZhu
# @ Time stamp     : [2024/11/13] First release.
# @ IDE            : PyCharm
#
# ----------------------------------------------------------------------------------------
# ---SELPORT--- #
import rnx_convert as conv
# ---STDPORT--- #
import queue
import threading
import tkinter as tk

from tkinter import ttk
from PIL import ImageTk
from base64 import b64decode
from tkinter import filedialog
# ------------- #
# global const
InPaths = []
# io oath combox index
I_Box_Counter=0
O_Box_Counter=0
# io format list & index
I_Format_Rnx_List=0
I_RINEX_BoxList=['2','3']
O_Format_Rnx_List=0
O_RINEX_BoxList=['2.10','2.11','2.12','3.00','3.01','3.02','3.03','3.04','3.05']
# ------------------------------------------------------------------------------------- #
def instanceOPT(parenthwnd, func):
    OPTIONS(parenthwnd, func)

class CALLBACK:
    @staticmethod
    def Get_I_File(File_I_Box):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        global I_Box_Counter
        path = filedialog.askopenfilename(
            title='RINEX OBS File',
            filetypes=[('RINEX OBS File(*.o*.*.*obs.*.*d)', '*.*o;*.*obs;*.*d'),
                       ('All Files', '*.*')]
        )
        if path and path not in File_I_Box['value']:
            File_I_Box['value'] += (path,)
            I_Box_Counter += 1
            File_I_Box.current(I_Box_Counter)
    @staticmethod
    def Get_I_Files(Files_I_ShowText):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        global InPaths
        paths = filedialog.askopenfilenames(
            title='RINEX OBS File',
            filetypes=[('RINEX OBS File(*.o*.*.*obs.*.*d)', '*.*o;*.*obs;*.*d'),
                       ('All Files', '*.*')]
        )
        for path in paths:
            if path and path not in InPaths:
                InPaths.append(path)
        Files_I_ShowText.delete('1.0', 'end')
        for path in InPaths:
            Files_I_ShowText.insert('end', path + '\n')
    @staticmethod
    def Clear_I_Files(Files_I_ShowText):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        global InPaths
        InPaths.clear()
        Files_I_ShowText.delete('1.0', 'end')
    @staticmethod
    def Get_O_Dir(File_O_Box):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        global O_Box_Counter
        path = filedialog.askdirectory()
        if path and path not in File_O_Box['value']:
            File_O_Box['value'] += (path + '/',)
            O_Box_Counter += 1
            File_O_Box.current(O_Box_Counter)
    @staticmethod
    def Enable_YN(File_O_ynVar, File_O_Box, File_O_Button):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        if File_O_ynVar.get() == 0:
            File_O_Box.config(state=tk.DISABLED)
            File_O_Button.config(state=tk.DISABLED)
        else:
            File_O_Box.config(state=tk.NORMAL)
            File_O_Button.config(state=tk.NORMAL)

    def Dir_or_name_get(self, path, mode):
        # -------------------------------------------------------------------------------
        # >
        # Method: Dir_or_name_get
        # Brief : Get the filedir or filename form path
        # Param : path : file path
        #         mode : 0==get file name & 1==get file dir
        # Return: mode==0 return filename,mode==1 return file dir
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        global nameend, filename, filedir
        match mode:
            case 0:
                path_len = len(path)
                while path_len > 0:
                    sig = path[path_len - 1:path_len]
                    if sig == '\\' or sig == '/':
                        filename = path[path_len:]
                        return filename
                    path_len -= 1

            case 1:
                path_len = len(path)
                while path_len > 0:
                    sig = path[path_len - 1:path_len]
                    if sig == '\\' or sig == '/':
                        filedir = path[:path_len]
                        return filedir
                    path_len -= 1

    def Convert(self,
                 Pro_style, File_O_ynVar, File_I_BoxVar, File_O_BoxVar, Convertcards, Exec_Progress):
        # -------------------------------------------------------------------------------
        # >
        # Method:
        # Brief :
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        global InPaths
        Counter=0
        State_O=0
        InPath=[]
        ErrorMsg=''
        OutDirec=''
        out_path=''
        Pro_style.configure(
            'text.Horizontal.TProgressbar',
            text='Converting...')
        Exec_Progress.config(value=0)
        if   Convertcards.index('current')==0:
            if not File_I_BoxVar.get(): ErrorMsg+=' path'
            else: InPath.append(File_I_BoxVar.get())
        elif Convertcards.index('current')==1:
            if not InPaths: ErrorMsg+=' path'
            else: InPath=InPaths.copy()
        if File_O_BoxVar.get(): OutDirec = File_O_BoxVar.get()
        if not File_O_BoxVar.get():
            if File_O_ynVar.get(): ErrorMsg+=' directory'
            else : pass
        if ErrorMsg:
            ErrorMsg='Error : no'+ErrorMsg+' !'
            Exec_Progress.config(value=0)
            Pro_style.configure('text.Horizontal.TProgressbar', text=ErrorMsg)
            return
        #
        resqueue=queue.Queue()
        Pro_style.configure(
            'text.Horizontal.TProgressbar',
            text='Converting...')
        for in_path in InPath:
            if OutDirec:
                out_path=OutDirec+'COV-'+self.Dir_or_name_get(in_path,0)
            if not OutDirec:
                out_path=(self.Dir_or_name_get(in_path,1)+'COV-'+
                          self.Dir_or_name_get(in_path,0))
            State_O+=conv._Convert_Un(in_path,
                                      out_path,
                                      I_RINEX_BoxList[I_Format_Rnx_List],
                                      O_RINEX_BoxList[O_Format_Rnx_List],
                                      resqueue)
            Counter+=1
            Exec_Progress.config(value=int(Counter*100/len(InPath)))
            Pro_style.configure(
                'text.Horizontal.TProgressbar',
                text='Converting...%d/%d'%(Counter, len(InPath)))

        if State_O<=len(InPath):
            #Exec_Progress.config(value=0)
            Pro_style.configure(
                'text.Horizontal.TProgressbar',
                text='Complete !    %d successful.    %d fails.'%(State_O, len(InPath)-State_O))

    def _Convert(self,
                  Pro_style, File_O_ynVar, File_I_BoxVar, File_O_BoxVar, Convertcards, Exec_Progress):

        T=threading.Thread(target=lambda :
        self.Convert(Pro_style, File_O_ynVar, File_I_BoxVar, File_O_BoxVar, Convertcards, Exec_Progress))
        T.start()

    @staticmethod
    def Move_center(hwnd, win_x, win_y):
        # -------------------------------------------------------------------------------
        # >
        # Method: Move_Ccenter
        # Brief : Move the window to the center of screen.
        # Param : hwnd : instance handle of window
        #         win_x: the x size of window
        #         win_y: the y size of window
        # Return: none
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        position_x = int((hwnd.winfo_screenwidth() - win_x) / 2)
        position_y = int((hwnd.winfo_screenheight() - win_y) / 2)
        hwnd.geometry(f'{win_x}x{win_y}+{position_x}+{position_y}')

# noinspection PyProtectedMember
class MAINGUI:
    def __init__(self, hwnd, func):
        # init
        # -------------------------------------------------------------------------------
        self.hwnd=hwnd
        self.func=func
        self.Pro_style=None
        self.ExecFrame=None
        self.BatchFrame=None
        self.SingleFrame=None
        self.Convertcards=None
        self.Exec_Progress=None

        self.File_O_ynVar=tk.IntVar()
        self.File_I_BoxVar=tk.StringVar()
        self.File_O_BoxVar=tk.StringVar()

        self.iconoptions=(b'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                          b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                          b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOrq6v/q6ur/6urq/+rq6'
                          b'v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v+CgoL/dnZ2/1RUVP9UVFT/VFRU'
                          b'/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU/3Z2dv+CgoL/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P'
                          b'/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                          b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                          b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/'
                          b'6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/4KCgv92dnb/VFRU/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP9'
                          b'UVFT/VFRU/1RUVP9UVFT/dnZ2/4KCgv/Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8'
                          b'PDw//Dw8P/w8PD/8PDw//Dw8P/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                          b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA6urqGAAAAAAAAAAAAAAAAAAAAAAA'
                          b'AAAAAAAAAAAAAADq6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+r'
                          b'q6v/q6ur/goKC/3Z2dv9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP92dnb/go'
                          b'KC/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw/8AA'
                          b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//8AAP//'
                          b'AAAAAAAAAAAAAAAAAAD//wAA//8AAAAAAAAAAAAAAAAAAP//AAD/fwAAAAAAAAAAAAAAAAAA//8AAA==')
        self.iconoptions=b64decode(self.iconoptions)
        self.iconoptions=ImageTk.PhotoImage(data=self.iconoptions)
        self.initGUI()

    def initGUI(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: initGUI
        # Brief : init of main gui
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.hwnd.title("KNZ_Convert")
        self.func.Move_center(self.hwnd, 400, 243)
        self.hwnd.maxsize( 1000, 243)
        self.hwnd.minsize(  400, 243)
        #
        icon_ico = (b'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAADjsAAA47AAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAA'
                    b'AAAAAAAAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAQAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAEgAAABAAAAAQAA'
                    b'AAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABIAAAAGAAAAAAAAAAAAAAAGAAAAEgAAABAAAAAQAAAAEAAAABAAAAAQAAA'
                    b'AEAAAABAAAAAQAAAAEAAAABIAAAAGAAAAAAAAAAAAAAAAAAAAAQAAALkAAAD3AAAA8AAAAPIAAADyAAAA8gAAAPIAAADyAAAA'
                    b'8gAAAPIAAADwAAAA9wAAALkAAAAAAAAAAAAAALkAAAD3AAAA8AAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADwAAAA9'
                    b'wAAALkAAAABAAAAAAAAAAAAAAARAAAA7wAAAP8AAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAAD/AAAA7w'
                    b'AAAA0AAAANAAAA7wAAAP8AAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAAD/AAAA7wAAABEAAAAAAAAAAAA'
                    b'AABAAAADxAAAA8gAAAB8AAAAMAAAAEQAAABAAAAAQAAAAEAAAABEAAAAMAAAAHwAAAPIAAADxAAAADAAAAAwAAADxAAAA8gAA'
                    b'AB8AAAAMAAAAEQAAABAAAAAQAAAAEAAAABEAAAAMAAAAHwAAAPIAAADxAAAAEAAAAAAAAAAAAAAAEAAAAPMAAADyAAAAEAAAA'
                    b'AAAAAABAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAQAAAA8gAAAPMAAAAMAAAADAAAAPMAAADyAAAAEAAAAAAAAAABAAAAAAAAAA'
                    b'AAAAAAAAAAAQAAAAAAAAAQAAAA8gAAAPMAAAAQAAAAAAAAAAAAAAAQAAAA8wAAAPIAAAARAAAAAAAAAAIAAAABAAAAAQAAAAE'
                    b'AAAACAAAAAAAAABEAAADwAAAA8QAAAAsAAAALAAAA8QAAAPAAAAARAAAAAAAAAAIAAAACAAAAAgAAAAEAAAACAAAAAAAAABEA'
                    b'AADyAAAA8wAAABAAAAAAAAAAAAAAABAAAADzAAAA8gAAABAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEAAAAPIAA'
                    b'ADzAAAADAAAAAwAAADzAAAA8gAAABAAAAAAAAAAAgAAAAEAAAABAAAAAgAAAAEAAAAAAAAAEAAAAPIAAADzAAAAEAAAAAAAAA'
                    b'AAAAAAEAAAAPMAAADyAAAAEAAAAAAAAAABAAAAAQAAAAEAAAABAAAAAgAAAAEAAAAAAAAAwwAAAMMAAAAAAAAAAAAAAMQAAAD'
                    b'DAAAAAAAAAAEAAAAAAAAABwAAAAcAAAAAAAAAAwAAAAAAAAAQAAAA8gAAAPMAAAAQAAAAAAAAAAAAAAAQAAAA8wAAAPIAAAAQ'
                    b'AAAAAAAAAAIAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAAAAAABAAAAAQAAAAAAAAAAAAAAAEAAADEA'
                    b'AAA0AAAABYAAAAAAAAAAAAAABAAAADyAAAA8wAAABAAAAAAAAAAAAAAABAAAADzAAAA8gAAABAAAAAAAAAAAAAAAAUAAAARAA'
                    b'AAEAAAABAAAAAQAAAAEQAAAA8AAAAPAAAAEQAAABEAAAAPAAAADwAAABIAAAAPAAAAEwAAANMAAAD/AAAAzwAAABgAAAAAAAA'
                    b'AEgAAAPIAAADzAAAAEAAAAAAAAAAAAAAAEAAAAPMAAADyAAAAEQAAAAAAAAADAAAAwgAAAPsAAADwAAAA8gAAAPIAAADyAAAA'
                    b'8wAAAPMAAADyAAAA8gAAAPMAAADzAAAA8gAAAPMAAADvAAAA8gAAAPwAAAD/AAAAzAAAAAAAAAAPAAAA8wAAAPMAAAAQAAAAA'
                    b'AAAAAAAAAAQAAAA8wAAAPIAAAARAAAAAAAAAAMAAADCAAAA+wAAAPAAAADyAAAA8gAAAPIAAADzAAAA8wAAAPIAAADyAAAA8w'
                    b'AAAPMAAADyAAAA8wAAAO8AAADzAAAA/AAAAP8AAADMAAAAAAAAAA8AAADzAAAA8wAAABAAAAAAAAAAAAAAABAAAADzAAAA8gA'
                    b'AABAAAAAAAAAAAAAAAAUAAAARAAAAEAAAABAAAAAQAAAAEQAAAA8AAAAPAAAAEQAAABEAAAAPAAAADwAAABIAAAAPAAAAEwAA'
                    b'ANMAAAD/AAAAzwAAABgAAAAAAAAAEgAAAPIAAADzAAAAEAAAAAAAAAAAAAAAEAAAAPMAAADyAAAAEAAAAAAAAAACAAAAAQAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAQAAAAAAAAAAAAAAAQAAAAEAAAAAAAAAAAAAAABAAAAxAAAANAAAAAWAAAAAAAAAA'
                    b'AAAAAQAAAA8gAAAPMAAAAQAAAAAAAAAAAAAAAQAAAA8wAAAPIAAAAQAAAAAAAAAAEAAAABAAAAAQAAAAEAAAACAAAAAQAAAAA'
                    b'AAADDAAAAwwAAAAAAAAAAAAAAwwAAAMMAAAAAAAAAAQAAAAAAAAAHAAAABwAAAAAAAAADAAAAAAAAABAAAADyAAAA8wAAABAA'
                    b'AAAAAAAAAAAAABAAAADzAAAA8gAAABAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAEAAAAPIAAADzAAAADAAAAAwAA'
                    b'ADzAAAA8gAAABAAAAAAAAAAAgAAAAEAAAABAAAAAgAAAAEAAAAAAAAAEAAAAPIAAADzAAAAEAAAAAAAAAAAAAAAEAAAAPMAAA'
                    b'DyAAAAEQAAAAAAAAACAAAAAQAAAAEAAAABAAAAAgAAAAAAAAARAAAA8AAAAPEAAAALAAAACwAAAPEAAADwAAAAEQAAAAAAAAA'
                    b'CAAAAAgAAAAIAAAABAAAAAgAAAAAAAAARAAAA8gAAAPMAAAAQAAAAAAAAAAAAAAAQAAAA8wAAAPIAAAAQAAAAAAAAAAEAAAAA'
                    b'AAAAAAAAAAAAAAABAAAAAAAAABAAAADyAAAA8wAAAAwAAAAMAAAA8wAAAPIAAAAQAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABA'
                    b'AAAAAAAABAAAADyAAAA8wAAABAAAAAAAAAAAAAAABAAAADxAAAA8gAAAB8AAAAMAAAAEQAAABAAAAAQAAAAEAAAABEAAAAMAA'
                    b'AAHwAAAPIAAADxAAAADAAAAAwAAADxAAAA8gAAAB8AAAAMAAAAEQAAABAAAAAQAAAAEAAAABEAAAAMAAAAHwAAAPIAAADxAAA'
                    b'AEAAAAAAAAAAAAAAAEQAAAO8AAAD/AAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA/wAAAO8AAAANAAAA'
                    b'DQAAAO8AAAD/AAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA/wAAAO8AAAARAAAAAAAAAAAAAAABAAAAu'
                    b'gAAAPcAAADwAAAA8gAAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPAAAAD3AAAAuQAAAAAAAAAAAAAAugAAAPcAAADwAAAA8g'
                    b'AAAPIAAADyAAAA8gAAAPIAAADyAAAA8gAAAPAAAAD3AAAAugAAAAEAAAAAAAAAAAAAAAAAAAAGAAAAEgAAABAAAAAQAAAAEAA'
                    b'AABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABIAAAAGAAAAAAAAAAAAAAAGAAAAEgAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAA'
                    b'ABAAAAAQAAAAEAAAABIAAAAGAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'EAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAA'
                    b'AAAAAAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    b'AAAAAAAAAAAAAAA////////////////QAGAApf0L+lAAYACgAAAAYAAAAGAAAABhdALoYQQCCGF0AghhAmQIYSpmGGEAAAhhA'
                    b'AAIYQAACGEAAAhhKmYYYQJkCGF0AghhBAIIYXQC6GAAAABgAAAAYAAAAFAAYACl/Qv6UABgAL///////////////8=')
        icon_ico = b64decode(icon_ico)
        icon_ico = ImageTk.PhotoImage(data=icon_ico)
        self.hwnd.tk.call('wm', 'iconphoto', self.hwnd._w, icon_ico)
        #
        self.initCONVERT()
        #
        self.initExecCtrl()
        #
        self.hwnd.protocol('WM_DELETE_WINDOW',self.hwnd.quit)
        self.hwnd.mainloop()

    def initCONVERT(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: initCONVERT
        # Brief : init of convert gui
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.Convertcards=tk.ttk.Notebook(self.hwnd)
        # Single convert
        # -------------------------------------------------------------------------------
        self.SingleConv()
        self.Convertcards.add(self.SingleFrame, text='Single Convert')
        # Batch convert
        # -------------------------------------------------------------------------------
        self.BatchConv()
        self.Convertcards.add(self.BatchFrame, text='Batch Convert')
        self.Convertcards.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx='0px', pady='0px')

    def SingleConv(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: SingleConv
        # Brief : Contrls of single convert
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.SingleFrame=ttk.Frame(self.hwnd)

        # Initialize of input frame
        File_I_Frame=tk.LabelFrame(
            self.SingleFrame,
            text='Object Observation of RINEX')
        File_I_Frame.pack(side=tk.TOP, fill=tk.X, padx='1px', pady='0px')

        # Initialize of input box
        File_I_Box=ttk.Combobox(
            File_I_Frame,
            width=47,
            height=4,
            values=('',),
            textvariable=self.File_I_BoxVar)
        File_I_Box.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, anchor='w', padx='1px', pady='1px')

        # Initialize of input Button
        File_I_Bbutton=ttk.Button(
            File_I_Frame,
            text='...',
            width=3,
            command=lambda :self.func.Get_I_File(File_I_Box))
        File_I_Bbutton.pack(side=tk.RIGHT, anchor='e', padx='1px', pady='1px')

    def BatchConv(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: BatchConv
        # Brief : Contrls of batch convert
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.BatchFrame=ttk.Frame(self.hwnd)

        #
        Files_I_Frame=tk.LabelFrame(
            self.BatchFrame,
            text='Objects Observation of RINEX')
        Files_I_Frame.pack(side=tk.TOP, fill=tk.X, padx='1px', pady='0px')

        #
        Files_I_CtrlFrame=ttk.Frame(Files_I_Frame)
        Files_I_CtrlFrame.pack(side=tk.RIGHT, fill=tk.Y, anchor='e', padx='1px', pady='1px')

        #
        Files_I_CtrlInput=ttk.Button(
            Files_I_CtrlFrame,
            text='...',
            width=3,
            command=lambda :self.func.Get_I_Files(Files_I_ShowText))
        Files_I_CtrlInput.pack(side=tk.TOP, anchor='e', padx='1px', pady='1px')

        Files_I_CtrlClear=ttk.Button(
            Files_I_CtrlFrame,
            text='x',
            width=3,
            command=lambda :self.func.Clear_I_Files(Files_I_ShowText))
        Files_I_CtrlClear.pack(side=tk.BOTTOM, anchor='e', padx='1px', pady='1px')

        #
        Files_I_ShowFrame=ttk.Frame(Files_I_Frame)
        Files_I_ShowFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, anchor='e', padx='1px', pady='1px')

        #
        ScrollbarX=ttk.Scrollbar(Files_I_ShowFrame,orient=tk.HORIZONTAL)
        ScrollbarX.pack(side=tk.BOTTOM, fill=tk.X)
        ScrollbarY=ttk.Scrollbar(Files_I_ShowFrame)
        ScrollbarY.pack(side=tk.RIGHT, fill=tk.Y)

        #
        Files_I_ShowText=tk.Text(
            Files_I_ShowFrame,
            xscrollcommand=ScrollbarX.set,
            yscrollcommand=ScrollbarY.set,
            height=4, wrap='none', font=('Segoe UI',9))
        Files_I_ShowText.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, anchor='w', padx='1px', pady='1px')
        ScrollbarX.config(command=Files_I_ShowText.xview)
        ScrollbarY.config(command=Files_I_ShowText.yview)

    def initExecCtrl(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: initExecCtrl
        # Brief : init of contrls
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.ExecFrame=ttk.Frame(self.hwnd)
        self.ExecFrame.pack(side=tk.TOP, fill=tk.X, padx='1px', pady='0px')
        #
        # -------------------------------------------------------------------------------
        self.ConvOut()
        #
        # -------------------------------------------------------------------------------
        self.ExecCtrl()

    def ConvOut(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: ConvOut
        # Brief : Contrls of output
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        ###
        File_O_Frame=tk.LabelFrame(
            self.ExecFrame,
            text='Output directory')
        File_O_Frame.pack(side=tk.TOP, fill=tk.X, padx='1px', pady='1px')

        #
        File_O_yn=ttk.Checkbutton(
            File_O_Frame,
            text='Directory',
            variable=self.File_O_ynVar,
            onvalue=1,
            offvalue=0,
            command=lambda :self.func.Enable_YN(
                self.File_O_ynVar,
                File_O_Box,
                File_O_Button))
        File_O_yn.pack(side=tk.LEFT, anchor='w', padx='1px', pady='0px')

        #
        File_O_Box=ttk.Combobox(
            File_O_Frame,
            width=36,
            height=4,
            values=('',),
            state=tk.DISABLED,
            textvariable=self.File_O_BoxVar)
        File_O_Box.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, anchor='w', padx='1px', pady='0px')

        #
        File_O_Button=ttk.Button(
            File_O_Frame,
            text='...',
            width=3,
            state=tk.DISABLED,
            command=lambda :self.func.Get_O_Dir(File_O_Box))
        File_O_Button.pack(side=tk.RIGHT, anchor='e', padx='1px', pady='0px')

    def ExecCtrl(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: ExecCtrl
        # Brief : Contrls of exe
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        CtrlButtonFrame=ttk.Frame(self.ExecFrame)
        CtrlButtonFrame.pack(side=tk.TOP, fill=tk.X, padx='1px', pady='0px')
        Conv_Option = ttk.Button(
            CtrlButtonFrame,
            image=self.iconoptions,
            width=3,
            command=lambda :instanceOPT(self.hwnd,self.func)
        )
        Conv_Option.pack(side=tk.RIGHT, padx='1px', pady='0px')
        #
        Conv_Button=ttk.Button(
            CtrlButtonFrame,
            text='Convert',
            width=10,
            command=lambda :self.func._Convert(
                self.Pro_style,
                self.File_O_ynVar,
                self.File_I_BoxVar,
                self.File_O_BoxVar,
                self.Convertcards,
                self.Exec_Progress))
        Conv_Button.pack(side=tk.RIGHT, padx='1px', pady='0px')
        #
        Exit_button=ttk.Button(
            CtrlButtonFrame,
            text='Exit',
            width=10,
            command=self.hwnd.quit)
        Exit_button.pack(side=tk.LEFT, padx='1px', pady='0px')

        #
        StateFrame=ttk.Frame(self.ExecFrame)
        StateFrame.pack(side=tk.TOP, fill=tk.X, padx='1px', pady='4px')
        self.Pro_style=ttk.Style(StateFrame)
        self.Pro_style.layout(
            'text.Horizontal.TProgressbar',
            [
                ('Horizontal.Progressbar.trough',
                    {'children': [('Horizontal.Progressbar.pbar',{'side': 'left', 'sticky': 'ns'})],
                     'sticky': 'nswe'}
                ),
                ('Horizontal.Progressbar.label',{'sticky': ''})
            ]
        )
        self.Pro_style.configure(
            'text.Horizontal.TProgressbar',
            text='No task.',
            foreground='#000000',
            font=('Segoe UI',9))
        self.Exec_Progress=ttk.Progressbar(
            StateFrame,
            value=0,
            length=400,
            maximum=100,
            mode='determinate',
            style='text.Horizontal.TProgressbar')
        self.Exec_Progress.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)


class OPTIONS:
    def __init__(self, parenthwnd, func):
        # init
        # -------------------------------------------------------------------------------
        self.func=func
        self.parenthwnd=parenthwnd

        self.opthwnd=None
        self.OptFrame=None
        self.ExeFrame=None
        self.MainFrame=None
        self.I_RINEX_Box=None
        self.O_RINEX_Box=None

        self.initGUI()

    def initGUI(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: initGUI
        # Brief : init of main gui
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.opthwnd=tk.Toplevel(self.parenthwnd)
        self.opthwnd.title("Options")
        self.opthwnd.resizable(0, 0)
        self.func.Move_center(self.opthwnd, 310, 110)

        # Set icon
        icon_ico=(b'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                  b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                  b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOrq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6'
                  b'urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v+CgoL/dnZ2/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU'
                  b'/1RUVP9UVFT/VFRU/3Z2dv+CgoL/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8P'
                  b'Dw//Dw8P/w8PD/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                  b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA6urq/+rq6v/q6'
                  b'ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/4KCgv92dnb/VFRU/1RUVP9UVFT/'
                  b'VFRU/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP9UVFT/dnZ2/4KCgv/Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8P'
                  b'D/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                  b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA6urqGAAAAAAAAAAAAAAAAAAAA'
                  b'AAAAAAAAAAAAAAAAADq6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q6ur/6urq/+rq6v/q'
                  b'6ur/goKC/3Z2dv9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP9UVFT/VFRU/1RUVP92dnb/goKC/8PDw//Dw8P'
                  b'/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw//Dw8P/w8PD/8PDw/8AAAAAAAAAAAAAAAAAAAAAAA'
                  b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//8AAP//AAAAAAAAAAAAAAAAAAD//wAA//8AA'
                  b'AAAAAAAAAAAAAAAAP//AAD/fwAAAAAAAAAAAAAAAAAA//8AAA==')
        icon_ico=b64decode(icon_ico)
        icon_ico=ImageTk.PhotoImage(data=icon_ico)
        self.opthwnd.tk.call('wm', 'iconphoto', self.opthwnd._w, icon_ico)

        # Mian frame
        self.MainFrame=ttk.Frame(self.opthwnd)
        self.MainFrame.pack()

        # init
        self.initOPTIONS()
        self.initEXECTRL()

    def initOPTIONS(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: initOPTIONS
        # Brief : Init options of format choose
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.OptFrame=ttk.Frame(self.MainFrame)
        self.OptFrame.pack(side=tk.TOP, fill=tk.BOTH)
        # -------------------------------------------------------------------------------
        # Origin format frame
        # -------------------------------------------------------------------------------
        I_FormatFrame=tk.LabelFrame(
            self.OptFrame,
            text='Origin Format')
        I_FormatFrame.pack(side=tk.LEFT, expand=tk.YES, padx='2px')


        Rnx_I_Frame=ttk.Frame(I_FormatFrame)
        Rnx_I_Frame.pack(side=tk.TOP, fill=tk.X, pady='2px', padx='2px')
        I_RINEX=ttk.Label(
            Rnx_I_Frame,
            text='RINEX:',
            style='I_RINEX.TLabel')
        I_RINEX.pack(side=tk.LEFT)
        self.I_RINEX_Box=ttk.Combobox(
            Rnx_I_Frame,
            width=10,
            values=I_RINEX_BoxList)
        self.I_RINEX_Box.set(I_RINEX_BoxList[I_Format_Rnx_List])
        self.I_RINEX_Box['state']='readonly'
        self.I_RINEX_Box.pack(side=tk.RIGHT)


        Rtc_I_Frame=ttk.Frame(I_FormatFrame)
        Rtc_I_Frame.pack(side=tk.TOP, fill=tk.X, pady='2px', padx='2px')
        I_RTCM=ttk.Label(
            Rtc_I_Frame,
            text='RTCM :',
            style='I_RTCM.TLabel')
        I_RTCM.pack(side=tk.LEFT)
        I_RTCM_BoxList=['2', '3', '4']
        I_RTCM_Box=ttk.Combobox(
            Rtc_I_Frame,
            width=10,
            state=tk.DISABLED,
            values=I_RTCM_BoxList)
        I_RTCM_Box.set(I_RTCM_BoxList[0])
        # I_RTCM_Box['state']='readonly'
        I_RTCM_Box.pack(side=tk.RIGHT)
        # -------------------------------------------------------------------------------
        # Target format frame
        # -------------------------------------------------------------------------------
        O_FormatFrame = tk.LabelFrame(
            self.OptFrame,
            text='Target Format')
        O_FormatFrame.pack(side=tk.RIGHT, expand=tk.YES, padx='2px')


        Rnx_O_Frame=ttk.Frame(O_FormatFrame)
        Rnx_O_Frame.pack(side=tk.TOP, fill=tk.X, pady='2px', padx='2px')
        O_RINEX=ttk.Label(
            Rnx_O_Frame,
            text='RINEX:',
            style='I_RINEX.TLabel')
        O_RINEX.pack(side=tk.LEFT)
        self.O_RINEX_Box=ttk.Combobox(
            Rnx_O_Frame,
            width=10,
            values=O_RINEX_BoxList)
        self.O_RINEX_Box.set(O_RINEX_BoxList[O_Format_Rnx_List])
        self.O_RINEX_Box['state']='readonly'
        self.O_RINEX_Box.pack(side=tk.RIGHT)


        Rtc_O_Frame=ttk.Frame(O_FormatFrame)
        Rtc_O_Frame.pack(side=tk.TOP, fill=tk.X, pady='2px', padx='2px')
        O_RTCM=ttk.Label(
            Rtc_O_Frame,
            text='RTCM :',
            style='I_RTCM.TLabel')
        O_RTCM.pack(side=tk.LEFT)
        O_RTCM_BoxList=['2', '3', '4']
        O_RTCM_Box=ttk.Combobox(
            Rtc_O_Frame,
            width=10,
            state=tk.DISABLED,
            values=O_RTCM_BoxList)
        O_RTCM_Box.set(I_RTCM_BoxList[0])
        # O_RTCM_Box['state']='readonly'
        O_RTCM_Box.pack(side=tk.RIGHT)

    def initEXECTRL(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: initEXECTRL
        # Brief : Init the gui of contrl frame
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        self.ExeFrame=ttk.Frame(self.MainFrame)
        self.ExeFrame.pack(side=tk.TOP, fill=tk.X, pady='2px', padx='2px')

        Cancel_Button = ttk.Button(
            self.ExeFrame,
            text='Cancel',
            command=self.opthwnd.destroy)
        Cancel_Button.pack(side=tk.LEFT)

        Confirm_Button = ttk.Button(
            self.ExeFrame,
            text='Confirm',
            command=lambda :[
                self.Get_IO_Format(),
                self.opthwnd.destroy()
            ])
        Confirm_Button.pack(side=tk.RIGHT)

    def Get_IO_Format(self):
        # -------------------------------------------------------------------------------
        # >
        # Method: Get_IO_Format
        # Brief : Get the origin & target file format
        # Author: @KenanZhu All Right Reserved.
        # -------------------------------------------------------------------------------
        global I_Format_Rnx_List, O_Format_Rnx_List
        I_Format_Rnx_List=I_RINEX_BoxList.index(self.I_RINEX_Box.get())
        O_Format_Rnx_List=O_RINEX_BoxList.index(self.O_RINEX_Box.get())


# Main program entry ---------------------------- #
if __name__ == "__main__":
    root=tk.Tk()
    call=CALLBACK()

    initGUI=MAINGUI(root, call)