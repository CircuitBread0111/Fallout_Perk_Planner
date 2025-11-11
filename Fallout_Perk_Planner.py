#!/usr/bin/env python3
#//////////////////////////
#|File: Fallout_Perk_Planner.py
#|Author: Jerrin C. Redmon
#|Version: 1.0.0
#|Date: November 10, 2025
#//////////////////////////

# Description #
# This script provides a Tkinter GUI to build Fallout 4 perk plans.
# It reads a flattened perks JSON, displays perk options with images,
# and generates/saves/preview a perk progression plan.

#-----------------------------------------------------------------

# Imports #
import tkinter as tk                                                                                                            # Tkinter main module for GUI
from tkinter import ttk, messagebox                                                                                             # ttk widgets and message box dialogs
from collections import defaultdict                                                                                             # default dict for grouping perks
import json                                                                                                                     # JSON parsing for perks data
import os                                                                                                                       # OS utilities (paths, listing, rename)
import re                                                                                                                       # Regular expressions for name normalization

# File Paths / Data #
with open("perks_flattened_full.json") as f:                                                                                    # Open flattened perks JSON file
    flattened_perks = json.load(f)                                                                                              # Load list of perk entries

# Initialize GUI #
root = tk.Tk()                                                                                                                  # Create the main Tk window
root.title("Fallout 4 Perk Planner")                                                                                            # Set window title
root.geometry("650x750")                                                                                                        # Set initial window size
root.configure(bg="#003366")                                                                                                    # Set background color

# Style Configuration #
style = ttk.Style()                                                                                                             # ttk Style object for themed widgets
style.theme_use('default')                                                                                                      # Use default theme for consistency
style.configure('.', background='#003366', foreground='#FFD700', fieldbackground='#003366')                                     # Base colors
style.configure('TLabel', background='#003366', foreground='#FFD700')                                                           # Label colors
style.configure('TButton', background='#003366', foreground='#FFD700')                                                          # Button colors
style.configure('TFrame', background='#003366')                                                                                 # Frame background
style.configure('TNotebook', background='#003366')                                                                              # Notebook background
style.configure('TNotebook.Tab', background='#003366', foreground='#FFD700')                                                    # Tab default
style.map('TNotebook.Tab', background=[('selected', '#FFD700')], foreground=[('selected', '#003366')])                          # Tab selected mapping

# SPECIAL Value Text #
spinbox_fg = '#222'                                                                                                             # black foreground for spinboxes
spinbox_bg = '#fff'                                                                                                             # white background for spinboxes

# Dictionary #
special_vars = {}                                                                                                               # Dict of tk.IntVar for each SPECIAL stat

# SPECIAL Perk Tabs #
special_frame = ttk.LabelFrame(root, text="SPECIAL Stats")                                                                      # Frame for SPECIAL inputs
special_frame.pack(fill="x", padx=10, pady=10)                                                                                  # Pack frame horizontally
for i, stat in enumerate("S P E C I A L".split()):                                                                              # Loop through each SPECIAL stat
    var = tk.IntVar(value=10)                                                                                                   # Default SPECIAL value 10
    special_vars[stat] = var                                                                                                    # Store IntVar in dict
    ttk.Label(special_frame, text=stat).grid(row=0, column=i)                                                                   # Label for stat
    sb = ttk.Spinbox(special_frame, from_=1, to=10, width=5, textvariable=var)                                                  # Spinbox widget
    sb.grid(row=1, column=i)                                                                                                    # Place spinbox below label
    sb.configure(foreground=spinbox_fg, background=spinbox_bg)                                                                  # Apply color styling

# User Interface #
main_tabs = ttk.Notebook(root)                                                                                                  # Top-level notebook for main sections
main_tabs.pack(fill="both", expand=True, padx=10, pady=10)                                                                      # Fill available space
perk_tab = ttk.Frame(main_tabs)                                                                                                 # Frame for perk selection tab
main_tabs.add(perk_tab, text="Perk Selection")                                                                                  # Add perk selection tab
notebook = ttk.Notebook(perk_tab)                                                                                               # Inner notebook for SPECIAL tabs
notebook.pack(fill="both", expand=True, padx=10, pady=10)                                                                       # Pack inner notebook

