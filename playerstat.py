import streamlit as st
import psycopg2 
import pandas as pd


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
    

def title():
    st.title("🔍 Search Players")

def playerstatistics():
    search = st.text_input(
        "Search a player",
        placeholder="like Virat Kohli, Sachin, Rohit, etc. "
        )
    # player search api
    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"

    querystring = {"plrN":f"{search}"}

    headers = {
        "x-rapidapi-key": "cfc139f9acmsh9c243115962adf0p162b35jsn49345f34cdca",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    search_data = response.json()

    # create player search list
    search_list = []
    for plyr in search_data['player']:
        search_list.append({
            'Name' : plyr['name'],
            'PlayerID' : plyr['id']
        })
    
    # searched names list
    search_names = []
    for names in search_list:
        search_names.append(names['Name'])
    
    # searches players ids list
    search_id = []
    for ids in search_list:
        search_id.append(ids['PlayerID'])

    # create a select box

    selected_player = st.selectbox(
        "Found Player",
        search_names
    )

    selected_player_id = next(
        i['PlayerID'] for i in search_list if i['Name']==selected_player
    )

    # personal information of selected player
    
    import requests

    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{selected_player_id}"

    headers = {
        "x-rapidapi-key": "cfc139f9acmsh9c243115962adf0p162b35jsn49345f34cdca",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    player_info = response.json()

    # cricketing information
    cricket_details = {
        'Role': player_info.get('role','unavailable'),
        'Batting Style' : player_info.get('bat', 'unavailable'),
        'Bowling style': player_info.get('bowl', 'unavailable'),
        'International Team' : player_info.get('intlTeam','unavailable') 
    }

    # personal details
    personal_details = {
        'Date of Birth' : player_info.get('DoB', 'unavailable'),
        'Birthplace' : player_info.get('birthPlace', 'unavailable'),
        'Height' : player_info.get('height', 'unavailable'),
        'Nickname' : player_info.get('nickName','unavailable')
    }

    # teams played for
    teams_detail = []
    for i in player_info['teamNameIds']:
        teams_detail.append(i['teamName'])

    # profile link
    player_profile_link = player_info['appIndex']['webURL']

    # batting profile of selected player

    # player batting info
    import requests

    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{selected_player_id}/batting"

    headers = {
        "x-rapidapi-key": "cfc139f9acmsh9c243115962adf0p162b35jsn49345f34cdca",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    player_batstat = response.json()

    # query to create bat stat table
    cursor.execute("drop table if exists player_batting_stats")
    cursor.execute("""
        create table player_batting_stats (
                Statistic varchar(15),
                Test float,
                ODI float,
                T20 float,
                IPL float
                )
    """)

    # query to insert batting statistics into the table
    query = """
        insert into player_batting_stats values
        (%s,%s,%s,%s,%s)
    """

    # nested execution of query to insert every row in the table
    for values in player_batstat['values']:
        row = values['values']
        cursor.execute(query,row)
    

    # bowling profile of selected player

    # player bowling info

    import requests

    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{selected_player_id}/bowling"

    headers = {
        "x-rapidapi-key": "cfc139f9acmsh9c243115962adf0p162b35jsn49345f34cdca",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    player_bowlstat = response.json()

    #query to create bowl stat table
    cursor.execute("drop table if exists player_bowling_stats")
    cursor.execute("""
        create table player_bowling_stats (
                Statistic varchar(15),
                Test varchar(10),
                ODI varchar(10),
                T20 varchar(10),
                IPL varchar(10)
                )
    """)

    # query to insert bowling statistics into the table
    query = """
        insert into player_bowling_stats values
        (%s,%s,%s,%s,%s)
    """

    # nested execution of query to insert every row in the table
    for values in player_bowlstat['values']:
        row = [None if value == "-/-" else value for value in values['values']]
        print(row)
        cursor.execute(query,row)
    
    # SHOWING DETAILS ON STREAMLIT APP

    st.write(f"# 📊 {selected_player}")

    profile, bat, bowl = st.tabs(["🪪 Profile", "🏏 Batting Stats", "⚡ Bowling Stats"])

    with profile:
        st.write("### 🗎 Personal Information")
        column1, column2, column3 = st.columns(3)

        with column1:
            st.markdown(f"""
                ##### 🏏 Cricket Details <br>
                Role : {cricket_details['Role']} <br>
                Batting : {cricket_details['Batting Style']} <br>
                Bowling : {cricket_details['Bowling style']} <br.
                International Team : {cricket_details['International Team']}
            """, True)
        with column2:
            st.markdown(f"""
                ##### 🗎 Personal Details <br>
                Nickname : {personal_details['Nickname']} <br>
                Date of Birth : {personal_details['Date of Birth']} <br>
                Birthplace : {personal_details['Birthplace']} <br>
                Height : {personal_details['Height']}
            """, True)
        with column3:
            st.markdown(f"##### 🏆 Teams Played for", True)
            for i in teams_detail:
                st.write(f"- {i}")
    
    # showing batting stats table
    with bat:
        st.write("#### 🏏Battin Career")
        st.write("##### 📊Batting Stats Overview")
        query = "select * from player_batting_stats"
        batting_stats = pd.read_sql(query,con)
        st.dataframe(batting_stats, hide_index=True, use_container_width=True)
    
    # showing bowling stats table
    with bowl:
        st.write("#### ⚡Bowling Career")
        st.write("##### 📊Bowling Stats Overview")
        query = "select * from player_bowling_stats"
        bowling_stats = pd.read_sql(query,con)
        st.dataframe(bowling_stats, hide_index=True, use_container_width=True)
    
    st.markdown(f"Cricbuzz Profile Link : {player_profile_link}")

    # st.write("## Personal Information")
    # st.write(f"Nickname : {personal_details['Nickname']}, DoB : {personal_details['Date of Birth']} Height : {personal_details['Height']}, Place of Birth : {personal_details['Birthplace']}")
    # st.write(f"Profile link : {player_profile_link}")
    # st.write(teams_detail)

def bat_table():
    query = "select * from player_batting_stats"
    batting_stats = pd.read_sql(query,con)
    st.write("### Batting Stats")
    st.dataframe(batting_stats, hide_index=True, use_container_width=True)

def bowl_table():
    query2 = "select * from player_bowling_stats"
    bowling_stats = pd.read_sql(query2, con)
    st.write("### Bowling Stats")
    st.dataframe(bowling_stats, hide_index=True, use_container_width=True)

    


