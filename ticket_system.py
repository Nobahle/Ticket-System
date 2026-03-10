import sqlite3
import string

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

# Ticket Classification Function
def classify_ticket(ticket):
    ticket_lower = ticket.lower()
    ticket_lower = ticket_lower.translate(str.maketrans('', '', string.punctuation))

    it_keywords = ["password", "computer", "wifi", "laptop", "printer", "email",
                   "system", "windows", "install", "software", "network", "login",
                   "internet", "server", "bug", "error", "update", "keyboard",
                   "mouse", "monitor", "pc", "connection"]

    finance_keywords = ["salary", "payment", "payslip", "invoice", "overtime",
                        "reimbursement", "budget", "expense", "tax", "deduction",
                        "bank", "transfer", "refund", "billing", "allowance"]

    hr_keywords = ["leave", "holiday", "vacation", "sick", "promotion",
                   "recruitment", "training", "attendance", "resignation",
                   "contract", "benefits", "hr", "employee", "hiring",
                   "disciplinary"]

    operations_keywords = ["office", "chair", "desk", "aircon", "air conditioner",
                           "cleaning", "maintenance", "equipment", "building",
                           "light", "electricity", "water", "parking", "security",
                           "meeting room", "facility", "supplies"]

    def contains_keyword(keywords):
        for kw in keywords:
            if kw in ticket_lower:
                return True
        return False

    if contains_keyword(it_keywords):
        return "IT"
    elif contains_keyword(finance_keywords):
        return "Finance"
    elif contains_keyword(hr_keywords):
        return "HR"
    elif contains_keyword(operations_keywords):
        return "Operations"

    return "Unrecognized"

# Save Ticket Function
def save_ticket(ticket, category):
    cursor.execute(
        "INSERT INTO tickets (ticket_text, category) VALUES (?, ?)",
        (ticket, category)
    )
    conn.commit()

# View All Tickets
def view_tickets():
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    if not tickets:
        print("\nNo tickets found.")
    else:
        print("\n--- Stored Tickets ---")
        for t in tickets:
            print(f"ID: {t[0]} | Ticket: {t[1]} | Category: {t[2]}")

# Delete Ticket Function
def delete_ticket(ticket_id):
    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    print(f"\nTicket ID {ticket_id} deleted successfully!")

# Main Menu
while True:
    print("\n===== Smart Ticket System =====")
    print("1. Submit Ticket")
    print("2. View Tickets")
    print("3. Delete Ticket")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        ticket = input("\nEnter your support ticket: ")
        category = classify_ticket(ticket)

        # If ticket is unrecognized, prompt user to assign a category
        if category == "Unrecognized":
            print("\nTicket could not be automatically classified.")
            category = input("Please manually assign a category (e.g., IT, Finance, HR, Operations): ").strip()
            if not category:
                category = "Unrecognized"

        save_ticket(ticket, category)
        print("\nTicket saved successfully!")
        print("Category:", category)

    elif choice == "2":
        view_tickets()

    elif choice == "3":
        view_tickets()
        try:
            ticket_id = int(input("\nEnter the ID of the ticket to delete: "))
            delete_ticket(ticket_id)
        except ValueError:
            print("Invalid ID! Please enter a number.")

    elif choice == "4":
        print("\nExiting system...")
        break

    else:
        print("\nInvalid option. Try again.")

conn.close()