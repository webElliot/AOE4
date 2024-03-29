import sys
from PyQt6.QtWidgets import QApplication
from app.load_css import load_css
from app.tablexfer import get_dataframe, load_build_order
from app.Widgets import OverlayWidget, OverlayButtons, VillagerWidget, WindowMinimize


class Resources(load_css):
    def __init__(self):
        BO_files = {
            "1": 'French 3 38 Feudal All-in_Castle Timing.bo',
            "2": 'Ayyubids desert raider opening into FC by VortiX.bo',
            "3": "Beastyqt mongol kashik.bo"
        }
        loaded = {
            '1': 'French Rush Good VS all EXCEPT RUS & Chinese',
            '2': 'Ayyubids desert raiders',
            '3': 'Mongols kashik'
        }
        print("""
        [1] French Rush Good VS all EXCEPT RUS & Chinese
        [2] Ayyubids desert raiders
        [3] Mongols kashik
        """)
        selected = input("Enter your choice:")
        while BO_files.get(selected) is None:
            print("\n Invalid choice. Please try again.")
            selected = input("Enter your choice:")



        super().__init__()
        self.vars()
        self.new = True
        self.current_index = 0  # Initialize the current index for DataFrame row iteration
        self.df = get_dataframe('ottomans_2.html')

        #self.df = load_build_order(BO_files.get(selected))
        self.app = QApplication(sys.argv)
        self.overlayButtons = OverlayButtons(self)
        self.description = OverlayWidget(str(f"Loaded {loaded.get(selected)}"),
                                         10, 200,
                                         maxWidth=400,
                                         maxHeight=200,
                                         color='white',
                                         css = self.load_css('description.css')
                                         )

        self.CivMenu = OverlayWidget(str(f"Loaded {loaded.get(selected)}"),
                                         10, 200,
                                         maxWidth=400,
                                         maxHeight=200,
                                         color='white',
                                         css=self.load_css('description.css')
                                         )
        [
            self.set_food(""), self.set_wood(""), self.set_gold(""), self.set_stone("")
        ]
        self.WindowMinimize = WindowMinimize(self, css= self.load_css('Minimize.css'))
        self.WindowMinimize.show()
        self.description.show()
        self.overlayButtons.show()

    def vars(self):
        self.y_start = 1210
        self.line_height = 50
        self.y_axis = {
            'food': self.y_start,
            'wood': self.y_start + 1 * self.line_height,
            'gold': self.y_start + 2 * self.line_height,
            'stone': self.y_start + 3 * self.line_height
        }
        self.x_axis = 220

        self.food = None
        self.wood = None
        self.gold = None
        self.stone = None




    def back(self):
        if self.current_index > 0:
            self.current_index -= 1
        self.update_overlays()

    def next(self):
        if self.new:
            self.new = False
            self.update_overlays()
        else:
            if self.current_index < len(self.df) - 1:
                self.current_index += 1
            self.update_overlays()

    def update_overlays(self):
        row = self.df.iloc[self.current_index]

        self.description.setText(row[1])
        self.set_food(row[2])
        self.set_wood(row[3])
        self.set_gold(row[4])
        self.set_stone(row[5])

    def set_food(self, value):
        if self.food is None:
            self.food = VillagerWidget(str(value), self.x_axis, self.y_axis.get('food'))
            self.food.show()
        else:
            self.food.setText(str(value))

    def set_wood(self, value):
        if self.wood is None:
            self.wood = VillagerWidget(str(value), self.x_axis, self.y_axis.get('wood'))
            self.wood.show()
        else:
            self.wood.setText(str(value))

    def set_gold(self, value):
        if self.gold is None:
            self.gold = VillagerWidget(str(value), self.x_axis, self.y_axis.get('gold'))
            self.gold.show()
        else:
            self.gold.setText(str(value))

    def set_stone(self, value):
        if self.stone is None:
            self.stone = VillagerWidget(str(value), self.x_axis, self.y_axis.get('stone'))
            self.stone.show()
        else:
            self.stone.setText(str(value))

    def run(self):
        sys.exit(self.app.exec())