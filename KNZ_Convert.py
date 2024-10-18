import threading
import tkinter as tk

from base64 import b64decode
from tkinter import filedialog, StringVar, IntVar
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk

import Read_o as obs

##Combox Count-er
ComboxCount  = 0
ComboxCount1 = 0

ObsPaths = []

def GetObsFilePath(ObsFileSelectBox):
    global ComboxCount
    path = filedialog.askopenfilename()
    if path and path not in ObsFileSelectBox['value']:
        ObsFileSelectBox['value'] += (path,)
        ComboxCount += 1
        ObsFileSelectBox.current(ComboxCount)

def GetObsFilesPath(ObsPathsShow):
    global ObsPaths
    paths = filedialog.askopenfilenames()
    for path in paths:
        if path and path not in ObsPaths:
            ObsPaths.append(path)
    ObsPathsShow.delete('1.0', 'end')
    for path in ObsPaths:
        ObsPathsShow.insert('end', path + '\n')

def ClearObsFilesPath(ObsPathsShow):
    global ObsPaths
    ObsPaths.clear()
    ObsPathsShow.delete('1.0','end')

def AskDirectory(AskDirectorySelectBox):
    global ComboxCount1
    path = filedialog.askdirectory()
    if path and path not in AskDirectorySelectBox['value']:
        AskDirectorySelectBox['value'] += (path + '/',)
        ComboxCount1 += 1
        AskDirectorySelectBox.current(ComboxCount1)

def AskOrNotCheck(AskOrNotCheckVar,
                  AskDirectorySelectBox,
                  AskDirectorySelectButton):

    if AskOrNotCheckVar.get() == 0:
        AskDirectorySelectBox.config(state=tk.DISABLED)
        AskDirectorySelectButton.config(state=tk.DISABLED)
    else:
        AskDirectorySelectBox.config(state=tk.NORMAL)
        AskDirectorySelectButton.config(state=tk.NORMAL)

def ConvertFile(ConvertState,
                ObsSelectBoxVar,
                AskOrNotCheckVar,
                DirectorySelectBoxVar,
                MainCradsOption):

    global ObsPaths
    ObsPath = []

    if MainCradsOption.index('current') == 0:
        if AskOrNotCheckVar.get():
            if not DirectorySelectBoxVar.get() and not ObsSelectBoxVar.get():
                ConvertState.config(text='Invalid Path & Directory !')
                return
            if not DirectorySelectBoxVar.get() and ObsSelectBoxVar.get():
                ConvertState.config(text='Invalid Directory !')
                return
            else:
                DirectoryOut = DirectorySelectBoxVar.get()

        if not AskOrNotCheckVar.get():
            DirectoryOut = ''

        if not ObsSelectBoxVar.get():
            ObsPath.clear()
            ConvertState.config(text='Invalid Path !')
            return
        else:
            ObsPath.clear()
            ObsPath.append(ObsSelectBoxVar.get())

    if MainCradsOption.index('current') == 1:
        if AskOrNotCheckVar.get():
            if not DirectorySelectBoxVar.get() and not ObsPaths:
                ConvertState.config(text='Invalid Path & Directory !')
                return
            if not DirectorySelectBoxVar.get() and ObsPaths:
                ConvertState.config(text='Invalid Directory !')
                return
            else:
                DirectoryOut = DirectorySelectBoxVar.get()

        if not AskOrNotCheckVar.get():
            DirectoryOut = ''

        if not ObsPaths:
            ObsPath.clear()
            ConvertState.config(text='Invalid Path !')
            return
        else:
            ObsPath.clear()
            ObsPath = ObsPaths.copy()
            pass

    state = 0
    count = 0
    ConvertState.config(text='Converting...')
    for Path in ObsPath:
        ConvertState.config(text='Converting... %d/%d'%(count, len(ObsPath)))
        state += obs.ReadObsVersion(Path, DirectoryOut)
        count += 1

    if state == len(ObsPath):
        ConvertState.config(text='Complete !  %d successful, %d fails'%(state, 0) )

    elif state and state < len(ObsPath):
        ConvertState.config(text='Complete !  %d successful, %d fails'%(state, len(ObsPath)-state) )

    elif state == 0:
        ConvertState.config(text='Fail !  %d successful, %d fails' % (0, len(ObsPath)) )

    ObsPath.clear()
    return

