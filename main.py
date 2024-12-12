import sys
import time
import sqlite3
from PyQt6.QtWidgets import QApplication,QStackedLayout, QMainWindow, QWidget, QLineEdit, QPushButton, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect, QScrollArea, QDialog
from PyQt6.QtGui import QIcon, QFont, QPixmap, QShortcut, QKeySequence, QLinearGradient, QColor, QPainter
from PyQt6.QtCore import Qt, QTimer, QRect, pyqtSignal
from screeninfo import get_monitors
from hangman import hangman_stage
from words import choose_word
from program import hangman
from ranking_database import add_to_base, fetch_all_scores
from typing import List

# TO do
# - after game screen; czas, wynik, opcja zagrania od nowa
# - ranking
# - menu poczatkowe; z polami wybory (gra, ranking,, specjalne tryby; czasowka 1min, tematyka)
# * Ranking w sql

class MainMenu(QWidget):
    def __init__(self, start_game, show_ranking, quit_app_event):
        super().__init__()

        # menu_header layout
        self.menu_header_layout= QHBoxLayout()
        self.menu_header_label = QLabel('Main menu')
        self.menu_header_logo = QLabel()

        img = QPixmap("media/hangman_icon.png")
        self.menu_header_logo.setPixmap(img)
        self.menu_header_logo.setScaledContents(True)


        # menu_content layout
        self.menu_content_layout = QHBoxLayout()
        self.menu_content_play_button = QPushButton("Play")
        self.menu_content_result_button = QPushButton("Ranking")
        
        self.menu_content_play_button.clicked.connect(start_game)
        self.menu_content_result_button.clicked.connect(show_ranking)


        # menu_footer layout
        self.menu_footer_layout = QHBoxLayout()
        self.menu_quit_button = QPushButton("Exit")
        
        self.menu_quit_button.clicked.connect(quit_app_event)


        # Initialize look settings
        self.initUI()


    def initUI(self):
        # Main layout settings
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setHorizontalSpacing(0)
        main_layout.setVerticalSpacing(0)

        # Shadow
        shadow_play_button = QGraphicsDropShadowEffect(self)
        shadow_play_button.setOffset(4, 4)
        shadow_play_button.setBlurRadius(10)
        shadow_play_button.setColor(Qt.GlobalColor.black)

        shadow_result_button = QGraphicsDropShadowEffect(self)
        shadow_result_button.setOffset(4, 4)
        shadow_result_button.setBlurRadius(10)
        shadow_result_button.setColor(Qt.GlobalColor.black)

        shadow_quit_button = QGraphicsDropShadowEffect(self)
        shadow_quit_button.setOffset(4, 4)
        shadow_quit_button.setBlurRadius(10)
        shadow_quit_button.setColor(Qt.GlobalColor.black)

        # Gradient


        # menu_header_section layout
        self.menu_header_widget = QWidget()
        self.menu_header_logo.setFixedSize(75, 75)
        self.menu_header_layout.addWidget(self.menu_header_label)
        self.menu_header_label.setCursor(Qt.CursorShape.OpenHandCursor)
        self.menu_header_layout.addWidget(self.menu_header_logo)
        self.menu_header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_header_widget.setLayout(self.menu_header_layout)
        self.menu_header_widget.setFixedHeight(100)
            # menu_header_section adding names for css
        self.menu_header_label.setObjectName("menu_header_label")
        self.menu_header_logo.setObjectName("menu_header_logo")
        self.menu_header_widget.setObjectName("menu_header_widget")


        # menu_content_section layout
        self.menu_content_widget = QWidget()
        self.menu_content_play_button.setGraphicsEffect(shadow_play_button)
        self.menu_content_result_button.setGraphicsEffect(shadow_result_button)
        self.menu_content_layout.addWidget(self.menu_content_play_button)
        self.menu_content_layout.addWidget(self.menu_content_result_button)
        self.menu_content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_content_widget.setLayout(self.menu_content_layout)
        self.menu_content_widget.setFixedHeight(450)
            # menu_content_section adding names for css
        self.menu_content_play_button.setObjectName("menu_content_play_button")
        self.menu_content_result_button.setObjectName("menu_content_result_button")
        self.menu_content_widget.setObjectName("menu_content_widget")
        

        #menu_footer_section layout
        self.menu_footer_widget = QWidget()
        self.menu_quit_button.setGraphicsEffect(shadow_quit_button)
        self.menu_footer_layout.addWidget(self.menu_quit_button)
        self.menu_footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_footer_widget.setLayout(self.menu_footer_layout)
        self.menu_footer_widget.setFixedHeight(100)
            # menu_footer_section adding names for css
        self.menu_footer_widget.setObjectName("menu_footer_widget")
        self.menu_quit_button.setObjectName("menu_quit_button")

        # Adding layouts to main layout
        main_layout.addWidget(self.menu_header_widget, 0, 0)
        main_layout.addWidget(self.menu_content_widget, 1, 0)
        main_layout.addWidget(self.menu_footer_widget, 2, 0)

        # Settings to grid layout
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 1)
        main_layout.setRowStretch(2, 1)
        main_layout.setColumnStretch(0, 1)


        # Setting css properties for elements in this layout
        self.setStyleSheet("""
                           /* Header css properties */
                           #menu_header_label {
                           font-size: 36px;
                           font-family: "Bradley Hand";
                           font-size: 800;
                           margin: 0px;
                           padding: 10px 0px;
                           letter-spacing: 2px;
                           }

                           #menu_header_label:hover {
                           color: #D3D3D3;
                           }

                           #menu_header_logo {
                           }

                           #menu_header_widget {
                           }

                           /* content css properties */
                           #menu_content_play_button, #menu_content_result_button, #menu_quit_button {
                           padding: 10px 20px;
                           color: white;
                           border: 2px solid black;
                           border-radius: 20px;
                           height: 75px;
                           width: 150px;
                           }

                           #menu_content_play_button:hover, #menu_content_result_button:hover {

                           }
                           
                           #menu_content_play_button:hover {
                           background-color: #3e8e41;
                           }
                           
                           #menu_content_result_button:hover {
                           background-color: #1976d2;
                           }

                           #menu_content_widget {
                           }

                           /* footer css properties */
                           #menu_quit_button {
                           height: 50px;
                           width: 100px;
                           }
                           #menu_quit_button:hover {
                           background-color: #d32f2f;
                           }
                           """)

        # Setting @main_layout as main layout
        self.setLayout(main_layout)
       
