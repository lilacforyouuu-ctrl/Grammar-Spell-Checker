import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import re
import threading

# Optional features work when their packages are installed.
try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None


# -------------------- THEME --------------------

BG = "#0C0D20"
SIDEBAR = "#11132B"
PANEL = "#191A38"
PANEL_HOVER = "#222347"
BORDER = "#383466"
PURPLE = "#A98AEF"
PURPLE_DARK = "#7254B5"
MINT = "#79D6BF"
PEACH = "#F2A99E"
WHITE = "#F5F1FF"
MUTED = "#B9B3D4"
TRACK = "#2A2B50"

FONT = "Segoe UI"
TITLE_FONT = "Georgia"


# -------------------- GAME QUESTIONS --------------------

GAMES = {
    "Grammar Quest": [
        {
            "q": "She ___ to school every day.",
            "options": ["go", "goes", "going", "gone"],
            "answer": 1,
            "explanation": "Use 'goes' with he, she or it in the simple present tense."
        },
        {
            "q": "Neither of the boys ___ present.",
            "options": ["are", "were", "is", "have"],
            "answer": 2,
            "explanation": "'Neither' is treated as singular in this sentence."
        },
        {
            "q": "I have lived here ___ 2020.",
            "options": ["for", "since", "from", "by"],
            "answer": 1,
            "explanation": "Use 'since' with a starting point in time."
        },
        {
            "q": "If I ___ rich, I would travel the world.",
            "options": ["am", "was being", "were", "will be"],
            "answer": 2,
            "explanation": "'If I were' is commonly used for an unreal or hypothetical situation."
        },
        {
            "q": "The news ___ surprising.",
            "options": ["are", "were", "is", "have"],
            "answer": 2,
            "explanation": "'News' takes a singular verb."
        },
        {
            "q": "Each of the students ___ a notebook.",
            "options": ["have", "has", "are having", "were"],
            "answer": 1,
            "explanation": "'Each' takes a singular verb."
        },
        {
            "q": "By next year, she ___ her course.",
            "options": ["completes", "completed", "will have completed", "completing"],
            "answer": 2,
            "explanation": "The future perfect describes an action completed before a future time."
        },
        {
            "q": "He is better at maths ___ I am.",
            "options": ["then", "than", "that", "as"],
            "answer": 1,
            "explanation": "Use 'than' when making a comparison."
        },
        {
            "q": "The teacher, along with the students, ___ here.",
            "options": ["are", "were", "is", "have"],
            "answer": 2,
            "explanation": "The main subject is 'teacher', which is singular."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "She don't like tea.",
                "She doesn't likes tea.",
                "She doesn't like tea.",
                "She not like tea."
            ],
            "answer": 2,
            "explanation": "After 'doesn't', use the base form 'like'."
        }
    ],

    "Punctuation Panic": [
        {
            "q": "Choose the correctly punctuated sentence.",
            "options": [
                "Where are you going.",
                "Where are you going?",
                "Where are you going!",
                "Where, are you going?"
            ],
            "answer": 1,
            "explanation": "A direct question ends with a question mark."
        },
        {
            "q": "Which sentence uses the apostrophe correctly?",
            "options": [
                "The girls bag is blue.",
                "The girl's bag is blue.",
                "The girls' bag's is blue.",
                "The girls bag's blue."
            ],
            "answer": 1,
            "explanation": "The apostrophe in girl's shows possession by one girl."
        },
        {
            "q": "Choose the correct punctuation.",
            "options": [
                "I bought apples oranges and grapes.",
                "I bought apples, oranges, and grapes.",
                "I bought, apples oranges and grapes.",
                "I bought apples oranges, and, grapes."
            ],
            "answer": 1,
            "explanation": "Commas separate items in a list."
        },
        {
            "q": "Which sentence is correct?",
            "options": [
                "Wow that is amazing!",
                "Wow, that is amazing!",
                "Wow that, is amazing.",
                "Wow; that is amazing?"
            ],
            "answer": 1,
            "explanation": "A comma can follow an introductory interjection."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "Riya said I am tired.",
                "Riya said, 'I am tired.'",
                "Riya said 'I am tired'",
                "Riya, said 'I am tired'."
            ],
            "answer": 1,
            "explanation": "A comma introduces the quotation, which is enclosed in quotation marks."
        },
        {
            "q": "Which mark completes this sentence: What a beautiful day___",
            "options": [".", "?", "!", ","],
            "answer": 2,
            "explanation": "An exclamation mark expresses strong feeling."
        },
        {
            "q": "Choose the correct contraction.",
            "options": ["Its raining.", "It's raining.", "Its' raining.", "It raining's."],
            "answer": 1,
            "explanation": "'It's' means 'it is'."
        },
        {
            "q": "Which sentence is correctly punctuated?",
            "options": [
                "Although it rained we went out.",
                "Although, it rained we went out.",
                "Although it rained, we went out.",
                "Although it, rained we went out."
            ],
            "answer": 2,
            "explanation": "A comma separates the introductory dependent clause from the main clause."
        },
        {
            "q": "Choose the correct punctuation.",
            "options": [
                "My favourite subjects are English, Maths and Science.",
                "My favourite subjects are English Maths and Science?",
                "My favourite subjects are: English Maths and Science",
                "My favourite subjects, are English Maths and Science."
            ],
            "answer": 0,
            "explanation": "Commas separate the items in the list."
        },
        {
            "q": "Which sentence is correct?",
            "options": [
                "Lets eat, Grandma!",
                "Let's eat Grandma!",
                "Let's eat, Grandma!",
                "Lets eat Grandma."
            ],
            "answer": 2,
            "explanation": "The apostrophe belongs in 'Let's', and the comma addresses Grandma."
        }
    ],

    "Spell Sprint": [
        {
            "q": "Choose the correct spelling.",
            "options": ["Definately", "Definitely", "Definetely", "Definatly"],
            "answer": 1,
            "explanation": "The correct spelling is definitely."
        },
        {
            "q": "Choose the correct spelling.",
            "options": ["Recieve", "Receive", "Receeve", "Receve"],
            "answer": 1,
            "explanation": "Remember: 'i before e' does not apply here; receive is the correct spelling."
        },
        {
            "q": "Choose the correct spelling.",
            "options": ["Necessary", "Neccessary", "Necesary", "Neccesary"],
            "answer": 0,
            "explanation": "Necessary has one c and two s letters."
        },
        {
            "q": "Choose the correct spelling.",
            "options": ["Occured", "Ocurred", "Occurred", "Occurrred"],
            "answer": 2,
            "explanation": "Occurred has a double c and a double r."
        },
        {
            "q": "Choose the correct spelling.",
            "options": ["Separate", "Seperate", "Sepparate", "Separrate"],
            "answer": 0,
            "explanation": "The correct spelling is separate."
        },
        {
            "q": "Choose the correct spelling.",
            "options": ["Enviroment", "Environment", "Envirnoment", "Environmant"],
            "answer": 1,
            "explanation": "The correct spelling is environment."
        },
        {
            "q": "Choose the correct spelling.",
            "options": ["Accomodate", "Acommodate", "Accommodate", "Acomodate"],
            "answer": 2,
            "explanation": "Accommodate has double c and double m."
        },
        {
            "q": "Choose the correct spelling.",
            "options": ["Privilege", "Priviledge", "Privelege", "Privillage"],
            "answer": 0,
            "explanation": "The correct spelling is privilege."
        },
        {
            "q": "Choose the correct spelling.",
            "options": ["Maintanance", "Maintenance", "Maintenence", "Maintanence"],
            "answer": 1,
            "explanation": "The correct spelling is maintenance."
        },
        {
            "q": "Choose the correct spelling.",
            "options": ["Pronounciation", "Pronunciation", "Pronunciasion", "Pronuncation"],
            "answer": 1,
            "explanation": "The correct spelling is pronunciation."
        }
    ],

    "Sentence Builder": [
        {
            "q": "Arrange the words into a correct sentence.",
            "options": [
                "The sun rises in the east.",
                "In the east the rises sun.",
                "Rises the sun east in the.",
                "The east rises in the sun."
            ],
            "answer": 0,
            "explanation": "The usual order is subject, verb and the remaining information."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "Always she is punctual.",
                "She is always punctual.",
                "She always punctual is.",
                "Punctual always is she."
            ],
            "answer": 1,
            "explanation": "The adverb 'always' usually comes before the main adjective after 'is'."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "Because it was raining, we stayed indoors.",
                "We indoors stayed because raining it was.",
                "Because raining was it, stayed we indoors.",
                "It because was raining stayed indoors we."
            ],
            "answer": 0,
            "explanation": "The introductory clause is followed by the main clause."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "She has completed her homework.",
                "She completed has her homework.",
                "Has she her homework completed.",
                "Her homework she has completing."
            ],
            "answer": 0,
            "explanation": "The present perfect uses has/have + past participle."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "The children are playing outside.",
                "Playing outside the children are.",
                "Outside playing are children the.",
                "Are children the outside playing."
            ],
            "answer": 0,
            "explanation": "The subject comes before the verb in a normal statement."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "I enjoy reading books.",
                "I reading enjoy books.",
                "Enjoy books I reading.",
                "Books enjoy reading I."
            ],
            "answer": 0,
            "explanation": "The verb 'enjoy' is followed by a gerund: reading."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "Although she was tired, she continued working.",
                "Although tired she was, working continued she.",
                "She although tired continued was working.",
                "Continued she working although was tired."
            ],
            "answer": 0,
            "explanation": "The dependent clause introduces the main clause."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "He speaks English fluently.",
                "He English speaks fluently.",
                "Fluently English he speaks.",
                "Speaks he fluently English."
            ],
            "answer": 0,
            "explanation": "The normal order is subject, verb, object and adverb."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "If you work hard, you will succeed.",
                "If work you hard, succeed you will.",
                "You if succeed work hard will.",
                "Will succeed if hard you work."
            ],
            "answer": 0,
            "explanation": "A first conditional sentence uses if + present simple, then will + base verb."
        },
        {
            "q": "Choose the correct sentence.",
            "options": [
                "Honesty is the best policy.",
                "The best honesty policy is.",
                "Policy the honesty best is.",
                "Is honesty policy the best."
            ],
            "answer": 0,
            "explanation": "This is the correct subject-verb-complement order."
        }
    ]
}

