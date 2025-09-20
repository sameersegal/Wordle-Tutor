"""
Simple Wordle AI Model Training Recipe

This script demonstrates a basic approach to training an AI model for Wordle strategy.
In a production environment, this would involve:
1. Collecting game data from human players
2. Training reinforcement learning or supervised models
3. Evaluating strategy effectiveness

For now, this provides a foundation for future ML integration.
"""

import json
import random
from typing import List, Dict, Tuple
from wordle_game import WordleGame
from ai_tutor import AITutor

class WordleDataGenerator:
    """Generate training data from simulated Wordle games"""
    
    def __init__(self):
        self.game = WordleGame()
        self.tutor = AITutor()
    
    def simulate_game(self, strategy: str = "random") -> Dict:
        """Simulate a single game and return game data"""
        self.game.reset_game()
        target_word = self.game.target_word
        
        game_data = {
            "target_word": target_word,
            "strategy": strategy,
            "guesses": [],
            "won": False,
            "attempts": 0
        }
        
        for attempt in range(6):
            if strategy == "random":
                guess = self._random_guess()
            elif strategy == "vowel_first":
                guess = self._vowel_first_strategy(attempt)
            elif strategy == "frequency_based":
                guess = self._frequency_based_strategy(attempt)
            else:
                guess = self._random_guess()
            
            success, result = self.game.make_guess(guess)
            
            if success:
                game_data["guesses"].append({
                    "attempt": attempt + 1,
                    "guess": guess,
                    "feedback": result["feedback"],
                    "letters_info": self.game.get_letters_info()
                })
                
                if result["won"]:
                    game_data["won"] = True
                    game_data["attempts"] = attempt + 1
                    break
                
                if result["game_over"]:
                    game_data["attempts"] = 6
                    break
        
        return game_data
    
    def _random_guess(self) -> str:
        """Make a random valid guess"""
        return random.choice(self.game.word_list)
    
    def _vowel_first_strategy(self, attempt: int) -> str:
        """Strategy that prioritizes vowels early"""
        if attempt == 0:
            # Start with vowel-heavy words
            vowel_words = ["AUDIO", "ARISE", "ABOUT"]
            valid_vowel_words = [w for w in vowel_words if w in self.game.word_list]
            if valid_vowel_words:
                return random.choice(valid_vowel_words)
            else:
                return self._random_guess()
        else:
            # Use available information to make informed guesses
            return self._frequency_based_strategy(attempt)
    
    def _frequency_based_strategy(self, attempt: int) -> str:
        """Strategy based on letter frequency"""
        letters_info = self.game.get_letters_info()
        
        # Filter words based on what we know
        valid_words = []
        for word in self.game.word_list:
            # Skip words with letters we know are not in the target
            if any(letter in word for letter in letters_info.get("not_in_word", set())):
                continue
            
            # Must contain letters we know are in the word
            known_letters = letters_info.get("correct", set()) | letters_info.get("wrong_position", set())
            if not all(letter in word for letter in known_letters):
                continue
            
            valid_words.append(word)
        
        if valid_words:
            return random.choice(valid_words)
        else:
            return self._random_guess()
    
    def generate_training_data(self, num_games: int = 100, strategies: List[str] = None) -> List[Dict]:
        """Generate training data from multiple simulated games"""
        if strategies is None:
            strategies = ["random", "vowel_first", "frequency_based"]
        
        training_data = []
        
        for i in range(num_games):
            strategy = random.choice(strategies)
            game_data = self.simulate_game(strategy)
            training_data.append(game_data)
            
            if (i + 1) % 20 == 0:
                print(f"Generated {i + 1}/{num_games} games...")
        
        return training_data

