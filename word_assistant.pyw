import time
from concurrent.futures.thread import ThreadPoolExecutor
import asyncio
import config
import wx
from docx import Document

import pyttsx3
import speech_recognition as sr


class MainPanel(wx.Panel):
    """ INITIALIZATION OF WIDGETS """

    # here is buttons, txt labels
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        """ SIZERS """
        VerticalSizer = wx.BoxSizer(wx.VERTICAL)
        HorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)

        """ BACKGROUND SETTINGS (?)"""
        HorizontalSizer.Add((1, 1), 1, wx.EXPAND)
        HorizontalSizer.Add(VerticalSizer, 0, wx.TOP, 100)
        HorizontalSizer.Add((1, 1), 0, wx.ALL, 75)
        self.SetSizer(HorizontalSizer)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.ForBackground)

        """ ADD BUTTONS """
        config.Btn_On_Assistent = wx.Button(self, -1, label="Включить", pos=(365, 26), size=(71, 45))
        self.Bind(wx.EVT_BUTTON, self.On_Assistent, config.Btn_On_Assistent)

        Button_BrowsePath_SavedFiles = wx.Button(self, -1, label="Искать", pos=(365, 80), size=(71, 20))
        self.Bind(wx.EVT_BUTTON, self.BrowsePath_SavedFiles, Button_BrowsePath_SavedFiles)

        Button_BrowseBrouser = wx.Button(self, -1, label="Искать", pos=(231, 110), size=(71, 20))
        self.Bind(wx.EVT_BUTTON, self.BrowsePath_BrowseBrouser, Button_BrowseBrouser)

        Button_PastToDoc = wx.Button(self, -1, label="Выгрузить в .docx", pos=(313, 110), size=(121, 20))
        self.Bind(wx.EVT_BUTTON, self.doxCreating, Button_PastToDoc)

        """ ADD ANOTHER WIDGETS """

        PathForSavedFiles = "Выберите файл для сохранения документов"
        config.Input_PathOfSavedFiles = wx.TextCtrl(self, value=PathForSavedFiles, style=wx.TE_PROCESS_ENTER,
                                                    size=(345, 20), pos=(20, 80))

        PathOfBrouser = "Выберите браузер"
        config.Input_PathOfBrouser = wx.TextCtrl(self, value=PathOfBrouser, style=wx.TE_PROCESS_ENTER,
                                                 size=(211, 20), pos=(20, 110))

        config.InputTextArea = wx.StaticText(self, label="""
        WordAssistent - транскрибатор для учебы и работы. Попробуйте
    использовать его для конспектирования, ведения наблюдений или  
    дневника. Что он может:
                                                 
        1. 'Ассистент, записывай' - начать транскрибацию.
        2. 'Точка', 'запятая', 'двоеточие', 'точка с запятой', 
    'восклицательный знак',  'вопросительный знак',  'минус',  'плюс', 
    'равно', 'сабака (при вводе почты)', <любое число>  -   поставить 
    знак препинания или символ.
        3. 'Новый абзац' - начать новый абзац.
        4. 'Ассистент, вставь картинку <запрос>' - поиск изображения в
    браузере.  Перед вами появится окно с выбором. Назовите номер 
    понравившегося изображения, и оно будет вставлено в документ.
        5. 'Ассистент, стоп' - завершить транскрибацию.
                                         
                                           
                                           
                                           
                                           
                                                
                                        
                                              Связь с разработчиком: lestreng.begi@gmail.com""",
                                             style=wx.CURSOR_QUESTION_ARROW,
                                             size=(416, 350), pos=(20, 141))

    """ BUTTON FUNCTION"""

    def BrowsePath_SavedFiles(self, event):
        dialog = wx.DirDialog(self, 'Куда сохранять создаваемые документы?', '', style=wx.DD_DEFAULT_STYLE)
        try:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            config.PathForSavedFiles = dialog.GetPath()
        finally:
            config.Input_PathOfSavedFiles.SetValue(config.PathForSavedFiles)
            dialog.Destroy()

    def BrowsePath_BrowseBrouser(self, event):
        dialog = wx.DirDialog(self, 'Выберите браузер для работы', '', style=wx.DD_DEFAULT_STYLE)
        try:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            config.PathOfBrouser = dialog.GetPath()
        finally:
            config.Input_PathOfBrouser.SetValue(config.PathOfBrouser)
            dialog.Destroy()

    def BrowsePath_FileV(self, event):
        dialog = wx.DirDialog(self, 'Выберите документ для работы с ним', '', style=wx.DD_DEFAULT_STYLE)
        try:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            config.PathForFileV = dialog.GetPath()
        finally:
            config.Input_PathOfFileV.SetValue(config.PathForFileV)
            dialog.Destroy()

    def Off_Assistent(self, event):
        config.chek_var = 0

        config.Btn_On_Assistent = wx.Button(self, -1, label="Включить", pos=(365, 26), size=(71, 45))
        self.Bind(wx.EVT_BUTTON, self.On_Assistent, config.Btn_On_Assistent)

        config.InputTextArea = wx.StaticText(self, label="""
        WordAssistent - транскрибатор для учебы и работы. Попробуйте
    использовать его для конспектирования, ведения наблюдений или  
    дневника. Что он может:

        1. 'Ассистент, записывай' - начать транскрибацию.
        2. 'Точка', 'запятая', 'двоеточие', 'точка с запятой', 
    'восклицательный знак',  'вопросительный знак',  'минус',  'плюс', 
    'равно', 'сабака (при вводе почты)', <любое число>  -   поставить 
    знак препинания или символ.
        3. 'Новый абзац' - начать новый абзац.
        4. 'Ассистент, вставь картинку <запрос>' - поиск изображения в
    браузере.  Перед вами появится окно с выбором. Назовите номер 
    понравившегося изображения, и оно будет вставлено в документ.
        5. 'Ассистент, стоп' - завершить транскрибацию.







                                            Связь с разработчиком: lestreng.begi@gmail.com""",
                                             style=wx.CURSOR_QUESTION_ARROW,
                                             size=(416, 350), pos=(20, 141))

        config.Output_RecText.Destroy()
        config.Btn_Off_Assistent.Destroy()

    config.startStaticText = ""
    def changeInterface(self):
        print('Interface of BUTTON CHANGING started')

        config.Output_RecText = wx.TextCtrl(self, value=config.startStaticText,
                                            style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE,
                                            size=(416, 350), pos=(20, 141))
        config.Btn_Off_Assistent = wx.Button(self, -1, label="Выключить", pos=(365, 26), size=(71, 45))
        self.Bind(wx.EVT_BUTTON, self.Off_Assistent, config.Btn_Off_Assistent)

        config.Btn_On_Assistent.Destroy()
        config.InputTextArea.Destroy()

        print('Interface of BUTTON CHANGING finished')


    async def On_VoiceAssistent(self):
        print('VOICE RECOGNIZE started')

        config.chek_var = 1

        while config.chek_var == 1:
            r = sr.Recognizer()

            with sr.Microphone(device_index=1) as sourse:
                audio = r.listen(sourse)
                try:
                    query = r.recognize_google(audio, language="ru-RU")
                    print(query.lower())

                    if query == "ассистент стоп":
                        self.Off_Assistent()
                    elif query == "ассистент зaписывай":
                        config.startStaticText = query

                except sr.UnknownValueError:
                    print("not recognized")
                    self.On_VoiceAssistent()

        print('VOICE RECOGNIZE finished')

    def On_Assistent(self, event):
        asyncio.run(self.changeInterface())
        time.sleep(3)
        asyncio.run(self.On_VoiceAssistent())

        """try:  # TODO: именование файлов 1, 2 ... , чтобы можно было создать несколько
            print('Docx creating started')

            document_name = config.PathForSavedFiles + '//' + 'Document' + ' '
            document_name_number = '1'
            config.document = Document()
            config.document.save(document_name + document_name_number)

            print('Docx creating finished')
        except:
            print('ERROR : NAME OF FILE')"""

    """ ANOTHER FUNCTIONS """

    def ForBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)

        dc.Clear()
        bmp = wx.Bitmap("background.jpg")
        dc.DrawBitmap(bmp, 0, 0)

    def doxCreating(self, event):
        docxFilename = config.PathForSavedFiles + "Document"
        config.Output_RecText.SaveFile(self, filename=docxFilename, fileType=wx.TEXT_TYPE_ANY)
""" FRAME SETTINGS """


# size, stile
class MainFrame(wx.Frame):

    def __init__(self):
        no_caption = (wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, size=(470, 550), style=no_caption)
        panel = MainPanel(self)
        self.Center()


# he doesn't do that he must do
class Main(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        dlg = MainFrame()
        dlg.Show()


if __name__ == "__main__":
    app = Main()
    app.MainLoop()
