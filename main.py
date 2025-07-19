import tkinter as tk
from tkinter import ttk, PhotoImage
from register import register_user
from detect_team import check_team_presence
from utils import recognize_user
import time

# Track login state
logged_in = False
current_user = None

def animate_label(label, end_text, delay=100, current_index=0):
    """Function to create a typing animation effect for labels"""
    if current_index <= len(end_text):
        label.config(text=end_text[:current_index] + "▌")
        label.after(delay, lambda: animate_label(label, end_text, delay, current_index + 1))
    else:
        label.config(text=end_text)

def slide_widget(widget, start_y, end_y, steps=20, delay=10, current_step=0):
    """Function to create a sliding animation for widgets"""
    if current_step <= steps:
        y = start_y + (end_y - start_y) * (current_step / steps)
        widget.place(rely=y, relx=0.5, anchor="center")
        widget.after(delay, lambda: slide_widget(widget, start_y, end_y, steps, delay, current_step + 1))
    else:
        widget.place(rely=end_y, relx=0.5, anchor="center")

def flash_success():
    """Creates a success flash effect"""
    flash = tk.Frame(app, bg="#4CAF50", width=400, height=350)
    flash.place(x=0, y=0)
    
    def fade_out(alpha=0.9):
        if alpha > 0:
            flash.configure(bg=f"#{int(76*alpha):02x}{int(175*alpha):02x}{int(80*alpha):02x}")
            app.after(20, lambda: fade_out(alpha - 0.1))
        else:
            flash.destroy()
    
    app.after(100, fade_out)

def login():
    global logged_in, current_user
    username = entry.get().strip()
    if not username:
        status_label.config(foreground="#F44336")
        animate_label(status_label, "⚠ Please enter a username.", 50)
        return

    # Show loading animation
    status_label.config(foreground="#2196F3")
    for i in range(5):
        status_label.config(text="Authenticating" + "." * (i % 4))
        app.update()
        time.sleep(0.3)

    result = recognize_user(username)
    if result:
        logged_in = True
        current_user = username
        flash_success()
        status_label.config(foreground="#4CAF50")
        animate_label(status_label, f"✅ Welcome back, {username}!", 50)
        app.after(1000, show_logged_in_screen)
    else:
        status_label.config(foreground="#F44336")
        animate_label(status_label, "❌ User does not exist.", 50)
            

def logout():
    global logged_in, current_user
    logged_in = False
    current_user = None
    status_label.config(foreground="#4CAF50")
    animate_label(status_label, "✅ Logged out successfully.", 50)
    app.after(800, show_home_screen)

def open_register_window():
    register_user()

def open_team_checker():
    check_team_presence()

def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def create_heading(text):
    heading = tk.Label(
        main_frame,
        text=text,
        font=("Montserrat", 22, "bold"),
        fg="#1E88E5",
        bg="#FFFFFF"
    )
    return heading

def create_label(text):
    return tk.Label(
        main_frame,
        text=text,
        font=("Roboto", 12),
        fg="#424242",
        bg="#FFFFFF"
    )

def create_button(text, command, color="#2196F3", hover_color="#1976D2"):
    frame = tk.Frame(main_frame, bg=color, pady=0, padx=0, highlightthickness=0)
    
    btn = tk.Label(
        frame,
        text=text,
        font=("Roboto", 12, "bold"),
        fg="white",
        bg=color,
        padx=20,
        pady=8,
        cursor="hand2"
    )
    btn.pack()
    
    def on_enter(e):
        frame.config(bg=hover_color)
        btn.config(bg=hover_color)
    
    def on_leave(e):
        frame.config(bg=color)
        btn.config(bg=color)
    
    def on_click(e):
        # Create click effect
        frame.config(bg=hover_color)
        btn.config(bg=hover_color)
        app.after(100, command)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", on_click)
    frame.bind("<Button-1>", on_click)
    
    return frame

