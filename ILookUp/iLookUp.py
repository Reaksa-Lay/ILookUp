import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import ast
import phonenumbers
import tkintermapview
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from key import key


### MAIN APPLICATION ###
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('925x500+300+200')
        self.root.config(bg='white')
        self.root.resizable(False, False)
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()
        LoginScreen(self.root, self.show_signup_screen, self.show_tracker_screen)

    def show_signup_screen(self):
        self.clear_screen()
        SignUpScreen(self.root, self.show_login_screen)

    def show_tracker_screen(self):
        self.clear_screen()
        PhoneTrackerScreen(self.root)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


### LOGIN SCREEN ###
class LoginScreen:
    def __init__(self, root, go_to_signup, go_to_tracker):
        self.root = root
        self.go_to_signup = go_to_signup
        self.go_to_tracker = go_to_tracker

        self.setup_ui()

    def setup_ui(self):
        self.root.title('Login')
        # Logo/Image
        image = Image.open('signIn.png').resize((300, 300), Image.LANCZOS)
        img = ImageTk.PhotoImage(image)
        Label(self.root, image=img, bg='white').place(x=80, y=50)
        self.root.image = img

        # Login Form
        frame = Frame(self.root, width=350, height=350, bg='white')
        frame.place(x=480, y=70)

        Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('calibri', 23, 'bold')).place(x=100, y=5)

        # Username
        self.user = self.create_entry(frame, 'Username', 30, 80)
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

        # Password
        self.code = self.create_entry(frame, 'Password', 30, 150, True)
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

        # Buttons
        Button(frame, text='Sign in', bg='#57a1f8', fg='white', width=39, pady=7, border=0, command=self.sign_in).place(x=35, y=204)
        Label(frame, text="Don't have an account?", fg='black', bg='white', font=('calibri', 10)).place(x=75, y=270)
        Button(frame, text='Sign up', bg='white', fg='#57a1f8', width=6, border=0, command=self.go_to_signup).place(x=215, y=270)

    def create_entry(self, frame, placeholder, x, y, password=False):
        entry = Entry(frame, width=25, fg='black', bg='white', border=0, font=('calibri', 11))
        entry.place(x=x, y=y)
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: self.clear_placeholder(entry, placeholder, password))
        entry.bind('<FocusOut>', lambda e: self.add_placeholder(entry, placeholder, password))
        return entry

    def clear_placeholder(self, entry, placeholder, password):
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            if password:
                entry.config(show='*')

    def add_placeholder(self, entry, placeholder, password):
        if not entry.get():
            entry.insert(0, placeholder)
            if password:
                entry.config(show='')

    def sign_in(self):
        username = self.user.get()
        password = self.code.get()

        try:
            with open('datasheet.txt', 'r') as file:
                accounts = ast.literal_eval(file.read())
        except FileNotFoundError:
            messagebox.showerror('Error', 'No accounts found. Please sign up first.')
            return

        if username in accounts and accounts[username] == password:
            self.go_to_tracker()
        else:
            messagebox.showerror('Error', 'Invalid username or password.')


### SIGN-UP SCREEN ###
class SignUpScreen:
    def __init__(self, root, go_to_login):
        self.root = root
        self.go_to_login = go_to_login

        self.setup_ui()

    def setup_ui(self):
        self.root.title('Sign up')
        image = Image.open('signUp.png')
        img = ImageTk.PhotoImage(image)
        Label(self.root, image=img, bg='white').place(x=400, y=50)
        self.root.image = img
        
        frame = Frame(self.root, width=350, height=390, bg='white')
        frame.place(x=50, y=50)

        Label(frame, text='Sign up', fg='#57a1f8', bg='white', font=('calibri', 23, 'bold')).place(x=100, y=5)

        # Username
        self.user = self.create_entry(frame, 'Username', 30, 80)
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

        # Password
        self.code = self.create_entry(frame, 'Password', 30, 150, True)
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

        # Confirm Password
        self.confirm_code = self.create_entry(frame, 'Confirm Password', 30, 220, True)
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

        # Buttons
        Button(frame, text='Sign up', bg='#57a1f8', fg='white', width=39, pady=7, border=0, command=self.sign_up).place(x=35, y=280)
        Label(frame, text='I have an account', fg='black', bg='white', font=('calibri', 9)).place(x=90, y=340)
        Button(frame, text='Sign in', bg='white', fg='#57a1f8', width=6, border=0, command=self.go_to_login).place(x=200, y=340)

    def create_entry(self, frame, placeholder, x, y, password=False):
        entry = Entry(frame, width=25, fg='black', bg='white', border=0, font=('calibri', 11))
        entry.place(x=x, y=y)
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: self.clear_placeholder(entry, placeholder, password))
        entry.bind('<FocusOut>', lambda e: self.add_placeholder(entry, placeholder, password))
        return entry

    def clear_placeholder(self, entry, placeholder, password):
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            if password:
                entry.config(show='*')

    def add_placeholder(self, entry, placeholder, password):
        if not entry.get():
            entry.insert(0, placeholder)
            if password:
                entry.config(show='')

    def sign_up(self):
        username = self.user.get()
        password = self.code.get()
        confirm_password = self.confirm_code.get()

        if password != confirm_password:
            messagebox.showerror('Error', 'Passwords do not match.')
            return

        try:
            with open('datasheet.txt', 'r') as file:
                accounts = ast.literal_eval(file.read())
        except FileNotFoundError:
            accounts = {}

        accounts[username] = password

        with open('datasheet.txt', 'w') as file:
            file.write(str(accounts))

        messagebox.showinfo('Success', 'Sign up successful.')
        self.go_to_login()


