from ics import Calendar
from datetime import datetime, timedelta
import pytz

# Function to parse events from a .ics file
def parse_ics(file_path):
    with open(file_path, 'r') as file:
        calendar = Calendar(file.read())
    events = []
    for event in calendar.events:
        events.append({"start": event.begin.datetime, "end": event.end.datetime})
    return events

# Function to find free time slots between 9:00 AM and 9:00 PM in a single calendar
def find_free_slots(events, start_of_day, end_of_day):
    free_slots = []
    events.sort(key=lambda x: x["start"])
    current_time = start_of_day

    for event in events:
        # Check if the event starts after the current free time
        if current_time < event["start"]:
            free_slots.append({"start": current_time, "end": event["start"]})
        # Update the current time to the later of the current free time or the event's end
        current_time = max(current_time, event["end"])

    # Check for free time at the end of the day
    if current_time < end_of_day:
        free_slots.append({"start": current_time, "end": end_of_day})

    return free_slots

# Function to find overlapping free slots between two calendars
def find_common_free_slots(free_slots1, free_slots2):
    common_slots = []
    i, j = 0, 0

    while i < len(free_slots1) and j < len(free_slots2):
        start1, end1 = free_slots1[i]["start"], free_slots1[i]["end"]
        start2, end2 = free_slots2[j]["start"], free_slots2[j]["end"]

        # Calculate the overlap
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)

        if overlap_start < overlap_end:  # There is a valid overlap
            common_slots.append({"start": overlap_start, "end": overlap_end})

        # Move to the next slot in the list that ends earlier
        if end1 < end2:
            i += 1
        else:
            j += 1

    return common_slots

# Function to format free slots for display
def format_slots(slots):
    return [
        f"{slot['start'].strftime('%A, %Y-%m-%d %I:%M %p')} to {slot['end'].strftime('%I:%M %p')}"
        for slot in slots
    ]

# Main computation
if __name__ == "__main__":
    # File paths
    file_path1 = "example.ics"
    file_path2 = "example_2.ics"

    # Parse events from both files
    events1 = parse_ics(file_path1)
    events2 = parse_ics(file_path2)

    # Define working hours in PST
    pst = pytz.timezone("America/Los_Angeles")
    working_hours_start = pst.localize(datetime(2025, 1, 9, 9, 0, 0))
    working_hours_end = pst.localize(datetime(2025, 1, 9, 21, 0, 0))

    # Find free slots for each calendar
    free_slots1 = find_free_slots(events1, working_hours_start, working_hours_end)
    free_slots2 = find_free_slots(events2, working_hours_start, working_hours_end)

    # Find common free slots
    common_free_slots = find_common_free_slots(free_slots1, free_slots2)

    # Format and display the results
    print("\nCommon Free Time Slots Between 9:00 AM and 9:00 PM (PST):")
    formatted_slots = format_slots(common_free_slots)
    for slot in formatted_slots:
        print(slot)
