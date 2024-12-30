from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QMessageBox
import random

class CodenamesGame(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize game variables
        self.words = ["Apple", "Banana", "Orange", "Grape", "Cherry", "Pear", "Peach", "Lemon", "Plum", "Mango",
                      "Pineapple", "Berry", "Fig", "Date", "Kiwi", "Melon", "Coconut", "Avocado", "Guava", "Papaya",
                      "Raspberry", "Blueberry", "Strawberry", "Blackberry", "Watermelon"]
        random.shuffle(self.words)
        
        self.team_blue_words = set(random.sample(self.words, 8))
        remaining_words = [word for word in self.words if word not in self.team_blue_words]
        self.team_red_words = set(random.sample(remaining_words, 8))
        remaining_words = [word for word in remaining_words if word not in self.team_red_words]
        self.neutral_words = set(random.sample(remaining_words, 8))
        self.assassin_word = (set(remaining_words) - self.neutral_words).pop()

        self.current_team = "Blue"
        self.scores = {"Blue": 0, "Red": 0}

        # Set up UI
        self.setWindowTitle("Codenames")
        self.resize(600, 600)

        self.layout = QVBoxLayout()
        self.grid = QGridLayout()

        self.buttons = {}
        for i, word in enumerate(self.words):
            button = QPushButton(word)
            button.setStyleSheet("font-size: 14px;")
            button.clicked.connect(lambda checked, b=button: self.handle_card_click(b))
            self.buttons[word] = button
            self.grid.addWidget(button, i // 5, i % 5)

        self.layout.addLayout(self.grid)

        self.info_label = QLabel("Team Blue's Turn")
        self.layout.addWidget(self.info_label)

        self.score_label = QLabel(self.get_score_text())
        self.layout.addWidget(self.score_label)

        self.show_words_button = QPushButton("Show Team Words")
        self.show_words_button.clicked.connect(self.show_team_words)
        self.layout.addWidget(self.show_words_button)

        self.setLayout(self.layout)

    def get_score_text(self):
        return f"Blue: {self.scores['Blue']} | Red: {self.scores['Red']}"

    def handle_card_click(self, button):
        word = button.text()
        if word in self.team_blue_words:
            if self.current_team == "Blue":
                button.setStyleSheet("background-color: lightblue; font-size: 14px;")
                self.scores["Blue"] += 1
                self.team_blue_words.remove(word)
            else:
                button.setStyleSheet("background-color: red; font-size: 14px;")
                self.scores["Red"] += 1
                self.switch_turn()

        elif word in self.team_red_words:
            if self.current_team == "Red":
                button.setStyleSheet("background-color: red; font-size: 14px;")
                self.scores["Red"] += 1
                self.team_red_words.remove(word)
            else:
                button.setStyleSheet("background-color: lightblue; font-size: 14px;")
                self.scores["Blue"] += 1
                self.switch_turn()

        elif word in self.neutral_words:
            button.setStyleSheet("background-color: gray; font-size: 14px;")
            self.neutral_words.remove(word)
            self.switch_turn()

        elif word == self.assassin_word:
            button.setStyleSheet("background-color: black; color: white; font-size: 14px;")
            QMessageBox.critical(self, "Game Over", f"{self.current_team} team guessed the assassin word. They lose!")
            self.reset_game()
            return

        button.setEnabled(False)
        self.info_label.setText(f"Team {self.current_team}'s Turn")
        self.score_label.setText(self.get_score_text())

    def switch_turn(self):
        self.current_team = "Red" if self.current_team == "Blue" else "Blue"

    def show_team_words(self):
        team_words = self.team_blue_words if self.current_team == "Blue" else self.team_red_words
        QMessageBox.information(self, "Team Words", f"Your team's words are: {', '.join(team_words)}")

    def reset_game(self):
        self.__init__()
        self.update()

if __name__ == "__main__":
    app = QApplication([])
    game = CodenamesGame()
    game.show()
    app.exec_()
