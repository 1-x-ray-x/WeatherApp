import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
#alignment
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # city label
        self.city_label = QLabel("Enter city name", self)
        #line edit widget
        self.city_input = QLineEdit(self)
        # button for get weather
        self.get_weather_button = QPushButton("Get Weather", self)
        #temperature label
        self.temperature_label = QLabel(self)
        # emoji
        self.emoji_label = QLabel(self)
        #weather description
        self.description_label = QLabel(self)
        #intiUi
        self.initUI()
    
    def initUI(self):
        #format widgets
        # window title
        self.setWindowTitle("Weather App")
        # window icon
        self.setWindowIcon(QIcon("weather-icon.png"))
        # layout (vertical)
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        # set layout
        self.setLayout(vbox)
        # centre align
        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # styles (unique object id for label)
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.get_weather_button.setObjectName("get_weather_button")
        
        self.setStyleSheet('''
            QLabel, QPushButton{
                font-family: calibri;   
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: Italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px
            }
                           ''')
        
        # connect signal to slot when button clicked
        self.get_weather_button.clicked.connect(self.get_weather)
    
    #get weather from api
    def get_weather(self):
        api_key = "9d150ca66b153a3061442a15bcac4842"
        
        #lookup city
        city = self.city_input.text()
        
        # create url
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try: 
            # response object
            response = requests.get(url)
            # raises an exception if theres any http errors
            response.raise_for_status()
            # converts the response to a json object
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
        
        #HTTP error
        # match each status code to a case
        # renames the http error as http_error variable
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorised:\nInvalid API Key")
                case 403:
                    self.display_error("Forbiddenenied:\nAccess Denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500: 
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad gateway:\nInvalid response from the server")
                case 503: 
                    self.display_error("Service Unavailable:\nServer is down")
                case 504: 
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")
        
        # connection error (internet)
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")
        # Timeout (too long)
        except requests.exceptions.Timeout:
            self.display_error("The Request Timed Out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\nCheck the URL")
        # network problems etc
        except requests.exceptions.RequestException as rec_error:
            self.display_error(f"Request Error:\n{rec_error}")
            
        

    
    #displays errors
    def display_error(self, message):
        # changes font size after error
        self.temperature_label.setStyleSheet("font-size: 30px;")
        # sets the temperature label text as the message
        self.temperature_label.setText(message)
        # clears after error
        self.emoji_label.clear()
        self.description_label.clear()

    #to display the weather
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        # main is a dictionary with temp key value pair in kelvin
        temperature_k = data["main"]["temp"]
        temperature_c = float(temperature_k - 273.15)
        # weather id
        weather_id = data["weather"][0]["id"]
        # 0 because its in a list with 1 item so enter the list
        description = data["weather"][0]["description"]
        
        #change temperature label to 0 decimal places
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        
        # emoji label
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        
        # weather description
        self.description_label.setText(description)
        
    # picture based off description
    # no change so static, aka no self or cls args
    @staticmethod
    def get_weather_emoji(weather_id):
        # 3 digit id for weather in data
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "😶‍🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🌞"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    # show the weatherapp
    weather_app.show()
    #clean exit
    sys.exit(app.exec_())