class Game(QWidget):
    result_signal = pyqtSignal(list)
    def __init__(self, show_results, same_letter):
        super().__init__()

        self.show_results = show_results
        self.same_letter = same_letter

        # game_header_layout
        self.game_header_layout= QHBoxLayout()
        self.game_header_label = QLabel('Hangman')
        self.game_header_logo = QLabel()

        img = QPixmap("media/hangman_icon.png")
        self.game_header_logo.setPixmap(img)
        self.game_header_logo.setScaledContents(True)
        
        # game_content_layout
        self.game_content_layout = QVBoxLayout()
        self.game_timer = QLabel("0:0")
        self.game_hangman = QLabel("")
        self.game_word = QLabel("word")

        # game_guessing_layout
        self.game_guessing_layout = QHBoxLayout()
        self.game_guess = QLineEdit()
        self.game_check = QPushButton("Click")

        self.game_check.clicked.connect(self.check_event)

        self.initUI()


    def initUI(self):
        # Main layout settings
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setHorizontalSpacing(0)
        main_layout.setVerticalSpacing(0)

        # Parameters
        self.font_hangman = QFont("Courier") 
        self.shortcut_enter = QShortcut(QKeySequence("Return"), self)


        # game_header_section
        self.game_header_widget = QWidget()
        self.game_header_layout.addWidget(self.game_header_label)
        self.game_header_layout.addWidget(self.game_header_logo)
        self.game_header_label.setCursor(Qt.CursorShape.OpenHandCursor)
        self.game_header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_header_widget.setLayout(self.game_header_layout)
        self.game_header_widget.setFixedHeight(100)
        self.game_header_logo.setFixedSize(75, 75)
        self.game_hangman.setFont(self.font_hangman)
            # menu_header_section adding names for css
        self.game_header_label.setObjectName("menu_header_label")
        self.game_header_logo.setObjectName("menu_header_logo")
        self.game_header_widget.setObjectName("menu_header_widget")

        # game_content_section
        self.game_content_widget = QWidget()
        self.game_content_layout.addWidget(self.game_timer)
        self.game_content_layout.addWidget(self.game_hangman)
        self.game_content_layout.addWidget(self.game_word)
        self.game_content_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.game_content_widget.setLayout(self.game_content_layout)
        self.game_content_widget.setFixedHeight(450)
        self.game_hangman.setFixedSize(150, 300)
        self.game_timer.setFixedHeight(50)
            # game_content_section adding names for css
        self.game_content_widget.setObjectName("game_content_widget")
        self.game_timer.setObjectName("game_timer")
        self.game_hangman.setObjectName("game_hangman")
        self.game_word.setObjectName("game_word")
        
        
        # game_guessing_section
        self.game_guessing_widget = QWidget()
        self.apply_shadow_effect_event(self.game_guess, Qt.GlobalColor.black)
        self.apply_shadow_effect_event(self.game_check, Qt.GlobalColor.black)
        self.game_guessing_layout.addWidget(self.game_guess)
        self.game_guessing_layout.addWidget(self.game_check)
        self.game_guess.setPlaceholderText("Please provide you guess...")
        self.shortcut_enter.activated.connect(self.check_event)
        self.game_check.clicked.connect(self.check_event)
        self.game_hangman.setFont(self.font_hangman)
        self.game_guessing_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_timer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_hangman.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.game_word.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_guessing_widget.setLayout(self.game_guessing_layout)
        self.game_guessing_widget.setFixedHeight(100)
        self.game_check.setFixedWidth(100)
        self.game_guess.setFixedWidth(500)
            # game_guessing_section adding names for css
        self.game_check.setObjectName("game_check")
        self.game_guess.setObjectName("game_guess")
        self.game_guessing_widget.setObjectName("game_guessing_widget")


        # Adding layouts to main layout
        main_layout.addWidget(self.game_header_widget, 0, 0)
        main_layout.addWidget(self.game_content_widget, 1, 0)
        main_layout.addWidget(self.game_guessing_widget, 2, 0)


        # Settings to grid layout
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 1)
        main_layout.setRowStretch(2, 1)
        main_layout.setColumnStretch(0, 1)

        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("""
                           /* Header css properties */
                           #menu_header_label {
                           font-size: 36px;
                           font-family: "Bradley Hand";
                           margin: 0px;
                           padding: 10px 0px;
                           letter-spacing: 2px;
                           }

                           #menu_header_label:hover {
                           color: #D3D3D3;
                           }
                           #game_header_logo {
                           padding: 10px 0px;
                           margin: 0px;
                           }
                           game_header_widget {
                           }
                           
                           /* Content css properties */
                           #game_timer {
                           color: white;
                           font-family: digital-clock-font;
                           }
                           #game_hangman, #word {
                           font-size: 20px;
                           color: white;
                           padding: 10px;
                           }
                           #word {
                           }

                           /* guessing css properties */
                           QLineEdit, #game_check {
                           padding: 10px 20px;
                           border: 2px solid black;
                           border-radius: 15px;
                            }
                           QLineEdit:hover {
                           background-color: #303030;
                           }
                           #game_check:hover {
                           background-color: #4527a0;
                           }
                           """)

        self.setLayout(main_layout)

    def game_status(self):
        self.start_time = time.time()
        #self.WORD_TO_GUESS = choose_word()
        self.WORD_TO_GUESS = "fraction"
        self.ITER = 0
        self.LETTERS = ["_" for i in range(len(self.WORD_TO_GUESS))]
        self.LETTERS_TO_DISPLAY = " ".join(self.LETTERS)
        self.GUESSED = []
        self.game_word.setText(self.LETTERS_TO_DISPLAY)
        self.WIN = False

    def check_event(self):
        self.GUESS = self.game_guess.text()
        self.game_guess.setText("")
        if self.GUESS.lower() in self.GUESSED:
            self.same_letter(self.GUESSED)
        self.ITER, self.LETTERS, self.GUESSED, self.WIN = hangman(ITER=self.ITER, GUESS=self.GUESS, WORD=self.WORD_TO_GUESS, LETTERS=self.LETTERS, GUESSED=self.GUESSED, WIN=self.WIN) 
        self.change_letters_event(self.LETTERS)
        if self.ITER > 0:
            self.change_stage(self.ITER)
        if self.WIN == True or self.ITER == 10:
            self.result_signal.emit([self.calculate_points(), self.game_timer.text(), self.WIN])
            self.game_timer.setText("")
            self.game_hangman.setText("")
            self.show_results()

    def update_time_event(self):
        timix = int(time.time() - self.start_time)
        minutes, seconds = divmod(timix, 60)

        time_text = f"{minutes}:{seconds}"
        self.game_timer.setText(f"{time_text}")

    def stop_timer(self):
        self.timer.stop()

    def change_stage(self, ITER):
        text = hangman_stage(ITER)
        self.game_hangman.setText(text)

    def change_letters_event(self, letters):
        text = " ".join(letters)
        self.game_word.setText(text)

    def apply_shadow_effect_event(self, widget, color):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setOffset(4, 4)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(color))
        widget.setGraphicsEffect(shadow_effect)

    def timer_checking(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_event)
        self.timer.start(1000)

    def on_show(self):
        self.timer_checking()
        self.game_status()

    def calculate_points(self) -> int:
        q = 1 if self.WIN == True else 0
        time_text = self.game_timer.text()
        time = time_text.split(":")
        time_points = round(100 - ((int(time[0])*60) + int(time[1])), 1)
        bdy_points = round(-2 * self.ITER, 1) 
        word_len = len(self.WORD_TO_GUESS)
        eq = ((time_points + bdy_points) * word_len) * q
        return eq

