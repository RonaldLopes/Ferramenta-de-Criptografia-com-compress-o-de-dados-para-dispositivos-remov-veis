from kivy.app import App
# kivy.require("1.8.0")
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App
# kivy.require("1.8.0")
import subprocess
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
import glob
import getpass
import os
# from kivy.config import Config
# Config.set('kivy','window_icon','abc.ico')
from lib.EcryptoAdvanced import *
from kivy.core.window import Window

Window.borderless = True

Window.size = (770,300)
class ScreenManagement(ScreenManager):
    pass
# LoginOperadorErrorPopup().open()
class PasswordSelect(Popup):
    def confirm(self,*args):
        self.app = App.get_running_app()
        self.app.password= self.ids.password.text
        self.dismiss(force=True,animation=False)

class ModeSelect(Popup):

    def confirm(self,*args):
        self.app = App.get_running_app()
        if(self.ids.btnConfirmaModo.text == 'Confirmar'):
            pass
        else:
            self.app.mode = self.ids.btnConfirmaModo.text
        self.dismiss(force=True,animation=False)

class DeviceSelect(Popup):
    def __init__(self, **kwargs):
        Clock.schedule_interval(self.updateDevicesList, 1)
        super(DeviceSelect, self).__init__(**kwargs)
    def confirm(self,*args):
        self.app = App.get_running_app()
        self.app.device = self.ids.listPorts.text
        self.dismiss(force=True,animation=False)

    def updateDevicesList(self, *args):
        user = getpass.getuser()
        ports = glob.glob('/media/'+str(user)+'/*')
        userDirectory = '/media/'+str(user)+'/'
        lista = []
        self.app = App.get_running_app()
        self.app.deviceDirectory= userDirectory
        for usb in ports:
            lista.append(usb.replace(userDirectory,''))
        self.ids.listPorts.values=lista

class ConfigScreen(Screen):
    pass

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        Clock.schedule_once(self.sendmessage, 1)
        Clock.schedule_interval(self.screenUpdate,5)
        super(HomeScreen, self).__init__(**kwargs)
    def screenUpdate(self,*args):
        self.app = App.get_running_app()
        if(self.app.mode!=None):
            if(self.app.mode=='Criptografar'):
                self.ids.imgMode.source = 'img/lockLogo.png'
            elif(self.app.mode=='Descriptografar'):
                self.ids.imgMode.source = 'img/unlockLogo.png'
    def setPassword(self,*args):
        PasswordSelect().open()
    def setDevice(self,*args):
        DeviceSelect().open()
    def setMode(self,*args):
        ModeSelect().open()
    def startCryptography(self):
        self.app = App.get_running_app()
        if(self.app.deviceDirectory!=None)and(self.app.device!=None)and(self.app.deviceDirectory != 'Selecione o dispositivo'):
            diretorio = str(self.app.deviceDirectory)+str(self.app.device)+ '/*'
            security = EcryptoAdvanced(diretorio=diretorio)
            if (self.app.mode != None) and (self.app.password != None) and (self.app.password !=''):
                try:
                    if (self.app.mode == 'Criptografar'):
                        self.sendNotification('Criptografando arquivos')
                        security.start(self.app.password)
                        self.sendNotification('Criptografia finalizada')
                    elif (self.app.mode == 'Descriptografar'):
                        self.sendNotification('Descriptografando arquivos')
                        security.deCryptoStart(self.app.password)
                        self.sendNotification('Descriptografia finalizada')
                except Exception as erro:
                    print('Erro identificado: '+str(erro))
                    self.sendNotification('Erro ao efetuar operação, senha incorreta ou arquivo inexistente!')
        else:
            diretorio = None

        security = None

    def sendNotification(self,msg):
        image = os.getcwd() + '/img/logo.png'
        subprocess.Popen(
            ['notify-send', '--icon=' + image, 'Ecrypto Advanced',
             str(msg)])
        return
    def sendmessage(self,*args):
        image = os.getcwd()+'/img/logo.png'
        user = getpass.getuser().capitalize()
        subprocess.Popen(
            ['notify-send', '--icon='+image, 'Ecrypto Advanced',
             'Bem vindo '+user+'!'])
        return



presentation = Builder.load_file("tela.kv")




class MainApp(App):

    def build(self):
        self.icon ='img/logo.png'
        self.title = 'Ecrypto Advanced 2.0 - Beta version'
        self.password = None # Criptografar depois para evitar acesso direto
        self.device = None # Dispositivo alvo
        self.active = True
        self.mode = None
        self.deviceDirectory=None
        print(self.get_application_icon())
        return presentation

# app = App.get_running_app()
if __name__ == "__main__":
    MainApp().run()
