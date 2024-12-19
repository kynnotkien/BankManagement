# - - - - - - - - - - - - - - - - - - #
#        Made by KynNotKien <3        #
# - - - - - - - - - - - - - - - - - - #

import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import uuid

# Path to CSV file
FILE_PATH = "users.csv"


class User:
    """Class representing a user."""
    def __init__(self, name, email, password, role, uid, balance):
        self.__name = name  # Private attribute
        self.__email = email  # Private attribute
        self.__password = password  # Private attribute
        self.role = role
        self.uid = uid
        self.balance = float(balance)

    def check_password(self, password):
        return self.__password == password

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_balance(self):
        return self.balance

    def set_balance(self, amount):
        self.balance = amount

    def set_password(self, new_password):
        self.__password = new_password

    @staticmethod
    def from_dict(data):
        """Create a User instance from a dictionary."""
        return User(data['name'],
                    data['email'],
                    data['password'],
                    data['role'],
                    data['uid'],
                    data['balance']
                    )

    def to_dict(self):
        """Convert the User instance to a dictionary."""
        return {
            'name': self.__name,
            'email': self.__email,
            'password': self.__password,
            'role': self.role,
            'uid': self.uid,
            'balance': self.balance
        }


class Admin(User):
    """Admin class inheriting from User"""
    def __init__(self, name, email, password, uid, balance):
        super().__init__(name, email, password, "admin", uid, balance)


