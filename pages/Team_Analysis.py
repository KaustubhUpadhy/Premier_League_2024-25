import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from urllib.parse import parse_qs

st.set_page_config(page_title="Team Analysis", layout="wide")

# Get team parameter from URL (if available)
try:
    query_params = st.query_params
    selected_team = query_params.get("team", "Liverpool").replace("_", " ")
except:
    selected_team = "Liverpool"

# Load data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("player_stats.csv")
    except:
        return pd.DataFrame()


@st.cache_data
def load_standings():
    try:
        return pd.read_csv("standings.csv")
    except:
        return pd.DataFrame()


df = load_data()
standings_df = load_standings()
ven = pd.read_csv("fixtures.csv")
team = pd.read_csv("team_stats.csv")
pl = pd.read_csv("player_possession_stats.csv")

if df.empty:
    st.error("Player stats data not found. Please ensure 'player_stats.csv' exists.")
    st.stop()

# Team selector (fallback if URL parameter doesn't work)
if "team" in df.columns:
    available_teams = sorted(df["team"].unique())
    if selected_team not in available_teams:
        selected_team = available_teams[0]

    selected_team = st.selectbox(
        "Select Team",
        available_teams,
        index=(
            available_teams.index(selected_team)
            if selected_team in available_teams
            else 0
        ),
    )
    st.markdown(
    f"<h1 style='text-align: center;'>{selected_team}: Team Analysis</h1>",
    unsafe_allow_html=True,
    )
    # Filter data for selected team
    team_data = df[df["team"] == selected_team].copy()
    attend_data = ven[ven["Home"] == selected_team].copy()
    team_stats = team[team["team"] == selected_team].copy()
    possession_data = pl[pl["team"] == selected_team].copy()

    if team_data.empty:
        st.warning(f"No data found for {selected_team}")
        st.stop()

    # Team Overview Section
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        total_players = len(team_data)
        st.metric("Total Players", total_players)

    with col2:
        if "goals" in team_data.columns:
            total_goals = team_data["goals"].sum()
            st.metric("Team Goals", int(total_goals))

    with col3:
        if "assists" in team_data.columns:
            total_assists = team_data["assists"].sum()
            st.metric("Team Assists", int(total_assists))

    with col4:
        if "Venue" in attend_data.columns:
            team_stadium = attend_data["Venue"].unique()
            st.metric("Team Stadium", str(team_stadium[0]))

    with col5:
        if "Venue" in attend_data.columns:
            team_attendance = attend_data["Attendance"].mean()
            st.metric("Avg. Attendance", int(team_attendance))

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        if "goals" in team_stats.columns:
            goals = int(team_stats["goals"].iloc[0])
            xg = float(team_stats["expected_goals"].iloc[0])
        st.markdown("### Goals Scored v/s Expected Goals")

        fig = go.Figure(
            data=[
                go.Bar(
                    x=["Goals"],
                    y=[int(goals)],
                    marker_color="blue",
                    text=[goals],
                    textposition="outside",
                    name="Goals",
                ),
                go.Bar(
                    x=["Expected Goals"],
                    y=[int(xg)],
                    marker_color="orange",
                    text=xg,
                    textposition="outside",
                    name="xG",
                ),
            ]
        )
        # Layout settings
        fig.update_layout(
            barmode="group",  # side-by-side bars
            showlegend=False,
            yaxis=dict(showticklabels=False, visible=False),
            xaxis=dict(showticklabels=True, tickfont=dict(size=14)),
            margin=dict(l=10, r=10, t=30, b=30),
            height=400,
            width=300,
        )

        st.plotly_chart(fig, use_container_width=False)

    with col2:
        if "possession" in team_stats.columns:
            possession_per = float(team_stats["possession"].iloc[0])
            # st.metric("Avg. Possession %", float(possession_per))
            fig = go.Figure(
                data=[
                    go.Pie(
                        values=[possession_per, 100 - possession_per],
                        labels=["Possession", "Non-possession"],
                        marker=dict(colors=["#57D457", "gray"]),
                        hole=0.4,
                        textinfo="none",
                        hoverinfo="label+value",
                        sort=False,
                        direction="clockwise",
                    )
                ]
            )
            fig.update_layout(
                showlegend=False,
                margin=dict(t=0, b=0, l=0, r=0),
                height=250,
                width=250,
            )
            st.markdown("### Avg. Possession %")
            st.plotly_chart(fig, use_container_width=False)

    # Team Position Analysis
    if "position" in team_data.columns:
        st.markdown("### 📊 Squad Composition")

        # Position distribution
        position_counts = team_data["position"].value_counts()

        fig = go.Figure(
            data=[
                go.Bar(
                    x=position_counts.index,
                    y=position_counts.values,
                    marker_color="#37003c",
                    text=position_counts.values,
                    textposition="auto",
                )
            ]
        )

        fig.update_layout(
            title=f"{selected_team} - Players by Position",
            xaxis_title="Position",
            yaxis_title="Number of Players",
            plot_bgcolor="white",
            height=400,
        )

        st.plotly_chart(fig, use_container_width=True)
        st.write("---")
    st.markdown("### 🏃‍♂️ Team Dribbling & Possession Stats")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Top 5 Dribblers (Take-on Success Rate)
        if not "take_on_success_rate" in possession_data.columns:
            possession_data["take_on_success_rate"] = (
                possession_data["successful_take_ons"]
                / possession_data["attempted_take_ons"]
            )
            top_dribblers = possession_data.nlargest(5, "successful_take_ons")[
                ["player", "take_on_success_rate", "attempted_take_ons"]
            ]
            if not top_dribblers.empty:

                fig_dribblers = go.Figure()
                fig_dribblers.add_trace(
                    go.Bar(
                        y=top_dribblers["player"],
                        x=top_dribblers["take_on_success_rate"],
                        orientation="h",
                        marker_color="#ff2d96",
                        text=[
                            f"{rate:.1%}"
                            for rate in top_dribblers["take_on_success_rate"]
                        ],
                        textposition="auto",
                        customdata=top_dribblers["attempted_take_ons"],
                        hovertemplate="<b>%{y}</b><br>Success Rate: %{x:.1%}<br>Attempts: %{customdata}<extra></extra>",
                    )
                )

                fig_dribblers.update_layout(
                    title="Top 5 Dribblers",
                    xaxis_title="Success Rate",
                    height=300,
                    plot_bgcolor="white",
                    showlegend=False,
                )

                st.plotly_chart(fig_dribblers, use_container_width=True)

    with col2:
        # Top 5 Progressive Carriers
        if "progressive_carries" in team_data.columns:
            top_carriers = team_data.nlargest(5, "progressive_carries")[
                ["name", "progressive_carries", "position"]
            ]
            if not top_carriers.empty:

                fig_carriers = go.Figure()
                fig_carriers.add_trace(
                    go.Bar(
                        y=top_carriers["name"],
                        x=top_carriers["progressive_carries"],
                        orientation="h",
                        marker_color="#00ff66",
                        text=top_carriers["progressive_carries"],
                        textposition="auto",
                        customdata=top_carriers["position"],
                        hovertemplate="<b>%{y}</b><br>Progressive Carries: %{x}<br>Position: %{customdata}<extra></extra>",
                    )
                )

                fig_carriers.update_layout(
                    title="Top 5 Progressive Carriers",
                    xaxis_title="Progressive Carries",
                    height=300,
                    plot_bgcolor="white",
                    showlegend=False,
                )

                st.plotly_chart(fig_carriers, use_container_width=True)

    with col3:
        # Top 5 Progressive Pass Recipients
        if "received_progressive_passes" in team_data.columns:
            top_receivers = team_data.nlargest(5, "received_progressive_passes")[
                ["name", "received_progressive_passes", "position"]
            ]
            if not top_receivers.empty:
                fig_receivers = go.Figure()
                fig_receivers.add_trace(
                    go.Bar(
                        y=top_receivers["name"],
                        x=top_receivers["received_progressive_passes"],
                        orientation="h",
                        marker_color="#4ac8ff",
                        text=top_receivers["received_progressive_passes"],
                        textposition="auto",
                        customdata=top_receivers["position"],
                        hovertemplate="<b>%{y}</b><br>Received: %{x}<br>Position: %{customdata}<extra></extra>",
                    )
                )

                fig_receivers.update_layout(
                    title="Top 5 Progressive Pass Recipients",
                    xaxis_title="Progressive Passes Received",
                    height=300,
                    plot_bgcolor="white",
                    showlegend=False,
                )

                st.plotly_chart(fig_receivers, use_container_width=True)

    # Team Contribution Analysis
    if not team_stats.empty:
        st.write("---")
        st.markdown("### 📊 Player Contribution to Team Stats")

        col1, col2 = st.columns(2)

        with col1:
            # Progressive Carries Contribution
            if (
                "progressive_carries" in team_data.columns
                and "progressive_carries" in team_stats.columns
            ):
                team_total_prog_carries = team_stats["progressive_carries"].iloc[0]
                team_data["prog_carries_pct"] = (
                    team_data["progressive_carries"] / team_total_prog_carries * 100
                ).round(1)

                # Get top 10 contributors
                top_prog_carries = team_data.nlargest(10, "prog_carries_pct")[
                    ["name", "prog_carries_pct", "progressive_carries"]
                ]

                fig_prog_carries = go.Figure()
                fig_prog_carries.add_trace(
                    go.Bar(
                        y=top_prog_carries["name"],
                        x=top_prog_carries["prog_carries_pct"],
                        orientation="h",
                        marker_color="#ff7300",
                        customdata=top_prog_carries["progressive_carries"],
                        hovertemplate="<b>%{y}</b><br>Contribution: %{x}%<br>Actual Carries: %{customdata}<extra></extra>",
                    )
                )

                fig_prog_carries.update_layout(
                    title="Progressive Carries Contribution (%)",
                    xaxis_title="Percentage of Team Total",
                    height=500,
                    plot_bgcolor="white",
                    showlegend=False,
                )

                st.plotly_chart(fig_prog_carries, use_container_width=True)

        with col2:
            # Progressive Passes Contribution
            if (
                "progressive_passes" in team_data.columns
                and "progressive_passes" in team_stats.columns
            ):
                team_total_prog_passes = team_stats["progressive_passes"].iloc[0]
                team_data["prog_passes_pct"] = (
                    team_data["progressive_passes"] / team_total_prog_passes * 100
                ).round(1)

                # Get top 10 contributors
                top_prog_passes = team_data.nlargest(10, "prog_passes_pct")[
                    ["name", "prog_passes_pct", "progressive_passes"]
                ]

                fig_prog_passes = go.Figure()
                fig_prog_passes.add_trace(
                    go.Bar(
                        y=top_prog_passes["name"],
                        x=top_prog_passes["prog_passes_pct"],
                        orientation="h",
                        marker_color="#c77dff",
                        customdata=top_prog_passes["progressive_passes"],
                        hovertemplate="<b>%{y}</b><br>Contribution: %{x}%<br>Actual Passes: %{customdata}<extra></extra>",
                    )
                )

                fig_prog_passes.update_layout(
                    title="Progressive Passes Contribution (%)",
                    xaxis_title="Percentage of Team Total",
                    height=500,
                    plot_bgcolor="white",
                    showlegend=False,
                )

                st.plotly_chart(fig_prog_passes, use_container_width=True)

    # Top Players Section
    st.write("---")
    st.markdown("### 🌟 Top Performers")

    # Top scorers
    if "goals" in team_data.columns:
        top_scorers = team_data.nlargest(5, "goals")[["name", "goals", "position"]]
        if not top_scorers.empty:
            st.markdown("**🥅 Top Scorers:**")
            st.dataframe(top_scorers, hide_index=True, use_container_width=True)

    # Top assisters
    if "assists" in team_data.columns:
        top_assisters = team_data.nlargest(5, "assists")[
            ["name", "assists", "position"]
        ]
        if not top_assisters.empty:
            st.markdown("**🎯 Top Assisters:**")
            st.dataframe(top_assisters, hide_index=True, use_container_width=True)

    # Most minutes played
    if "minutes" in team_data.columns:
        most_minutes = team_data.nlargest(5, "minutes")[["name", "minutes", "position"]]
        if not most_minutes.empty:
            st.markdown("**⏱️ Most Minutes Played:**")
            st.dataframe(most_minutes, hide_index=True, use_container_width=True)

    st.write("---")

    # Full Squad Table
    st.markdown("### 👥 Full Squad")

    # Select relevant columns for display
    display_cols = ["name", "position"]
    if "goals" in team_data.columns:
        display_cols.append("goals")
    if "assists" in team_data.columns:
        display_cols.append("assists")
    if "minutes" in team_data.columns:
        display_cols.append("minutes")

    squad_display = (
        team_data[display_cols].sort_values("minutes", ascending=False)
        if "minutes" in display_cols
        else team_data[display_cols]
    )

    st.dataframe(squad_display, hide_index=True, use_container_width=True)

else:
    st.error(
        "Team information not found in the dataset. Please check your data structure."
    )

# Back to homepage button
st.write("---")
if st.button("🏠 Back to Homepage"):
    st.switch_page("app.py")