class Results(QWidget):
    def __init__(self, start_game, quit_app_event, save_score):
        super().__init__()
        self.save_score = save_score

        # results_header layout
        self.results_header_layout = QHBoxLayout()
        self.results_header_label = QLabel("Your results")

        # results_content layout
        self.results_content_layout = QVBoxLayout()
        self.results_content_time = QLabel("Time: xx:xx")
        self.results_content_score = QLabel("Score: X points")

        # results_footer_layout
        self.results_footer_layout = QHBoxLayout()
        self.results_footer_play_button = QPushButton("Play again")
        self.results_footer_exit_button = QPushButton("Exit")

        self.results_footer_play_button.clicked.connect(start_game)
        self.results_footer_exit_button.clicked.connect(quit_app_event)

        
        self.initUI()


    def initUI(self):
        # Main layout settings
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setHorizontalSpacing(0)
        main_layout.setVerticalSpacing(0)

        # Shadow


        # results_header_section layout
        self.results_header_widget = QWidget()
        self.results_header_label.setFixedHeight(100)
        self.results_header_layout.addWidget(self.results_header_label)
        self.results_header_widget.setFixedHeight(150)
        self.results_header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_header_widget.setLayout(self.results_header_layout)
            #   results_header_section adding names for css
        self.results_header_label.setObjectName("results_header_label")
        self.results_header_widget.setObjectName("results_header_widget")


        # results_content_section layout
        self.results_content_widget = QWidget()
        self.results_content_layout.addWidget(self.results_content_time)
        self.results_content_layout.addWidget(self.results_content_score)
        self.results_content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_content_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_content_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_content_widget.setFixedHeight(350)
        self.results_content_widget.setLayout(self.results_content_layout)
            # results_content_section adding names for css
        self.results_content_widget.setObjectName("results_content_widget")
        self.results_content_time.setObjectName("results_content_time")
        self.results_content_score.setObjectName("results_content_score")


        # results_footer_section layout
        self.results_footer_widget = QWidget()
        self.results_footer_layout.addWidget(self.results_footer_play_button)
        self.results_footer_layout.addWidget(self.results_footer_exit_button)
        self.results_footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_footer_widget.setLayout(self.results_footer_layout)
        self.apply_shadow_effect_event(self.results_footer_play_button, 'black')
        self.apply_shadow_effect_event(self.results_footer_exit_button, 'black')
        self.results_footer_widget.setFixedHeight(150)
            # results_footer_section adding names for css
        self.results_footer_play_button.setObjectName("results_footer_play_button")
        self.results_footer_exit_button.setObjectName("results_footer_exit_button")
        self.results_footer_widget.setObjectName("results_footer_widget")

        # Adding layouts to main layout
        main_layout.addWidget(self.results_header_widget)
        main_layout.addWidget(self.results_content_widget)
        main_layout.addWidget(self.results_footer_widget)

        # Settings to grid layout
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 1)
        main_layout.setRowStretch(2, 1)
        main_layout.setColumnStretch(0, 1)

        
        # Setting css properties for elements in this layout
        self.setStyleSheet("""
                           /* results_header section */
                           #results_header_widget {
                           }
                           #results_header_label {
                           font-size: 50px;
                           font-family: 'Century Gothic';
                           font-weight: bold;

                           }

                           /* results_content section */
                           #results_content_widget  {
                           }
                           #results_content_score, #results_content_time{
                           font-size: 30px;
                           font-weight: 600;
                           text-align: center;
                           
                           }
                           #results_content_time{
                           }

                           /* results_footer section */
                           #results_footer_widget {
                           }
                           #results_footer_play_button, #results_footer_exit_button {
                           height: 50px;
                           width: 100px;
                           font-size: 20px;
                           padding: 10px 20px;
                           text-align: center;
                           border: 2px solid black;
                           border-radius: 20px;
                           }
                           #results_footer_play_button:hover {
                           background-color: #3e8e41;
                           }
                           #results_footer_exit_button:hover {
                           background-color: #d32f2f;
                           }
                           
""")

        # Setting @main_layout as main layout
        self.setLayout(main_layout)

    def apply_shadow_effect_event(self, widget, color):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setOffset(4, 4)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(color))
        widget.setGraphicsEffect(shadow_effect)

    def receive_signal(self, points_time_win_list):
        self.update_results(points_time_win_list)


    def update_results(self, points_time_win_list):
        points = str(points_time_win_list[0])
        time = str(points_time_win_list[1])
        win = points_time_win_list[2]
        self.results_header_label.setText("You have won!" if win == True else "You lost...")
        self.results_content_score.setText(f"Points: {points}")
        self.results_content_time.setText(f"Time: {time}")
        if win:
            add_to_base(int(points))



    def on_show_result(self, points_time_win_list):
        self.update_results(points_time_win_list)

    

