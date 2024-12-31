from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QMessageBox
import random

with open('substantivos.txt', 'r') as file:
    lines = file.readlines()

# Remove any trailing newline characters and store each line as an element in the list
lines = [line.strip() for line in lines]


class CodenamesGame(QWidget):
    def __init__(self):
        super().__init__()

        self.buttons = []  # Store button references
        self.available_words = lines
        self.repetead_words = []
        self.initialize_game()
        self.setup_ui()

    def initialize_game(self):
        # Initialize game variables
        self.available_words = [a for a in self.available_words if a not in self.repetead_words]
        self.words = random.sample(self.available_words, 25)
        random.shuffle(self.words)
        self.team_blue_words = set(random.sample(self.words, 8))
        remaining_words = [word for word in self.words if word not in self.team_blue_words]
        self.team_red_words = set(random.sample(remaining_words, 8))
        remaining_words = [word for word in remaining_words if word not in self.team_red_words]
        self.neutral_words = set(random.sample(remaining_words, 8))
        self.assassin_word = (set(remaining_words) - self.neutral_words).pop()
        print(self.assassin_word)
        print('Azul:', self.team_blue_words)
        print('Vermelho:', self.team_red_words)

        for word in self.words:
            self.repetead_words.append(word)

        print('Repetidas:', self.repetead_words)
        self.current_team = "Blue"
        self.scores = {"Blue": 0, "Red": 0}

    def setup_ui(self):
        self.setWindowTitle("Codenomes")
        self.resize(500, 500)

        self.layout = QVBoxLayout()
        self.grid = QGridLayout()

        self.buttons.clear()
        for i in range(25):
            button = QPushButton(self.words[i])
            button.setStyleSheet("""
                                 font-size: 30px;
                                 height: 100 px
                                 """)
            button.clicked.connect(lambda checked, b=button: self.handle_card_click(b))
            self.buttons.append(button)
            self.grid.addWidget(button, i // 5, i % 5)

        self.layout.addLayout(self.grid)

        self.info_label = QLabel("Vez do time Azul!")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            font-size: 40px; 
            color: blue;      
        """)
        self.layout.addWidget(self.info_label)

        self.score_label = QLabel(self.get_score_text())
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("""
                                       font-size: 40px
                                       """)
        self.layout.addWidget(self.score_label)

        # Mostrar palavras Time Azul
        self.switch = QPushButton("Trocar timel")
        self.switch.setStyleSheet("""
            height: 40 px;
            width: 60px;
            color: purple;      
        """)
        self.switch.clicked.connect(self.switch_func)
        self.layout.addWidget(self.switch)

        # Mostrar palavras Time Azul
        self.show_words_button_blue = QPushButton("Palavras time Azul")
        self.show_words_button_blue.setStyleSheet("""
            height: 40 px;
            width: 60px;
            color: blue;      
        """)
        self.show_words_button_blue.clicked.connect(self.show_team_blue_words)
        self.layout.addWidget(self.show_words_button_blue)

        # Mostrar palavras Time Vermelho
        self.show_words_button_red = QPushButton("Palavras time Vermelho")
        self.show_words_button_red.setStyleSheet("""
            height: 40 px;
            width: 60px;
            color: red;      
        """)
        self.show_words_button_red.clicked.connect(self.show_team_red_words)
        self.layout.addWidget(self.show_words_button_red)

        self.setLayout(self.layout)

    def switch_func(self):
        print('oi')
        self.switch_turn()
        cor = ""
        if  self.current_team == 'Blue':
            cor = 'Azul'
            self.info_label.setText(f"Vez do time {cor}")
            self.info_label.setStyleSheet("""
                font-size: 40px; 
                color: blue;      
            """)
        else:
            cor = 'Vermelho'
            self.info_label.setText(f"Vez do time {cor}")
            self.info_label.setStyleSheet("""
                font-size: 40px; 
                color: red;      
            """)

    def reset_ui(self):
        # Reset words, buttons, and scores
        self.initialize_game()

        for i, button in enumerate(self.buttons):
            button.setText(self.words[i])
            button.setStyleSheet("""
                                 font-size: 30px;
                                 height: 100 px
                                 """)
            button.setEnabled(True)

        self.info_label.setText("Vez do time Azul")
        self.info_label.setStyleSheet("""
            font-size: 40px; 
            color: blue;      
        """)
        self.score_label.setText(self.get_score_text())

    def get_score_text(self):
        return f"Azul: {self.scores['Blue']}| Vermelho: {self.scores['Red']}"

    def handle_card_click(self, button):
        word = button.text()
        if word in self.team_blue_words:
            if self.current_team == "Blue":
                button.setStyleSheet("""
                                     background-color: lightblue;
                                     font-size: 30px;
                                     height: 100 px;
                                     """)
                self.scores["Blue"] += 1
                self.team_blue_words.remove(word)
            else:
                button.setStyleSheet("""background-color: lightblue; 
                                     font-size: 30px;
                                     height: 100 px;
                                     """)
                self.scores["Blue"] += 1
                self.switch_turn()

        elif word in self.team_red_words:
            if self.current_team == "Red":
                button.setStyleSheet("""
                                     background-color: red; 
                                     font-size: 30px;
                                     height: 100 px;
                                     """)
                self.scores["Red"] += 1
                self.team_red_words.remove(word)
            else:
                button.setStyleSheet("""
                                     background-color: red;
                                     font-size: 30px;
                                     height: 100 px;
                                     """)
                self.scores["Red"] += 1
                self.switch_turn()

        elif word in self.neutral_words:
            button.setStyleSheet("""
                                 background-color: gray;
                                 font-size: 30px;
                                 height: 100 px;
                                 """)
            self.neutral_words.remove(word)
            self.switch_turn()

        elif word == self.assassin_word:
            button.setStyleSheet("""
                                 background-color: black; 
                                 color: white; font-size: 30px;
                                 height: 100 px
                                 """)
            QMessageBox.critical(self, f"Fim de jogo", f"Palavra assasina!!!")
            self.reset_ui()
            return

        button.setEnabled(False)
        cor = ""
        if  self.current_team == 'Blue':
            cor = 'Azul'
            self.info_label.setText(f"Vez do time {cor}")
            self.info_label.setStyleSheet("""
                font-size: 40px; 
                color: blue;      
            """)
        else:
            cor = 'Vermelho'
            self.info_label.setText(f"Vez do time {cor}")
            self.info_label.setStyleSheet("""
                font-size: 40px; 
                color: red;      
            """)
            
        #self.info_label.setText(f"Team {self.current_team}'s Turn")
        if self.scores['Blue'] == 8:
            QMessageBox.information(self, "Azul ganhou!", f"Vitória do time AZUL!")
            self.reset_ui()
        if self.scores['Red'] == 8:
            QMessageBox.information(self, "Vermelho ganhou!", f"Vitória do time VERMELHO!")
            self.reset_ui()
            
        self.score_label.setText(self.get_score_text())

    def switch_turn(self):
        self.current_team = "Red" if self.current_team == "Blue" else "Blue"

    def show_team_blue_words(self):
        #team_words = self.team_blue_words if self.current_team == "Blue" else self.team_red_words
        blue_string = ""
        for blue_word in self.team_blue_words:
            blue_string += f'\n{blue_word.upper()}'
        #QMessageBox.information(self, "Palavras time Azul", f"{','.join(self.team_blue_words)} \n\n Palavra proíbida: {self.assassin_word.upper()}")
        QMessageBox.information(self, "Palavras time Azul", f"{blue_string} \n\n Palavra proíbida: {self.assassin_word.upper()}")
    
    def show_team_red_words(self):
        #team_words = self.team_blue_words if self.current_team == "Blue" else self.team_red_words
        red_string = ""
        for red_word in self.team_red_words:
            red_string += f'\n{red_word.upper()}'
        #QMessageBox.information(self, "Palavras time Vermelho", f"{', '.join(self.team_red_words)}\n\n Palavra proíbida: {self.assassin_word.upper()}")
        QMessageBox.information(self, "Palavras time Azul", f"{red_string} \n\n Palavra proíbida: {self.assassin_word.upper()}")

if __name__ == "__main__":
    app = QApplication([])
    game = CodenamesGame()
    game.show()
    app.exec_()
