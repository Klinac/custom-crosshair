import tkinter as tk
from tkinter import ttk
import math

class CrosshairOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crosshair Overlay")
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'black')
        self.root.configure(bg='black')
        self.root.overrideredirect(True)
        
        # Make window click-through (mouse events pass through to underlying windows)
        try:
            # Windows-specific code to make window click-through
            import ctypes
            from ctypes import wintypes
            
            def make_clickthrough():
                hwnd = ctypes.windll.user32.FindWindowW(None, "Crosshair Overlay")
                if hwnd == 0:
                    # If title doesn't work, get the window handle another way
                    hwnd = self.root.winfo_id()
                
                # Get current window style
                style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE
                # Add WS_EX_TRANSPARENT flag to make click-through
                style |= 0x20  # WS_EX_TRANSPARENT
                ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
            
            # Apply click-through after window is created
            self.root.after(100, make_clickthrough)
        except:
            # If Windows-specific code fails, continue without click-through
            pass
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size and position to center
        window_size = 200
        x = (screen_width - window_size) // 2
        y = (screen_height - window_size) // 2
        self.root.geometry(f"{window_size}x{window_size}+{x}+{y}")
        
        # Create canvas for crosshair
        self.canvas = tk.Canvas(self.root, width=window_size, height=window_size, 
                               bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # Crosshair settings
        self.settings = {
            'length': 20,
            'thickness': 1,
            'center_gap': 0,
            'dot_size': 3.78844,
            'circle_radius': 0,
            'outline_opacity': 0,
            'color': {'r': 255, 'g': 255, 'b': 255, 'a': 255}
        }
        
        self.draw_crosshair()
        
    def draw_crosshair(self):
        self.canvas.delete("all")
        center_x = center_y = 100
        
        # Convert RGB to hex
        color = f"#{self.settings['color']['r']:02x}{self.settings['color']['g']:02x}{self.settings['color']['b']:02x}"
        
        length = self.settings['length']
        thickness = self.settings['thickness']
        gap = self.settings['center_gap']
        
        # Draw horizontal line
        if length > 0:
            # Left line
            self.canvas.create_rectangle(
                center_x - length - gap, center_y - thickness//2,
                center_x - gap, center_y + thickness//2 + 1,
                fill=color, outline=color
            )
            # Right line
            self.canvas.create_rectangle(
                center_x + gap, center_y - thickness//2,
                center_x + length + gap, center_y + thickness//2 + 1,
                fill=color, outline=color
            )
            
            # Vertical line
            # Top line
            self.canvas.create_rectangle(
                center_x - thickness//2, center_y - length - gap,
                center_x + thickness//2 + 1, center_y - gap,
                fill=color, outline=color
            )
            # Bottom line
            self.canvas.create_rectangle(
                center_x - thickness//2, center_y + gap,
                center_x + thickness//2 + 1, center_y + length + gap,
                fill=color, outline=color
            )
        
        # Draw center dot
        if self.settings['dot_size'] > 0:
            dot_size = self.settings['dot_size']
            if dot_size <= 3:
                # For small dots, use rectangle for pixel-perfect rendering
                half_size = dot_size / 2
                self.canvas.create_rectangle(
                    center_x - half_size, center_y - half_size,
                    center_x + half_size, center_y + half_size,
                    fill=color, outline=color, width=0
                )
            else:
                # For larger dots, use oval for circular shape
                dot_radius = dot_size / 2
                self.canvas.create_oval(
                    center_x - dot_radius, center_y - dot_radius,
                    center_x + dot_radius, center_y + dot_radius,
                    fill=color, outline=color, width=0
                )
        
        # Draw circle
        if self.settings['circle_radius'] > 0:
            radius = self.settings['circle_radius']
            outline_color = color if self.settings['outline_opacity'] > 0 else ""
            self.canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=outline_color, width=1, fill=""
            )
    
    def update_setting(self, key, value):
        if key in ['r', 'g', 'b', 'a']:
            self.settings['color'][key] = value
        else:
            self.settings[key] = value
        self.draw_crosshair()