class Ranking(QWidget):
    def __init__(self, return_to_menu):
        super().__init__()
        
        # ranking_header layout
        self.ranking_header_layout = QHBoxLayout()
        self.ranking_header_label = QLabel("Ranking")

        # ranking_content layout
        self.ranking_content_layout = QVBoxLayout()
        self.ranking_content_scroll_area = QScrollArea()
        

        # ranking_footer layout
        self.ranking_footer_layout = QHBoxLayout()
        self.ranking_menu_button = QPushButton("Back")

        self.ranking_menu_button.clicked.connect(return_to_menu)

        self.populate_ranking_content()
        self.initUI()

    def initUI(self):
        # Main layout settings
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setHorizontalSpacing(0)
        main_layout.setVerticalSpacing(0)

        # ranking_header_section layout
        self.ranking_header_widget = QWidget()
        self.ranking_header_layout.addWidget(self.ranking_header_label)
        self.ranking_header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ranking_header_widget.setFixedHeight(100)
        self.ranking_header_widget.setLayout(self.ranking_header_layout)
            # ranking_header_section adding names for css
        self.ranking_header_widget.setObjectName("ranking_header_widget")
        self.ranking_header_label.setObjectName("ranking_header_label")

        # ranking_content_section layout
        self.ranking_content_widget = QWidget()
        self.ranking_content_scroll_area.setWidgetResizable(True)
        self.ranking_content_layout.addWidget(self.ranking_content_scroll_area)
        self.ranking_content_widget.setFixedHeight(400)
        self.ranking_content_widget.setLayout(self.ranking_content_layout)

        # ranking_footer_section layout
        self.ranking_footer_widget = QWidget()
        self.ranking_footer_layout.addWidget(self.ranking_menu_button)
        self.ranking_footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ranking_footer_widget.setFixedHeight(100)
        self.ranking_footer_widget.setLayout(self.ranking_footer_layout)
        self.apply_shadow_effect_event(self.ranking_menu_button, QColor("black"))
            # ranking_footer_section adding names for css
        self.ranking_menu_button.setObjectName("ranking_menu_button")

        
        # Adding layouts to main layout
        main_layout.addWidget(self.ranking_header_widget)
        main_layout.addWidget(self.ranking_content_widget)
        main_layout.addWidget(self.ranking_footer_widget)

        # Settings to grid layout
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 1)
        main_layout.setRowStretch(2, 1)
        main_layout.setColumnStretch(0, 1)

        # Setting css properties for elements in this layout
        self.setStyleSheet("""
                           /* ranking_header section */
                           #ranking_header_widget {
                           }
                           #ranking_header_label {
                           color: white;
                           font-size: 30px;
                           font-family: 'Roboto';
                           font-weight: bold;
                           }

                           /* ranking_footer section */
                           #ranking_menu_button {
                           height: 50px;
                           width: 100px;
                           font-size: 20px;
                           padding: 10px 20px;
                           text-align: center;
                           border: 2px solid black;
                           border-radius: 20px;
                           }
                           #ranking_menu_button:hover {
                           background-color: #212121;
                           }
                           """)

        # Setting @main_layout as main layout
        self.setLayout(main_layout)

    def populate_ranking_content(self):
        try:
            results = fetch_all_scores()

            scroll_content_widget = QWidget()
            scroll_content_layout = QVBoxLayout()
            scroll_content_widget.setLayout(scroll_content_layout)

            for index, (score, date) in enumerate(results, start=1):
                row_widget = QWidget()
                row_layout = QHBoxLayout()
                row_layout.setContentsMargins(10, 10, 10, 10)

                position_label = QLabel(f"{index}")
                username_label = QLabel(date)
                score_label = QLabel(f"{str(score)} points")

                row_layout.addWidget(position_label)
                row_layout.addWidget(username_label)
                row_layout.addWidget(score_label)
                username_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                username_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
                position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                score_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                score_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
                row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                row_widget.setFixedHeight(50)
                position_label.setFixedWidth(30)
                username_label.setFixedWidth(450)
                row_widget.setLayout(row_layout)

                row_widget.setStyleSheet("""
                                         QWidget {
                                         border: 2px dotted rgba(0, 0, 0, 0.2);
                                         border-radius: 25px;
                                         }
                                         """)
                position_label.setStyleSheet("""
                                             border: None;
                                             font-size: 16px;
                                             font-weight: bold;
                                             """)
                username_label.setStyleSheet("""
                                             border: None;
                                             font-size: 16px;
                                             font-weight: 700;
                                             """)
                score_label.setStyleSheet("""
                                     border: None;
                                          font-size: 16px;
                                          font-weight: 600;
                                     """)

                scroll_content_layout.addWidget(row_widget)
            self.ranking_content_scroll_area.setWidget(scroll_content_widget)

        except sqlite3.Error as e:
            error_label = QLabel("[Error]: Loading data failed...")
            error_label.setStyleSheet('color: red;')
    
    def apply_shadow_effect_event(self, widget, color):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setOffset(4, 4)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(color))
        widget.setGraphicsEffect(shadow_effect)

