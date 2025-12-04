"""
Pomodoro CLI Timer
A command-line Pomodoro technique timer for productivity tracking

Usage:
    python pomodoro.py start "Task name"    - Start a new pomodoro session
    python pomodoro.py stats                - View your productivity stats
    python pomodoro.py history              - View session history
    python pomodoro.py today                - View today's sessions

Requirements:
    Standard library only for basic features
    Optional: pip install pyttsx3 (for text-to-speech)
"""

import time # For countdown timer and sleep()
import json # To save/load session data to file
import sys # To read command-line arguments (sys.argv)
from datetime import datetime # To track dates and times
import os # To check for file existence
import platform # To detect operating system for sound compatibility

# Try to import text-to-speech (optional)
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

class PomodoroTimer:
    # Initialize the Pomodoro timer
    def __init__(self, data_file="pomodoro_data.json"):
        self.data_file = data_file
        self.work_duration = 25 * 60  # 25 minutes in seconds (easier for time.sleep())
        self.break_duration = 5 * 60   # 5 minutes in seconds
        self.sessions = self.load_sessions()
        self.sound_mode = None  # User's sound preference (set on first start)
        self.tts_engine = None  # Text-to-speech engine instance (initialized if needed)
    
    def load_sessions(self):
        # Use existing data file or create new
        if os.path.exists(self.data_file): # Does file exist?
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f) # Read JSON from file
            except:
                return [] # If file is corrupted, start fresh
        return [] # No file yet, start with an empty list (to make sure that program does not crash)
    
    def save_sessions(self):
        """Save session history to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.sessions, f, indent=2) # indent for readability, called after each pomodoro completion
    
    def play_sound(self, sound_type):
        """Play sound based on user preference and event type"""
        if self.sound_mode == 'beeps':
            self._play_beep(sound_type)
        elif self.sound_mode == 'tts':
            self._play_tts(sound_type)
        # If 'none', do nothing (silent mode)
    
    def _play_beep(self, sound_type):
        """Play system beep sounds - works on Windows, Mac, Linux"""
        system = platform.system()
        
        if system == 'Windows':
            import winsound
            if sound_type == 'start':
                winsound.Beep(800, 200)  # 800Hz frequency, 200ms duration
            elif sound_type == 'complete':
                # Triple beep celebration for work completion!
                for _ in range(3):
                    winsound.Beep(1000, 300)  # Higher pitch, longer duration
                    time.sleep(0.1)
            elif sound_type == 'break_end':
                winsound.Beep(600, 400)  # Lower tone for break end
        else:
            # Mac/Linux - use system bell (terminal beep)
            if sound_type == 'start':
                os.system('echo -e "\\a"')  # Single beep
            elif sound_type == 'complete':
                for _ in range(3):
                    os.system('echo -e "\\a"')
                    time.sleep(0.2)
            elif sound_type == 'break_end':
                os.system('echo -e "\\a"')
    
    def _play_tts(self, sound_type):
        """Play text-to-speech announcements"""
        if not TTS_AVAILABLE:
            print("⚠️  TTS not available, falling back to beeps")
            self._play_beep(sound_type)
            return
        
        # Initialize TTS engine on first use
        if self.tts_engine is None:
            self.tts_engine = pyttsx3.init()
            # Adjust speech rate for better clarity (default is ~200)
            self.tts_engine.setProperty('rate', 150)
        
        # Different messages for different events
        messages = {
            'start': 'Pomodoro session starting. Stay focused!',
            'complete': 'Great work! Pomodoro complete. Time for a break.',
            'break_end': 'Break time is over. Ready for the next session?'
        }
        
        message = messages.get(sound_type, '')
        if message:
            self.tts_engine.say(message)
            self.tts_engine.runAndWait()  # Wait for speech to finish
    
    def choose_sound_mode(self):
        """Ask user for sound preference at start of session"""
        print("\n🔊 Sound Preferences")
        print("=" * 50)
        print("1. Beeps - Simple system beeps")
        
        if TTS_AVAILABLE:
            print("2. TTS - Text-to-speech announcements")
        else:
            print("2. TTS - (Not available - install with: pip install pyttsx3)")
        
        print("3. None - Silent mode")
        
        # Keep asking until valid choice
        while True:
            choice = input("\nChoose sound mode (1/2/3): ").strip()
            
            if choice == '1':
                self.sound_mode = 'beeps'
                print("✅ Beeps enabled")
                break
            elif choice == '2':
                if TTS_AVAILABLE:
                    self.sound_mode = 'tts'
                    print("✅ Text-to-speech enabled")
                    break
                else:
                    print("❌ TTS not available. Please choose 1 or 3.")
            elif choice == '3':
                self.sound_mode = 'none'
                print("✅ Silent mode")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    # where the magic happens - countdown timer
    def countdown(self, duration, label):
        # display countdown timer
        print(f"\n🍅 {label} - {duration // 60} minutes")
        print("=" * 50)
        
        end_time = time.time() + duration # when timer should end
        
        while time.time() < end_time: # keep looping until time is up
            remaining = int(end_time - time.time()) # seconds left
            mins, secs = divmod(remaining, 60) # convert to mins:secs format
            
            # Clear line and print timer
            timer_display = f"⏱️  {mins:02d}:{secs:02d} remaining" # formatted string with leading zeros
            print(f"\r{timer_display}", end="", flush=True)  # carriage return, moves cursor to start of line, flush and overwrites text
            # then 'end-' makes sure it doesn't go to new line while flush updates the display immediately
            
            time.sleep(1) # wait a second before updating
        
        print(f"\n\n✅ {label} complete!")
        return True
    
    def start_session(self, task_name):
        """Start a new Pomodoro session"""
        # Ask for sound preference if not set yet
        if self.sound_mode is None:
            self.choose_sound_mode()
        
        print(f"\n🎯 Starting Pomodoro for: {task_name}")
        print("=" * 50)
        
        # Play start sound
        self.play_sound('start')
        
        # Work session (25 minutes)
        completed = self.countdown(self.work_duration, "Work Session")
        
        if completed:
            # Play completion sound
            self.play_sound('complete')
            
            # Log the session and create session record
            session = {
                'task': task_name,
                'date': datetime.now().strftime('%Y-%m-%d'), # format date as YYYY-MM-DD
                'time': datetime.now().strftime('%H:%M:%S'), # format time as HH:MM:SS
                'duration': self.work_duration // 60,
                'completed': True
            }
            self.sessions.append(session) # add to list of sessions
            self.save_sessions() # save to file
            
            print(f"\n🎉 Pomodoro completed! Great work on '{task_name}'!")
            
            # Ask about break
            take_break = input("\n🌴 Take a 5-minute break? (y/n): ").lower()
            if take_break == 'y':
                self.countdown(self.break_duration, "Break Time")
                self.play_sound('break_end')  # Sound when break ends
                print("\n💪 Ready for the next session!")
    
    def show_today(self):
        """Show today's completed sessions"""
        today = datetime.now().strftime('%Y-%m-%d') # get today's date
        today_sessions = [s for s in self.sessions if s['date'] == today] # filter sessions for today, loops through all sessions and picks only those from today 
        
        if not today_sessions:
            print("\n📅 No sessions completed today yet.")
            print("Start one with: python pomodoro.py start \"Your task\"")
            return
        
        print(f"\n📅 Today's Sessions ({today})")
        print("=" * 50)
        
        # Display each session
        for i, session in enumerate(today_sessions, 1):
            print(f"{i}. {session['task']}")
            print(f"   Time: {session['time']} | Duration: {session['duration']} min")
        
        # calculate totals
        print(f"\n✅ Total pomodoros today: {len(today_sessions)}")
        total_minutes = sum(s['duration'] for s in today_sessions) # adds up all durations
        print(f"⏱️  Total focus time: {total_minutes} minutes ({total_minutes/60:.1f} hours)")
    
    def show_history(self, limit=10):
        """Show recent session history"""
        # if you want to see more than default 10, you can modify limit parameter
        # e.g., timer.show_history(limit=20)
        # self.sessions[-limit:] = last N sessions from the end of the list
        # [::-1] reverses the list to show most recent first
        if not self.sessions:
            print("\n📝 No sessions recorded yet.")
            print("Start one with: python pomodoro.py start \"Your task\"")
            return
        
        print(f"\n📝 Recent Sessions (Last {limit})")
        print("=" * 50)
        
        recent = self.sessions[-limit:][::-1]  # Last N sessions, reversed
        
        for i, session in enumerate(recent, 1):
            print(f"{i}. {session['task']}")
            print(f"   {session['date']} at {session['time']} | {session['duration']} min")
    
    def show_stats(self):
        """Show productivity statistics"""
        if not self.sessions:
            print("\n📊 No data yet. Complete some pomodoros first!")
            return
        
        print("\n📊 Productivity Statistics")
        print("=" * 50)
        
        # Total sessions
        total_sessions = len(self.sessions)
        print(f"🍅 Total pomodoros: {total_sessions}")
        
        # Total time
        total_minutes = sum(s['duration'] for s in self.sessions)
        hours = total_minutes / 60
        print(f"⏱️  Total focus time: {total_minutes} minutes ({hours:.1f} hours)")
        
        # Sessions by day
        days = {}
        for session in self.sessions:
            date = session['date']
            days[date] = days.get(date, 0) + 1 # Count sessions per day
        
        print(f"\n📅 Active days: {len(days)}")
        print(f"📈 Average per active day: {total_sessions / len(days):.1f} pomodoros")
        
        # Most productive day
        # max() finds the day with the most sessions
        if days:
            best_day = max(days.items(), key=lambda x: x[1])
            # lambda x: x[1] means "sort by second item in tuple (the count of sessions)"
            # items() returns [(date, count), (date, count), ...] 
            print(f"🏆 Most productive day: {best_day[0]} ({best_day[1]} pomodoros)")
        
        # Recent streak
        print("\n🔥 Recent Activity:")
        recent_days = sorted(days.keys())[-7:]  # Last 7 days with activity
        for day in recent_days:
            bar = "🍅" * days[day] # multiply string by count
            print(f"   {day}: {bar} ({days[day]})")

