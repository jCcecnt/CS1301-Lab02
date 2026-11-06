# This creates the page for displaying data visualizations.

import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---

#load .json file
with open("data.json", "r") as file:
    data = json.load(file)
players = data["data_points"]
#test that players are loaded correctly
st.write("Players loaded:", len(players))
#intiialize x and y axis. X axis is player names, y axis is projected points
names = []
projections = []
# labelling each players name with their projected points
for player in players:
    names.append(player["player"])
    projections.append(player["projected points"])
#making the graph fig is the graph itself like the visual, and ax is the axes variable that we can modify to set things to the axes. like naming the axis and such
fig, ax = plt.subplots(figsize = (12, 6))
#sets a bar chart with names correlated to projections based off of each indice
ax.bar(names, projections)
#sets a title
ax.set_title("Projected Fantasy Points by Player")
#Sets x axis as Player
ax.set_xlabel("Player")
#Sets y axis as Projected Fantasy points
ax.set_ylabel("Projected Fantasy Points")
#sets some formatting things, Rotates each player name to make it look nicer and to avoid overcrowding
plt.xticks(rotation=75)
#Makes sure that each bar has room on the graph.
plt.tight_layout()
#plots the figure
st.pyplot(fig)


#Things for Graph 2. Titles the second graph
st.header("Player Performance Analyzer")


#This sets that if theres no player chosen upon first time running the code. Default to the first player in the list of player names
if "selected_player" not in st.session_state:
    st.session_state["selected_player"] = names[0]

#creates a dropdown containing all the names
whatPlayer = st.selectbox("Choose a player", names, key = "selected_player")

selectedPlayer = None

#sets selectedPlayer to the player's stat dictionary selected in the drop down menu
for player in players:
    if player["player"] == whatPlayer:
        selectedPlayer = player
        break

#Labels for each JSON key
whatStats = {"Fantasy Points": "weekly_points","Total Yards": "weekly_yards","Touches": "weekly_touches","Touchdowns": "weekly_touchdowns"}

#Create Stats dropdown. This also sets the first/default value to FantasyPoints
if "selected_stat" not in st.session_state:
    st.session_state["selected_stat"] = "Fantasy Points"

stat = st.selectbox("Choose a statistic", list(whatStats.keys()), key="selected_stat")

#Retrieve weekly performance
keyStat = whatStats[stat]

weeklyPerformance = selectedPlayer[keyStat]


#Create the graph based on weeks and fantasy performances. 
weeks = [1, 2, 3, 4, 5]

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(weeks, weeklyPerformance, marker="o")


ax2.set_title(whatPlayer + " - " + stat + " by Week")
ax2.set_xlabel("Week")
ax2.set_ylabel(stat)
ax2.set_xticks(weeks)

plt.tight_layout()
st.pyplot(fig2)

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.divider()
st.header("NFL Week 8 Receiving Yards")

receiverData = pd.read_csv("data.csv")
st.dataframe(receiverData)

names = receiverData["Category"].tolist()
yards = receiverData["Value"].tolist()



fig3, ax3 = plt.subplots(figsize = (12, 6))
ax3.pie(yards, labels=names, autopct = "%1.1f%%")

receiverStatLegend = []
for i in range(len(names)):
    receiverStatLegend.append(f"{names[i]}: {yards[i]} yards")
ax3.legend(receiverStatLegend, loc = "upper right", bbox_to_anchor=(1.5, 1))
ax3.set_title("NFL Receiving Yards by Wide Receiver Week 8")

plt.tight_layout()
st.pyplot(fig3)

st.header("Compare 3 wide receivers")
if "selected1" not in st.session_state:
    st.session_state["selected1"] = names[0]

if "selected2" not in st.session_state:
    if len(names) > 1:
        st.session_state["selected2"] = names[1]
    else:
        st.session_state["selected2"] = names[0]
if "selected3" not in st.session_state:
    if len(names) > 2:
        st.session_state["selected3"] = names[2]
    else:
        st.session_state["selected3"] = names[0]
selectPlayer1 = st.selectbox("Choose a player", names, key = "selected1")
selectPlayer2 = st.selectbox("Choose a second player", names, key = "selected2")
selectPlayer3 = st.selectbox("Choose a third player", names, key= "selected3")

index1 = names.index(selectPlayer1)
index2 = names.index(selectPlayer2)
index3 = names.index(selectPlayer3)

player1Yards = yards[index1]
player2Yards = yards[index2]
player3Yards = yards[index3]

compareNames = [selectPlayer1, selectPlayer2, selectPlayer3]
compareStats = [player1Yards, player2Yards, player3Yards]

fig4, ax4 = plt.subplots(figsize=(10, 6))
ax4.bar(compareNames, compareStats)

ax4.set_title("Week 8 Wide Receiver Comparisons")
ax4.set_xlabel("Wide Receivers")
ax4.set_ylabel("Receiving Yards")
plt.tight_layout()
st.pyplot(fig4)

meanYards = sum(compareStats) / len(compareStats)


sortedYards = sorted(compareStats)
medianYards = sortedYards[1]

if "previousMean" not in st.session_state:
    st.session_state["previousMean"] = meanYards
if "previousMedian" not in st.session_state:
    st.session_state["previousMedian"] = medianYards

deltaMean = meanYards - st.session_state["previousMean"]
deltaMedian = medianYards - st.session_state["previousMedian"]

st.metric("Mean Receiving Yards", round(meanYards, 2), delta=round(deltaMean, 2))
st.metric("Median Receiving Yards", medianYards, delta=round(deltaMedian, 2))

st.session_state["previousMean"] = meanYards
st.session_state["previousMedian"] = medianYards