# Perk Widget Registry #
perk_widgets = {}                                                                                                               # Dictionary to hold perk widgets

# Group Perks #
grouped_perks = defaultdict(set)                                                                                                # Map SPECIAL -> set of perks
for p in flattened_perks:                                                                                                       # Iterate loaded perk entries
    for stat, val in p["special"].items():                                                                                      # For each SPECIAL in perk
        grouped_perks[stat].add(p["perk"])                                                                                      # Add perk to that group's set

# Perk Collection #
perk_names_set = set()                                                                                                          # Set of unique perk names
for p in flattened_perks:                                                                                                       # Collect unique names from JSON
    perk_names_set.add(p["perk"])                                                                                               # Add perk name




# Utilities #
def normalize_name(name):                                                                                                       # Normalize filenames / perk names
    return re.sub(r'[^a-zA-Z0-9_]', '', name.replace(' ', '_')).lower()




# Image Scanning #
image_folder = "perk_images"                                                                                                    # Use the new folder for perk icons
perk_image_files = {}                                                                                                           # Map normalized name -> file path
if os.path.isdir(image_folder):                                                                                                 # Only scan if folder exists
    for fname in os.listdir(image_folder):                                                                                      # Iterate files in folder
        name, ext = os.path.splitext(fname)                                                                                     # Split name and extension
        if ext.lower() in [".png", ".jpg", ".jpeg", ".gif"]:                                                                    # Supported formats
            simple_name = normalize_name(name)                                                                                  # Normalize base name
            perk_image_files[simple_name] = os.path.join(image_folder, fname)                                                   # Store path



