import random
from typing import List, Tuple, Dict

class WordleGame:
    def __init__(self):
        self.word_list = self._load_word_list()
        self.target_word = ""
        self.guesses = []
        self.max_attempts = 6
        self.game_over = False
        self.won = False
        self.reset_game()
    
    def _load_word_list(self) -> List[str]:
        """Load a list of valid 5-letter words"""
        # For now, using a basic word list. In production, this would load from a file
        words = [
            "ABOUT", "ABOVE", "ABUSE", "ACTOR", "ACUTE", "ADMIT", "ADOPT", "ADULT", "AFTER", "AGAIN",
            "AGENT", "AGREE", "AHEAD", "ALARM", "ALBUM", "ALERT", "ALIEN", "ALIGN", "ALIKE", "ALIVE",
            "ALLOW", "ALONE", "ALONG", "ALTER", "AMONG", "ANGER", "ANGLE", "ANGRY", "APART", "APPLE",
            "APPLY", "ARENA", "ARGUE", "ARISE", "ARRAY", "ASIDE", "ASSET", "AUDIO", "AUDIT", "AVOID",
            "AWARD", "AWARE", "BADLY", "BAKER", "BASES", "BASIC", "BEACH", "BEGAN", "BEGIN", "BEING",
            "BELOW", "BENCH", "BILLY", "BIRTH", "BLACK", "BLAME", "BLANK", "BLIND", "BLOCK", "BLOOD",
            "BOARD", "BOOST", "BOOTH", "BOUND", "BRAIN", "BRAND", "BRASS", "BRAVE", "BREAD", "BREAK",
            "BREED", "BRIEF", "BRING", "BROAD", "BROKE", "BROWN", "BUILD", "BUILT", "BUYER", "CABLE",
            "CALIF", "CARRY", "CATCH", "CAUSE", "CHAIN", "CHAIR", "CHAOS", "CHARM", "CHART", "CHASE",
            "CHEAP", "CHECK", "CHEST", "CHIEF", "CHILD", "CHINA", "CHOSE", "CIVIL", "CLAIM", "CLASS",
            "CLEAN", "CLEAR", "CLICK", "CLIMB", "CLOCK", "CLOSE", "CLOUD", "COACH", "COAST", "COULD",
            "COUNT", "COURT", "COVER", "CRAFT", "CRASH", "CRAZY", "CREAM", "CRIME", "CROSS", "CROWD",
            "CROWN", "CRUDE", "CURVE", "CYCLE", "DAILY", "DANCE", "DATED", "DEALT", "DEATH", "DEBUT",
            "DELAY", "DEPTH", "DOING", "DOUBT", "DOZEN", "DRAFT", "DRAMA", "DRANK", "DRAWN", "DREAM",
            "DRESS", "DRILL", "DRINK", "DRIVE", "DROVE", "DYING", "EAGER", "EARLY", "EARTH", "EIGHT",
            "ELITE", "EMPTY", "ENEMY", "ENJOY", "ENTER", "ENTRY", "EQUAL", "ERROR", "EVENT", "EVERY",
            "EXACT", "EXIST", "EXTRA", "FAITH", "FALSE", "FAULT", "FIBER", "FIELD", "FIFTH", "FIFTY",
            "FIGHT", "FINAL", "FIRST", "FIXED", "FLASH", "FLEET", "FLOOR", "FLUID", "FOCUS", "FORCE",
            "FORTH", "FORTY", "FORUM", "FOUND", "FRAME", "FRANK", "FRAUD", "FRESH", "FRONT", "FRUIT",
            "FULLY", "FUNNY", "GIANT", "GIVEN", "GLASS", "GLOBE", "GOING", "GRACE", "GRADE", "GRAND",
            "GRANT", "GRASS", "GRAVE", "GREAT", "GREEN", "GROSS", "GROUP", "GROWN", "GUARD", "GUESS",
            "GUEST", "GUIDE", "HAPPY", "HARRY", "HEART", "HEAVY", "HENCE", "HENRY", "HORSE", "HOTEL",
            "HOUSE", "HUMAN", "IDEAL", "IMAGE", "INDEX", "INNER", "INPUT", "ISSUE", "JAPAN", "JIMMY",
            "JOINT", "JONES", "JUDGE", "KNOWN", "LABEL", "LARGE", "LASER", "LATER", "LAUGH", "LAYER",
            "LEARN", "LEASE", "LEAST", "LEAVE", "LEGAL", "LEVEL", "LEWIS", "LIGHT", "LIMIT", "LINKS",
            "LIVES", "LOCAL", "LOOSE", "LOWER", "LUCKY", "LUNCH", "LYING", "MAGIC", "MAJOR", "MAKER",
            "MARCH", "MARIA", "MATCH", "MAYBE", "MAYOR", "MEANT", "MEDIA", "METAL", "MIGHT", "MINOR",
            "MINUS", "MIXED", "MODEL", "MONEY", "MONTH", "MORAL", "MOTOR", "MOUNT", "MOUSE", "MOUTH",
            "MOVED", "MOVIE", "MUSIC", "NEEDS", "NEVER", "NEWLY", "NIGHT", "NOISE", "NORTH", "NOTED",
            "NOVEL", "NURSE", "OCCUR", "OCEAN", "OFFER", "OFTEN", "ORDER", "OTHER", "OUGHT", "PAINT",
            "PANEL", "PAPER", "PARTY", "PEACE", "PETER", "PHASE", "PHONE", "PHOTO", "PIANO", "PICKED",
            "PIECE", "PILOT", "PITCH", "PLACE", "PLAIN", "PLANE", "PLANT", "PLATE", "POINT", "POUND",
            "POWER", "PRESS", "PRICE", "PRIDE", "PRIME", "PRINT", "PRIOR", "PRIZE", "PROOF", "PROUD",
            "PROVE", "QUEEN", "QUICK", "QUIET", "QUITE", "RADIO", "RAISE", "RANGE", "RAPID", "RATIO",
            "REACH", "READY", "REALM", "REBEL", "REFER", "RELAX", "REPAY", "REPLY", "RIGHT", "RIVAL",
            "RIVER", "ROBIN", "ROGER", "ROMAN", "ROUGH", "ROUND", "ROUTE", "ROYAL", "RURAL", "SCALE",
            "SCENE", "SCOPE", "SCORE", "SENSE", "SERVE", "SETUP", "SEVEN", "SHALL", "SHAPE", "SHARE",
            "SHARP", "SHEET", "SHELF", "SHELL", "SHIFT", "SHINE", "SHIRT", "SHOCK", "SHOOT", "SHORT",
            "SHOWN", "SIGHT", "SILLY", "SINCE", "SIXTH", "SIXTY", "SIZED", "SKILL", "SLEEP", "SLIDE",
            "SMALL", "SMART", "SMILE", "SMITH", "SMOKE", "SNAKE", "SNOW", "SOLID", "SOLVE", "SORRY",
            "SOUND", "SOUTH", "SPACE", "SPARE", "SPEAK", "SPEED", "SPEND", "SPENT", "SPLIT", "SPOKE",
            "SPORT", "STAFF", "STAGE", "STAKE", "STAND", "START", "STATE", "STEAM", "STEEL", "STICK",
            "STILL", "STOCK", "STONE", "STOOD", "STORE", "STORM", "STORY", "STRIP", "STUCK", "STUDY",
            "STUFF", "STYLE", "SUGAR", "SUITE", "SUPER", "SWEET", "TABLE", "TAKEN", "TASTE", "TAXES",
            "TEACH", "TERRY", "TEXAS", "THANK", "THEFT", "THEIR", "THEME", "THERE", "THESE", "THICK",
            "THING", "THINK", "THIRD", "THOSE", "THREE", "THREW", "THROW", "THUMB", "TIGHT", "TIRED",
            "TITLE", "TODAY", "TOPIC", "TOTAL", "TOUCH", "TOUGH", "TOWER", "TRACK", "TRADE", "TRAIL",
            "TRAIN", "TREAT", "TREND", "TRIAL", "TRIBE", "TRICK", "TRIED", "TRIES", "TRUCK", "TRULY",
            "TRUNK", "TRUST", "TRUTH", "TWICE", "TWIST", "TYLER", "ULTRA", "UNCLE", "UNDER", "UNDUE",
            "UNION", "UNITY", "UNTIL", "UPPER", "UPSET", "URBAN", "USAGE", "USUAL", "VALID", "VALUE",
            "VIDEO", "VIRUS", "VISIT", "VITAL", "VOCAL", "VOICE", "WASTE", "WATCH", "WATER", "WAVE",
            "WAYS", "WEIRD", "WHATEVER", "WHEEL", "WHERE", "WHICH", "WHILE", "WHITE", "WHOLE", "WHOSE",
            "WOMAN", "WOMEN", "WORLD", "WORRY", "WORSE", "WORST", "WORTH", "WOULD", "WRITE", "WRONG",
            "WROTE", "YIELD", "YOUNG", "YOUTH"
        ]
        return words
    
    def reset_game(self):
        """Start a new game"""
        self.target_word = random.choice(self.word_list).upper()
        self.guesses = []
        self.game_over = False
        self.won = False
    
    def is_valid_word(self, word: str) -> bool:
        """Check if a word is valid (5 letters and in word list)"""
        word = word.upper().strip()
        return len(word) == 5 and word.isalpha() and word in self.word_list
    
    def make_guess(self, guess: str) -> Tuple[bool, Dict]:
        """Make a guess and return result"""
        guess = guess.upper().strip()
        
        if self.game_over:
            return False, {"error": "Game is over"}
        
        if len(self.guesses) >= self.max_attempts:
            self.game_over = True
            return False, {"error": "No more attempts left"}
        
        if not self.is_valid_word(guess):
            return False, {"error": "Invalid word. Must be a 5-letter word."}
        
        # Calculate feedback for the guess
        feedback = self._calculate_feedback(guess)
        
        self.guesses.append({
            "word": guess,
            "feedback": feedback
        })
        
        # Check if won
        if guess == self.target_word:
            self.won = True
            self.game_over = True
        
        # Check if out of attempts
        if len(self.guesses) >= self.max_attempts:
            self.game_over = True
        
        return True, {
            "guess": guess,
            "feedback": feedback,
            "attempt": len(self.guesses),
            "game_over": self.game_over,
            "won": self.won,
            "target_word": self.target_word if self.game_over else None
        }
    
    def _calculate_feedback(self, guess: str) -> List[str]:
        """Calculate feedback for each letter in the guess"""
        if len(guess) != 5 or len(self.target_word) != 5:
            return ["not_in_word"] * 5
        
        feedback = []
        target_chars = list(self.target_word)
        guess_chars = list(guess)
        
        # First pass: mark correct positions
        for i in range(5):
            if guess_chars[i] == target_chars[i]:
                feedback.append("correct")
                target_chars[i] = None  # Mark as used
                guess_chars[i] = None   # Mark as processed
            else:
                feedback.append("unknown")
        
        # Second pass: mark wrong positions
        for i in range(5):
            if guess_chars[i] is not None:  # Not processed in first pass
                if guess_chars[i] in target_chars:
                    feedback[i] = "wrong_position"
                    # Remove one occurrence from target_chars
                    target_chars[target_chars.index(guess_chars[i])] = None
                else:
                    feedback[i] = "not_in_word"
        
        return feedback
    
    def get_game_state(self) -> Dict:
        """Get current game state"""
        return {
            "guesses": self.guesses,
            "attempts_left": self.max_attempts - len(self.guesses),
            "game_over": self.game_over,
            "won": self.won,
            "target_word": self.target_word if self.game_over else None
        }
    
    def get_letters_info(self) -> Dict:
        """Get information about which letters have been tried"""
        tried_letters = set()
        correct_letters = set()
        wrong_position_letters = set()
        not_in_word_letters = set()
        
        for guess_info in self.guesses:
            word = guess_info["word"]
            feedback = guess_info["feedback"]
            
            for i, (letter, fb) in enumerate(zip(word, feedback)):
                tried_letters.add(letter)
                if fb == "correct":
                    correct_letters.add(letter)
                elif fb == "wrong_position":
                    wrong_position_letters.add(letter)
                elif fb == "not_in_word":
                    not_in_word_letters.add(letter)
        
        return {
            "tried": tried_letters,
            "correct": correct_letters,
            "wrong_position": wrong_position_letters,
            "not_in_word": not_in_word_letters
        }