class Save_score_window(QDialog):
    # Do dokonczenia
    def __init__(self, game_score=List, parent=None):
        super().__init__(parent)
        POINTS = game_score[0]
        TIME = game_score[1]
        monitor = get_monitors()
        main_screen = monitor[0]

        app_width, app_height = 350, 200
        
        self.setWindowTitle("Save your score")
        self.setGeometry((main_screen.width - app_width)//2, (main_screen.height - app_height)//2 +250, app_width, app_height)

        main_layout = QVBoxLayout()

        provide_layout = QHBoxLayout()
        provide_widget = QWidget()
        name = QLineEdit()
        name.setPlaceholderText("Provide your name...")
        provide_layout.addWidget(name)
        provide_widget.setFixedHeight(50)
        provide_widget.setLayout(provide_layout)

        buttons_layout = QHBoxLayout()
        button_widget = QWidget()
        accept_button = QPushButton("Save")
        skip_button = QPushButton("Skip")
        buttons_layout.addWidget(accept_button)
        buttons_layout.addWidget(skip_button)
        button_widget.setLayout(buttons_layout)
        button_widget.setFixedHeight(100)

        self.apply_shadow_effect_event(skip_button, QColor("black"))
        self.apply_shadow_effect_event(accept_button, QColor("black"))
        self.apply_shadow_effect_event(name, QColor("black"))

        skip_button.setObjectName("skip_button")
        accept_button.setObjectName("accept_button")
        name.setObjectName("name")

        self.setStyleSheet("""
                           #skip_button, #accept_button {
                           width: 75px;
                           height: 50px;
                           color: white;
                           padding: 5px 10px;
                           border: 2px solid rgba(0,0,0,0.3);
                           border-radius: 25px;
                           }
                           #accept_button:hover {
                           background-color: #3e8e41;
                           }
                           #skip_button:hover {
                           background-color: #d32f2f;
                           }
                           #name {
                           padding: 5px 20px;
                           color: white;
                           font-weight: bold;
                           border: 2px solid rgba(0,0,0,0.3);
                           border-radius: 10px;

                           }
                           """)
        
        skip_button.clicked.connect(self.close_window)
        accept_button.clicked.connect(self.append_to_base(POINTS=POINTS, NAME=name.text))

        main_layout.addWidget(provide_widget)
        main_layout.addWidget(button_widget)
        self.setLayout(main_layout)

    def apply_shadow_effect_event(self, widget, color):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setOffset(4, 4)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(color))
        widget.setGraphicsEffect(shadow_effect)

    def close_window(self):
        self.close()

    def append_to_base(self, POINTS, NAME ):
        add_to_base(player_name= NAME,
                    score= POINTS
                    )

