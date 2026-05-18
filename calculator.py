import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
import os
from datetime import datetime

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("500x700")
        self.root.minsize(400, 600)
        
        # Variables
        self.history = []
        self.dark_mode = True
        self.current_theme = "dark"
        
        # Load history from file
        self.load_history()
        
        # Setup UI
        self.setup_ui()
        self.apply_theme()
        
        # Bind keyboard
        self.bind_keyboard()
        
    def setup_ui(self):
        # Main container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Top frame for theme toggle and history
        self.top_frame = tk.Frame(self.main_container)
        self.top_frame.pack(fill="x", pady=(0, 10))
        
        # Theme toggle button
        self.theme_btn = tk.Button(
            self.top_frame,
            text="🌙 Dark" if self.dark_mode else "☀️ Light",
            font=("Arial", 10),
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="left", padx=5)
        
        # History button
        self.history_btn = tk.Button(
            self.top_frame,
            text="📜 History",
            font=("Arial", 10),
            command=self.show_history
        )
        self.history_btn.pack(side="left", padx=5)
        
        # Clear history button
        self.clear_history_btn = tk.Button(
            self.top_frame,
            text="🗑️ Clear History",
            font=("Arial", 10),
            command=self.clear_history
        )
        self.clear_history_btn.pack(side="left", padx=5)
        
        # Entry display
        self.entry = tk.Entry(
            self.main_container,
            font=("Arial", 28),
            bd=10,
            relief=tk.RIDGE,
            justify="right"
        )
        self.entry.pack(fill="x", ipadx=8, ipady=15, pady=(0, 10))
        
        # History display (hidden initially)
        self.history_frame = tk.Frame(self.main_container)
        self.history_text = tk.Text(
            self.history_frame,
            font=("Arial", 10),
            height=8,
            width=50,
            state="disabled"
        )
        self.history_text.pack(fill="both", expand=True)
        self.history_scrollbar = tk.Scrollbar(self.history_text)
        self.history_scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.main_container)
        self.buttons_frame.pack(expand=True, fill="both")
        
        # Scientific buttons frame
        self.scientific_frame = tk.Frame(self.buttons_frame)
        self.scientific_frame.pack(fill="x", pady=(0, 10))
        
        # Scientific buttons
        scientific_buttons = [
            'sin', 'cos', 'tan', 'sqrt',
            'log', 'ln', 'π', 'e',
            'x²', 'x³', '1/x', '|x|',
            '(', ')', '^', 'mod'
        ]
        
        # Create scientific buttons in rows
        for i in range(0, len(scientific_buttons), 4):
            row_frame = tk.Frame(self.scientific_frame)
            row_frame.pack(fill="x", pady=2)
            for j in range(4):
                if i+j < len(scientific_buttons):
                    btn = scientific_buttons[i+j]
                    button = tk.Button(
                        row_frame,
                        text=btn,
                        font=("Arial", 10),
                        height=1,
                        width=6,
                        command=lambda b=btn: self.scientific_function(b)
                    )
                    button.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        
        # Main calculator buttons
        main_buttons = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '⌫'],
            ['1', '2', '3', '-', '='],
            ['0', '.', '+', '±', '%']
        ]
        
        # Create main buttons
        for row in main_buttons:
            row_frame = tk.Frame(self.buttons_frame)
            row_frame.pack(expand=True, fill="both", pady=2)
            
            for btn in row:
                button = tk.Button(
                    row_frame,
                    text=btn,
                    font=("Arial", 18),
                    height=2,
                    width=5
                )
                button.pack(side="left", expand=True, fill="both", padx=2, pady=2)
                
                if btn == "=":
                    button.config(command=self.calculate, bg="green")
                elif btn == "C":
                    button.config(command=self.clear, bg="red")
                elif btn == "⌫":
                    button.config(command=self.backspace, bg="orange")
                elif btn == "±":
                    button.config(command=self.negate)
                elif btn == "%":
                    button.config(command=self.percent)
                else:
                    button.config(command=lambda b=btn: self.click(b))
    
    def bind_keyboard(self):
        """Bind keyboard keys to calculator functions"""
        self.root.bind('<Key>', self.key_press)
        self.entry.bind('<Return>', lambda event: self.calculate())
        self.entry.bind('<BackSpace>', lambda event: self.backspace())
        self.entry.bind('<Escape>', lambda event: self.clear())
        
    def key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        if key.isdigit() or key in '+-*/.()':
            self.click(key)
        elif key == '\r':  # Enter key
            self.calculate()
        elif key == '\x08':  # Backspace
            self.backspace()
    
    def click(self, value):
        """Add value to entry"""
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current + str(value))
    
    def clear(self):
        """Clear entry"""
        self.entry.delete(0, tk.END)
    
    def backspace(self):
        """Delete last character"""
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current[:-1])
    
    def negate(self):
        """Negate current value"""
        try:
            current = self.entry.get()
            if current and current[0] == '-':
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, current[1:])
            elif current:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, '-' + current)
        except:
            pass
    
    def percent(self):
        """Convert to percentage"""
        try:
            current = self.entry.get()
            value = eval(current) / 100
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(value))
        except:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")
    
    def scientific_function(self, func):
        """Handle scientific calculations"""
        try:
            current = self.entry.get()
            if not current:
                current = "0"
            
            value = eval(current)
            
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'tan':
                result = math.tan(math.radians(value))
            elif func == 'sqrt':
                result = math.sqrt(value)
            elif func == 'log':
                result = math.log10(value)
            elif func == 'ln':
                result = math.log(value)
            elif func == 'π':
                result = math.pi
            elif func == 'e':
                result = math.e
            elif func == 'x²':
                result = value ** 2
            elif func == 'x³':
                result = value ** 3
            elif func == '1/x':
                result = 1 / value if value != 0 else "Error"
            elif func == '|x|':
                result = abs(value)
            elif func == 'mod':
                self.entry.insert(tk.END, '%')
                return
            elif func == '^':
                self.entry.insert(tk.END, '**')
                return
            else:
                result = "Error"
            
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
            
            # Add to history
            self.add_to_history(f"{func}({value}) = {result}")
            
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")
    
    def calculate(self):
        """Calculate the expression"""
        try:
            expression = self.entry.get()
            # Replace ^ with ** for power operation
            expression = expression.replace('^', '**')
            result = eval(expression)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
            
            # Add to history
            self.add_to_history(f"{expression} = {result}")
            
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")
    
    def add_to_history(self, calculation):
        """Add calculation to history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history.append(f"[{timestamp}] {calculation}")
        
        # Keep only last 50 calculations
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
        # Save to file
        self.save_history()
        
        # Update history display if visible
        if self.history_frame.winfo_ismapped():
            self.update_history_display()
    
    def update_history_display(self):
        """Update the history text widget"""
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        
        for calc in reversed(self.history):
            self.history_text.insert(tk.END, calc + "\n\n")
        
        self.history_text.config(state="disabled")
    
    def show_history(self):
        """Show history window"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("400x500")
        
        # Apply theme to history window
        if self.dark_mode:
            history_window.configure(bg="#2b2b2b")
        
        text_widget = tk.Text(history_window, font=("Arial", 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_widget)
        scrollbar.pack(side="right", fill="y")
        
        for calc in reversed(self.history):
            text_widget.insert(tk.END, calc + "\n\n")
        
        text_widget.config(state="disabled")
    
    def clear_history(self):
        """Clear calculation history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all history?"):
            self.history = []
            self.save_history()
            messagebox.showinfo("Success", "History cleared successfully!")
    
    def save_history(self):
        """Save history to file"""
        try:
            with open("calculator_history.json", "w") as f:
                json.dump(self.history, f)
        except:
            pass
    
    def load_history(self):
        """Load history from file"""
        try:
            if os.path.exists("calculator_history.json"):
                with open("calculator_history.json", "r") as f:
                    self.history = json.load(f)
        except:
            self.history = []
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        self.dark_mode = not self.dark_mode
        self.theme_btn.config(text="🌙 Dark" if self.dark_mode else "☀️ Light")
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme to all widgets"""
        if self.dark_mode:
            bg_color = "#2b2b2b"
            fg_color = "white"
            entry_bg = "#3c3c3c"
            button_bg = "#4a4a4a"
            button_fg = "white"
            frame_bg = "#2b2b2b"
        else:
            bg_color = "#f0f0f0"
            fg_color = "black"
            entry_bg = "white"
            button_bg = "#e0e0e0"
            button_fg = "black"
            frame_bg = "#f0f0f0"
        
        # Apply to root window
        self.root.configure(bg=bg_color)
        self.main_container.configure(bg=bg_color)
        self.top_frame.configure(bg=bg_color)
        self.buttons_frame.configure(bg=bg_color)
        self.scientific_frame.configure(bg=bg_color)
        
        # Apply to entry
        self.entry.configure(bg=entry_bg, fg=fg_color, insertbackground=fg_color)
        
        # Apply to all buttons
        for widget in [self.theme_btn, self.history_btn, self.clear_history_btn]:
            widget.configure(bg=button_bg, fg=button_fg)
        
        for frame in self.buttons_frame.winfo_children():
            if isinstance(frame, tk.Frame):
                frame.configure(bg=frame_bg)
                for button in frame.winfo_children():
                    if isinstance(button, tk.Button):
                        current_bg = button.cget("bg")
                        if current_bg not in ["green", "red", "orange"]:
                            button.configure(bg=button_bg, fg=button_fg)
                        else:
                            # Keep colored buttons but adjust text color if needed
                            button.configure(fg="white")
        
        for frame in self.scientific_frame.winfo_children():
            if isinstance(frame, tk.Frame):
                frame.configure(bg=frame_bg)
                for button in frame.winfo_children():
                    if isinstance(button, tk.Button):
                        button.configure(bg=button_bg, fg=button_fg)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop() 