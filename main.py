from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob, random
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
from pathlib import Path 
from hoverable import HoverBehavior


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def login(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file) #giving us a dictionary
            if uname in users and users[uname]['password'] == pword:
                self.manager.current = "login_screen_success"
            else:
                self.ids.login_wrong.text = "Wrong username or password"
            
    



class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
        
        users[uname] = {'username': uname, 'password': pword, 'created': datetime.now().strftime("date: %Y-%m-%d time: %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users,file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def back_login(self):
        self.manager.transition.direction = 'right' #changing transition of the screen to the right direction
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
    
    def get_quote(self,feel):
        feel = feel.lower()
        feeling_quotes = glob.glob("quotes/*txt")
        feeling_quotes = [Path(filename).stem for filename in feeling_quotes] #!

        if feel in feeling_quotes:
            with open(f"quotes/{feel}.txt ",encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)


class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()