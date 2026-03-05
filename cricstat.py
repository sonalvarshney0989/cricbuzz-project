import streamlit as st
import psycopg2
import pandas as pd
import live
import playerstat
import sqlquery
import crudops

# creating SQL connection
con = psycopg2.connect(
    host = 'localhost',
    user = 'postgres',
    database = 'sonal',
    password = 'sonal0989',
    port = 5432
)

cursor = con.cursor()
con.autocommit=True

st.set_page_config(layout="wide")

# create a naviagation side bar
st.sidebar.title("Dashboard")
st.title("Cricbuzz LiveStats")        # title on our main page


#create 4 pages
select = st.sidebar.radio(
    "Select Page",
    ["Live Stats", "Search Players", "📊SQL Query", "CRUD Operations"]
)

# when live page selected
if select == "Live Stats":
    live.title()
    # live.match()

# when player search page selected   
elif select == "Search Players":
    playerstat.title()
    # playerstat.playerstatistics()

# when SQL query page selected
elif select == "📊SQL Query":
    st.subheader("🏏 Database Query Questions")

    question_list = [
        "1- Players representing India",
        "2 -Recent matches",
        "3- Top 10 highest run scorers in ODI",
        "4- Venue having capacity of more than 25,000 spectators",
        "5- Win count of each team",
        "6- Count of players belonging to each playing role",
        "7- Highest individual batting score in each format",
        "8- Series started in 2024",
        "9- All rounder player statistics",
        "10- Last 20 completed matches",
        "11- Player performance comparision across different formats",
        "12- Team performance at home vs away",
        "13- Batting partnership of cinsecutive batsmen",
        "14- Bowling performance at different venues",
        "15- Close match performing players",
        "16- Batting perfromance over the year",
        "17- Win when winning the toss",
        "18- Economical bowlers in limited overs",
        "19- Consistent batsmen",
        "20- Matches played in different format by each player",
        "21- Player ranking",
        "22- Head-to-head match prediction analysis between teams",
        "23- Recent form and momentum of player",
        "24- Best player combination",
        "25- Time-series analysis"
    ]

    selection = st.selectbox(
        "☑️ Select a question to analyse",
        question_list
    )

    if selection == question_list[0]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question1()
            st.markdown("📊 Query Result:")

            # get data from database table
            query1 ="""
                    select
                    player_name, playing_role, batting_style, bowling_style
                    from indian_team
                """
            players_table = pd.read_sql(query1, con)

            # display on dashboard
            st.dataframe(players_table, use_container_width=True, hide_index=True)
    
    elif selection == question_list[1]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question2()
            st.markdown("📊 Query Result:")

            query2 = """
                select
                description,
                team1,
                team2,
                venue,
                city,
                status
                from recent_matches
            """

            # get data from database table 
            matches = pd.read_sql(query2, con)

            # display on dashboard
            st.dataframe(
                matches,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "match_description" : st.column_config.TextColumn(
                        "Match Description",
                        width= "large"
                    ),
                    "team1" : st.column_config.TextColumn(
                        "Team 1"
                    ),
                    "team2" : st.column_config.TextColumn(
                        "Team 2"
                    ),
                    "venue" : st.column_config.TextColumn(
                        "Venue"
                    ),
                    "match_date" : st.column_config.DateColumn(
                        "Date"
                    )
                }
            )
    
    # QUESTION 3
    elif selection == question_list[2]:
        st.markdown(f"#### {selection}")
        
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question3()
            st.markdown("📊 Query Result:")
            query3 = """
                select 
                id,
                player_name,
                runs,
                average
                from odi_top_scorers
            """
            # get data from database table 
            odi_top_scorers = pd.read_sql(query3, con)

            # display on dashboard
            st.dataframe(
                odi_top_scorers,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id" : st.column_config.TextColumn(
                        "Player ID"
                    ),
                    "player_name" : st.column_config.TextColumn(
                        "Player Name"
                    ),
                    "average" : st.column_config.TextColumn(
                        "Batting Average"
                    ),
                    "runs" : st.column_config.TextColumn(
                        "Runs Scored"
                    )
                }
            )

    
    # QUESTION 4

    elif selection == question_list[3]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question4()
            st.markdown("📊 Query Result:")
            query4 = """
                        select 
                        venue_name,
                        city,
                        country,
                        capacity
                        from ground_capacity
                    """
            # get data from database table 
            ground_capacity = pd.read_sql(query4, con)
            st.dataframe(
                        ground_capacity,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "groundname" : st.column_config.TextColumn(
                                "venue Name"
                            ),
                            "city" : st.column_config.TextColumn(
                                "City"
                            ),
                            "country" : st.column_config.TextColumn(
                                "Country"
                            ),
                            "capacity" : st.column_config.TextColumn(
                                "Capacity"
                            )
                        }
                    )

    # QUESTION 5
    elif selection == question_list[4]:
        st.markdown(f"#### {selection}")
        
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question5()
            st.markdown("📊 Query Result:")
            query5 = """
                select 
                team_name,
                total_wins
                from team_wins
            """
            # get data from database table 
            team_wins = pd.read_sql(query5, con)

            # display on dashboard
            st.dataframe(
                team_wins,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "team_name" : st.column_config.TextColumn(
                        "Team Name"
                    ),
                    "total_wins" : st.column_config.TextColumn(
                        "Count of wins"
                    )
                }
            )


    # QUESTION 6
    elif selection == question_list[5]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question6()
            st.markdown("📊 Query Result:")
            query6 = """
                select 
                player_name,
                playing_role
                from indian_team
            """
            # get data from database table 
            indian_team = pd.read_sql(query6, con)

            # display on dashboard
            st.dataframe(
                indian_team,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "player_name" : st.column_config.TextColumn(
                        "Player Name"
                    ),
                    "playing_role" : st.column_config.TextColumn(
                        "Playing Role"
                    )
                }
            )

        
    # QUESTION 7
    elif selection == question_list[6]:
        st.markdown(f"#### {selection}")

        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question7()
            st.markdown("📊 Query Result:")
            query7 = """
                select 
                player_id,
                player_name,
                test_value,
                odi_value,
                t20_value
                from player_batting_summary
                """
            # get data from database table 
            player_batting_summary = pd.read_sql(query7, con)

            # display on dashboard
            st.dataframe(
                player_batting_summary,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "player_id" : st.column_config.TextColumn(
                        "Format"
                    ),
                    "player_name" : st.column_config.TextColumn(
                        "Highest Score"
                    ),
                    "test_value" : st.column_config.TextColumn(
                        "Highest Score"
                    ),
                    "odi_value" : st.column_config.TextColumn(
                        "Highest Score"
                    ),
                    "t20_value" : st.column_config.TextColumn(
                        "Highest Score"
                    )
                }
            )


# when CRUDs page selected
elif select == "CRUD Operations":
    st.subheader("CRUD Operations")
    crudops.title()


# when CRUDs page selected
elif select == "🛠️ CRUD Operations":
    st.title("🛠️ CRUD Operations")
    crudops.title()

    choice = st.selectbox(
        "Chose an operation:",
        ["➕Create (Add Player)", "📖Read (Load Players)", "🖊️Update player (Edit Player)", "🗑️Delete (Remove Player)"]
    )

    if choice == "➕Create (Add Player)":
        # crudops.create()
        crudops.add()
    
    elif choice == "📖Read (Load Players)":
        crudops.read()

    elif choice == "🖊️Update player (Edit Player)":
            crudops.update()

    elif choice == "🗑️Delete (Remove Player)":
            crudops.delete()