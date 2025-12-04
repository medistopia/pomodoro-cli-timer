# 🍅 Pomodoro CLI Timer

A feature-rich command-line Pomodoro technique timer with sound effects and comprehensive productivity tracking. Built with Python using only standard library dependencies (with optional TTS support).

## Features

- ⏱️ **Live Countdown Timer** - Real-time display updates every second
- 🔊 **Sound Preferences** - Choose between system beeps, text-to-speech, or silent mode
- 💾 **Session Tracking** - Automatically saves all completed pomodoros to JSON
- 📊 **Productivity Stats** - View detailed analytics of your focus time
- 📅 **Daily Summaries** - Track today's completed sessions
- 📝 **Session History** - Review your recent work sessions
- 🎯 **Task-Based** - Associate each pomodoro with a specific task

## Installation

### Prerequisites
- Python 3.7+

### Setup
```bash
git clone https://github.com/medistopia/pomodoro-cli-timer.git
cd pomodoro-cli-timer
```

No additional installation required - uses Python standard library!

### Optional: Text-to-Speech
For voice announcements, install the TTS library:
```bash
pip install pyttsx3
```

## Usage

### Start a Pomodoro Session
```bash
python pomodoro.py start "Study Machine Learning"
```

On first start, you'll choose your sound preference:
- **Beeps** - Simple system sounds (works immediately)
- **TTS** - Voice announcements (requires pyttsx3)
- **Silent** - No sound notifications

### View Commands
```bash
# Show today's completed sessions
python pomodoro.py today

# View recent session history
python pomodoro.py history

# See productivity statistics
python pomodoro.py stats

# Display help
python pomodoro.py help
```

## Sample Output

### Starting a Session
```
🔊 Sound Preferences
==================================================
1. Beeps - Simple system beeps
2. TTS - Text-to-speech announcements
3. None - Silent mode

Choose sound mode (1/2/3): 1
✅ Beeps enabled

🎯 Starting Pomodoro for: Study Machine Learning
==================================================

🍅 Work Session - 25 minutes
==================================================
⏱️  24:59 remaining
```

### Productivity Stats
```
📊 Productivity Statistics
==================================================
🍅 Total pomodoros: 47
⏱️  Total focus time: 1175 minutes (19.6 hours)

📅 Active days: 8
📈 Average per active day: 5.9 pomodoros
🏆 Most productive day: 2024-12-02 (12 pomodoros)

🔥 Recent Activity:
   2024-11-28: 🍅🍅🍅 (3)
   2024-11-29: 🍅🍅🍅🍅🍅 (5)
   2024-12-01: 🍅🍅🍅🍅 (4)
   2024-12-02: 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 (12)
```

## How It Works

### The Pomodoro Technique
1. Choose a task to work on
2. Set timer for 25 minutes (1 pomodoro)
3. Work with full focus until timer completes
4. Take a 5-minute break
5. After 4 pomodoros, take a longer 15-30 minute break

### Data Storage
All sessions are saved to `pomodoro_data.json` with the following information:
- Task name
- Date and time
- Duration
- Completion status

### Sound System
- **Beeps Mode**: Uses system beeps with different tones for start, completion, and break end
  - Windows: `winsound` library (built-in)
  - Mac/Linux: System bell via terminal
- **TTS Mode**: Text-to-speech voice announcements
  - Powered by `pyttsx3` library
  - Clear voice prompts for each event

## Project Structure

```
pomodoro-cli-timer/
├── pomodoro.py              # Main application
├── pomodoro_data.json       # Generated session data (not tracked in git)
├── README.md                # This file
└── LICENSE                  # MIT License
```

## Technical Details

### Key Features Implementation

**Live Countdown Display**
- Uses carriage return (`\r`) to update timer on same line
- Formatted time display with leading zeros (MM:SS)
- Non-blocking countdown with `time.sleep(1)`

**Data Persistence**
- JSON file storage for easy human readability
- Automatic session logging after each completion
- Graceful error handling for corrupted data files

**Cross-Platform Sound**
- Platform detection via `platform.system()`
- Windows: `winsound.Beep()` with custom frequencies
- Mac/Linux: System bell via `os.system()`
- Optional TTS with `pyttsx3` library

**Command-Line Interface**
- Argument parsing with `sys.argv`
- Multiple command support (start, today, history, stats)
- Input validation and error messages

## Technologies Used

- **Python 3** - Core programming language
- **JSON** - Data storage format
- **datetime** - Timestamp tracking
- **platform** - OS detection for sound compatibility
- **pyttsx3** - Text-to-speech (optional)

## Code Quality

- ✅ Fully commented and annotated
- ✅ Object-oriented design with `PomodoroTimer` class
- ✅ Error handling for file operations
- ✅ Input validation for user commands
- ✅ Clean separation of concerns (UI, data, logic)

## Future Enhancements

- [ ] Custom session durations via command-line flags
- [ ] Long break automation after 4 pomodoros
- [ ] Weekly/monthly productivity reports
- [ ] Export data to CSV format
- [ ] Task categories and tagging
- [ ] Pause/resume functionality
- [ ] Integration with calendar apps

## Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open source and available under the MIT License.

## Author

**Joshua V.**  
University of North Georgia - Computer Science  
[LinkedIn](https://www.linkedin.com/in/jevene/) | [GitHub](https://github.com/medistopia)

## Acknowledgments

- Built as part of a machine learning engineer career roadmap
- Inspired by the Pomodoro Technique by Francesco Cirillo
- Thanks to the Python community for excellent documentation

---

**Happy focusing! 🍅⏱️**

*Remember: The key to productivity is not working harder, but working smarter with focused intervals.*