class CrosshairSettings:
    def __init__(self, crosshair_overlay):
        self.crosshair = crosshair_overlay
        self.root = tk.Tk()
        self.root.title("Crosshair Settings")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left panel for settings
        settings_frame = tk.Frame(main_frame, bg='#2b2b2b', width=400)
        settings_frame.pack(side='left', fill='y', padx=(0, 20))
        settings_frame.pack_propagate(False)
        
        # Right panel for preview
        preview_frame = tk.Frame(main_frame, bg='#1a1a1a', relief='sunken', bd=2)
        preview_frame.pack(side='right', fill='both', expand=True)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(preview_frame, bg='#1a1a1a', width=300, height=300)
        self.preview_canvas.pack(expand=True)
        
        self.create_settings_ui(settings_frame)
        self.update_preview()
        
    def create_settings_ui(self, parent):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TFrame', background='#2b2b2b')
        
        # Crosshair Settings Title
        title_label = tk.Label(parent, text="Crosshair Settings", 
                              font=('Arial', 16, 'bold'), 
                              bg='#2b2b2b', fg='white')
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Type dropdown
        self.create_dropdown(parent, "Type", ["Create", "Crosshair", "Dot", "Circle"])
        
        # Length slider
        self.length_var = tk.DoubleVar(value=self.crosshair.settings['length'])
        self.create_slider(parent, "Length", self.length_var, 0, 50, 
                          lambda v: self.update_crosshair('length', int(v)))
        
        # Thickness slider
        self.thickness_var = tk.DoubleVar(value=self.crosshair.settings['thickness'])
        self.create_slider(parent, "Thickness", self.thickness_var, 1, 10,
                          lambda v: self.update_crosshair('thickness', int(v)))
        
        # Center Gap slider
        self.gap_var = tk.DoubleVar(value=self.crosshair.settings['center_gap'])
        self.create_slider(parent, "Center Gap", self.gap_var, 0, 20,
                          lambda v: self.update_crosshair('center_gap', int(v)))
        
        # Dot Size slider
        self.dot_var = tk.DoubleVar(value=self.crosshair.settings['dot_size'])
        self.create_slider(parent, "Dot Size", self.dot_var, 0, 20,
                          lambda v: self.update_crosshair('dot_size', float(v)))
        
        # Circle Radius slider
        self.circle_var = tk.DoubleVar(value=self.crosshair.settings['circle_radius'])
        self.create_slider(parent, "Circle Radius", self.circle_var, 0, 50,
                          lambda v: self.update_crosshair('circle_radius', int(v)))
        
        # Outline Opacity slider
        self.opacity_var = tk.DoubleVar(value=self.crosshair.settings['outline_opacity'])
        self.create_slider(parent, "Outline Opacity", self.opacity_var, 0, 255,
                          lambda v: self.update_crosshair('outline_opacity', int(v)))
        
        # Color Settings Title
        color_title = tk.Label(parent, text="Color Settings", 
                              font=('Arial', 14, 'bold'), 
                              bg='#2b2b2b', fg='white')
        color_title.pack(anchor='w', pady=(30, 20))
        
        # RGB sliders
        self.r_var = tk.DoubleVar(value=self.crosshair.settings['color']['r'])
        self.create_slider(parent, "R", self.r_var, 0, 255,
                          lambda v: self.update_crosshair('r', int(v)))
        
        self.g_var = tk.DoubleVar(value=self.crosshair.settings['color']['g'])
        self.create_slider(parent, "G", self.g_var, 0, 255,
                          lambda v: self.update_crosshair('g', int(v)))
        
        self.b_var = tk.DoubleVar(value=self.crosshair.settings['color']['b'])
        self.create_slider(parent, "B", self.b_var, 0, 255,
                          lambda v: self.update_crosshair('b', int(v)))
        
        self.a_var = tk.DoubleVar(value=self.crosshair.settings['color']['a'])
        self.create_slider(parent, "A", self.a_var, 0, 255,
                          lambda v: self.update_crosshair('a', int(v)))
    
    def create_dropdown(self, parent, label, options):
        frame = tk.Frame(parent, bg='#2b2b2b')
        frame.pack(fill='x', pady=10)
        
        label_widget = tk.Label(frame, text=label, bg='#2b2b2b', fg='white', width=15, anchor='w')
        label_widget.pack(side='left')
        
        var = tk.StringVar(value=options[0])
        dropdown = ttk.Combobox(frame, textvariable=var, values=options, state='readonly')
        dropdown.pack(side='right', padx=(10, 0))
        
        return var
    
    def create_slider(self, parent, label, var, min_val, max_val, callback):
        frame = tk.Frame(parent, bg='#2b2b2b')
        frame.pack(fill='x', pady=8)
        
        label_widget = tk.Label(frame, text=label, bg='#2b2b2b', fg='white', width=15, anchor='w')
        label_widget.pack(side='left')
        
        value_label = tk.Label(frame, text=str(int(var.get())), bg='#2b2b2b', fg='white', width=8)
        value_label.pack(side='right')
        
        slider = tk.Scale(frame, from_=min_val, to=max_val, orient='horizontal',
                         bg='#2b2b2b', fg='white', highlightthickness=0,
                         troughcolor='#404040', activebackground='#00bcd4',
                         variable=var, showvalue=0, length=200)
        slider.pack(side='right', padx=(10, 10))
        
        def on_change(val):
            value_label.config(text=str(int(float(val))))
            callback(float(val))
            self.update_preview()
        
        slider.config(command=on_change)
        
        return slider
    
    def update_crosshair(self, key, value):
        self.crosshair.update_setting(key, value)
    
    def update_preview(self):
        self.preview_canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.update_preview)
            return
        
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # Convert RGB to hex
        settings = self.crosshair.settings
        color = f"#{settings['color']['r']:02x}{settings['color']['g']:02x}{settings['color']['b']:02x}"
        
        # Scale down the crosshair for preview
        scale = 0.8
        length = int(settings['length'] * scale)
        thickness = max(1, int(settings['thickness'] * scale))
        gap = int(settings['center_gap'] * scale)
        
        # Draw crosshair preview
        if length > 0:
            # Horizontal line
            self.preview_canvas.create_rectangle(
                center_x - length - gap, center_y - thickness//2,
                center_x - gap, center_y + thickness//2 + 1,
                fill=color, outline=color
            )
            self.preview_canvas.create_rectangle(
                center_x + gap, center_y - thickness//2,
                center_x + length + gap, center_y + thickness//2 + 1,
                fill=color, outline=color
            )
            
            # Vertical line
            self.preview_canvas.create_rectangle(
                center_x - thickness//2, center_y - length - gap,
                center_x + thickness//2 + 1, center_y - gap,
                fill=color, outline=color
            )
            self.preview_canvas.create_rectangle(
                center_x - thickness//2, center_y + gap,
                center_x + thickness//2 + 1, center_y + length + gap,
                fill=color, outline=color
            )
        
        # Draw center dot
        if settings['dot_size'] > 0:
            dot_size = settings['dot_size'] * scale
            if dot_size <= 3:
                # For small dots, use rectangle for pixel-perfect rendering
                half_size = dot_size / 2
                self.preview_canvas.create_rectangle(
                    center_x - half_size, center_y - half_size,
                    center_x + half_size, center_y + half_size,
                    fill=color, outline=color, width=0
                )
            else:
                # For larger dots, use oval for circular shape
                dot_radius = dot_size / 2
                self.preview_canvas.create_oval(
                    center_x - dot_radius, center_y - dot_radius,
                    center_x + dot_radius, center_y + dot_radius,
                    fill=color, outline=color, width=0
                )
        
        # Draw circle
        if settings['circle_radius'] > 0:
            radius = settings['circle_radius'] * scale
            outline_color = color if settings['outline_opacity'] > 0 else ""
            self.preview_canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=outline_color, width=1, fill=""
            )

def main():
    # Create crosshair overlay
    overlay = CrosshairOverlay()
    
    # Create settings window
    settings = CrosshairSettings(overlay)
    
    # Handle window closing
    def on_closing():
        overlay.root.quit()
        settings.root.quit()
    
    settings.root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start both windows
    def run_overlay():
        overlay.root.mainloop()
    
    def run_settings():
        settings.root.mainloop()
    
    import threading
    overlay_thread = threading.Thread(target=run_overlay, daemon=True)
    overlay_thread.start()
    
    run_settings()

if __name__ == "__main__":
    main()