class Letter_again_window(QDialog):
    # Do dokonczenia
    def __init__(self, letters_used: list, parent=None):
        super().__init__(parent)

        monitor = get_monitors()
        main_screen = monitor[0]

        app_width, app_height = 350, 200
        
        self.setWindowTitle("[Error]: You have provided the same letter again")
        self.setGeometry((main_screen.width - app_width)//2, (main_screen.height - app_height)//2 + 350, app_width, app_height)
        
        #self.setWindowTitle("[Error]: You have provided the same letter again")
        layout = QVBoxLayout()
        letters_layout = QGridLayout()
        letters_widget = QWidget()
        back_widget = QWidget()
        back_layout = QHBoxLayout()
        back_button = QPushButton("Okey!")
        back_button.setObjectName("btn")
        back_button.clicked.connect(self.close_window)
        num_rows = 3
        letters = [
        "q", "a", "z", "w", "s", "x", "e", "d", "c", "r", 
        "f", "v", "t", "g", "b", "y", "h", "n", "u", "j", 
        "m", "i", "k", "o", "l", "p"
        ]   
        # num_cols = -(-len(letters) // num_rows)    

        for index, letter in enumerate(letters):
            row = index % num_rows
            col = index // num_rows
            letter_widget = QLabel(letter)
            # self.apply_shadow_effect_event(letter_widget, QColor("black"))
            letter_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bg = "red" if letter in letters_used else "rgba(0,0,0,0.15)"
            letter_widget.setStyleSheet(f"border: 1px solid rgba(0,0,0,0.3); padding: 0px 5px; background-color: {bg};")
            letters_layout.addWidget(letter_widget, row, col)

        self.apply_shadow_effect_event(back_button, QColor("black"))
        back_layout.addWidget(back_button)
        back_button.setStyleSheet("""
                                        #btn {
                                        border: 1px solid rgba(0,0,0,0.3); padding: 0px 5px;
                                        height: 50px;
                                        width: 75px;
                                        } 
                                        #btn:hover {
                                        background-color: rgba(0,0,0,0.15);
                                        }
                                        """)
        letters_widget.setLayout(letters_layout)
        letters_widget.setFixedSize(350, 150)
        back_widget.setFixedSize(350, 50)
        back_widget.setLayout(back_layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(letters_widget)
        layout.addWidget(back_widget)
        self.setLayout(layout)  

    def apply_shadow_effect_event(self, widget, color):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setOffset(4, 4)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(color))
        widget.setGraphicsEffect(shadow_effect)

    def close_window(self):
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        monitors = get_monitors()
        main_screen = monitors[0]

        # HYPER PARAMETERS
        MAIN_SCREEN_WIDTH, MAIN_SCREEN_HEIGHT = main_screen.width, main_screen.height
        APP_WIDTH, APP_HEIGHT = 650, 650

        # APP SETTINGS
        self.setFixedSize(APP_WIDTH, APP_HEIGHT)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.move((MAIN_SCREEN_WIDTH - APP_WIDTH) // 2, (MAIN_SCREEN_HEIGHT - APP_HEIGHT) // 2)

        self.stacked_layout = QStackedLayout()

        self.main_menu = MainMenu(self.start_game, self.show_ranking, self.quit_app_event)
        self.game = Game(self.show_results, self.same_letter)
        self.results = Results(self.start_game, self.quit_app_event, self.save_score)
        self.ranking = Ranking(self.return_to_menu)

        self.stacked_layout.addWidget(self.main_menu)
        self.stacked_layout.addWidget(self.game)
        self.stacked_layout.addWidget(self.results)
        self.stacked_layout.addWidget(self.ranking)

        self.stacked_layout.currentChanged.connect(self.on_layout_changed)

        central_widget = QWidget()
        central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(central_widget)

    def on_layout_changed(self, index):
        """Method activated when layout changes"""
        widget = self.stacked_layout.widget(index)
        if hasattr(widget, "on_show"):
            widget.on_show()


    def start_game(self):
        """Go to game layout"""
        self.stacked_layout.setCurrentWidget(self.game)

        self.game.result_signal.connect(self.results.receive_signal)

    def show_results(self):
        """Go to results layout"""
        self.stacked_layout.setCurrentWidget(self.results)

    def show_ranking(self):
        """Go to ranking layout"""
        self.stacked_layout.setCurrentWidget(self.ranking)

    def return_to_menu(self):
        """Go to main menu"""
        self.stacked_layout.setCurrentWidget(self.main_menu)

    def quit_app_event(self):
        """Exit from app"""
        QApplication.quit()

    def save_score(self, game_score):
        """Pop up window with save score option"""
        popup = Save_score_window(game_score)
        popup.exec()

    def same_letter(self, letters_used):
        """Pop up window with same letter error"""
        popup = Letter_again_window(letters_used)
        popup.exec()


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("/Users/konrad/Desktop/Projects/PyQT/media/hangman_icon.png"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()