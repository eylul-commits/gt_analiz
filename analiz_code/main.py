import pandas as pd

# Load Excel file
df = pd.read_excel("gt.xlsx")

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Define time slots
def assign_time_slot(hour):
    TRTHour = hour + 3
    if 9 <= TRTHour < 13:
        return "Slot 1 (09:00 - 13:00)"
    elif 13 <= TRTHour < 18:
        return "Slot 2 (13:00 - 18:00)"
    elif 18 <= TRTHour <= 23:
        return "Slot 3 (18:00 - 23:00)"
    else:
        return "Outside Working Hours"

# Assign Time Slot and Worker
df['Time Slot'] = df['Date'].dt.hour.apply(assign_time_slot)
df['Worker'] = df['Date'].dt.date.astype(str) + " - " + df['Time Slot']

# Calculate engagement score
df['Engagement Score'] = df['Likes'] + df['Retweet Count'] + df['Views Count']

# --- Most Liked Tweets ---
top_liked = df.sort_values(by='Likes', ascending=False).head(3)

# --- Most Retweeted Tweets ---
top_retweeted = df.sort_values(by='Retweet Count', ascending=False).head(3)

# --- Time Slot Performance ---
slot_performance = df.groupby('Time Slot').agg({
    'Likes': 'mean',
    'Retweet Count': 'mean',
    'Views Count': 'mean',
    'Tweet ID': 'count'
}).rename(columns={'Tweet ID': 'Tweet Count'})

# Calculate average engagement score for each time slot
slot_performance['Avg Engagement Score'] = slot_performance['Likes'] + slot_performance['Retweet Count'] + slot_performance['Views Count']

# Get worst 5 time slots
worst_time_slots = slot_performance.sort_values(by='Avg Engagement Score', ascending=True).head(5)

# --- Daily Performance Analysis ---
daily_performance = df.groupby(df['Date'].dt.date).agg({
    'Likes': 'sum',
    'Retweet Count': 'sum', 
    'Views Count': 'sum',
    'Tweet ID': 'count'
}).rename(columns={'Tweet ID': 'Post Count'})

# Calculate daily engagement score
daily_performance['Daily Engagement Score'] = daily_performance['Likes'] + daily_performance['Retweet Count'] + daily_performance['Views Count']

# Get worst 5 days
worst_days = daily_performance.sort_values(by='Daily Engagement Score', ascending=True).head(5)

# --- Top 3 Workers ---
worker_performance = df.groupby('Worker').agg({
    'Likes': 'sum',
    'Retweet Count': 'sum',
    'Views Count': 'sum',
    'Engagement Score': 'sum',
    'Tweet ID': 'count'
}).rename(columns={'Tweet ID': 'Tweet Count'}).sort_values(by='Engagement Score', ascending=False)

top_3_workers = worker_performance.head(5)

# --- Display Results ---
print("=== Top 3 Most Liked Tweets ===")
print(top_liked[['Date', 'Text', 'Likes', 'Tweet URL']], end='\n\n')

print("=== Top 3 Most Retweeted Tweets ===")
print(top_retweeted[['Date', 'Text', 'Retweet Count', 'Tweet URL']], end='\n\n')

print("=== Average Engagement by Time Slot ===")
print(slot_performance, end='\n\n')

print("=== Worst 5 Time Slots (Lowest Average Engagement) ===")
print(worst_time_slots, end='\n\n')

print("=== Worst 5 Days (Lowest Total Engagement) ===")
print(worst_days, end='\n\n')

print("=== Most Successful Workers ===")
print(top_3_workers)
