import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def convert_files(folder_path, status_label, progress_bar, root):
    if not folder_path:
        messagebox.showerror("Feil", "Vennligst velg en mappe først.")
        return

    # Finn alle AIFF-filer (både .aiff og .aif)
    aiff_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.aiff', '.aif'))]
    
    if not aiff_files:
        messagebox.showwarning("Ingen filer", "Fant ingen AIFF-filer i den valgte mappen.")
        return

    progress_bar["maximum"] = len(aiff_files)
    progress_bar["value"] = 0

    success_count = 0
    for i, filename in enumerate(aiff_files):
        input_path = os.path.join(folder_path, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(folder_path, f"{base_name}.flac")

        status_label.config(text=f"Konverterer ({i+1}/{len(aiff_files)}): {filename}")
        root.update_idletasks()

        # FFmpeg-kommando for hi-res FLAC konvertering
        cmd = ['ffmpeg', '-y', '-i', input_path, '-c:a', 'flac', output_path]
        
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                success_count += 1
            else:
                print(f"Feil ved konvertering av {filename}: {result.stderr}")
        except Exception as e:
            print(f"Feil: {e}")

        progress_bar["value"] = i + 1

    status_label.config(text=f"Ferdig! Konverterte {success_count} av {len(aiff_files)} filer.")
    messagebox.showinfo("Fullført", f"Konverteringen er ferdig!\n{success_count} av {len(aiff_files)} filer ble konvertert til FLAC.")

def start_conversion(folder_entry, status_label, progress_bar, root):
    folder_path = folder_entry.get()
    # Kjører i egen tråd slik at grensesnittet ikke henger seg opp under konvertering
    threading.Thread(target=convert_files, args=(folder_path, status_label, progress_bar, root), daemon=True).start()

def browse_folder(folder_entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

def main():
    root = tk.Tk()
    root.title("AIFF til Hi-Res FLAC Konverterer")
    root.geometry("480x260")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use('clam')

    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    title_label = ttk.Label(frame, text="AIFF til Hi-Res FLAC", font=("Helvetica", 14, "bold"))
    title_label.pack(pady=(0, 15))

    # Mappe-velger
    folder_frame = ttk.Frame(frame)
    folder_frame.pack(fill=tk.X, pady=5)

    folder_entry = ttk.Entry(folder_frame, width=35)
    folder_entry.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)

    browse_btn = ttk.Button(folder_frame, text="Velg mappe...", command=lambda: browse_folder(folder_entry))
    browse_btn.pack(side=tk.RIGHT)

    # Status og fremgang
    status_label = ttk.Label(frame, text="Klar til å velge mappe", font=("Helvetica", 10))
    status_label.pack(pady=(15, 5))

    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=5, fill=tk.X)

    # Start-knapp
    convert_btn = ttk.Button(frame, text="Start Konvertering", command=lambda: start_conversion(folder_entry, status_label, progress_bar, root))
    convert_btn.pack(pady=(15, 0))

    root.mainloop()

if __name__ == "__main__":
    main()