class BankApp:
    """Main bank application"""
    def __init__(self):
        self.current_user = None
        self.__users = []  # Private attribute for user storage
        self.setup_csv()
        self.load_users()
        self.show_login_screen()

    def setup_csv(self):
        """Initialize the CSV file if it doesn't exist."""
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "name",
                    "email",
                    "password",
                    "role",
                    "uid",
                    "balance"
                ])

    def load_users(self):
        """Load users from the CSV file."""
        with open(FILE_PATH, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = Admin.from_dict(row) if row['role'] == 'admin' \
                    else User.from_dict(row)
                self.__users.append(user)

    def save_users(self):
        """Save all users to the CSV file."""
        with open(FILE_PATH, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "name",
                "email",
                "password",
                "role",
                "uid",
                "balance"
                ])
            writer.writeheader()
            for user in self.__users:
                writer.writerow(user.to_dict())

    def find_user(self, email):
        """Find a user by email."""
        for user in self.__users:
            if user.get_email() == email:
                return user
        return None

    def add_user(self, user):
        """Add a new user to the application."""
        self.__users.append(user)
        self.save_users()

    def login(self, email, password):
        """Authenticate a user based on email and password."""
        user = self.find_user(email)
        if user and user.check_password(password):
            return user
        return None

    def show_login_screen(self):
        """Login window (check email, password)"""
        def handle_login():
            email = email_entry.get()
            password = password_entry.get()
            user = self.login(email, password)
            if user:
                self.current_user = user
                login_window.destroy()
                if user.role == 'admin':
                    self.show_admin_screen()
                else:
                    self.show_user_screen()
            else:
                messagebox.showerror("Error", "Invalid email or password")

        # Register window active
        def handle_register():
            login_window.destroy()
            self.show_register_screen()

        # Login interface
        login_window = tk.Tk()
        login_window.title("Login")
        login_window.geometry("600x400")

        login_frame = tk.Frame(login_window)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(login_window, text="Login", font=('Arial', 20))\
            .pack(pady=50)
        tk.Label(login_frame, text="Email:", font=('Arial', 20))\
            .grid(row=0, column=0, pady=5, padx=5)
        email_entry = tk.Entry(login_frame, font=('Arial', 20))
        email_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(login_frame, text="Password:", font=('Arial', 20))\
            .grid(row=1, column=0, pady=5, padx=5)
        password_entry = tk.Entry(login_frame, show="*", font=('Arial', 20))
        password_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Button(login_frame, text="Login", command=handle_login,
                  font=('Arial', 15)).grid(row=2, column=0, pady=5, padx=5)
        tk.Button(login_frame, text="Register", command=handle_register,
                  font=('Arial', 15)).grid(row=2, column=1, pady=5, padx=5)

        login_window.mainloop()

    def show_register_screen(self):
        """Display the registration window."""
        def handle_register():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            uid = str(uuid.uuid4())[:8]  # UID generate (only take 8)
            balance = balance_entry.get()

            if not (name and email and password and balance):
                messagebox.showerror("Error", "Please complete the form!")
                return

            try:
                balance = float(balance)  # Validate balance is a number
            except ValueError:
                messagebox.showerror("Error", "Balance must be a valid number")
                return
            if self.find_user(email):
                messagebox.showerror("Error", "Email is already registered!")
                return

            new_user = User(name, email, password, "user", uid, balance)
            self.add_user(new_user)  # Add user's information
            messagebox.showinfo("Success", "Account registered successfully!")
            register_window.destroy()
            self.show_login_screen()

        # Register interface
        register_window = tk.Tk()
        register_window.title("Register")
        register_window.geometry("600x400")

        register_frame = tk.Frame(register_window)
        register_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(register_window, text="Register", font=('Arial', 20))\
            .pack(pady=10)
        tk.Label(register_frame, text="Name:", font=('Arial', 20))\
            .grid(row=0, column=0, pady=5, padx=5)
        name_entry = tk.Entry(register_frame, font=('Arial', 20))
        name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(register_frame, text="Email:", font=('Arial', 20))\
            .grid(row=1, column=0, pady=5, padx=5)
        email_entry = tk.Entry(register_frame, font=('Arial', 20))
        email_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(register_frame, text="Password:", font=('Arial', 20))\
            .grid(row=2, column=0, pady=5, padx=5)
        password_entry = tk.Entry(register_frame, show="*", font=('Arial', 20))
        password_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(register_frame, text="Balance:", font=('Arial', 20))\
            .grid(row=3, column=0, pady=5, padx=5)
        balance_entry = tk.Entry(register_frame, font=('Arial', 20))
        balance_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Button(register_frame, text="Register", command=handle_register,
                  font=('Arial', 15))\
            .grid(row=4, column=0, columnspan=2, pady=5, padx=5)

        register_window.mainloop()

    def show_admin_screen(self):
        """Admin window (show all users's, name, email, role)"""
        def refresh_user_list():
            for row in user_tree.get_children():
                user_tree.delete(row)
            for user in self.__users:
                user_tree.insert("", "end", values=(user.uid,
                                                    user.get_name(),
                                                    user.get_email(),
                                                    user.role,
                                                    user.get_balance()))

        def delete_user():
            """Delete user in database => refresh"""
            selected = user_tree.selection()
            if selected:
                email = user_tree.item(selected[0], "values")[1]
                user = self.find_user(email)
                if user:
                    self.__users.remove(user)
                    self.save_users()
                    refresh_user_list()
                    messagebox.showinfo("Success", f"User {email} deleted.")
            else:
                messagebox.showerror("Error", "Choose a user to delete!")

        def reset_password():
            """Reset password (change user's password to password123)"""
            selected = user_tree.selection()
            if selected:
                email = user_tree.item(selected[0], "values")[1]
                user = self.find_user(email)
                if user:
                    new_password = "password123"
                    user.set_password(new_password)
                    self.save_users()
                    messagebox.showinfo(
                        "Success",
                        f"Password for {email} reset to '{new_password}'"
                    )
            else:
                messagebox.showerror("Error", "Please choose a user to reset!")

        # Admin interface
        admin_window = tk.Tk()
        admin_window.title("Admin Dashboard")
        admin_window.geometry("600x400")

        columns = ("uid", "name", "email", "role", "balance")
        user_tree = ttk.Treeview(admin_window,
                                 columns=columns, show="headings")

        for col in columns:
            user_tree.heading(col, text=col.capitalize())
            user_tree.column(col, width=100, anchor='center')

        user_tree.pack(fill=tk.BOTH, expand=True)

        admin_buttons_frame = tk.Frame(admin_window)
        admin_buttons_frame.pack(side=tk.TOP)

        tk.Button(admin_buttons_frame, text="Refresh",
                  command=refresh_user_list)\
            .grid(column=0, row=0, padx=5, pady=0)
        tk.Button(admin_buttons_frame, text="Delete User",
                  command=delete_user).grid(column=1, row=0, padx=5, pady=0)
        tk.Button(admin_buttons_frame, text="Reset Password",
                  command=reset_password).grid(column=2, row=0, padx=5, pady=0)

        refresh_user_list()
        admin_window.mainloop()

    def show_user_screen(self):
        """User window: show user's information(uid, name, balance)"""
        def transfer_money():
            recipient_email = recipient_entry.get()
            amount = amount_transfer_entry.get()
            if not recipient_email or not amount:
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            recipient = self.find_user(recipient_email)
            if not recipient:
                messagebox.showerror("Error", "Recipient not found.")
                return
            try:
                amount = float(amount)
                if amount <= 0 or amount > self.current_user.get_balance():
                    messagebox.showerror("Error", "Invalid amount.")
                    return

                self.current_user.set_balance(
                    self.current_user.get_balance() - amount)
                recipient.set_balance(recipient.get_balance() + amount)
                self.save_users()
                messagebox.showinfo("Success", "Transfer completed.")
                user_window.destroy()
                self.show_user_screen()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount format.")

        def deposit_money():
            """Deposit money (add money to user's balance)"""
            amount_deposit_withdraw = amount_money_entry.get()
            if not amount_deposit_withdraw:
                messagebox.showerror("Error", "Please fill in the field.")
                return
            try:
                amount_deposit_withdraw = float(amount_deposit_withdraw)
                if amount_deposit_withdraw <= 0 or \
                        amount_deposit_withdraw > \
                        self.current_user.get_balance():
                    messagebox.showerror("Error", "Invalid amount.")
                    return
                self.current_user.set_balance(
                    self.current_user.get_balance() + amount_deposit_withdraw)
                self.save_users()
                messagebox.showinfo("Success", "Deposit completed.")
                user_window.destroy()
                self.show_user_screen()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount format.")

        def withdraw_money():
            """Withdraw money (subtract money from user's balance)"""
            amount_deposit_withdraw = amount_money_entry.get()
            if not amount_deposit_withdraw:
                messagebox.showerror("Error", "Please fill in the field.")
                return
            try:
                amount_deposit_withdraw = float(amount_deposit_withdraw)
                if (amount_deposit_withdraw <= 0 or
                        amount_deposit_withdraw >
                        self.current_user.get_balance()):
                    messagebox.showerror("Error", "Invalid amount.")
                    return
                self.current_user.set_balance(
                    self.current_user.get_balance() - amount_deposit_withdraw)
                self.save_users()
                messagebox.showinfo("Success", "Deposit completed.")
                user_window.destroy()
                self.show_user_screen()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount format.")

        def calculate_interest():
            """Calculate interest
            (interest = interest_amount * balance / 100)"""
            global interest_apply
            interest = interest_amount.get()
            times = interest_times.get()
            if not interest or not times:
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            try:
                interest = float(interest)
                times = int(times)
                if times <= 0:
                    messagebox.showerror("Error", "Invalid times.")
                    return
                for i in range(times):
                    interest = interest * self.current_user.get_balance() / 100
                interest_apply = round(
                    self.current_user.get_balance() + interest, 2)
                new_balance.config(text=f"New balance: {interest_apply}")

            except ValueError:
                messagebox.showerror("Error", "Invalid amount format.")

        def apply_interest():
            self.current_user.set_balance(interest_apply)
            self.save_users()
            messagebox.showinfo("Success", "Interest applied.")
            user_window.destroy()
            self.show_user_screen()

        # User infterface
        user_window = tk.Tk()
        user_window.title("User Dashboard")
        user_window.geometry("600x400")

        # Frames
        main_user_frame = tk.Frame(user_window)
        user_info_frame = tk.Frame(main_user_frame, padx=15, pady=15)
        transfer_money_frame = tk.Frame(main_user_frame, padx=15, pady=15)
        wd_dps_money_frame = tk.Frame(main_user_frame, padx=15, pady=15)
        calculate_interest_frame = tk.Frame(main_user_frame, padx=0, pady=15)

        main_user_frame.pack()
        user_info_frame.grid(column=0, row=0, padx=15, pady=15)
        transfer_money_frame.grid(column=1, row=0, padx=15, pady=15)
        wd_dps_money_frame.grid(column=0, row=1, padx=15, pady=15)
        calculate_interest_frame.grid(column=1, row=1, padx=15, pady=15)

        # User information
        tk.Label(
            user_info_frame,
            text=f"Welcome, {self.current_user.get_name()}!",
            font=('Arial', 15)
        ).grid()
        tk.Label(
            user_info_frame,
            text=f"UID: {self.current_user.uid}",
            font=('Arial', 15)
        ).grid()
        tk.Label(
            user_info_frame,
            text=f"Balance: {self.current_user.get_balance()}",
            font=('Arial', 15)
        ).grid()

        # Transfer money
        tk.Label(transfer_money_frame, text="Transfer Money",
                 font=('Arial', 15)).grid()
        tk.Label(transfer_money_frame, text="Recipient Email:").grid()
        recipient_entry = tk.Entry(transfer_money_frame)
        recipient_entry.grid()

        tk.Label(transfer_money_frame, text="Amount:").grid()
        amount_transfer_entry = tk.Entry(transfer_money_frame)
        amount_transfer_entry.grid()
        tk.Button(transfer_money_frame, text="Transfer",
                  command=transfer_money).grid()

        # Deposit / Withdraw money
        tk.Label(wd_dps_money_frame, text="Deposit / Withdraw money",
                 font=('Arial', 15)).grid(column=0, row=0)
        amount_money_entry = tk.Entry(wd_dps_money_frame)
        amount_money_entry.grid(column=0, row=1)

        wd_dps_money_frame_button = tk.Frame(wd_dps_money_frame)
        wd_dps_money_frame_button.grid(column=0, row=2)
        tk.Button(wd_dps_money_frame_button, text="Deposit money",
                  command=deposit_money).grid(column=0, row=0, padx=2, pady=2)
        tk.Button(wd_dps_money_frame_button, text="Withdraw money",
                  command=withdraw_money).grid(column=1, row=0, padx=2, pady=2)

        tk.Label(calculate_interest_frame, text="Caculate interest")\
            .grid(column=1, row=0)
        tk.Label(calculate_interest_frame, text="Interest Amount:")\
            .grid(column=0, row=1)
        interest_amount = tk.Entry(calculate_interest_frame)
        interest_amount.grid(column=1, row=1)

        # Calculate interest
        tk.Label(calculate_interest_frame, text="Interest Times:")\
            .grid(column=0, row=2)
        interest_times = tk.Entry(calculate_interest_frame)
        interest_times.grid(column=1, row=2)
        tk.Button(calculate_interest_frame, text="Calculate",
                  command=calculate_interest).grid(column=0, row=3)

        new_balance = tk.Label(calculate_interest_frame, text="New balance")
        new_balance.grid(column=1, row=3)
        tk.Button(calculate_interest_frame, text="Apply to your balance",
                  command=apply_interest).grid(column=1, row=4)
        user_window.mainloop()


if __name__ == "__main__":  # Run the application
    BankApp()