# Perk checklist #
for stat in "S P E C I A L":                                                                                                    # Iterate SPECIAL tabs S..L
                                                                                                                                # Build an ordered list of unique perks for this SPECIAL stat, in JSON order
    ordered_perks = []                                                                                                          # List[(required_special, perk_name)]
    seen = set()                                                                                                                # Track seen perk names for order
    for p in flattened_perks:                                                                                                   # Iterate all perk entries
        if stat in p["special"]:                                                                                                # If this perk affects current SPECIAL
            perk = p["perk"]                                                                                                    # Perk name
            if perk not in seen:                                                                                                # If not already added
                ordered_perks.append((p["special"][stat], perk))                                                                # Append tuple
                seen.add(perk)                                                                                                  # Mark as seen
                                                                                                                                # Only add a tab if there are perks for this stat
    if not ordered_perks:
        continue
    lf = ttk.Frame(notebook)                                                                                                    # Create frame for this stat tab
    notebook.add(lf, text=f"{stat}")                                                                                            # Add tab to inner notebook

                                                                                                                                # --- Add scrollable canvas ---
    canvas = tk.Canvas(lf, bg="#003366", highlightthickness=0)                                                                  # Canvas for scrolling content
    scrollbar = ttk.Scrollbar(lf, orient="vertical", command=canvas.yview)                                                      # Vertical scrollbar
    scroll_frame = ttk.Frame(canvas)                                                                                            # Frame inside canvas to hold widgets

    scroll_frame_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")                                            # Place frame
    canvas.configure(yscrollcommand=scrollbar.set)                                                                              # Connect scrollbar to canvas
    canvas.pack(side="left", fill="both", expand=True)                                                                          # Pack canvas left
    scrollbar.pack(side="right", fill="y")                                                                                      # Pack scrollbar right

    def _on_frame_configure(event, c=canvas, f=scroll_frame):
        c.configure(scrollregion=c.bbox("all"))                                                                                 # Update scrollregion when frame changes
    scroll_frame.bind("<Configure>", _on_frame_configure)                                                                       # Bind configure event

    def _on_mousewheel(event, c=canvas):
        c.yview_scroll(int(-1*(event.delta/120)), "units")                                                                      # Mousewheel scroll handler
    canvas.bind_all("<MouseWheel>", _on_mousewheel)                                                                             # Bind mousewheel globally

                                                                                                                                # Display perks in JSON order, no group headers
    for _, perk in ordered_perks:                                                                                               # For each perk in order
        f = ttk.Frame(scroll_frame)                                                                                             # Row frame for this perk
        f.pack(anchor="w", pady=6, padx=8)                                                                                      # Pack row with padding
        enabled = tk.BooleanVar()                                                                                               # BooleanVar for enabled checkbox
                                                                                                                                # Use normalized name for image lookup
        simple_perk = normalize_name(perk)                                                                                      # Normalized name for matching images
        img_path = perk_image_files.get(simple_perk)                                                                            # Lookup image path if present
        if img_path and os.path.exists(img_path):                                                                               # If image file exists
            try:
                                                                                                                                # Use PhotoImage for PNG, fallback to PIL for JPG/JPEG/GIF
                if img_path.lower().endswith('.png'):
                    perk_img = tk.PhotoImage(file=img_path)                                                                     # Native Tk image for PNG
                else:
                    try:
                        from PIL import Image, ImageTk                                                                          # PIL fallback for other formats
                        pil_img = Image.open(img_path).resize((32, 32))                                                         # Resize icon
                        perk_img = ImageTk.PhotoImage(pil_img)                                                                  # Convert PIL -> PhotoImage
                    except Exception:
                        perk_img = None                                                                                         # If PIL not available or failed
                if perk_img:
                    img_label = tk.Label(f, image=perk_img, bg="#003366")                                                       # Label to show image
                    img_label.image = perk_img                                                                                  # Keep a reference to prevent GC
                    img_label.pack(side="left", padx=(0, 8))
                else:
                    ttk.Label(f, text="[No Image]").pack(side="left", padx=(0, 8))                                              # Fallback text
            except Exception:
                ttk.Label(f, text="[No Image]").pack(side="left", padx=(0, 8))                                                  # On error fallback
        else:
            ttk.Label(f, text="[No Image]").pack(side="left", padx=(0, 8))                                                      # No image found
        ttk.Checkbutton(f, text=perk, variable=enabled).pack(side="left", padx=(0, 8))                                          # Perk checkbox
        ttk.Label(f, text="Ranks").pack(side="left", padx=(0, 2))                                                               # Label for ranks
        rank = tk.IntVar(value=1)                                                                                               # Rank IntVar default 1
        rank_slider = tk.Scale(f, from_=1, to=5, orient=tk.HORIZONTAL, variable=rank, length=120, fg='black', bg='#003366', highlightbackground='#003366') # Rank slider
        rank_slider.pack(side="left", padx=(0, 12))                                                                             # Pack rank slider
        ttk.Label(f, text="Priority").pack(side="left", padx=(0, 2))                                                            # Label for priority
        prio = tk.IntVar(value=1)                                                                                               # Priority IntVar default 1
        prio_slider = tk.Scale(f, from_=1, to=10, orient=tk.HORIZONTAL, variable=prio, length=120, fg='black', bg='#003366', highlightbackground='#003366') # Priority slider
        prio_slider.pack(side="left", padx=(0, 8))                                                                              # Pack priority slider
        perk_widgets[perk] = (enabled, rank, prio)                                                                              # Register widgets for this perk

# Generate Tab #
generate_tab = ttk.Frame(main_tabs)                                                                                             # Frame for Generate tab
main_tabs.add(generate_tab, text="Generate Plan")                                                                               # Add Generate Plan tab
tree = ttk.Treeview(generate_tab, columns=("Level", "Perk", "Rank"), show="headings")                                           # Treeview to show plantree.heading("Level", text="Level")                                                                 # Column heading Level
tree.heading("Perk", text="Perk")                                                                                               # Column heading Perktree.heading("Rank", text="Rank")                                                                   # Column heading Rank
tree.pack(fill="both", expand=True, padx=10, pady=10)                                                                           # Pack the treeview


# Save Tab #
save_tab = ttk.Frame(main_tabs)                                                                                                 # Frame for Save tab
main_tabs.add(save_tab, text="Save Plan")                                                                                       # Add Save Plan tab