def show_home_screen():
    clear_frame()
    
    # Create gradient header
    header = tk.Canvas(main_frame, width=380, height=70, bg="#FFFFFF", highlightthickness=0)
    header.create_rectangle(0, 0, 380, 70, fill="#2196F3", outline="")
    header.create_rectangle(0, 60, 380, 70, fill="#1E88E5", outline="")
    header.pack(pady=(0, 20))
    
    # Add logo text on header
    header.create_text(190, 35, text="FaceID System", fill="white", font=("Montserrat", 20, "bold"))
    
    # Add animated subtitle
    subtitle = create_label("")
    subtitle.pack(pady=(0, 20))
    animate_label(subtitle, "Secure Authentication System", 50)
    
    # User frame with cleaner styling
    user_frame = tk.Frame(main_frame, bg="#FFFFFF", padx=20, pady=20)
    user_frame.pack(pady=10, fill=tk.X)
    
    # Create a subtle shadow effect
    shadow_canvas = tk.Canvas(user_frame, bg="#FFFFFF", highlightthickness=0)
    shadow_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Username label with better styling
    tk.Label(
        user_frame,
        text="Username",
        font=("Roboto", 12, "bold"),
        fg="#1E88E5",
        bg="#FFFFFF"
    ).pack(anchor=tk.W, pady=(0, 5))
    
    # Modern username entry field - no icon now
    global entry_frame
    entry_frame = tk.Frame(user_frame, bg="#FFFFFF")
    entry_frame.pack(fill=tk.X, pady=(0, 15))
    
    # Bottom border only style
    border_frame = tk.Frame(entry_frame, height=2, bg="#E0E0E0")
    
    global entry
    entry = tk.Entry(
        entry_frame,
        font=("Roboto", 13),
        bd=0,
        highlightthickness=0,
        bg="#FFFFFF",
        insertbackground="#2196F3",  # Cursor color
        insertwidth=2
    )
    entry.pack(fill=tk.X, ipady=8, padx=8)
    border_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    # Change border color on focus
    def on_entry_focus(event):
        border_frame.config(bg="#2196F3")  # Accent color when focused
        
    def on_entry_focusout(event):
        border_frame.config(bg="#E0E0E0")  # Default color when not focused
        
    entry.bind("<FocusIn>", on_entry_focus)
    entry.bind("<FocusOut>", on_entry_focusout)
    
    # Button section
    button_frame = tk.Frame(main_frame, bg="#FFFFFF")
    button_frame.pack(pady=20)
    
    login_btn = create_button("🔓  Login with Face", login)
    login_btn.pack(pady=5)
    
    register_btn = create_button("➕  Register New User", open_register_window, color="#4CAF50", hover_color="#388E3C")
    register_btn.pack(pady=10)
    
    # Create an empty spacer frame for better positioning of status message
    spacer_frame = tk.Frame(main_frame, bg="#FFFFFF", height=30)
    spacer_frame.pack()
    
    # Status label - now positioned below the username field
    global status_label
    status_label = tk.Label(
        main_frame,
        text="",
        font=("Roboto", 11),
        fg="#424242",
        bg="#FFFFFF",
        height=2
    )
    status_label.pack(pady=5)
    
    # Add footer
    footer = tk.Label(
        main_frame,
        text="© 2025 FaceID System • Secure Authentication",
        font=("Roboto", 8),
        fg="#9E9E9E",
        bg="#FFFFFF"
    )
    footer.pack(side=tk.BOTTOM, pady=10)

def show_logged_in_screen():
    clear_frame()
    
    # Profile picture placeholder (circle)
    profile_frame = tk.Frame(main_frame, bg="#FFFFFF")
    profile_frame.pack(pady=20)
    
    canvas = tk.Canvas(profile_frame, width=100, height=100, bg="#FFFFFF", highlightthickness=0)
    # Create gradient effect for profile
    canvas.create_oval(5, 5, 95, 95, fill="#2196F3", outline="#E3F2FD", width=3)
    for i in range(20):
        canvas.create_oval(5+i, 5+i, 95-i, 95-i, outline="#1E88E5", width=0)
    canvas.create_text(50, 50, text=current_user[0].upper(), fill="white", font=("Montserrat", 36, "bold"))
    canvas.pack()
    
    welcome = create_heading(f"Welcome, {current_user}!")
    welcome.pack(pady=10)
    
    descriptor = create_label("You've been successfully authenticated")
    descriptor.pack(pady=(0, 20))
    
    # Quick actions section with card-like styling
    action_frame = tk.Frame(main_frame, bg="#F5F5F5", padx=20, pady=20, bd=0)
    
    # Create a rounded look with a canvas
    action_canvas = tk.Canvas(action_frame, bg="#F5F5F5", highlightthickness=0)
    action_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    
    action_frame.pack(fill=tk.X, padx=10)
    

    
    team_btn = create_button("👥  Check Team Presence", open_team_checker, color="#FF9800", hover_color="#F57C00")
    team_btn.pack(pady=5, fill=tk.X)
    
    logout_btn = create_button("🚪  Logout", logout, color="#F44336", hover_color="#D32F2F")
    logout_btn.pack(pady=10, fill=tk.X)
    
    global status_label
    status_label = tk.Label(
        main_frame,
        text="",
        font=("Roboto", 11),
        fg="#424242",
        bg="#FFFFFF",
        height=2
    )
    status_label.pack(pady=15)
    
    # Last login info
    last_login = tk.Label(
        main_frame,
        text=f"Last login: {time.strftime('%B %d, %Y at %H:%M')}",
        font=("Roboto", 9),
        fg="#9E9E9E",
        bg="#FFFFFF"
    )
    last_login.pack(side=tk.BOTTOM, pady=10)

# GUI setup
app = tk.Tk()
app.title("FaceID System")
app.geometry("400x600")
app.configure(bg="#FFFFFF")
app.resizable(False, False)

# Try to set app icon
try:
    app.iconbitmap("face_icon.ico")
except:
    pass

# Modern styling
style = ttk.Style()
style.theme_use("clam")

# Container frame
main_frame = tk.Frame(app, bg="#FFFFFF", width=400)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

show_home_screen()

app.mainloop()

