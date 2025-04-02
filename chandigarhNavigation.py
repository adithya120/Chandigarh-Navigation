import tkinter as tk
from tkinter import ttk
import webbrowser
import heapq
from PIL import Image, ImageTk

# Chandigarh Map (Simplified)
chandigarh_map = {
    "Sector 17": {"Sector 22": 3, "Sector 35": 4, "Sector 9": 2},
    "Sector 22": {"Sector 17": 3, "Sector 35": 2, "Sector 43": 5},
    "Sector 35": {"Sector 17": 4, "Sector 22": 2, "Sector 43": 3, "Sector 48": 6},
    "Sector 43": {"Sector 22": 5, "Sector 35": 3, "Sector 48": 2, "Sector 1": 7},
    "Sector 48": {"Sector 35": 6, "Sector 43": 2, "Sector 1": 4},
    "Sector 9": {"Sector 17": 2, "Sector 1": 5},
    "Sector 1": {"Sector 9": 5, "Sector 48": 4, "Sector 43": 7}
}

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        if current_node == end:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            return current_distance, path[::-1]

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return float('inf'), []

def find_shortest_path():
    start_sector = start_combobox.get()
    end_sector = end_combobox.get()

    distance, path = dijkstra(chandigarh_map, start_sector, end_sector)

    if distance == float('inf'):
        result_label.config(text="No path found.", foreground="red")
    else:
        result_label.config(text=f"Shortest distance: {distance} km\nPath: {' -> '.join(path)}", foreground="green")

def open_map():
    start_sector = start_combobox.get()
    end_sector = end_combobox.get()
    if start_sector and end_sector:
        query = f"https://www.google.com/maps/dir/{start_sector.replace(' ', '+')}/{end_sector.replace(' ', '+')}"
        webbrowser.open_new(query)
    else:
        result_label.config(text="Please select start and end sectors.", foreground="red")

# Tkinter GUI
window = tk.Tk()
window.title("Chandigarh Navigator")
window.geometry("600x400")  # Increased window size

# Background Image
try:
    bg_image = Image.open("chandigarh_bg.jpeg")  # Replace with your image path
    bg_photo = ImageTk.PhotoImage(bg_image.resize((600, 400)))
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except FileNotFoundError:
    print("Background image not found. Using default background.")

# Sector Selection
sectors = list(chandigarh_map.keys())

start_label = tk.Label(window, text="Start Sector:", bg="lightblue", font=("Arial", 12))
start_label.pack(pady=5)
start_combobox = ttk.Combobox(window, values=sectors, font=("Arial", 10))
start_combobox.pack(pady=5)

end_label = tk.Label(window, text="End Sector:", bg="lightblue", font=("Arial", 12))
end_label.pack(pady=5)
end_combobox = ttk.Combobox(window, values=sectors, font=("Arial", 10))
end_combobox.pack(pady=5)

find_button = tk.Button(window, text="Find Path", command=find_shortest_path, bg="green", fg="white", font=("Arial", 12))
find_button.pack(pady=10)

map_button = tk.Button(window, text="Open in Map", command=open_map, bg="blue", fg="white", font=("Arial", 12))
map_button.pack(pady=10)

result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack(pady=10)

window.mainloop()