### PHONE TRACKER SCREEN ###
class PhoneTrackerScreen:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("ILookUp - Phone Number Tracker")

        self.search_history = []  # To store search history
        self.map_widget = None
        self.my_label = None

        self.geoCoder = OpenCageGeocode(key)  # OpenCage API client

        self.setup_ui()

    def setup_ui(self):
        # Title Label
        label = tk.Label(self.root, text="ILookUp (Phone Number Tracker)", font=("Calibri", 18, "bold"))
        label.pack(pady=10)

        # Input Field for Phone Number
        style = ttk.Style()
        style.configure("TEntry", font=('calibri', 14), padding=10, relief="flat", borderwidth=2)
        self.phone_input = ttk.Entry(self.root, style="TEntry", justify="center", font=('calibri', 12), width=25)
        self.phone_input.insert(0, "Enter phone number here...")
        self.phone_input.bind("<FocusIn>", self.clear_placeholder)
        self.phone_input.bind("<FocusOut>", self.add_placeholder)
        self.phone_input.pack(pady=10, padx=50)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        search_button = ttk.Button(button_frame, text="Search", command=self.get_result, style="TButton")
        search_button.pack(side=tk.LEFT, padx=5)

        history_button = ttk.Button(button_frame, text="View History", command=self.view_history, style="TButton")
        history_button.pack(side=tk.LEFT, padx=5)

        # Result Display
        self.result = tk.Text(self.root, height=5, width=30, font=("Calibri", 10), wrap=tk.WORD)
        self.result.pack(pady=10)

    def clear_placeholder(self, event):
        if self.phone_input.get() == "Enter phone number here...":
            self.phone_input.delete(0, tk.END)

    def add_placeholder(self, event):
        if not self.phone_input.get():
            self.phone_input.insert(0, "Enter phone number here...")

    def get_result(self):
        # Clear previous map and results
        self.result.delete("1.0", tk.END)
        if self.my_label:
            self.my_label.destroy()

        num = self.phone_input.get().strip()
        if not num or num == "Enter phone number here...":
            messagebox.showerror("Error", "Invalid Phone Number or Number box is empty.")
            return

        try:
            num1 = phonenumbers.parse(num)
        except phonenumbers.NumberParseException:
            messagebox.showerror("Error", "Invalid Phone Number format.")
            return

        location = geocoder.description_for_number(num1, "en")
        service_provider = carrier.name_for_number(num1, "en")
        query = str(location)
        results = self.geoCoder.geocode(query)

        if not results:
            messagebox.showerror("Error", "Location not found for the given number.")
            return

        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']

        # Display map
        self.my_label = tk.LabelFrame(self.root)
        self.my_label.pack(pady=20)

        self.map_widget = tkintermapview.TkinterMapView(self.my_label, width=450, height=450, corner_radius=10)
        self.map_widget.set_position(lat, lng)
        self.map_widget.set_marker(lat, lng, text="Phone Location")
        self.map_widget.set_zoom(10)
        self.map_widget.pack()

        address = tkintermapview.convert_coordinates_to_address(lat, lng)

        # Store search history
        search_info = {
            "number": num,
            "country": location,
            "service_provider": service_provider,
            "latitude": lat,
            "longitude": lng,
            "street": address.street,
            "city": address.city,
            "postal": address.postal
        }
        self.search_history.append(search_info)

        # Display results
        self.result.insert(tk.END, f"Country: {location}\n")
        self.result.insert(tk.END, f"Service provider: {service_provider}\n")
        self.result.insert(tk.END, f"Latitude: {lat}\n")
        self.result.insert(tk.END, f"Longitude: {lng}\n")
        self.result.insert(tk.END, f"Street Address: {address.street}\n")
        self.result.insert(tk.END, f"City Address: {address.city}\n")
        self.result.insert(tk.END, f"Postal Code: {address.postal}\n")

    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Search History")
        history_window.geometry("600x400")

        history_text = tk.Text(history_window, wrap=tk.WORD, height=20, width=70)
        history_text.pack(pady=10)

        if not self.search_history:
            history_text.insert(tk.END, "No history available.")
            return

        for idx, record in enumerate(self.search_history, 1):
            history_text.insert(tk.END, f"Search {idx}:\n")
            history_text.insert(tk.END, f"  Number: {record['number']}\n")
            history_text.insert(tk.END, f"  Country: {record['country']}\n")
            history_text.insert(tk.END, f"  Service Provider: {record['service_provider']}\n")
            history_text.insert(tk.END, f"  Latitude: {record['latitude']}\n")
            history_text.insert(tk.END, f"  Longitude: {record['longitude']}\n")
            history_text.insert(tk.END, f"  Street Address: {record['street']}\n")
            history_text.insert(tk.END, f"  City Address: {record['city']}\n")
            history_text.insert(tk.END, f"  Postal Code: {record['postal']}\n")
            history_text.insert(tk.END, "-" * 40 + "\n")


if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()
