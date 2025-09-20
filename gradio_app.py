import gradio as gr
import json
from wordle_game import WordleGame
from ai_tutor import AITutor

class WordleTutorApp:
    def __init__(self):
        self.game = WordleGame()
        self.tutor = AITutor()
        self.game_history = []
        self.tutor_messages = []
    
    def start_new_game(self):
        """Start a new game"""
        self.game.reset_game()
        self.game_history = []
        self.tutor_messages = []
        
        # Get initial tutor suggestion
        initial_suggestion = self.tutor.get_suggestion(self.game)
        self.tutor_messages.append(("🤖 AI Tutor", initial_suggestion))
        
        return (
            self._create_game_board(),
            self._format_tutor_messages(),
            "",  # Clear input
            "🎮 New game started! Make your first guess.",
            gr.update(interactive=True)  # Enable input
        )
    
    def make_guess(self, guess_input):
        """Process a guess from the user"""
        if not guess_input or not guess_input.strip():
            return (
                self._create_game_board(),
                self._format_tutor_messages(),
                guess_input,
                "⚠️ Please enter a 5-letter word.",
                gr.update(interactive=True)
            )
        
        # Make the guess
        success, result = self.game.make_guess(guess_input)
        
        if not success:
            error_msg = result.get("error", "Invalid guess")
            return (
                self._create_game_board(),
                self._format_tutor_messages(),
                guess_input,
                f"❌ {error_msg}",
                gr.update(interactive=True)
            )
        
        # Add to game history
        self.game_history.append(result)
        
        # Get tutor analysis of the guess
        analysis = self.tutor.analyze_guess(self.game, result)
        if analysis:
            self.tutor_messages.append(("📊 Analysis", analysis))
        
        # Get next suggestion or final analysis
        if result["game_over"]:
            final_analysis = self.tutor.get_final_analysis(self.game)
            self.tutor_messages.append(("🏁 Final Analysis", final_analysis))
            
            if result["won"]:
                status_msg = f"🎉 Congratulations! You found the word '{result['target_word']}' in {result['attempt']} attempts!"
            else:
                status_msg = f"😔 Game over! The word was '{result['target_word']}'. Better luck next time!"
            
            input_interactive = False
        else:
            next_suggestion = self.tutor.get_suggestion(self.game)
            self.tutor_messages.append(("💡 Next Move", next_suggestion))
            status_msg = f"Attempt {result['attempt']}/{self.game.max_attempts} complete. {self.game.max_attempts - result['attempt']} attempts remaining."
            input_interactive = True
        
        return (
            self._create_game_board(),
            self._format_tutor_messages(),
            "",  # Clear input
            status_msg,
            gr.update(interactive=input_interactive)
        )
    
    def _create_game_board(self):
        """Create the visual game board"""
        board_html = """
        <div style="font-family: Arial, sans-serif; max-width: 400px; margin: 0 auto;">
            <style>
                .wordle-grid {
                    display: grid;
                    grid-template-rows: repeat(6, 1fr);
                    gap: 5px;
                    margin: 20px 0;
                }
                .wordle-row {
                    display: grid;
                    grid-template-columns: repeat(5, 1fr);
                    gap: 5px;
                }
                .wordle-cell {
                    width: 60px;
                    height: 60px;
                    border: 2px solid #d3d6da;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    font-weight: bold;
                    text-transform: uppercase;
                    background-color: white;
                }
                .correct {
                    background-color: #6aaa64 !important;
                    color: white;
                    border-color: #6aaa64;
                }
                .wrong-position {
                    background-color: #c9b458 !important;
                    color: white;
                    border-color: #c9b458;
                }
                .not-in-word {
                    background-color: #787c7e !important;
                    color: white;
                    border-color: #787c7e;
                }
                .filled {
                    border-color: #878a8c;
                }
            </style>
            <div class="wordle-grid">
        """
        
        for row in range(6):
            board_html += '<div class="wordle-row">'
            
            if row < len(self.game_history):
                # Filled row with guess
                guess_info = self.game_history[row]
                word = guess_info["guess"]
                feedback = guess_info["feedback"]
                
                for i in range(5):
                    letter = word[i] if i < len(word) else ""
                    css_class = feedback[i] if i < len(feedback) else ""
                    css_class = css_class.replace("_", "-")  # Convert to CSS class name
                    
                    board_html += f'<div class="wordle-cell {css_class}">{letter}</div>'
            else:
                # Empty row
                for _ in range(5):
                    board_html += '<div class="wordle-cell"></div>'
            
            board_html += '</div>'
        
        board_html += """
            </div>
        </div>
        """
        
        return board_html
    
    def _format_tutor_messages(self):
        """Format tutor messages for display"""
        if not self.tutor_messages:
            return "🤖 **AI Tutor**: Ready to help you solve Wordle! Click 'New Game' to start."
        
        formatted_messages = []
        for sender, message in self.tutor_messages[-5:]:  # Show last 5 messages
            formatted_messages.append(f"**{sender}**:\n{message}\n")
        
        return "\n---\n".join(formatted_messages)
    
    def create_interface(self):
        """Create the Gradio interface"""
        with gr.Blocks(title="Wordle Tutor", theme=gr.themes.Soft()) as interface:
            gr.Markdown("""
            # 🎯 Wordle Tutor
            
            **Play Wordle with AI assistance!** 
            
            Guess the 5-letter word in 6 attempts. The AI tutor will provide hints and analysis to help you improve your strategy.
            
            **Color coding:**
            - 🟢 **Green**: Correct letter in correct position
            - 🟡 **Yellow**: Correct letter in wrong position  
            - ⬜ **Gray**: Letter not in the word
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("## 🎮 Game Board")
                    game_board = gr.HTML(self._create_game_board())
                    
                    with gr.Row():
                        guess_input = gr.Textbox(
                            label="Your Guess",
                            placeholder="Enter a 5-letter word...",
                            max_lines=1,
                            interactive=False
                        )
                        guess_btn = gr.Button("Submit Guess", variant="primary")
                    
                    new_game_btn = gr.Button("🆕 New Game", variant="secondary")
                    status_msg = gr.Textbox(
                        label="Status",
                        value="Click 'New Game' to start playing!",
                        interactive=False
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("## 🤖 AI Tutor")
                    tutor_output = gr.Markdown(
                        self._format_tutor_messages(),
                        elem_classes="tutor-panel"
                    )
            
            # Event handlers
            new_game_btn.click(
                fn=self.start_new_game,
                outputs=[game_board, tutor_output, guess_input, status_msg, guess_input]
            )
            
            guess_btn.click(
                fn=self.make_guess,
                inputs=[guess_input],
                outputs=[game_board, tutor_output, guess_input, status_msg, guess_input]
            )
            
            guess_input.submit(
                fn=self.make_guess,
                inputs=[guess_input],
                outputs=[game_board, tutor_output, guess_input, status_msg, guess_input]
            )
            
            # Add custom CSS
            interface.css = """
            .tutor-panel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
                max-height: 500px;
                overflow-y: auto;
                font-size: 14px;
            }
            """
        
        return interface

def main():
    app = WordleTutorApp()
    interface = app.create_interface()
    
    print("🎯 Starting Wordle Tutor...")
    print("🤖 AI-powered Wordle game with hints and analysis")
    print("🌐 Open your browser and navigate to the provided URL")
    
    interface.launch(
        share=False,
        debug=True,
        show_error=True
    )

if __name__ == "__main__":
    main()