def _ConvertFile(ConvertState,
                 ObsSelectBoxVar,
                 AskOrNotCheckVar,
                 DirectorySelectBoxVar,
                 MainCradsOption):

    global ObsPaths

    T = threading.Thread(target=lambda :ConvertFile(ConvertState,
                                                    ObsSelectBoxVar,
                                                    AskOrNotCheckVar,
                                                    DirectorySelectBoxVar,
                                                    MainCradsOption))
    T.start()


def InitGUI(hwnd):

    # GUI Instantiate
    hwnd.title("KNZ_Convert")
    hwnd.geometry('400x400')
    hwnd.minsize(400, 230)
    hwnd.maxsize(400, 230)

    icon_ico =(b'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAA'
               b'ABAAAPY6AQD2OgEAAAAAAAAAAAA6IjAAMywqADItKQMyLSkAMi0pADIt'
               b'KQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMi0pADItKQAyLSkB'
               b'Mi0pAjItKQAyLSkAMi0oADItKAAyLSgAMi0oADItKAEyLSgBMi0pADIt'
               b'KQAyLSgAMi0oAAAAAAAAAAAAAAAAADItKQAyLSkBMi0pADItKRkyLSlH'
               b'Mi0pUzItKVMyLSlTMi0pVDItKVQyLSlUMi0pUzItKVQyLSlSMi0pOzIt'
               b'KQoyLSkAMi0pATItKAAyLSgSMi0oIjItKBcyLSgIMy0pAA8+CQAyLSgB'
               b'Mi0oATItKAAyLSgAMi0pAAAAAAAAAAAAMi0pAzItKQAyLSlkMi0p+jIt'
               b'Kf8yLSn+Mi0p/zItKf8yLSn/Mi0p/zItKf8yLSn/Mi0p/zItKf4yLSn/'
               b'Mi0p2zItKSkyLSkAMi0pBTItKF8yLShvMi0oajItKGMyLShIMi0oHjEu'
               b'MQAyLScAMi0oATItKAAyLSgAMi0pAAAAAAAyLSkAMi0pGDItKfEyLSn/'
               b'Mi0puzItKaEyLSmjMi0pozItKaMyLSmjMi0pozItKaMyLSmjMi0pozIt'
               b'KdEyLSn/Mi0przItKQAyLSYAMi0oRTItKGwyLShhMi0oYTItKHMyLShu'
               b'Mi0oSTItKAwyLSgAMi0oATItKAAyLSgAMS4oADItKQAyLSlDMi0p/zIt'
               b'Kb0yLSkAMi0pAjItKQAAAAAAAAAAAAAAAAAAAAAAAAAAADItKQIyLSkA'
               b'Mi0pIjItKf8yLSnjMi0pCTItKQAyLSgOMi0oYzItKG0yLSglMi0oJjIt'
               b'KF4yLShzMi0oXTItKBMyLSgAMi0oATItKAAyLSgAMi0pADItKU8yLSn/'
               b'Mi0ppzItKQAyLSkHMi0pBDItKQQyLSkEMi0pBDItKQQyLSkEMi0pBTIt'
               b'KQAyLSkSMi0p8zItKfEyLSkQMi0pADItKAAyLSgrMi0oZDItKBgyLSgA'
               b'Mi0oCTItKEgyLShxMi0oXTItKAwyLSgAMi0oATItKAAyLSkAMi0pUTIt'
               b'Kf8yLSmnMi0pADItKQYyLSkCMi0pAjItKQIyLSkCMi0pAjItKQIyLSkD'
               b'Mi0pADItKRMyLSnyMi0p8jItKRAyLSkAMi0pATItKQEyLSkEMi0oADIt'
               b'KAIxKSAAMi8rATItKEgyLShyMi0oSjItJwAyLScAMi0oADItKQAyLSlQ'
               b'Mi0p/zItKaYyLSkAMi0pAzItKQAAAAAAAAAAAAAAAAAAAAAAAAAAADIt'
               b'KQEyLSkAMi0pEDItKfIyLSnyMi0pEDItKQAyLSkBMi0oATItKAAyLSgA'
               b'Mi0oADItKAEyLSgAMi0oCTItKFwyLShuMi0oIDItKAAyLSgBMi0pADIt'
               b'KVMyLSn/Mi0p5DItKbYyLSm7Mi0pujItKboyLSm6Mi0pujItKboyLSm6'
               b'Mi0pujItKbkyLSm9Mi0p/zItKe8yLSkRMi0pADItKQEyLSgAMi0oADMt'
               b'KQAyLSgAMi0oADItKAIyLSgAMi0oLTItKHIyLShJMi0oADItKAEyLSkA'
               b'Mi0pVTItKf8yLSn8Mi0p/zItKf8yLSn/Mi0p/zItKf8yLSn/Mi0p/zIt'
               b'Kf8yLSn/Mi0p/zItKf4yLSn/Mi0p7jItKREyLSkAMi0pAQAAAAAAAAAA'
               b'AAAAADIrJwAyLSgAMi0oATItKAAyLSgMMi0oYzItKGIyLSgJMi0oADIt'
               b'KQAyLSlRMi0p/zItKbwyLSk2Mi0pQzItKUEyLSlBMi0pQTItKUEyLSlB'
               b'Mi0pQTItKUIyLSk+Mi0pTTItKfYyLSnxMi0pEDItKQAyLSkBAAAAAAAA'
               b'AAAAAAAAAAAAADItKAAyLSgAMy0nADMtJwAyLShQMi0objItKBYyLSgA'
               b'Mi0pADItKU0yLSn/Mi0pqTItKQAyLSkDMi0pAAAAAAAAAAAAAAAAAAAA'
               b'AAAAAAAAMi0pATItKQAyLSkSMi0p9DItKe4yLSkOMi0pADItKQEAAAAA'
               b'AAAAAAAAAAAAAAAAAAAAADItKAAyLSgBMi0oADItKEgyLSh2Mi0oITIt'
               b'KAAyLSkAMi0pODItKf8yLSnVMi0pIjItKRMyLSkUMi0pEzItKRMyLSkT'
               b'Mi0pEzItKRMyLSkVMi0pDTItKVEyLSn/Mi0p1zItKgIyLSkAMi0pAQAA'
               b'AAAAAAAAAAAAAAAAAAAAAAAAMi0oADItKAEyLSgAMi0oLzItKGIyLSgR'
               b'Mi0oADItKQAyLSkGMi0p0zItKf8yLSn6Mi0p8zItKfIyLSnyMi0p8jIt'
               b'KfIyLSnyMi0p8jItKfIyLSn1Mi0p+zItKf8yLSmJMi0pADItKQMyLSkA'
               b'AAAAAAAAAAAAAAAAAAAAAAAAAAAyLSkAMy0oADMtKAAzLSgBMi0oBDMt'
               b'KAAzLSgAMi0pAjItKQAyLSknMi0psTItKeYyLSnyMi0p8jItKfIyLSny'
               b'Mi0p8jItKfIyLSnyMi0p8jItKfAyLSndMi0piDItKQcyLSkAMi0pAjIt'
               b'KQEyLSkBMi0pATItKQEyLSkBMi0pATItKQEyLSkBMi0pATItKAEyLSgA'
               b'Mi0oADItKAAyLSkAMi0pATItKQEyLSkAMi0pCDItKRAyLSkQMi0pEDIt'
               b'KRAyLSkQMi0pEDItKRAyLSkQMi0pDzItKQMyLSkAMi0pBDItKQEyLSkA'
               b'Mi0pAAAAAAAAAAAAAAAAAAAAAAAAAAAAMy0oADItKQAyLSkAMi0pAzIt'
               b'KQIyLSkAMi0pADItKQAyLSkAMi0pAjItKQMyLSkAMi0pADMtKQAAAAAA'
               b'AAAAAAAAAAAAAAAAAAAAADItKQAyLSkAMi0pATItKQQyLSkAMi0pBDIt'
               b'KREyLSkSMi0pEjItKRIyLSkSMi0pEjItKRIyLSkSMi0pEjItKQkyLSkA'
               b'Mi0pATItKQEyLSkAMi0oADItKAAyLSgAMi0oATItKQEyLSkBMi0pATIt'
               b'KQEyLSkBMi0pATItKQEyLSkBMi0pATItKQIyLSkAMi0pCDItKYsyLSng'
               b'Mi0p8jItKfQyLSn0Mi0p9DItKfQyLSn0Mi0p9DItKfQyLSn0Mi0p6TIt'
               b'KbUyLSkpMi0pADItKQIzLSgAMy0oADItKAQzLSgBMy0oADMtKAAyLSoA'
               b'AAAAAAAAAAAAAAAAAAAAAAAAAAAyLSkAMi0pAzItKQAyLSmKMi0p/zIt'
               b'KfsyLSnzMi0p7zItKfAyLSnwMi0p8DItKfAyLSnwMi0p8DItKfAyLSn5'
               b'Mi0p/zItKdUyLSkGMi0pADItKAAyLSgRMi0oYjItKC8yLSgAMi0oATIt'
               b'KAAAAAAAAAAAAAAAAAAAAAAAAAAAADItKQEyLSkAMi0pAjItKdgyLSn/'
               b'Mi0pTDItKQgyLSkQMi0pDzItKQ4yLSkOMi0pDjItKQ4yLSkPMi0pDjIt'
               b'KRwyLSnTMi0p/zItKTgyLSkAMi0oADItKCEyLSh2Mi0oSDItKAAyLSgB'
               b'Mi0pAAAAAAAAAAAAAAAAAAAAAAAAAAAAMi0pATItKQAyLSkOMi0p7jIt'
               b'KfUyLSkTMi0pADItKQEAAAAAAAAAAAAAAAAAAAAAAAAAADItKQAyLSkD'
               b'Mi0pADItKaoyLSn/Mi0pTTItKQAyLSgAMi0oFjItKG4yLShPMi0nADIt'
               b'JwAyLSgAMi0oAAAAAAAAAAAAAAAAAAAAAAAyLSkBMi0pADItKRAyLSny'
               b'Mi0p8zItKRYyLSkBMi0pBjItKQUyLSkFMi0pBTItKQUyLSkFMi0pBTIt'
               b'KQgyLSkAMi0pqDItKf8yLSlRMi0pADItKAAyLSgJMi0oYzItKGMyLSgM'
               b'Mi0oADItKAEyLSgAMS0nAAAAAAAAAAAAAAAAADItKQEyLSkAMi0pEDIt'
               b'KfIyLSnyMi0pEDItKQAyLSkBAAAAAAAAAAAAAAAAAAAAAAAAAAAyLSkA'
               b'Mi0pAzItKQAyLSmmMi0p/zItKVAyLSkAMi0oATItKAAyLShJMi0ocjIt'
               b'KC0yLSgAMi0oAjItKAAyLSgAMy0oADItKAAyLSgAMi0pATItKQAyLSkR'
               b'Mi0p8DItKfkyLSlvMi0pYzItKWYyLSllMi0pZTItKWUyLSllMi0pZTIt'
               b'KWUyLSlnMi0pXDItKcgyLSn/Mi0pUjItKQAyLSgBMi0oADItKCAyLShu'
               b'Mi0oXDItKAkyLSkAMi0oATItKAAyLSgAMi0oADItKAEyLSkBMi0pADIt'
               b'KREyLSnuMi0p/zItKf4yLSn/Mi0p/zItKf8yLSn/Mi0p/zItKf8yLSn/'
               b'Mi0p/zItKf8yLSn/Mi0p/DItKf8yLSlVMi0pADItKQAyLScAMi0nADIt'
               b'KEoyLShyMi0oSDItKgEyLiMAMi0oAjItKAAyLSkEMi0pATItKQEyLSkA'
               b'Mi0pETItKe8yLSn8Mi0pmTItKZAyLSmSMi0pkjItKZIyLSmSMi0pkjIt'
               b'KZIyLSmSMi0pkzItKYwyLSnXMi0p/zItKVMyLSkAMi0oADItKAEyLSgA'
               b'Mi0oDTItKF4yLShxMi0oSDItKAgyLSgAMi0oGDItKGQyLSgrMi0oADIt'
               b'KQAyLSkQMi0p8TItKfIyLSkQMi0pADItKQEAAAAAAAAAAAAAAAAAAAAA'
               b'AAAAADItKQAyLSkDMi0pADItKacyLSn/Mi0pTzItKQAyLSgAMi0oADIt'
               b'KAEyLSgAMi0oFDItKF0yLShzMi0oXjItKCYyLSglMi0obTItKGMyLSgO'
               b'Mi0pADItKQkyLSniMi0p/zItKSUyLSkAMi0pAgAAAAAAAAAAAAAAAAAA'
               b'AAAAAAAAMi0pADItKQEyLSkAMi0pvzItKf8yLSlCMi0pADItJwAyLSgA'
               b'Mi0oADItKAEyLSgAMi0oDDItKEkyLShuMi0oczItKGEyLShhMi0obDIt'
               b'KEUyLSYAMi0pADItKa4yLSn/Mi0p0zItKaYyLSmmMi0ppjItKaYyLSmm'
               b'Mi0ppjItKaYyLSmmMi0ppTItKb4yLSn/Mi0p8DItKRcyLSkAAAAAADEt'
               b'KAAyLSgAMi0oADItKAEyLScANSwwADItKB4yLShIMi0oYzItKGoyLShv'
               b'Mi0oXzItKQUyLSkAMi0pJzItKdkyLSn/Mi0p/jItKf8yLSn/Mi0p/zIt'
               b'Kf8yLSn/Mi0p/zItKf8yLSn+Mi0p/zItKfgyLSliMi0pADItKQMAAAAA'
               b'AAAAADEtKAAyLSgAMi0oADItKAEyLSgBKR8XADItKAAyLSgIMi0oFzIt'
               b'KCIyLSgSMi0oADItKQEyLSkAMi0pCTItKTgyLSlPMi0pUTItKVAyLSlR'
               b'Mi0pUTItKVEyLSlRMi0pUTItKVAyLSlEMi0pFzItKQAyLSkBMi0pAAAA'
               b'AAAAAAAAAAAAADEuKQAyLSgAMi0pADItKQAyLSgBMi0oATItKAAyLSgA'
               b'Mi0oADIuKAAyLSkAMi0pADItKQIyLSkBMi0pADItKQAAAAAAAAAAAAAA'
               b'AAAAAAAAAAAAAAAAAAAAAAAAMi0pADItKQAyLSkAMi0pAzItKQAyLikA'
               b'y/pKL6AAoZdAAEALgABgFYn0IAqIBDEEiAQgBIn0IUKAACCigAAvIYAA'
               b'L5GJ9C+RgAAvkYAAT9JAAEABkAEv0kn0gAmAAgACS/IAAYn0AAGJ9C+R'
               b'ifQAEYT0L5FFBAABQoQAASAEAAEgjC+RUAQvkagGAAHQAgAC6IUABfRS'
               b'X9I=')

    icon_ico = b64decode(icon_ico)
    icon_ico = ImageTk.PhotoImage(data=icon_ico)
    hwnd.tk.call('wm', 'iconphoto', root._w, icon_ico)

