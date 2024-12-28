import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Function to load the dataset
def load_dataset():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            print(f"Selected file: {file_path}")  # Debugging line to check the file path
            global data
            data = pd.read_csv(file_path)
            print(f"Data loaded: {data.head()}")  # Debugging line to check the first few rows of the data
            messagebox.showinfo("File Loaded", f"Dataset loaded successfully from {os.path.basename(file_path)}!")
            analyze_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the dataset. Error: {str(e)}")
    else:
        messagebox.showerror("File Selection", "No file was selected!")

# Function to check if the dataset is loaded
def check_data_loaded():
    if 'data' not in globals():
        messagebox.showerror("Data Not Loaded", "Please upload a dataset first.")
        return False
    return True

# Function to analyze basic statistics and display in GUI
def analyze_data():
    if not check_data_loaded():
        return
    mean_price = data['Cost in Rs. (CR)'].mean()
    median_price = data['Cost in Rs. (CR)'].median()
    mode_price = data['Cost in Rs. (CR)'].mode()[0]
    std_dev_price = data['Cost in Rs. (CR)'].std()
    variance_price = data['Cost in Rs. (CR)'].var()
    price_range = data['Cost in Rs. (CR)'].max() - data['Cost in Rs. (CR)'].min()

    result_text.set(f"Mean Price: {mean_price:.2f} Cr\n"
                    f"Median Price: {median_price:.2f} Cr\n"
                    f"Mode Price: {mode_price:.2f} Cr\n"
                    f"Standard Deviation: {std_dev_price:.2f} Cr\n"
                    f"Variance: {variance_price:.2f} Cr\n"
                    f"Price Range: {price_range:.2f} Cr")

# Function to plot top players by auction price
def plot_top_players():
    if not check_data_loaded():
        return
    top_players = data.groupby('Player Name')['Cost in Rs. (CR)'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 8))
    top_players.plot(kind='bar', color='orange', ax=ax, title='Top Players by Auction Price')
    ax.set_xlabel('Player')
    ax.set_ylabel('Price (in Crores)')
    ax.set_xticklabels(top_players.index, rotation=45)
    display_plot(fig)

# Function to plot team spending analysis
def plot_team_spending():
    if not check_data_loaded():
        return
    team_spending = data.groupby('2023 Squad')['Cost in Rs. (CR)'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    team_spending.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette("Set2"), ax=ax, title='Total Spending by Team')
    ax.set_ylabel('')
    display_plot(fig)

# Function to plot average team spending
def plot_average_team_spending():
    if not check_data_loaded():
        return
    avg_team_spending = data.groupby('2023 Squad')['Cost in Rs. (CR)'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_team_spending.plot(kind='bar', color='skyblue', ax=ax, title='Average Player Price by Team')
    ax.set_xlabel('Team')
    ax.set_ylabel('Average Price (in Crores)')
    ax.set_xticklabels(avg_team_spending.index, rotation=45)
    display_plot(fig)

# Function to plot player price distribution
def plot_price_distribution():
    if not check_data_loaded():
        return
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['Cost in Rs. (CR)'], bins=20, kde=True, ax=ax)
    ax.set_title('Distribution of Player Prices')
    ax.set_xlabel('Price (in Crores)')
    ax.set_ylabel('Frequency')
    display_plot(fig)

# Function to plot spending by player role
def plot_role_spending():
    if not check_data_loaded():
        return
    role_spending = data.groupby('Type')['Cost in Rs. (CR)'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    role_spending.plot(kind='bar', color='lightgreen', ax=ax, title='Total Spending by Player Role')
    ax.set_xlabel('Role')
    ax.set_ylabel('Total Price (in Crores)')
    ax.set_xticklabels(role_spending.index, rotation=45)
    display_plot(fig)

# Function to search player details
def search_player():
    if not check_data_loaded():
        return
    player_name = search_entry.get().strip().lower()
    if player_name == "":
        messagebox.showwarning("Input Error", "Please enter a valid player name.")
        return

    player_data = data[data['Player Name'].str.lower() == player_name]
    
    if player_data.empty:
        result_text.set(f"No player found with name: {player_name.capitalize()}")
    else:
        details = player_data.iloc[0]
        details_text = (f"Player Name: {details['Player Name']}\n"
                        f"Team: {details['2023 Squad']}\n"
                        f"Role: {details['Type']}\n"
                        f"Price: {details['Cost in Rs. (CR)']} Crores\n")
        result_text.set(details_text)

# Function to display plot within the scrollable canvas
def display_plot(fig):
    for widget in canvas_frame.winfo_children():
        widget.destroy()  # Clear previous plots

    canvas_plot = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_plot.draw()
    canvas_widget = canvas_plot.get_tk_widget()
    canvas_widget.pack()

# Function to save the analysis results to CSV
def save_analysis_results():
    if not check_data_loaded():
        return
    team_spending = data.groupby('2023 Squad')['Cost in Rs. (CR)'].sum()
    save_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV Files", "*.csv")])
    if save_path:
        team_spending.to_csv(save_path, header=True)
        messagebox.showinfo("Save Successful", f"Analysis results saved to {os.path.basename(save_path)}!")

# Creating the Tkinter GUI window
window = tk.Tk()
window.title("IPL 2023 Auction Analysis")
window.geometry("850x600")

# Create a frame for the canvas
main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas to contain the content
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside the canvas
content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Create a frame within the scrollable area to hold the content
canvas_frame = tk.Frame(content_frame)
canvas_frame.pack()

# Upload Button
upload_btn = tk.Button(content_frame, text="Upload Dataset", command=load_dataset, bg="lightblue", font=('Arial', 12))
upload_btn.pack(pady=10)

# Label for displaying results
result_text = tk.StringVar()
result_label = tk.Label(content_frame, textvariable=result_text, font=('Arial', 12), justify="left")
result_label.pack(pady=10)

# Player Search Entry and Button
search_label = tk.Label(content_frame, text="Search Player:", font=('Arial', 12))
search_label.pack(pady=5)
search_entry = tk.Entry(content_frame, font=('Arial', 12))
search_entry.pack(pady=5)
search_btn = tk.Button(content_frame, text="Find Player", command=search_player, bg="lightgreen", font=('Arial', 12))
search_btn.pack(pady=5)

# Buttons to trigger analysis and visualizations
top_players_btn = tk.Button(content_frame, text="Plot Top Players by Auction Price", command=plot_top_players, bg="orange", font=('Arial', 12))
top_players_btn.pack(pady=10)

team_spending_btn = tk.Button(content_frame, text="Plot Team Spending Analysis", command=plot_team_spending, bg="lightgreen", font=('Arial', 12))
team_spending_btn.pack(pady=10)

avg_team_spending_btn = tk.Button(content_frame, text="Plot Average Player Price by Team", command=plot_average_team_spending, bg="skyblue", font=('Arial', 12))
avg_team_spending_btn.pack(pady=10)

price_distribution_btn = tk.Button(content_frame, text="Plot Price Distribution", command=plot_price_distribution, bg="purple", font=('Arial', 12))
price_distribution_btn.pack(pady=10)

role_spending_btn = tk.Button(content_frame, text="Plot Spending by Player Role", command=plot_role_spending, bg="lightpink", font=('Arial', 12))
role_spending_btn.pack(pady=10)

save_analysis_btn = tk.Button(content_frame, text="Save Analysis Results", command=save_analysis_results, bg="lightcoral", font=('Arial', 12))
save_analysis_btn.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()
