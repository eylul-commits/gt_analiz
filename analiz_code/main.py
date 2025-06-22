import pandas as pd

# Load Excel file
df = pd.read_excel("gt.xlsx")

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Define time slots
def assign_time_slot(hour):
    if 9 <= hour < 13:
        return "Slot 1 (09:00 - 13:00)"
    elif 13 <= hour < 18:
        return "Slot 2 (13:00 - 18:00)"
    elif 18 <= hour <= 23:
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

print("=== Most Successful Workers ===")
print(top_3_workers)
