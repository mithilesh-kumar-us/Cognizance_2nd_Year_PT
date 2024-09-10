import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

# Establish a connection to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Update with my MySQL password
    database="Skyway_airline"
)

# Create a cursor object to execute SQL queries
db_cursor = db_connection.cursor()

class AirlineSystem:
    def __init__(self, window):
        self.window = window
        self.window.title("Skyway Airline System")
        self.window.geometry("800x600")

        # Load background image
        self.bg_image = Image.open("/Users/mithileshus/Desktop/RDBMS/Background.jpeg")
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.bg_image)

        # Canvas for background image
        self.bg_canvas = tk.Canvas(self.window, width=800, height=600)
        self.bg_canvas.pack(fill=tk.BOTH, expand=True)
        self.bg_canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Call the login page first
        self.create_login_screen()

    def create_login_screen(self):
        # Clear the current canvas to prepare for login form
        self.bg_canvas.delete("all")
        self.bg_canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Create a login form
        login_frame = tk.Frame(self.bg_canvas, bg="white", bd=5)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        user_label = ttk.Label(login_frame, text="Username:", font=("Arial", 12))
        user_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        pass_label = ttk.Label(login_frame, text="Password:", font=("Arial", 12))
        pass_label.grid(row=1, column=0, padx=10, pady=10)
        self.pass_entry = ttk.Entry(login_frame, show="*")
        self.pass_entry.grid(row=1, column=1, padx=10, pady=10)

        login_btn = ttk.Button(login_frame, text="Login", command=self.check_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def check_login(self):
        user = self.username_entry.get()
        passwd = self.pass_entry.get()

        db_cursor.execute("SELECT * FROM users WHERE user_id = %s AND password = %s", (user, passwd))
        result = db_cursor.fetchone()

        if result:
            messagebox.showinfo("Login Successful", "Welcome!")
            self.load_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def load_main_interface(self):
        # Clear the login screen and show the flight management system
        self.bg_canvas.delete("all")
        self.bg_canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Create the main system content here
        self.main_frame = tk.Frame(self.bg_canvas, bg="white", bd=5)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a notebook with tabs for available flights, booked flights, and booking/cancellation
        tab_control = ttk.Notebook(self.main_frame)
        tab_control.pack(pady=10, expand=True)

        self.available_tab = ttk.Frame(tab_control)
        self.booked_tab = ttk.Frame(tab_control)
        self.booking_tab = ttk.Frame(tab_control)

        tab_control.add(self.available_tab, text="Available Flights")
        tab_control.add(self.booked_tab, text="Booked Flights")
        tab_control.add(self.booking_tab, text="Book Flight")

        # Search section for available flights
        self.search_frame = ttk.Frame(self.available_tab)
        self.search_frame.pack(pady=10, fill=tk.X)

        self.start_label = ttk.Label(self.search_frame, text="Search Start Location:")
        self.start_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.search_btn = ttk.Button(self.search_frame, text="Search", command=self.search_flights)
        self.search_btn.pack(side=tk.RIGHT, padx=5)

        # Create a treeview to display available flights
        self.flights_tree = ttk.Treeview(self.available_tab)
        self.flights_tree["columns"] = ("flight_id", "start", "destination", "fare", "departure", "arrival")

        self.flights_tree.column("#0", width=0, stretch=tk.NO)
        self.flights_tree.column("flight_id", anchor=tk.W, width=100)
        self.flights_tree.column("start", anchor=tk.W, width=100)
        self.flights_tree.column("destination", anchor=tk.W, width=100)
        self.flights_tree.column("fare", anchor=tk.W, width=50)
        self.flights_tree.column("departure", anchor=tk.W, width=150)
        self.flights_tree.column("arrival", anchor=tk.W, width=150)

        self.flights_tree.heading("#0", text="", anchor=tk.W)
        self.flights_tree.heading("flight_id", text="Flight ID", anchor=tk.W)
        self.flights_tree.heading("start", text="Start", anchor=tk.W)
        self.flights_tree.heading("destination", text="Destination", anchor=tk.W)
        self.flights_tree.heading("fare", text="Fare", anchor=tk.W)
        self.flights_tree.heading("departure", text="Departure Time", anchor=tk.W)
        self.flights_tree.heading("arrival", text="Arrival Time", anchor=tk.W)

        self.flights_tree.pack(fill=tk.BOTH, expand=True)

        # Create a treeview to display booked flights
        self.bookings_tree = ttk.Treeview(self.booked_tab)
        self.bookings_tree["columns"] = ("book_id", "user", "flight_id", "date")

        self.bookings_tree.column("#0", width=0, stretch=tk.NO)
        self.bookings_tree.column("book_id", anchor=tk.W, width=50)
        self.bookings_tree.column("user", anchor=tk.W, width=100)
        self.bookings_tree.column("flight_id", anchor=tk.W, width=100)
        self.bookings_tree.column("date", anchor=tk.W, width=150)

        self.bookings_tree.heading("#0", text="", anchor=tk.W)
        self.bookings_tree.heading("book_id", text="Booking ID", anchor=tk.W)
        self.bookings_tree.heading("user", text="User", anchor=tk.W)
        self.bookings_tree.heading("flight_id", text="Flight ID", anchor=tk.W)
        self.bookings_tree.heading("date", text="Booking Date", anchor=tk.W)

        self.bookings_tree.pack(fill=tk.BOTH, expand=True)

        # Cancel flight section
        self.cancel_frame = ttk.Frame(self.booked_tab)
        self.cancel_frame.pack(pady=10, anchor="e")

        self.cancel_btn = ttk.Button(self.cancel_frame, text="Cancel Flight", command=self.cancel_booking)
        self.cancel_btn.pack()

        # Create a form to book a flight
        self.book_form = ttk.Frame(self.booking_tab)
        self.book_form.pack(fill=tk.BOTH, expand=True)

        # Booking section
        self.book_sec = ttk.Frame(self.book_form)
        self.book_sec.pack(pady=20)

        self.user_lbl = ttk.Label(self.book_sec, text="User Name:")
        self.user_lbl.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.user_input = ttk.Entry(self.book_sec)
        self.user_input.grid(row=0, column=1, padx=5, pady=5)

        self.flight_lbl = ttk.Label(self.book_sec, text="Flight ID:")
        self.flight_lbl.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.flight_input = ttk.Entry(self.book_sec)
        self.flight_input.grid(row=1, column=1, padx=5, pady=5)

        self.book_flight_btn = ttk.Button(self.book_sec, text="Book Flight", command=self.book_a_flight)
        self.book_flight_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Load available flights and booked flights
        self.populate_available_flights()
        self.populate_booked_flights()

    def populate_available_flights(self):
        # Fetch available flights from the database
        db_cursor.execute("SELECT * FROM available_flights")
        flights = db_cursor.fetchall()

        # Clear current items in the treeview
        self.flights_tree.delete(*self.flights_tree.get_children())

        # Insert flights into the treeview
        for flight in flights:
            self.flights_tree.insert("", tk.END, values=flight)

    def populate_booked_flights(self):
        # Fetch booked flights from the database
        db_cursor.execute("SELECT * FROM bookings")
        bookings = db_cursor.fetchall()

        # Clear current items in the treeview
        self.bookings_tree.delete(*self.bookings_tree.get_children())

        # Insert bookings into the treeview
        for booking in bookings:
            self.bookings_tree.insert("", tk.END, values=booking)

    def book_a_flight(self):
        # Get the user name and flight number from the form
        user_name = self.user_input.get()
        flight_id = self.flight_input.get()

        # Check if the flight number is valid and available
        db_cursor.execute("SELECT * FROM available_flights WHERE flight_id = %s", (flight_id,))
        flight = db_cursor.fetchone()

        if flight:
            # Book the flight
            db_cursor.execute("INSERT INTO bookings (user_name, flight_id) VALUES (%s, %s)",
                            (user_name, flight_id))
            db_connection.commit()

            # Show success message
            messagebox.showinfo("Success", f"Flight {flight_id} booked successfully!")
            # Refresh the available flights and booked flights
            self.populate_available_flights()
            self.populate_booked_flights()
        else:
            # Show error message
            messagebox.showerror("Error", f"Flight {flight_id} not found.")

    def search_flights(self):
        # Get the search term from the entry
        search_term = self.search_entry.get()

        # Clear the current contents of the treeview
        for item in self.flights_tree.get_children():
            self.flights_tree.delete(item)

        # Search for flights in the database
        db_cursor.execute("SELECT * FROM available_flights WHERE start_location LIKE %s", ('%' + search_term + '%',))
        flights = db_cursor.fetchall()

        # Add the flights to the treeview
        for flight in flights:
            self.flights_tree.insert("", tk.END, values=flight)

    def cancel_booking(self):
        # Get the selected booking from the treeview
        selected_booking = self.bookings_tree.selection()

        if selected_booking:
            booking = self.bookings_tree.item(selected_booking)['values']
            booking_id = booking[0]

            # Confirm cancellation
            response = messagebox.askyesno("Cancel Flight", f"Are you sure you want to cancel booking {booking_id}?")

            if response:
                # Delete the booking from the database
                db_cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
                db_connection.commit()

                # Refresh the treeview
                self.bookings_tree.delete(selected_booking)

                # Show success message
                messagebox.showinfo("Success", f"Booking {booking_id} cancelled.")
        else:
            # Show error message if no booking is selected
            messagebox.showerror("Error", "Please select a booking to cancel.")

# Create the main window and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineSystem(root)
    root.mainloop()