# Preview Tab #
preview_tab = ttk.Frame(main_tabs)                                                                                              # Frame for Preview tab
main_tabs.add(preview_tab, text="Print Preview")                                                                                # Add Print Preview tab

# Plan generation #
plan = {}

# Check SPECIAL Requirements
def meets_special(player_special, perk_special):
    return True                                                                                                                 # SPECIAL check disabled (assume all 10)

# Generate Perk Plan #
def generate_plan():
    global plan
    selected_perks = {}                                                                                                         # Collect selected perks and settings
    for perk, (enabled_var, rank_var, priority_var) in perk_widgets.items():
        if enabled_var.get():                                                                                                   # If checkbox enabled
            selected_perks[perk] = {
                "max_rank": rank_var.get(),                                                                                     # User chosen max rank for perk
                "priority": priority_var.get()                                                                                  # User chosen priority for perk
            }

    if not selected_perks:
        messagebox.showerror("Error", "Select at least one perk.")                                                              # Require selection
        return

    special_input = {k: v.get() for k, v in special_vars.items()}                                                               # Current SPECIAL values
    used = set()                                                                                                                # Set of (perk, rank) already planned
    progress = {perk: 0 for perk in selected_perks}                                                                             # Track current rank progress per perk
    plan = {}                                                                                                                   # Resulting plan mapping level -> perk entry

    for level in range(2, 101):                                                                                                 # Iterate levels 2..100
        available = []                                                                                                          # Candidate perk ranks available at this level
        for p in flattened_perks:                                                                                               # Consider each perk/rank entry
            perk = p["perk"]                                                                                                    # Perk name
            rank = p["rank"]                                                                                                    # Rank number for this entry
            if perk not in selected_perks:                                                                                      # Skip perks user didn't enable
                continue
            max_rank = selected_perks[perk]["max_rank"]                                                                         # User max rank
            priority = selected_perks[perk]["priority"]                                                                         # User priority
            if (perk, rank) in used or rank > max_rank:                                                                         # Skip if already used or beyond max
                continue
            if progress[perk] != rank - 1:                                                                                      # Ensure rank progression (must be next)
                continue
            if level < p["min_level"]:                                                                                          # Skip until min level reached
                continue
            if not meets_special(special_input, p["special"]):                                                                  # Check SPECIAL reqs
                continue
            available.append((priority, p["min_level"], p["rank"], p))                                                          # Add candidate

        if available:
            available.sort(key=lambda x: (x[0], x[1], x[2]))                                                                    # Sort by priority, min_level, rank
            chosen = available[0][3]                                                                                            # Choose top candidate
            used.add((chosen["perk"], chosen["rank"]))                                                                          # Mark used
            progress[chosen["perk"]] = chosen["rank"]                                                                           # Update progress
            plan[level] = chosen                                                                                                # Record in plan
        else:
            plan[level] = None                                                                                                  # No perk at this level

    for i in tree.get_children():                                                                                               # Clear existing tree rows
        tree.delete(i)
    for lvl in range(2, 101):                                                                                                   # Populate tree with plan
        p = plan[lvl]
        if p:
            tree.insert("", "end", values=(lvl, p["perk"], p["rank"]))
        else:
            tree.insert("", "end", values=(lvl, "-", "-"))

# Export Perk Plan to Text File #
def export_plan():
    filepath = "perk_plan_output.txt"                                                                                           # Output filename
    special_input = {k: v.get() for k, v in special_vars.items()}                                                               # Current SPECIAL values
    with open(filepath, "w") as f:                                                                                              # Write formatted text file
        f.write("Fallout 4 Perk Planner Output\n")
        f.write("===================================\n\n")
        f.write("SPECIAL distribution:\n")
        for stat in "S P E C I A L".split():
            f.write(f"  {stat}: {special_input.get(stat, 0)}\n")                                                                # Write each SPECIAL value
        f.write("\n")
        f.write("+--------+----------------------+------+\n")
        f.write("| Level  | Perk                 | Rank |\n")
        f.write("+--------+----------------------+------+\n")
        for lvl in range(2, 101):
            p = plan.get(lvl)
            if p:
                f.write("| {:<6} | {:<20} | {:<4} |\n".format(lvl, p["perk"], p["rank"]))                                       # Write perk row
            else:
                f.write("| {:<6} | {:<20} | {:<4} |\n".format(lvl, "-", "-"))                                                   # Empty row
        f.write("+--------+----------------------+------+\n")
    messagebox.showinfo("Saved", f"Perk plan saved to {filepath}")                                                              # Notify user

