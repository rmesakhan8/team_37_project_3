import calendar
import random

# Define constants
SHIFTS = ["7:00AM - 1:00PM", "1:00PM - 7:00PM"]
PAY_RATE = 20  # hourly pay rate for paid caregivers

# Caregivers data
caregivers = [
    {"name": "Jack", "phone": "123-456-7890", "email": "jack@example.com", "pay_rate": PAY_RATE, "hours": 0, "availability": {}},
    {"name": "John", "phone": "987-654-3210", "email": "john@abc.com", "pay_rate": PAY_RATE, "hours": 0, "availability": {}},
    {"name": "Jacob", "phone": "555-555-5555", "email": "jacob@123.com", "pay_rate": PAY_RATE, "hours": 0, "availability": {}},
    # plz add more caregivers, we need 8
]

# Create default availability schedule
def create_default_availability():
    availability = {}
    for day in range(1, 8):  # Monday-Sunday
        availability[day] = {
            SHIFTS[0]: "available",
            SHIFTS[1]: "available"
        }
    return availability

# Update caregiver availability
def update_availability(caregiver):
    print(f"Updating availability for {caregiver['name']}")
    for day in range(1, 8):
        day_name = calendar.day_name[day - 1]
        print(f"\nDay: {day_name}")
        
        for shift in SHIFTS:
            status = input(f"Enter availability for {shift} (preferred/available/unavailable): ").strip().lower()
            if status in ["preferred", "available", "unavailable"]:
                caregiver["availability"].setdefault(day, {})[shift] = status
            else:
                print(f"Invalid input. Defaulting to 'available'.")
                caregiver["availability"].setdefault(day, {})[shift] = "available"

# Generate schedule for a month
def generate_schedule(year, month):
    num_days = calendar.monthrange(year, month)[1]
    schedule = {day: {SHIFTS[0]: None, SHIFTS[1]: None} for day in range(1, num_days + 1)}

    for day in range(1, num_days + 1):
        for shift in SHIFTS:
            # Assign caregivers based on availability and preferences
            available_caregivers = [
                caregiver for caregiver in caregivers
                if caregiver["availability"].get(day % 7 + 1, {}).get(shift, "unavailable") != "unavailable"
            ]
            preferred_caregivers = [
                caregiver for caregiver in available_caregivers
                if caregiver["availability"].get(day % 7 + 1, {}).get(shift) == "preferred"
            ]
            # Randomly select caregiver if more than 1 are available
            selected_caregiver = random.choice(preferred_caregivers or available_caregivers or [None])
            if selected_caregiver:
                schedule[day][shift] = selected_caregiver["name"]
                selected_caregiver["hours"] += 6  # Each shift is 6 hours
    return schedule

# Display schedule as an HTML calendar
def display_schedule_as_html(schedule, year, month):
    html = f"""
    <html>
    <head>
        <title>Schedule for {calendar.month_name[month]} {year}</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Schedule for {calendar.month_name[month]} {year}</h1>
        <table>
            <tr>
                <th>Sun</th>
                <th>Mon</th>
                <th>Tue</th>
                <th>Wed</th>
                <th>Thu</th>
                <th>Fri</th>
                <th>Sat</th>
            </tr>
    """
    first_weekday, num_days = calendar.monthrange(year, month)
    current_day = 1
    for week in range((num_days + first_weekday) // 7 + 1):
        html += "<tr>"
        for day in range(7):
            if week == 0 and day < first_weekday or current_day > num_days:
                html += "<td></td>"
            else:
                shifts = schedule[current_day]
                am = shifts[SHIFTS[0]] or "N/A"
                pm = shifts[SHIFTS[1]] or "N/A"
                html += f"<td>{current_day}<br><b>AM:</b> {am}<br><b>PM:</b> {pm}</td>"
                current_day += 1
        html += "</tr>"
    html += "</table></body></html>"

    with open(f"schedule_{year}_{month}.html", "w") as file:
        file.write(html)
    print(f"Schedule for {calendar.month_name[month]} {year} saved as HTML.")

# Calculate and display pay report
# plz add monthly pay report too
def calculate_pay_report():
    total_weekly = 0
    print("\nWeekly Pay Report")
    print("=" * 20)
    for caregiver in caregivers:
        gross_pay = caregiver["hours"] * caregiver["pay_rate"]
        total_weekly += gross_pay
        print(f"{caregiver['name']}: ${gross_pay:.2f}")
        caregiver["hours"] = 0  # Reset hours for next period
    print(f"\nTotal Weekly Pay: ${total_weekly:.2f}")

# Main program
if __name__ == "__main__":
    # Initialize caregiver availability
    for caregiver in caregivers:
        caregiver["availability"] = create_default_availability()

    # Allow updating caregiver availability
    for caregiver in caregivers:
        update_availability(caregiver)

    # Get schedule details
    year = int(input("Enter the year: "))
    month = int(input("Enter the month (1-12): "))

    # Generate and display schedule
    schedule = generate_schedule(year, month)
    display_schedule_as_html(schedule, year, month)

    # Calculate and display pay report
    calculate_pay_report()
