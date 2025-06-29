import pandas as pd
import matplotlib.pyplot as plt

# Figuring out the dataframe and filtering
df = pd.read_csv("player_stats.csv")
positions = df["position"].unique()
# print(positions)

defenders = [
    "DF",
    "DF,MF",
    "MF,DF",
    "DF,FW",
]

# Assigning the Filter and axis's
mins = int(input("Enter Minimum Minutes you want to see:"))
min_prog_pass = int(input("Enter Minimum Progressive Passes you want to see:"))

filt = df.loc[
    df["position"].isin(defenders)
    & (df["minutes"] >= mins)
    & (df["progressive_passes"] >= min_prog_pass)
]
# print(filt)

x = filt["progressive_passes"]
y = filt["progressive_carries"]


# Creating & Designing the Scatter Plot
colors = [
    "#ff2d96",
    "#faff00",
    "#00ffff",
    "#ff7300",
    "#00ff66",
    "#4ac8ff",
    "#c77dff",
    "#ff4d4d",
    "#1abc9c",
    "#f1c40f",
]

plt.figure(figsize=(10, 6), facecolor="#0e1a26")

for i, (x_val, y_val) in enumerate(zip(x, y)):
    plt.scatter(x_val, y_val, color=colors[i % len(colors)])

plt.gca().set_facecolor("#0e1a26")
plt.gca().tick_params(colors="#c77dff")
for spine in plt.gca().spines.values():
    spine.set_color("white")

# To add Player names to the Label Points
for i, idx in enumerate(filt.index):
    player_name = filt.loc[idx, "name"]  # Get actual player name
    plt.annotate(
        player_name, (x[idx], y[idx]), fontsize=8, color="silver"
    )  # annotates the scatter points with the player names

# Labelling
plt.xlabel("Progression via Pass (Season Total)", color="white")
plt.ylabel("Progression via Carry (Season Total)", color="white")
plt.title("Premier League 2024-25: Ball Progression - Pass + Carry", color="white")
plt.grid("True")
plt.show()
