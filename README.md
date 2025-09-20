# Wordle-Tutor
RLFT AI Tutor for Wordle

## 🎯 Overview

Wordle-Tutor is an interactive Gradio application that lets you play Wordle while receiving AI-powered hints and strategy guidance. The app features a complete Wordle game implementation with visual feedback and an intelligent tutor that analyzes your moves and provides strategic suggestions.

## ✨ Features

### 🎮 Core Game Features
- **Complete Wordle Game**: Guess a 5-letter word in 6 attempts
- **Visual Game Board**: HTML/CSS grid with color-coded feedback
  - 🟢 Green: Correct letter in correct position
  - 🟡 Yellow: Correct letter in wrong position
  - ⬜ Gray: Letter not in the word
- **Word Validation**: Only accepts valid 5-letter words from built-in dictionary
- **Game State Management**: Tracks attempts, detects wins/losses

### 🤖 AI Tutor Features
- **Opening Strategy**: Suggests optimal starting words
- **Move Analysis**: Analyzes each guess and provides feedback
- **Progressive Hints**: Adapts suggestions based on game progress
- **Pattern Recognition**: Identifies letter patterns and frequencies
- **Final Analysis**: Comprehensive game review at the end

### 🧠 Model Training Component
- **Strategy Simulation**: Tests different playing strategies
- **Performance Analysis**: Compares strategy effectiveness
- **Pattern Extraction**: Identifies successful word patterns
- **Data Generation**: Creates training data for future ML models

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sameersegal/Wordle-Tutor.git
   cd Wordle-Tutor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Gradio app**:
   ```bash
   python gradio_app.py
   ```

4. **Open your browser** and navigate to the provided URL (typically `http://127.0.0.1:7860`)

## 🎯 How to Play

1. **Start a New Game**: Click the "🆕 New Game" button
2. **Get AI Guidance**: Read the initial strategy suggestions in the AI Tutor panel
3. **Make Your Guess**: Enter a 5-letter word in the input box
4. **Analyze Results**: Review the color-coded feedback and AI analysis
5. **Continue Playing**: Use the AI hints to improve your next guess
6. **Learn and Improve**: Review the final analysis to enhance your Wordle skills

## 🔧 Components

### `gradio_app.py`
Main application file containing the Gradio interface and game orchestration.

### `wordle_game.py`
Core Wordle game logic including:
- Game state management
- Word validation
- Feedback calculation
- Win/loss detection

### `ai_tutor.py`
AI tutor implementation featuring:
- Strategic suggestions
- Move analysis
- Pattern recognition
- Adaptive hints

### `model_training.py`
Model training recipe including:
- Game simulation
- Strategy comparison
- Data generation
- Performance analysis

## 🎲 AI Strategies

The AI tutor uses several strategic approaches:

### Opening Strategy
- Recommends vowel-rich words like AUDIO, ABOUT, AROSE
- Avoids repeated letters in early guesses
- Prioritizes common letter combinations

### Mid-Game Analysis
- Tracks correct and misplaced letters
- Suggests word patterns based on known information
- Provides position-specific guidance

### Advanced Tactics
- Considers letter frequency in English
- Analyzes common word endings (-ER, -ED, -ING)
- Adapts difficulty based on remaining attempts

## 📊 Model Training

Run the training pipeline to analyze different strategies:

```bash
python model_training.py
```

This will:
1. Simulate 200 games using different strategies
2. Analyze win rates and average attempts
3. Identify top-performing opening words
4. Save training data to `wordle_model_data.json`

## 🛠️ Customization

### Adding New Words
Edit the `word_list` in `wordle_game.py` to add new valid words.

### Modifying AI Strategies
Update the suggestion methods in `ai_tutor.py` to implement new hint strategies.

### Training New Models
Use the generated data from `model_training.py` to train machine learning models for improved gameplay.

## 🔮 Future Enhancements

- **Deep Learning Models**: Train neural networks on gameplay data
- **Reinforcement Learning**: Implement Q-learning for optimal strategies
- **Multiplayer Mode**: Add competitive Wordle gameplay
- **Difficulty Levels**: Implement word lists of varying difficulty
- **Statistics Tracking**: Personal gameplay analytics and improvement tracking

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Wordle game concept by Josh Wardle
- Built with [Gradio](https://gradio.app/) for the web interface
- Uses common English word lists for validation