def generate_plan_and_update_tree():
    global plan
    generate_plan()                                                                                                             # Generate plan and rely on generate_plan to update tree


ttk.Button(generate_tab, text="Generate Perk Plan", command=generate_plan_and_update_tree).pack(pady=10)                        # Generate button

def export_plan_tab():
    export_plan()                                                                                                               # Invoke export_plan when Save button pressed

ttk.Button(save_tab, text="Save Plan to File", command=export_plan_tab).pack(pady=20)                                           # Save button

# Preview Tab Display #
def show_preview_tab():
    global plan
    for widget in preview_tab.winfo_children():
        widget.destroy()                                                                                                        # Clear existing preview widgets
    text_widget = tk.Text(preview_tab, wrap=tk.NONE, font=("Courier", 10), bg="#003366", fg="#FFD700")                          # Text widget for preview
    text_widget.pack(fill=tk.BOTH, expand=True)                                                                                 # Fill available preview space
    special_input = {k: v.get() for k, v in special_vars.items()}                                                               # Current SPECIAL values
    text_widget.insert(tk.END, "Fallout 4 Perk Planner Output\n")
    text_widget.insert(tk.END, "="*35 + "\n\n")
    text_widget.insert(tk.END, "SPECIAL distribution:\n")
    for stat in "S P E C I A L".split():
        text_widget.insert(tk.END, f"  {stat}: {special_input.get(stat, 0)}\n")                                                 # Insert SPECIAL values
    text_widget.insert(tk.END, "+--------+----------------------+------+\n")
    text_widget.insert(tk.END, "| Level  | Perk                 | Rank |\n")
    text_widget.insert(tk.END, "+--------+----------------------+------+\n")
    for lvl in range(2, 101):
        p = plan.get(lvl)
        if p:
            text_widget.insert(tk.END, "| {:<6} | {:<20} | {:<4} |\n".format(lvl, p["perk"], p["rank"]))                        # Insert perk row
        else:
            text_widget.insert(tk.END, "| {:<6} | {:<20} | {:<4} |\n".format(lvl, "-", "-"))                                    # Insert empty row
    text_widget.insert(tk.END, "+--------+----------------------+------+\n")

refresh_btn = ttk.Button(preview_tab, text="Refresh Preview", command=show_preview_tab)                                         # Refresh preview button
refresh_btn.pack(pady=10)

main_tabs.bind("<<NotebookTabChanged>>", lambda e: show_preview_tab() if main_tabs.index('current') == main_tabs.tabs().index(main_tabs.tabs()[-1]) else None) # Auto-refresh preview when last tab selected

folder = 'images'                                                                                                               # Folder to sanitize filenames in
if os.path.isdir(folder):                                                                                                       # If images folder exists
    for fname in os.listdir(folder):                                                                                            # Iterate files
        name, ext = os.path.splitext(fname)                                                                                     # Split name and extension
        new_name = re.sub(r'[^a-zA-Z0-9_]', '', name.replace(' ', '_')).lower() + ext.lower()                                   # Sanitized filename
        src = os.path.join(folder, fname)                                                                                       # Source path
        dst = os.path.join(folder, new_name)                                                                                    # Destination path
        if src != dst and not os.path.exists(dst):                                                                              # Avoid overwriting existing sanitized files
            os.rename(src, dst)                                                                                                 # Rename file
print('Renaming complete.')                                                                                                     # Log completion

# Mainloop #
root.mainloop()                                                                                                                 # Start Tkinter event loop
# EOF #
