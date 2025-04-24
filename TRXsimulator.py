import tkinter as tk
from tkinter import ttk
import random
import threading
import time
import math

class SMeterCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='white', bd=1, highlightthickness=1)
        self.value = 0
        self.width = kwargs.get('width', 100)
        self.height = kwargs.get('height', 60)
        self.draw_scale()
        self.create_needle()
        
    def draw_scale(self):
        # Dessine l'échelle
        self.create_text(self.width/2, 10, text="S3 S5 S7 S9 +10 +30dB", font=('Arial', 8))
        # Arc de mesure (inversé pour pointer vers le haut)
        self.create_arc(10, 10, self.width-10, self.height*2-10,
                       start=0, extent=180, style='arc')
                       
    def create_needle(self):
        # Crée l'aiguille (pointant vers le haut par défaut)
        center_x = self.width / 2
        center_y = self.height - 10
        length = self.height * 0.6
        self.needle = self.create_line(center_x, center_y,
                                     center_x, center_y - length,
                                     fill='red', width=2, tags='needle')
                                     
    def set_value(self, value):
        self.value = min(1.0, max(0.0, value))
        angle = (self.value * 180) -180 # 0-1 to 0-180 degrees
        rad = math.radians(angle)
        center_x = self.width / 2
        center_y = self.height - 10
        length = self.height * 0.6
        end_x = center_x + length * math.sin(rad)
        end_y = center_y - length * math.cos(rad)
        self.coords(self.needle, center_x, center_y, end_x, end_y)

