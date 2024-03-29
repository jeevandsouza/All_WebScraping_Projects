from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import ttk
import schedule
import time

def update_table():
    data_to_scrape = requests.get("https://www.premierleague.com/tables")
    soup = BeautifulSoup(data_to_scrape.text, "html.parser")

    for item in tree.get_children():
        tree.delete(item)

    team_elements = soup.find_all("td", class_="league-table__team team")

    i = 0
    for team_element in team_elements:
        team_name = team_element.find("span", class_="league-table__team-name--long").text.strip()
        td_list = []
        curr_element  = team_element
        for _ in range(6):
            curr_element = curr_element.find_next_sibling("td")
            td_list.append(curr_element.text)
        points_element = team_element.find_next_sibling("td", class_="league-table__points")
        points = points_element.text.strip() if points_element else "N/A"
        tree.insert("", "end", values=(team_name, td_list[0], td_list[1], td_list[2], td_list[3], td_list[4], points))
        i = i+1
        if(i >= 20): #junk values were adding up so limit it to first 20 values
            break

# Initial table creation
root = tk.Tk()
root.title("Premier League Table")

style = ttk.Style()
style.configure("Treeview", background="aaa7cc", fieldbackground="#aaa7cc", foreground="black", font=("Arial", 10))
style.map("Treeview", background=[('selected', '#aaa7cc')])
# Create Treeview
tree = ttk.Treeview(root, columns=("Team", "Won", "Drawn", "Lost", "Goals Scored", "Goals Conceded", "Points"), show="headings")
tree.heading("Team", text="Team", anchor="center")
tree.heading("Won", text="Won", anchor="center")
tree.heading("Drawn", text="Drawn", anchor="center")
tree.heading("Lost", text="Lost", anchor="center")
tree.heading("Goals Scored", text="Goals Scored", anchor="center")
tree.heading("Goals Conceded", text="Goals Conceded", anchor="center")
tree.heading("Points", text="Points", anchor="center")

# Initial data fetch and table update
update_table()

tree.pack(fill="both", expand=True)
window_width = 800
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width/2) - (window_width/2)
y_coordinate = (screen_height/2) - (window_height/2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
root.mainloop()

# Schedule the update every day at a specific time (e.g., 00:00)
schedule.every().day.at("00:00").do(update_table)

# Keep the script running to allow scheduled updates
while True:
    schedule.run_pending()
    time.sleep(1)
