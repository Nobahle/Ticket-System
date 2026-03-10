import sqlite3

# Connect to database
conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_text TEXT,
    category TEXT
)
""")

# -----------------------------
# Ticket Classification Function
# -----------------------------
def classify_ticket(ticket):

    ticket = ticket.lower()

    it_keywords = ["password", "computer", "wifi", "laptop", "printer", "email", "system"]
    finance_keywords = ["salary", "payment", "payslip", "invoice", "overtime"]
    hr_keywords = ["leave", "holiday", "vacation", "sick", "promotion"]

    for word in it_keywords:
        if word in ticket:
            return "IT"

    for word in finance_keywords:
        if word in ticket:
            return "Finance"

    for word in hr_keywords:
        if word in ticket:
            return "HR"

    return "Operations"


# -----------------------------
# Save Ticket Function
# -----------------------------
def save_ticket(ticket, category):

    cursor.execute(
        "INSERT INTO tickets (ticket_text, category) VALUES (?, ?)",
        (ticket, category)
    )

    conn.commit()


# -----------------------------
# View All Tickets
# -----------------------------
def view_tickets():

    cursor.execute("SELECT * FROM tickets")

    tickets = cursor.fetchall()

    if not tickets:
        print("\nNo tickets found.")
    else:
        print("\n--- Stored Tickets ---")
        for t in tickets:
            print(f"ID: {t[0]} | Ticket: {t[1]} | Category: {t[2]}")


# -----------------------------
# Main Menu
# -----------------------------
while True:

    print("\n===== Smart Ticket System =====")
    print("1. Submit Ticket")
    print("2. View Tickets")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":

        ticket = input("\nEnter your support ticket: ")

        category = classify_ticket(ticket)

        save_ticket(ticket, category)

        print("\nTicket saved successfully!")
        print("Category:", category)

    elif choice == "2":

        view_tickets()

    elif choice == "3":

        print("\nExiting system...")
        break

    else:
        print("\nInvalid option. Try again.")


conn.close()