class RadioAmateur:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulateur poste radioamateur LOTA")
        
        # Définition des bandes
        self.bands = {
            "10m": (28.000, 29.700),  # MHz
            "2m": (144.000, 146.000),
            "70cm": (430.000, 440.000)
        }
        
        # Paramètres radio
        self.current_band = "2m"
        self.frequency = self.bands[self.current_band][0]
        self.mode = "FM"
        self.volume = 0.5
        self.squelch = 0.2
        self.is_transmitting = False
        self.is_receiving = False
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        title_label = ttk.Label(main_frame, text="Simulateur poste radioamateur LOTA",
                              font=('Arial', 12, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # S-mètre
        self.s_meter = SMeterCanvas(main_frame, width=100, height=60)
        self.s_meter.grid(row=0, column=3, padx=5, sticky='E')
        
        # Sélecteur de bande
        ttk.Label(main_frame, text="Bande:").grid(row=1, column=0, sticky='W')
        self.band_var = tk.StringVar(value=self.current_band)
        band_select = ttk.Combobox(main_frame, textvariable=self.band_var,
                                 values=list(self.bands.keys()),
                                 state='readonly')
        band_select.grid(row=1, column=1, sticky='W')
        band_select.bind('<<ComboboxSelected>>', self.change_band)
        
        # Fréquence
        ttk.Label(main_frame, text="Fréquence:").grid(row=2, column=0, sticky='W')
        self.freq_var = tk.StringVar(value=f"{self.frequency:.3f} MHz")
        freq_label = ttk.Label(main_frame, textvariable=self.freq_var)
        freq_label.grid(row=2, column=1, sticky='W')
        
        # Slider fréquence
        self.freq_scale = ttk.Scale(main_frame, from_=0, to=1,
                                  orient=tk.HORIZONTAL,
                                  command=self.change_frequency)
        self.freq_scale.grid(row=3, column=0, columnspan=4, sticky='EW', pady=5)
        
        # Mode
        ttk.Label(main_frame, text="Mode:").grid(row=4, column=0, sticky='W')
        modes = ['FM', 'USB', 'LSB', 'CW']
        self.mode_var = tk.StringVar(value='FM')
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=4, column=1, columnspan=3, sticky='W')
        for i, mode in enumerate(modes):
            ttk.Radiobutton(mode_frame, text=mode, variable=self.mode_var,
                          value=mode, command=self.change_mode).pack(side=tk.LEFT)
        
        # Volume et Squelch
        for i, (label, var) in enumerate([("Volume:", "volume"), ("Squelch:", "squelch")]):
            ttk.Label(main_frame, text=label).grid(row=5+i, column=0, sticky='W')
            scale = ttk.Scale(main_frame, from_=0, to=1,
                            orient=tk.HORIZONTAL,
                            command=getattr(self, f'change_{var}'))
            scale.set(getattr(self, var))
            scale.grid(row=5+i, column=1, columnspan=3, sticky='EW', pady=5)
        
        # PTT
        self.ptt_button = ttk.Button(main_frame, text="APPUYER POUR PARLER (PTT)",
                                   command=self.ptt_action)
        self.ptt_button.grid(row=7, column=0, columnspan=4, pady=10)
        
        # Indicateurs
        indicator_frame = ttk.Frame(main_frame)
        indicator_frame.grid(row=8, column=0, columnspan=4, sticky='EW')
        
        self.rx_label = ttk.Label(indicator_frame, text="RX: Inactif",
                                background='gray')
        self.rx_label.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.tx_label = ttk.Label(indicator_frame, text="TX: Inactif",
                                background='gray')
        self.tx_label.pack(side=tk.RIGHT, expand=True, padx=2)
        
        # Démarrer la réception
        self.start_receiving()
        
    def change_band(self, event=None):
        old_band = self.current_band
        self.current_band = self.band_var.get()
        min_freq, max_freq = self.bands[self.current_band]
        
        # Ajuster la fréquence pour la nouvelle bande
        if old_band != self.current_band:
            self.frequency = min_freq
            self.freq_var.set(f"{self.frequency:.3f} MHz")
            self.freq_scale.set(0)  # Reset le slider
            
    def change_frequency(self, value):
        min_freq, max_freq = self.bands[self.current_band]
        freq_range = max_freq - min_freq
        
        if self.current_band == "2m":
            # Pas de 12.5KHz pour la bande 2m
            steps = round(float(value) * (freq_range * 1250)) / 1250
            self.frequency = min_freq + steps
        else:
            # Pas de 1KHz pour les autres bandes
            steps = round(float(value) * (freq_range * 1000)) / 1000
            self.frequency = min_freq + steps
            
        self.freq_var.set(f"{self.frequency:.3f} MHz")

    def change_mode(self):
        self.mode = self.mode_var.get()
        
    def change_volume(self, value):
        self.volume = float(value)
        
    def change_squelch(self, value):
        self.squelch = float(value)
        
    def ptt_action(self):
        if not self.is_transmitting:
            self.start_transmitting()
        else:
            self.stop_transmitting()
            
    def start_transmitting(self):
        self.is_transmitting = True
        self.tx_label.configure(background='red')
        self.ptt_button.configure(style='Transmit.TButton')
        threading.Thread(target=self.transmit_simulation, daemon=True).start()
        
    def stop_transmitting(self):
        self.is_transmitting = False
        self.tx_label.configure(background='gray')
        self.ptt_button.configure(style='TButton')
        
    def start_receiving(self):
        self.is_receiving = True
        threading.Thread(target=self.receive_simulation, daemon=True).start()
        
    def transmit_simulation(self):
        while self.is_transmitting:
            level = random.uniform(0.7, 0.95)
            self.root.after(0, self.s_meter.set_value, level)
            time.sleep(0.1)
        self.root.after(0, self.s_meter.set_value, 0)
        
    def receive_simulation(self):
        while self.is_receiving:
            if not self.is_transmitting:
                signal_level = random.uniform(0.7, 0.95)
                if signal_level > self.squelch:
                    self.root.after(0, lambda: self.rx_label.configure(background='green'))
                else:
                    self.root.after(0, lambda: self.rx_label.configure(background='gray'))
                self.root.after(0, self.s_meter.set_value, signal_level)
            time.sleep(0.3)
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    radio = RadioAmateur()
    radio.run()
