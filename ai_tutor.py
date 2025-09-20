import random
from typing import List, Dict, Set
from wordle_game import WordleGame

class AITutor:
    def __init__(self):
        self.word_patterns = self._load_common_patterns()
        self.strategy_tips = [
            "Start with words containing common vowels (A, E, I, O, U)",
            "Use words with common consonants like R, S, T, L, N",
            "Avoid repeating letters in early guesses to gather more information",
            "Pay attention to letter frequency in English words",
            "Consider word endings like -ING, -ED, -ER, -LY"
        ]
    
    def _load_common_patterns(self) -> Dict:
        """Load common letter patterns and frequencies"""
        return {
            "common_starts": ["TH", "ST", "SP", "SC", "SH", "PR", "PL", "FL", "FR", "BR", "CR", "DR", "GR", "TR"],
            "common_ends": ["ER", "ED", "ING", "ION", "LY", "AL", "IC", "LE", "TH", "ES"],
            "common_vowels": ["E", "A", "I", "O", "U"],
            "common_consonants": ["R", "S", "T", "L", "N", "D"],
            "frequent_letters": ["E", "T", "A", "O", "I", "N", "S", "H", "R", "D", "L", "U"]
        }
    
    def get_suggestion(self, game: WordleGame) -> str:
        """Get AI tutor suggestion based on current game state"""
        game_state = game.get_game_state()
        letters_info = game.get_letters_info()
        attempt_number = len(game_state["guesses"])
        
        if attempt_number == 0:
            return self._get_opening_suggestion()
        elif attempt_number == 1:
            return self._get_second_guess_suggestion(game_state, letters_info)
        else:
            return self._get_advanced_suggestion(game_state, letters_info)
    
    def _get_opening_suggestion(self) -> str:
        """Suggest opening strategy"""
        suggestions = [
            "💡 **Opening Strategy**: Start with a word that has common vowels and consonants.",
            "🎯 **Recommended starters**: ADIEU, AUDIO, AROSE, STONE, SLATE",
            "📊 **Why**: These words help you discover the most common letters quickly.",
            "✨ **Tip**: Avoid words with repeated letters for your first guess!"
        ]
        return "\n".join(suggestions)
    
    def _get_second_guess_suggestion(self, game_state: Dict, letters_info: Dict) -> str:
        """Suggest strategy for second guess"""
        last_guess = game_state["guesses"][-1]
        feedback = last_guess["feedback"]
        
        suggestions = ["💡 **Second Guess Strategy**:"]
        
        # Count how many letters were found
        correct_count = feedback.count("correct")
        wrong_pos_count = feedback.count("wrong_position")
        
        if correct_count > 0:
            suggestions.append(f"✅ Great! You found {correct_count} correct letter(s) in the right position.")
        
        if wrong_pos_count > 0:
            suggestions.append(f"🔄 You found {wrong_pos_count} correct letter(s) in wrong positions.")
        
        if correct_count + wrong_pos_count == 0:
            suggestions.append("🔍 None of those letters are in the target word. Try completely different letters.")
            suggestions.append("💭 Consider: BLURT, CHAMP, FLING, WHISK")
        else:
            suggestions.append("🎯 Build on what you've learned - use the correct letters and try new positions for the yellow ones.")
        
        # Add specific letter guidance
        if letters_info["correct"]:
            suggestions.append(f"🟢 Keep these letters in their positions: {', '.join(letters_info['correct'])}")
        
        if letters_info["wrong_position"]:
            suggestions.append(f"🟡 Move these letters to different positions: {', '.join(letters_info['wrong_position'])}")
        
        if letters_info["not_in_word"]:
            suggestions.append(f"❌ Avoid these letters: {', '.join(letters_info['not_in_word'])}")
        
        return "\n".join(suggestions)
    
    def _get_advanced_suggestion(self, game_state: Dict, letters_info: Dict) -> str:
        """Suggest advanced strategies for later guesses"""
        attempt_number = len(game_state["guesses"])
        
        suggestions = [f"💡 **Attempt {attempt_number + 1} Strategy**:"]
        
        # Analyze what we know
        known_letters = letters_info["correct"] | letters_info["wrong_position"]
        
        if len(known_letters) >= 3:
            suggestions.append("🎯 You have good information! Focus on arranging known letters correctly.")
            suggestions.append("💭 Think about common word patterns and letter combinations.")
        elif len(known_letters) >= 1:
            suggestions.append("🔍 You're making progress! Try to find more letters while using what you know.")
        else:
            suggestions.append("🆘 Consider trying completely different letters - you might be missing common ones.")
        
        # Add pressure/encouragement based on attempts left
        attempts_left = game_state["attempts_left"]
        if attempts_left <= 2:
            suggestions.append(f"⏰ Only {attempts_left} attempts left! Think carefully about word patterns.")
            if known_letters:
                suggestions.append("🎲 Consider all possible arrangements of your known letters.")
        elif attempts_left == 3:
            suggestions.append("⚠️ Getting close to the end - make each guess count!")
        
        # Pattern suggestions
        if len(known_letters) >= 2:
            suggestions.append("📚 **Common patterns to consider:**")
            if "E" in known_letters:
                suggestions.append("   • Words ending in -ER, -ED, -LE")
            if "S" in known_letters:
                suggestions.append("   • Words starting with S-, or ending in -S")
            if "T" in known_letters:
                suggestions.append("   • Words with -TH-, -ST-, or -NT-")
        
        return "\n".join(suggestions)
    
    def analyze_guess(self, game: WordleGame, guess_result: Dict) -> str:
        """Analyze the result of a guess and provide feedback"""
        if not guess_result or "feedback" not in guess_result:
            return ""
        
        feedback = guess_result["feedback"]
        word = guess_result["guess"]
        
        analysis = ["🔍 **Guess Analysis**:"]
        
        correct_positions = []
        wrong_positions = []
        not_in_word = []
        
        for i, (letter, fb) in enumerate(zip(word, feedback)):
            if fb == "correct":
                correct_positions.append(f"{letter} (position {i+1})")
            elif fb == "wrong_position":
                wrong_positions.append(f"{letter} (not position {i+1})")
            elif fb == "not_in_word":
                not_in_word.append(letter)
        
        if correct_positions:
            analysis.append(f"🟢 **Correct positions**: {', '.join(correct_positions)}")
        
        if wrong_positions:
            analysis.append(f"🟡 **Wrong positions**: {', '.join(wrong_positions)}")
        
        if not_in_word:
            analysis.append(f"❌ **Not in word**: {', '.join(not_in_word)}")
        
        # Add strategic insight
        if feedback.count("correct") >= 2:
            analysis.append("💪 Excellent! You're getting close to the solution.")
        elif feedback.count("correct") + feedback.count("wrong_position") >= 3:
            analysis.append("🎯 Good progress! Focus on rearranging the letters you've found.")
        elif feedback.count("correct") + feedback.count("wrong_position") == 0:
            analysis.append("🔄 Time to try completely different letters!")
        
        return "\n".join(analysis)
    
    def get_final_analysis(self, game: WordleGame) -> str:
        """Provide final analysis when game ends"""
        game_state = game.get_game_state()
        
        if game_state["won"]:
            attempts = len(game_state["guesses"])
            analysis = [f"🎉 **Congratulations!** You solved it in {attempts} attempts!"]
            
            if attempts <= 3:
                analysis.append("⭐ **Excellent performance!** You're a Wordle master!")
            elif attempts <= 4:
                analysis.append("👍 **Great job!** Very solid solving skills.")
            elif attempts <= 5:
                analysis.append("✅ **Well done!** You got there in the end.")
            else:
                analysis.append("😅 **Phew!** That was close, but you made it!")
        else:
            target_word = game_state["target_word"]
            analysis = [f"😔 **Game Over!** The word was: **{target_word}**"]
            analysis.append("💪 Don't worry - every game teaches you something new!")
            analysis.append("🎯 **Next time**: Try starting with words containing common vowels and consonants.")
        
        # Add some learning points
        analysis.append("\n📚 **What you learned this game**:")
        letters_info = game.get_letters_info()
        
        if letters_info["correct"]:
            analysis.append(f"✅ Letters you correctly identified: {', '.join(letters_info['correct'])}")
        
        if letters_info["wrong_position"]:
            analysis.append(f"🟡 Letters you found but misplaced: {', '.join(letters_info['wrong_position'])}")
        
        analysis.append(f"📊 Total letters tried: {len(letters_info['tried'])}")
        
        return "\n".join(analysis)
    
    def get_random_tip(self) -> str:
        """Get a random strategy tip"""
        return f"💡 **Tip**: {random.choice(self.strategy_tips)}"