class GUI:
    def __init__(self, hwnd):

        # GUI Initialize
        InitGUI(hwnd)

        ##Combox Var
        self.ObsSelectBoxVar = StringVar()
        self.DirectorySelectBoxVar = StringVar()
        ##CheckButton Var
        self.AskOrNotCheckButtonVar = IntVar()

        # MainFrame Initialize
        self.Mainframe0 = None
        self.Mainframe1 = None
        self.InitMainFrame(hwnd)

        hwnd.protocol("WM_DELETE_WINDOW", hwnd.quit)
        hwnd.mainloop()

    def InitMainFrame(self, hwnd):

        # FrameCrads Initialize
        self.MainCradsOption = tk.ttk.Notebook(hwnd)

        # Obs File Initialize
        self.InitSingleObsCtrl(hwnd)
        self.InitBatchObsCtrl(hwnd)

        # FrameCrads Instantiate
        self.MainCradsOption.add(self.Mainframe0, text='Single Convert')
        self.MainCradsOption.add(self.Mainframe1, text='Batch Convert')
        self.MainCradsOption.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx='2px', pady='0px')

        # Execute Frame Initialize
        self.InitExecFrame(hwnd)

    def InitSingleObsCtrl(self, hwnd):

        # MainFrame Initialize
        self.Mainframe0 = ttk.Frame(hwnd)

        # Obs File Select Frame Initialize
        ObsSelectFrame1 = ttk.LabelFrame(self.Mainframe0, text='Object Observation of RINEX')
        ObsSelectFrame1.pack(side=tk.TOP, fill=tk.X, padx='2px', pady='1px')

        ObsFileSelectBox = ttk.Combobox(ObsSelectFrame1, width=46, height=4, values=('',),
                                        textvariable=self.ObsSelectBoxVar)
        ObsFileSelectBox.pack(side=tk.LEFT, anchor='w', padx='1px', pady='1px')

        ObsFileSelectButton = ttk.Button(ObsSelectFrame1, text='...', width=3,
                                         command=lambda: GetObsFilePath(ObsFileSelectBox))
        ObsFileSelectButton.pack(side=tk.RIGHT, anchor='e', padx='1px', pady='1px')

    def InitBatchObsCtrl(self, hwnd):

        # MainFrame Initialize
        self.Mainframe1 = ttk.Frame(hwnd)

        # Obs FileS Select Frame Initialize
        ObsSelectFrame1 = ttk.LabelFrame(self.Mainframe1, text='Objects Observation of RINEX')
        ObsSelectFrame1.pack(side=tk.TOP, fill=tk.X, padx='2px', pady='1px')

        #
        ObsCtrlFrame1 = ttk.Frame(ObsSelectFrame1)
        ObsCtrlFrame1.pack(side=tk.RIGHT, fill=tk.Y, anchor='e', padx='1px', pady='0px')

        ObsFileSelectButton = ttk.Button(ObsCtrlFrame1, text='...', width=3,
                                         command=lambda: GetObsFilesPath(ObsPathsShow))
        ObsFileSelectButton.pack(side=tk.TOP, anchor='e', padx='1px', pady='1px')

        ObsFileClearButton = ttk.Button(ObsCtrlFrame1, text='x', width=3,
                                         command=lambda: ClearObsFilesPath(ObsPathsShow))
        ObsFileClearButton.pack(side=tk.BOTTOM, anchor='e', padx='1px', pady='1px')

        #
        ObsShowFrame1 = ttk.Frame(ObsSelectFrame1)
        ObsShowFrame1.pack(side=tk.LEFT, fill=tk.Y, padx='1px', pady='0px')

        ScrollbarX = ttk.Scrollbar(ObsShowFrame1, orient=tk.HORIZONTAL)
        ScrollbarX.pack(side=tk.BOTTOM, fill=tk.X)

        ScrollbarY = ttk.Scrollbar(ObsShowFrame1)
        ScrollbarY.pack(side=tk.RIGHT, fill=tk.Y)

        ObsPathsShow = tk.Text(ObsShowFrame1, xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set,
                               height=4 ,wrap='none')
        ObsPathsShow.pack(side=tk.LEFT, fill=tk.X,anchor='w', padx='1px', pady='1px')

        ScrollbarX.config(command=ObsPathsShow.xview)
        ScrollbarY.config(command=ObsPathsShow.yview)

    def InitExecFrame(self, hwnd):

        #
        BottomExecFrame = ttk.Frame(hwnd)
        BottomExecFrame.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx='1px', pady='0px')

        # Output Directory Frame Initialize
        AskDirectoryFrame1 = ttk.LabelFrame(BottomExecFrame, text='Output directory')
        AskDirectoryFrame1.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx='1px', pady='0px')

        ## CheckButton Initialize
        AskOrNotCheckButton = ttk.Checkbutton(AskDirectoryFrame1, text='Directory',
                                              variable=self.AskOrNotCheckButtonVar, onvalue=1, offvalue=0,
                                              command=lambda: AskOrNotCheck(self.AskOrNotCheckButtonVar,
                                                                            AskDirectorySelectBox,
                                                                            AskDirectorySelectButton))
        AskOrNotCheckButton.pack(side=tk.LEFT, anchor='w', padx='1px', pady='0px')

        ## SelectBox Initialize
        AskDirectorySelectBox = ttk.Combobox(AskDirectoryFrame1, width=36, height=4, values=('',),
                                             state=tk.DISABLED, textvariable=self.DirectorySelectBoxVar)
        AskDirectorySelectBox.pack(side=tk.LEFT, anchor='w', padx='1px', pady='0px')

        ## SelectButton Initialize
        AskDirectorySelectButton = ttk.Button(AskDirectoryFrame1, text='...', width=3,
                                              state=tk.DISABLED, command=lambda: AskDirectory(AskDirectorySelectBox))
        AskDirectorySelectButton.pack(side=tk.RIGHT, anchor='e', padx='2px', pady='0px')

        # The bottom control buttons
        BottomCtrFrame0 = ttk.Frame(BottomExecFrame)
        BottomCtrFrame0.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx='1px', pady='0px')

        ConvertButton = ttk.Button(BottomCtrFrame0, text='Convert', width=8,
                                   command=lambda: _ConvertFile(ConvertState,
                                                                self.ObsSelectBoxVar,
                                                                self.AskOrNotCheckButtonVar,
                                                                self.DirectorySelectBoxVar,
                                                                self.MainCradsOption))
        ConvertButton.pack(side=tk.RIGHT, expand=tk.YES, padx='1px', pady='0px')

        ExitButton = ttk.Button(BottomCtrFrame0, text='Exit', width=8,
                                command=hwnd.quit)
        ExitButton.pack(side=tk.RIGHT, expand=tk.YES, padx='1px', pady='0px')

        # Convert state bar
        StateFrame = ttk.Frame(BottomExecFrame)
        StateFrame.pack(side=tk.TOP, fill=tk.X, padx='1px', pady='0px')
        ConvertState = ttk.Label(StateFrame, text="None")
        ConvertState.pack(side=tk.LEFT, anchor='nw')


if __name__ == "__main__":
    # Main window
    root = tk.Tk()
    myGUI = GUI(root)