# simple instruction function
def show_help():
    """Display help information"""
    help_text = """

🍅 Pomodoro CLI Timer
=====================

COMMANDS:
    start "task"    Start a new 25-minute pomodoro session
    today           View today's completed sessions
    history         View recent session history
    stats           View productivity statistics
    help            Show this help message

EXAMPLES:
    python pomodoro.py start "Study Python"
    python pomodoro.py today
    python pomodoro.py stats

ABOUT POMODORO TECHNIQUE:
    • Work for 25 minutes (1 pomodoro)
    • Take a 5-minute break
    • After 4 pomodoros, take a longer 15-30 minute break

TIP: Stay focused during your pomodoro - no distractions! 🎯
"""
    print(help_text)


def main():
    """Main CLI entry point"""
    timer = PomodoroTimer() # create timer instance
    
    if len(sys.argv) < 2: # if no command provided
        show_help()
        return
    
    command = sys.argv[1].lower() # get first argument as command
    
    if command == "start":
        if len(sys.argv) < 3: # needs task name
            print("❌ Error: Please provide a task name")
            print('Usage: python pomodoro.py start "Your task name"')
            return
        
        task_name = " ".join(sys.argv[2:]) # join all args after command as task name
        timer.start_session(task_name) # start the session
    
    elif command == "today":
        timer.show_today()
    
    elif command == "history":
        timer.show_history()
    
    elif command == "stats":
        timer.show_stats()
    
    elif command == "help":
        show_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python pomodoro.py help' for usage information")


if __name__ == "__main__":
    main()