class WordleModelTrainer:
    """Basic framework for training Wordle AI models"""
    
    def __init__(self):
        self.training_data = []
    
    def load_data(self, data: List[Dict]):
        """Load training data"""
        self.training_data = data
    
    def analyze_strategies(self) -> Dict:
        """Analyze effectiveness of different strategies"""
        strategy_stats = {}
        
        for game in self.training_data:
            strategy = game["strategy"]
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {
                    "games": 0,
                    "wins": 0,
                    "total_attempts": 0,
                    "win_rate": 0.0,
                    "avg_attempts": 0.0
                }
            
            stats = strategy_stats[strategy]
            stats["games"] += 1
            if game["won"]:
                stats["wins"] += 1
                stats["total_attempts"] += game["attempts"]
        
        # Calculate averages
        for strategy, stats in strategy_stats.items():
            if stats["games"] > 0:
                stats["win_rate"] = stats["wins"] / stats["games"]
                if stats["wins"] > 0:
                    stats["avg_attempts"] = stats["total_attempts"] / stats["wins"]
        
        return strategy_stats
    
    def extract_patterns(self) -> Dict:
        """Extract patterns from successful games"""
        patterns = {
            "best_openers": {},
            "effective_sequences": [],
            "letter_frequency": {}
        }
        
        # Analyze opening moves
        for game in self.training_data:
            if game["won"] and game["guesses"]:
                opener = game["guesses"][0]["guess"]
                if opener not in patterns["best_openers"]:
                    patterns["best_openers"][opener] = {"count": 0, "success_rate": 0}
                patterns["best_openers"][opener]["count"] += 1
        
        # Calculate success rates for openers
        opener_totals = {}
        for game in self.training_data:
            if game["guesses"]:
                opener = game["guesses"][0]["guess"]
                if opener not in opener_totals:
                    opener_totals[opener] = 0
                opener_totals[opener] += 1
        
        for opener, stats in patterns["best_openers"].items():
            if opener in opener_totals:
                stats["success_rate"] = stats["count"] / opener_totals[opener]
        
        return patterns
    
    def save_model_data(self, filename: str = "wordle_model_data.json"):
        """Save analyzed data for future model training"""
        # Convert sets to lists for JSON serialization
        def convert_sets_to_lists(obj):
            if isinstance(obj, dict):
                return {k: convert_sets_to_lists(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_sets_to_lists(item) for item in obj]
            elif isinstance(obj, set):
                return list(obj)
            else:
                return obj
        
        model_data = {
            "training_data": convert_sets_to_lists(self.training_data),
            "strategy_analysis": self.analyze_strategies(),
            "patterns": self.extract_patterns()
        }
        
        with open(filename, 'w') as f:
            json.dump(model_data, f, indent=2)
        
        print(f"Model data saved to {filename}")

def main():
    """Main training pipeline"""
    print("🤖 Wordle AI Model Training Recipe")
    print("==================================")
    
    # Generate training data
    print("\n📊 Generating training data...")
    data_generator = WordleDataGenerator()
    training_data = data_generator.generate_training_data(num_games=200)
    
    # Analyze the data
    print("\n🔍 Analyzing strategies...")
    trainer = WordleModelTrainer()
    trainer.load_data(training_data)
    
    strategy_stats = trainer.analyze_strategies()
    print("\nStrategy Performance:")
    for strategy, stats in strategy_stats.items():
        print(f"  {strategy}:")
        print(f"    Win Rate: {stats['win_rate']:.2%}")
        print(f"    Avg Attempts (when won): {stats['avg_attempts']:.1f}")
        print(f"    Games Played: {stats['games']}")
    
    # Extract patterns
    patterns = trainer.extract_patterns()
    print(f"\n📈 Found {len(patterns['best_openers'])} unique opening words")
    
    # Show top openers
    top_openers = sorted(patterns['best_openers'].items(), 
                        key=lambda x: x[1]['success_rate'], reverse=True)[:5]
    print("\nTop Opening Words:")
    for word, stats in top_openers:
        print(f"  {word}: {stats['success_rate']:.2%} success rate ({stats['count']} wins)")
    
    # Save the model data
    print("\n💾 Saving model data...")
    trainer.save_model_data()
    
    print("\n✅ Training recipe complete!")
    print("\n🔮 Next steps for production ML model:")
    print("  1. Collect real human game data")
    print("  2. Implement reinforcement learning (e.g., Q-learning)")
    print("  3. Train neural networks on game sequences")
    print("  4. Evaluate against human players")
    print("  5. Deploy model in production app")

if __name__ == "__main__":
    main()