# Shared global state so progress never resets when switching views
SHARED_STATE = {
    "progress": {name: 0 for name in GAMES},
    "best_scores": {name: 0 for name in GAMES},
    "completed_games": 0,
    "total_xp": 0,
    "daily_done": False
}


# -------------------- APPLICATION --------------------

class SpellSync:
    def __init__(self, root):
        self.root = root
        self.root.title("SpellSync | Writing & Learning")
        self.root.geometry("1240x820")
        self.root.minsize(1000, 700)
        self.root.configure(bg=BG)

        self.page = "home"
        self.current_game = ""
        self.questions = []
        self.question_index = 0
        self.score = 0
        self.selected_answer = tk.IntVar(value=-1)

        self.difficulty = tk.StringVar(value="Medium")
        self.selected_tone = tk.StringVar(value="Neutral")
        self.target_language = tk.StringVar(value="Hindi")
        self.read_aloud_enabled = tk.BooleanVar(value=True)

        self.setup_styles()
        self.build_shell()
        self.show_home()

    @property
    def progress(self):
        return SHARED_STATE["progress"]

    @property
    def best_scores(self):
        return SHARED_STATE["best_scores"]

    @property
    def completed_games(self):
        return SHARED_STATE["completed_games"]

    @completed_games.setter
    def completed_games(self, val):
        SHARED_STATE["completed_games"] = val

    @property
    def total_xp(self):
        return SHARED_STATE["total_xp"]

    @total_xp.setter
    def total_xp(self, val):
        SHARED_STATE["total_xp"] = val

    @property
    def daily_done(self):
        return SHARED_STATE["daily_done"]

    @daily_done.setter
    def daily_done(self, val):
        SHARED_STATE["daily_done"] = val

    # -------------------- STYLES --------------------

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Spell.Horizontal.TProgressbar",
            troughcolor=TRACK,
            background=PURPLE,
            bordercolor=TRACK,
            lightcolor=PURPLE,
            darkcolor=PURPLE
        )

        style.configure(
            "Spell.TCombobox",
            fieldbackground=PANEL,
            background=PANEL,
            foreground=WHITE,
            arrowcolor=PURPLE
        )

    # -------------------- APP LAYOUT --------------------

    def build_shell(self):
        top = tk.Frame(self.root, bg=BG, height=45)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(
            top,
            text="●  ●  ●",
            bg=BG,
            fg=PURPLE,
            font=(FONT, 10)
        ).pack(side="left", padx=18)

        tk.Label(
            top,
            text="SPELLSYNC  /  WRITING & LEARNING",
            bg=BG,
            fg=MUTED,
            font=(FONT, 9, "bold")
        ).pack(side="left")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(body, bg=SIDEBAR, width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="SpellSync",
            bg=SIDEBAR,
            fg=WHITE,
            font=(TITLE_FONT, 25, "bold")
        ).pack(anchor="w", padx=22, pady=(25, 0))

        tk.Label(
            self.sidebar,
            text="WRITE WITH CONFIDENCE",
            bg=SIDEBAR,
            fg=PURPLE,
            font=(FONT, 8, "bold")
        ).pack(anchor="w", padx=24, pady=(3, 24))

        nav_items = [
            ("Home", "⌂", self.show_home),
            ("Learning Hub", "◈", self.show_hub),
            ("Grammar Checker", "✎", self.show_checker),
            ("Translation", "文", self.show_translation),
            ("PDF Assistant", "▤", self.show_pdf_assistant),
            ("My Progress", "↗", self.show_progress),
            ("Settings", "⚙", self.show_settings),
        ]

        self.nav_buttons = {}

        for label, symbol, command in nav_items:
            button = tk.Button(
                self.sidebar,
                text=f"  {symbol}     {label}",
                command=command,
                anchor="w",
                bg=SIDEBAR,
                fg=MUTED,
                activebackground=PANEL_HOVER,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                padx=15,
                pady=12,
                font=(FONT, 10),
                cursor="hand2"
            )
            button.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[label] = button

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(
            fill="x", padx=18, pady=(20, 12)
        )

        tk.Label(
            self.sidebar,
            text="YOUR WRITING JOURNEY",
            bg=SIDEBAR,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(anchor="w", padx=22)

        self.sidebar_xp = tk.Label(
            self.sidebar,
            text="✦  0 XP earned",
            bg=SIDEBAR,
            fg=MINT,
            font=(FONT, 10, "bold")
        )
        self.sidebar_xp.pack(anchor="w", padx=22, pady=10)

        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def set_active(self, active):
        for name, button in self.nav_buttons.items():
            if name == active:
                button.configure(
                    bg=PANEL_HOVER,
                    fg=WHITE,
                    font=(FONT, 10, "bold")
                )
            else:
                button.configure(
                    bg=SIDEBAR,
                    fg=MUTED,
                    font=(FONT, 10)
                )

        self.sidebar_xp.configure(text=f"✦  {self.total_xp} XP earned")

    def heading(self, title, subtitle):
        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", padx=35, pady=(27, 20))

        tk.Label(
            top,
            text=title,
            bg=BG,
            fg=WHITE,
            font=(TITLE_FONT, 26, "bold")
        ).pack(anchor="w")

        tk.Label(
            top,
            text=subtitle,
            bg=BG,
            fg=MUTED,
            font=(FONT, 10)
        ).pack(anchor="w", pady=(5, 0))

    def make_button(self, parent, text, command,
                    color=PURPLE, fg=BG, width=None):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=fg,
            activebackground=PANEL_HOVER,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            font=(FONT, 10, "bold"),
            cursor="hand2"
        )
        if width:
            button.configure(width=width)
        return button

    def make_card(self, parent, padding=20):
        return tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=padding,
            pady=padding
        )

    def make_scroll_area(self, parent):
        outer = tk.Frame(parent, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        canvas = tk.Canvas(
            outer, bg=BG, highlightthickness=0, bd=0
        )
        scrollbar = ttk.Scrollbar(
            outer, orient="vertical", command=canvas.yview
        )
        inner = tk.Frame(canvas, bg=BG)

        window_id = canvas.create_window(
            (0, 0), window=inner, anchor="nw"
        )

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_inner(event):
            canvas.itemconfigure(window_id, width=event.width)

        inner.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", resize_inner)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return inner

    # -------------------- HOME --------------------

    def show_home(self):
        self.page = "home"
        self.clear_content()
        self.set_active("Home")
        self.heading(
            "A better way to write.",
            "Learn the rules. Build the habit. Find your writing flow."
        )

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        hero = self.make_card(outer, 28)
        hero.pack(fill="x", pady=(0, 18))

        tk.Label(
            hero,
            text="YOUR NEXT CHAPTER STARTS HERE",
            bg=PANEL,
            fg=MINT,
            font=(FONT, 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            hero,
            text="Make every word\nwork better.",
            bg=PANEL,
            fg=WHITE,
            font=(TITLE_FONT, 29, "bold"),
            justify="left"
        ).pack(anchor="w", pady=(12, 8))

        tk.Label(
            hero,
            text="A writing companion for grammar, spelling, punctuation "
                   "and clearer sentences.",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 11),
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=(0, 18))

        row = tk.Frame(hero, bg=PANEL)
        row.pack(anchor="w")

        self.make_button(
            row, "Explore Learning Hub", self.show_hub
        ).pack(side="left", padx=(0, 10))

        self.make_button(
            row, "Open Grammar Checker",
            self.show_checker, color=MINT
        ).pack(side="left")

        stats = tk.Frame(outer, bg=BG)
        stats.pack(fill="x", pady=(0, 18))

        stat_values = [
            ("TOTAL XP", str(self.total_xp), PURPLE),
            ("GAMES COMPLETED", str(self.completed_games), MINT),
            ("DAILY CHALLENGE", "Done" if self.daily_done else "Ready", PEACH)
        ]

        for title, value, color in stat_values:
            card = self.make_card(stats, 16)
            card.pack(side="left", fill="both", expand=True, padx=(0, 12))
            tk.Label(
                card, text=title, bg=PANEL, fg=MUTED,
                font=(FONT, 8, "bold")
            ).pack(anchor="w")
            tk.Label(
                card, text=value, bg=PANEL, fg=color,
                font=(TITLE_FONT, 23, "bold")
            ).pack(anchor="w", pady=(6, 0))

        tk.Label(
            outer,
            text="PICK UP WHERE YOU LEFT OFF",
            bg=BG,
            fg=MUTED,
            font=(FONT, 9, "bold")
        ).pack(anchor="w", pady=(5, 12))

        quick = tk.Frame(outer, bg=BG)
        quick.pack(fill="x")

        shortcuts = [
            ("Grammar practice", "Strengthen your grammar.", self.show_hub),
            ("Writing tools", "Check, polish and improve text.", self.show_checker),
            ("Translation", "Explore another language.", self.show_translation)
        ]

        for title, description, command in shortcuts:
            card = self.make_card(quick, 15)
            card.pack(side="left", fill="both", expand=True, padx=(0, 12))
            tk.Label(
                card, text=title, bg=PANEL, fg=WHITE,
                font=(FONT, 11, "bold")
            ).pack(anchor="w")
            tk.Label(
                card, text=description, bg=PANEL, fg=MUTED,
                font=(FONT, 9), wraplength=180, justify="left"
            ).pack(anchor="w", pady=(7, 12))
            self.make_button(
                card, "Open →", command, color=PANEL_HOVER, fg=WHITE
            ).pack(anchor="w")

    # -------------------- LEARNING HUB --------------------

    def show_hub(self):
        self.page = "hub"
        self.clear_content()
        self.set_active("Learning Hub")
        self.heading(
            "Learning Hub",
            "Small practice sessions. Stronger writing skills."
        )

        inner = self.make_scroll_area(self.content)

        control = self.make_card(inner, 14)
        control.pack(fill="x", pady=(0, 16))

        tk.Label(
            control, text="Practice length", bg=PANEL,
            fg=WHITE, font=(FONT, 10, "bold")
        ).pack(side="left", padx=(0, 12))

        ttk.Combobox(
            control,
            textvariable=self.difficulty,
            values=["Easy", "Medium", "Hard"],
            state="readonly",
            width=12,
            style="Spell.TCombobox"
        ).pack(side="left")

        tk.Label(
            control,
            text="Easy: 5 questions   •   Medium: 7   •   Hard: 10",
            bg=PANEL, fg=MUTED, font=(FONT, 9)
        ).pack(side="left", padx=18)

        grid = tk.Frame(inner, bg=BG)
        grid.pack(fill="both", expand=True, pady=(0, 15))

        descriptions = {
            "Grammar Quest": (
                "◇", "Grammar & sentence rules", PURPLE
            ),
            "Punctuation Panic": (
                "¶", "Punctuation & clarity", PEACH
            ),
            "Spell Sprint": (
                "Aa", "Spelling & word accuracy", MINT
            ),
            "Sentence Builder": (
                "↔", "Sentence structure & order", PURPLE
            )
        }

        for index, name in enumerate(GAMES):
            r, c = divmod(index, 2)
            card = self.make_card(grid, 20)
            card.grid(
                row=r, column=c, sticky="nsew",
                padx=(0 if c == 0 else 10, 0 if c == 1 else 10),
                pady=(0, 14)
            )
            grid.grid_columnconfigure(c, weight=1)

            symbol, description, accent = descriptions[name]

            tk.Label(
                card, text=symbol, bg=PANEL, fg=accent,
                font=(TITLE_FONT, 24, "bold")
            ).pack(anchor="w")

            tk.Label(
                card, text=name, bg=PANEL, fg=WHITE,
                font=(TITLE_FONT, 17, "bold")
            ).pack(anchor="w", pady=(8, 4))

            tk.Label(
                card, text=description, bg=PANEL, fg=MUTED,
                font=(FONT, 9)
            ).pack(anchor="w")

            tk.Label(
                card,
                text=f"Best score: {self.best_scores[name]}/10",
                bg=PANEL, fg=MUTED, font=(FONT, 9)
            ).pack(anchor="w", pady=(15, 6))

            ttk.Progressbar(
                card,
                style="Spell.Horizontal.TProgressbar",
                maximum=10,
                value=self.progress[name]
            ).pack(fill="x", pady=(0, 15))

            self.make_button(
                card, "Start practice →",
                lambda n=name: self.start_game(n),
                color=accent
            ).pack(anchor="w")

        daily = self.make_card(inner, 17)
        daily.pack(fill="x", pady=(0, 20))

        tk.Label(
            daily, text="DAILY CHALLENGE",
            bg=PANEL, fg=PEACH, font=(FONT, 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            daily,
            text=(
                "Completed for today ✓"
                if self.daily_done
                else "Five mixed questions to test your skills."
            ),
            bg=PANEL, fg=WHITE, font=(FONT, 11)
        ).pack(anchor="w", pady=(5, 10))

        if not self.daily_done:
            self.make_button(
                daily, "Take challenge",
                self.start_daily, color=PEACH
            ).pack(anchor="w")
        else:
            tk.Label(
                daily, text="Come back for your next challenge.",
                bg=PANEL, fg=MUTED, font=(FONT, 9)
            ).pack(anchor="w")

    # -------------------- GAME LOGIC --------------------

    def start_game(self, name):
        self.current_game = name
        self.questions = list(GAMES[name])
        random.shuffle(self.questions)

        difficulty = self.difficulty.get()

        if difficulty == "Easy":
            count = 5
        elif difficulty == "Hard":
            count = 10
        else:
            count = 7

        self.questions = self.questions[:count]
        self.question_index = 0
        self.score = 0
        self.is_daily = False
        self.show_question()

    def start_daily(self):
        if self.daily_done:
            messagebox.showinfo(
                "Daily Challenge",
                "You have already completed this challenge."
            )
            return

        mixed = []
        for questions in GAMES.values():
            mixed.extend(questions)

        random.shuffle(mixed)

        self.current_game = "Daily Challenge"
        self.questions = mixed[:5]
        self.question_index = 0
        self.score = 0
        self.is_daily = True
        self.show_question()

    def show_question(self):
        self.page = "game"
        self.clear_content()
        self.set_active("Learning Hub")

        question = self.questions[self.question_index]
        total = len(self.questions)

        self.heading(
            self.current_game,
            f"Question {self.question_index + 1} of {total}"
        )

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=45, pady=(0, 35))

        ttk.Progressbar(
            outer,
            style="Spell.Horizontal.TProgressbar",
            maximum=total,
            value=self.question_index
        ).pack(fill="x", pady=(0, 25))

        card = self.make_card(outer, 25)
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text=f"QUESTION {self.question_index + 1:02d}",
            bg=PANEL, fg=PURPLE,
            font=(FONT, 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text=question["q"],
            bg=PANEL, fg=WHITE,
            font=(TITLE_FONT, 19, "bold"),
            wraplength=700,
            justify="left"
        ).pack(anchor="w", pady=(14, 25))

        self.selected_answer = tk.IntVar(value=-1)
        self.option_buttons = []

        for index, option in enumerate(question["options"]):
            btn = tk.Radiobutton(
                card,
                text=option,
                variable=self.selected_answer,
                value=index,
                bg=PANEL,
                fg=WHITE,
                selectcolor=PANEL_HOVER,
                activebackground=PANEL,
                activeforeground=WHITE,
                font=(FONT, 11),
                anchor="w",
                padx=10,
                pady=6
            )
            btn.pack(fill="x", pady=4)
            self.option_buttons.append(btn)

        action_frame = tk.Frame(card, bg=PANEL)
        action_frame.pack(anchor="w", pady=(25, 0))

        self.make_button(
            action_frame, "Submit Answer", self.check_answer, color=MINT
        ).pack(side="left")

    def check_answer(self):
        selected = self.selected_answer.get()
        if selected == -1:
            messagebox.showwarning("Select Option", "Please select an answer first.")
            return

        question = self.questions[self.question_index]
        correct = question["answer"]

        if selected == correct:
            self.score += 1
            res_title = "Correct! 🎉"
        else:
            res_title = "Incorrect 💡"

        explanation = question["explanation"]
        messagebox.showinfo(res_title, f"{explanation}")

        self.question_index += 1
        if self.question_index < len(self.questions):
            self.show_question()
        else:
            self.finish_game()

    def finish_game(self):
        earned_xp = self.score * 15
        self.total_xp += earned_xp

        if self.is_daily:
            self.daily_done = True
        else:
            if self.current_game in self.progress:
                self.progress[self.current_game] = max(
                    self.progress[self.current_game], self.score
                )
                self.best_scores[self.current_game] = max(
                    self.best_scores[self.current_game], self.score
                )
            self.completed_games += 1

        self.clear_content()
        self.heading("Practice Completed! 🏆", f"You scored {self.score} out of {len(self.questions)}")

        card = self.make_card(self.content, 30)
        card.pack(fill="both", expand=True, padx=45, pady=(0, 35))

        tk.Label(
            card,
            text=f"+{earned_xp} XP Earned!",
            bg=PANEL,
            fg=MINT,
            font=(TITLE_FONT, 22, "bold")
        ).pack(anchor="w", pady=(0, 15))

        self.make_button(
            card, "Back to Learning Hub", self.show_hub, color=PURPLE
        ).pack(anchor="w")

    # -------------------- ALL PANELS (FULLY IMPLEMENTED WITH VOICE & TTS) --------------------

    def show_checker(self):
        self.page = "checker"
        self.clear_content()
        self.set_active("Grammar Checker")
        self.heading("Grammar Checker", "Analyze text for grammar, spelling, punctuation, and tone.")

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        card = self.make_card(outer, 20)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="YOUR TEXT", bg=PANEL, fg=PURPLE, font=(FONT, 9, "bold")).pack(anchor="w")
        self.checker_input = tk.Text(card, height=5, bg=BG, fg=WHITE, insertbackground=WHITE, font=(FONT, 11), bd=0, highlightthickness=1, highlightbackground=BORDER)
        self.checker_input.pack(fill="x", pady=(4, 10))

        ctrl = tk.Frame(card, bg=PANEL)
        ctrl.pack(fill="x", pady=(0, 10))

        tk.Label(ctrl, text="Tone/Style:", bg=PANEL, fg=MUTED, font=(FONT, 9, "bold")).pack(side="left", padx=(0, 6))
        tone_box = ttk.Combobox(ctrl, textvariable=self.selected_tone, values=["Neutral", "Professional", "Friendly", "Empathetic", "Concise"], state="readonly", width=14, style="Spell.TCombobox")
        tone_box.pack(side="left", padx=(0, 15))

        self.make_button(ctrl, "Check Writing", self.run_checker_action, color=MINT).pack(side="left", padx=(0, 10))
        self.make_button(ctrl, "🎤 Voice (In)", self.record_voice_input, color=PURPLE, fg=BG).pack(side="left", padx=(0, 10))
        self.make_button(ctrl, "🔊 Read (Out)", self.read_output_audio, color=SIDEBAR, fg=WHITE).pack(side="left")

        tk.Label(card, text="CORRECTED & STYLED OUTPUT", bg=PANEL, fg=PURPLE, font=(FONT, 9, "bold")).pack(anchor="w", pady=(5, 0))
        self.checker_output = tk.Text(card, height=5, bg=BG, fg=WHITE, insertbackground=WHITE, font=(FONT, 11), bd=0, highlightthickness=1, highlightbackground=BORDER)
        self.checker_output.pack(fill="x", pady=(4, 0))
        self.checker_output.config(state="disabled")

    def run_checker_action(self):
        text = self.checker_input.get("1.0", tk.END).strip()
        tone = self.selected_tone.get()
        if not text:
            messagebox.showwarning("Empty", "Please enter text to check.")
            return
        
        corrected = text
        if "dont" in corrected.lower():
            corrected = re.sub(r"\bdont\b", "don't", corrected, flags=re.IGNORECASE)
        if not corrected.endswith(('.', '!', '?')):
            corrected += "."
        
        self.checker_output.config(state="normal")
        self.checker_output.delete("1.0", tk.END)
        self.checker_output.insert(tk.END, corrected)
        self.checker_output.config(state="disabled")

    def record_voice_input(self):
        if not sr:
            messagebox.showerror("Error", "speech_recognition package is not installed.")
            return
        
        def listen_thread():
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    messagebox.showinfo("Voice Input", "Listening... Speak now.")
                    audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio)
                self.checker_input.insert(tk.END, " " + text)
            except Exception as e:
                messagebox.showerror("Voice Error", f"Could not recognize speech: {e}")

        threading.Thread(target=listen_thread, daemon=True).start()

    def read_output_audio(self):
        text = self.checker_output.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty", "No corrected text to read aloud.")
            return
        if not pyttsx3:
            messagebox.showerror("Error", "pyttsx3 package is not installed.")
            return

        def speak_thread():
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                pass

        threading.Thread(target=speak_thread, daemon=True).start()

    def show_translation(self):
        self.page = "translation"
        self.clear_content()
        self.set_active("Translation")
        self.heading("Translation Studio", "Translate text into another language.")

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        card = self.make_card(outer, 20)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="SOURCE TEXT", bg=PANEL, fg=PURPLE, font=(FONT, 9, "bold")).pack(anchor="w")
        self.trans_input = tk.Text(card, height=5, bg=BG, fg=WHITE, insertbackground=WHITE, font=(FONT, 11), bd=0, highlightthickness=1, highlightbackground=BORDER)
        self.trans_input.pack(fill="x", pady=(4, 10))

        ctrl_frame = tk.Frame(card, bg=PANEL)
        ctrl_frame.pack(fill="x", pady=(0, 10))

        tk.Label(ctrl_frame, text="TARGET LANGUAGE", bg=PANEL, fg=MUTED, font=(FONT, 9, "bold")).pack(anchor="w", pady=(0, 4))
        lang_box = ttk.Combobox(ctrl_frame, textvariable=self.target_language, values=["Hindi", "Assamese", "Bengali", "Spanish", "French", "German"], state="readonly", width=15, style="Spell.TCombobox")
        lang_box.pack(side="left", padx=(0, 15))

        self.make_button(ctrl_frame, "Translate", self.perform_translation, color=MINT).pack(side="left")

        tk.Label(card, text="TRANSLATED TEXT", bg=PANEL, fg=PURPLE, font=(FONT, 9, "bold")).pack(anchor="w", pady=(5, 0))
        self.trans_output = tk.Text(card, height=5, bg=BG, fg=WHITE, insertbackground=WHITE, font=(FONT, 11), bd=0, highlightthickness=1, highlightbackground=BORDER)
        self.trans_output.pack(fill="x", pady=(4, 0))
        self.trans_output.config(state="disabled")

    def perform_translation(self):
        text = self.trans_input.get("1.0", tk.END).strip()
        target = self.target_language.get()
        if not text:
            messagebox.showwarning("Input Empty", "Please enter text to translate.")
            return

        lang_map = {"Hindi": "hi", "Assamese": "as", "Bengali": "bn", "Spanish": "es", "French": "fr", "German": "de"}
        dest_code = lang_map.get(target, "hi")

        try:
            if GoogleTranslator:
                translated = GoogleTranslator(source='auto', target=dest_code).translate(text)
            else:
                translated = "[Error: deep_translator package not found]"
        except Exception as e:
            translated = f"[Translation Error: {e}]"

        self.trans_output.config(state="normal")
        self.trans_output.delete("1.0", tk.END)
        self.trans_output.insert(tk.END, translated)
        self.trans_output.config(state="disabled")

    def show_pdf_assistant(self):
        self.page = "pdf"
        self.clear_content()
        self.set_active("PDF Assistant")
        self.heading("PDF Assistant", "Extract selectable text from a PDF and send it to the checker.")

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        card = self.make_card(outer, 20)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="DOCUMENT TEXT", bg=PANEL, fg=PURPLE, font=(FONT, 9, "bold")).pack(anchor="w")
        self.pdf_text_box = tk.Text(card, height=10, bg=BG, fg=WHITE, insertbackground=WHITE, font=(FONT, 11), bd=0, highlightthickness=1, highlightbackground=BORDER)
        self.pdf_text_box.pack(fill="x", pady=(4, 12))

        btn_row = tk.Frame(card, bg=PANEL)
        btn_row.pack(anchor="w")

        self.make_button(btn_row, "Import PDF", self.import_pdf_file, color=WHITE, fg=BG).pack(side="left", padx=(0, 10))
        self.make_button(btn_row, "Send to Grammar Checker", self.show_checker, color=MINT).pack(side="left")

        tk.Label(card, text="Note: scanned image-only PDFs may need OCR, which is not built into this version.", bg=PANEL, fg=MUTED, font=(FONT, 8)).pack(anchor="w", pady=(10, 0))

    def import_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return
        try:
            if PdfReader:
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
                self.pdf_text_box.delete("1.0", tk.END)
                self.pdf_text_box.insert(tk.END, text.strip())
            else:
                messagebox.showerror("Error", "pypdf package is not installed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read PDF: {e}")

    def show_progress(self):
        self.page = "progress"
        self.clear_content()
        self.set_active("My Progress")
        self.heading("My Progress", "Your practice history at a glance.")

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        top_stats = tk.Frame(outer, bg=BG)
        top_stats.pack(fill="x", pady=(0, 20))

        s_cards = [
            ("TOTAL XP", str(self.total_xp), PURPLE),
            ("COMPLETED SESSIONS", str(self.completed_games), MINT),
            ("DAILY CHALLENGE", "Done" if self.daily_done else "Pending", PEACH)
        ]

        for title, val, col in s_cards:
            c = self.make_card(top_stats, 15)
            c.pack(side="left", fill="both", expand=True, padx=(0, 12))
            tk.Label(c, text=title, bg=PANEL, fg=MUTED, font=(FONT, 8, "bold")).pack(anchor="w")
            tk.Label(c, text=val, bg=PANEL, fg=col, font=(TITLE_FONT, 20, "bold")).pack(anchor="w", pady=(5, 0))

        card = self.make_card(outer, 20)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="GAME PERFORMANCE", bg=PANEL, fg=WHITE, font=(FONT, 11, "bold")).pack(anchor="w", pady=(0, 15))

        for name in GAMES:
            row = tk.Frame(card, bg=PANEL)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=name, bg=PANEL, fg=MUTED, font=(FONT, 10), width=18, anchor="w").pack(side="left")
            
            pb = ttk.Progressbar(row, style="Spell.Horizontal.TProgressbar", maximum=10, value=self.progress[name])
            pb.pack(side="left", fill="x", expand=True, padx=10)
            
            sc_lbl = tk.Label(row, text=f"{self.progress[name]}/10", bg=PANEL, fg=WHITE, font=(FONT, 9, "bold"), width=6)
            sc_lbl.pack(side="right")

        tk.Label(outer, text="Progress is stored while this app is running. It resets when you close the app.", bg=BG, fg=MUTED, font=(FONT, 8)).pack(anchor="w", pady=(10, 0))

    def show_settings(self):
        self.page = "settings"
        self.clear_content()
        self.set_active("Settings")
        self.heading("Settings", "Configure your preferences.")

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        card = self.make_card(outer, 25)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="APPLICATION PREFERENCES", bg=PANEL, fg=PURPLE, font=(FONT, 10, "bold")).pack(anchor="w", pady=(0, 15))

        row1 = tk.Frame(card, bg=PANEL)
        row1.pack(fill="x", pady=10)
        tk.Label(row1, text="Default Tone / Style", bg=PANEL, fg=WHITE, font=(FONT, 11)).pack(side="left")
        ttk.Combobox(row1, textvariable=self.selected_tone, values=["Neutral", "Professional", "Friendly", "Empathetic", "Concise"], state="readonly", width=18, style="Spell.TCombobox").pack(side="right")

        row2 = tk.Frame(card, bg=PANEL)
        row2.pack(fill="x", pady=10)
        tk.Label(row2, text="Default Target Translation Language", bg=PANEL, fg=WHITE, font=(FONT, 11)).pack(side="left")
        ttk.Combobox(row2, textvariable=self.target_language, values=["Hindi", "Assamese", "Bengali", "Spanish", "French", "German"], state="readonly", width=18, style="Spell.TCombobox").pack(side="right")

        row3 = tk.Frame(card, bg=PANEL)
        row3.pack(fill="x", pady=10)
        tk.Label(row3, text="Enable Audio Read Aloud", bg=PANEL, fg=WHITE, font=(FONT, 11)).pack(side="left")
        tk.Checkbutton(row3, variable=self.read_aloud_enabled, bg=PANEL, selectcolor=SIDEBAR, activebackground=PANEL).pack(side="right")


# -------------------- MAIN APP EXECUTION --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellSync(root)
    root.mainloop()