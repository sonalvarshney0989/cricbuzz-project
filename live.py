import streamlit as st
import psycopg2
import pandas as pd

# connection to database

con = psycopg2.connect(
    user = 'postgres',
    password = 'sonal0989',
    port = 5432,
    database = 'sonal',
    host = 'localhost'
)
cursor = con.cursor()
con.autocommit=True

def title():
    st.title("⌚ Live Matches")

def match():
    # Live Matches
    # api call
    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
        "x-rapidapi-key": "cfc139f9acmsh9c243115962adf0p162b35jsn49345f34cdca",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    # getting final information in human readable form
    live_data = response.json()
    LiveMatches = []
    ListLiveMatches = []
    LiveMatchID = []
    for matchtype in live_data['typeMatches']:
        for seriesmatch in matchtype['seriesMatches']:
            if 'seriesAdWrapper' in seriesmatch:
                seriesmatch = seriesmatch['seriesAdWrapper']
                Series_ID = seriesmatch['seriesId']
                Series_Name = seriesmatch['seriesName']
                Matches = seriesmatch['matches']
                for match in Matches:
                    if 'matchInfo' in match:
                        match_info = match['matchInfo']
                        #match_info
                        matchID = match_info['matchId']
                        matchNum = match_info['matchDesc']
                        s_name = match_info['seriesName']
                        format = match_info['matchFormat']
                        date = match_info['startDate']
                        venue = match_info['venueInfo']['ground']
                        city = match_info['venueInfo']['city']
                        team1 = match_info['team1']['teamName']
                        team2 = match_info['team2']['teamName']
                        status = match_info['status']    
                    if 'matchScore' in match:
                        match_score = match['matchScore']

                    
                        #match score
                        #team1
                        if 'team1Score' in match_score:
                            if 'runs' in match_score['team1Score']['inngs1']:
                                runst1 = match_score['team1Score']['inngs1']['runs']
                            else:
                                runst1 = '0'
                            if 'overs' in match_score['team1Score']['inngs1']:
                                overst1 = match_score['team1Score']['inngs1']['overs']
                            else:
                                overst1 = '0'
                            if 'wickets' in match_score['team1Score']['inngs1']:
                                wktst1 = match_score['team1Score']['inngs1']['wickets']
                            else:
                                wktst1 = '0'
                        else:
                            runst1, overst1, wktst1 = '0','0','0'
                        #team2
                        if 'team2Score' in match_score:
                            if 'runs' in match_score['team2Score']['inngs1']:
                                runst2 = match_score['team2Score']['inngs1']['runs']
                            else:
                                runst2 = '0'
                            if 'overs' in match_score['team2Score']['inngs1']:
                                overst2 = match_score['team2Score']['inngs1']['overs']
                            else:
                                overst2 = '0'
                            if 'wickets' in match_score['team2Score']['inngs1']:
                                wktst2 = match_score['team2Score']['inngs1']['wickets']
                            else:
                                wktst2 = '0'
                        else:
                            runst2, overst2, wktst2 = '0','0','0'
                    else:
                        runst1,runst2,overst1,overst2,wktst1,wktst2 = '0','0','0','0','0','0'
                    LiveMatches.append({
                        'Team1 name' : team1,
                        'Team2 name' : team2,
                        'series' : s_name,
                        'Format' : format,
                        'Match ID' : f"{matchID}",
                        'Match Num' : matchNum,
                        'Date' : date,
                        'Venue' : f"{venue}, {city}",
                        'Team1 runs' : runst1,
                        'Team2 runs' : runst2,
                        'Team1 Score' : f"{runst1}/{wktst1} ({overst1})",
                        'Team2 Score' : f"{runst2}/{wktst2} ({overst2})",
                        'Status' : status
                    })
                    ListLiveMatches.append(
                        f"{team1} vs {team2}" 
                    )
                    LiveMatchID.append({
                        "Match name" : f"{team1} vs {team2}" ,
                        "Match ID": f"{matchID}"
                    })
    match_list = [i["Match name"] for i in LiveMatchID]



    selected_match = st.selectbox(
        "Select Match",
        match_list
    )
    selected_matchid = next(
        id["Match ID"] for id in LiveMatchID if id["Match name"]==selected_match
    )
    for matches in LiveMatches:
        if matches["Match ID"] == selected_matchid:
            st.write(f"Series : {matches['series']}")
            st.write(f"Match : {matches['Match Num']}")
            st.write(f"Format : {matches['Format']}")
            st.write(f"Venue : {matches['Venue']}")
            st.write(f"{matches['Team1 name']}'s score : {matches['Team1 Score']}")
            st.write(f"{matches['Team2 name']}'s score : {matches['Team2 Score']}")
            st.write(f"Status : {matches['Status']}")
    
    
    # for scorecard
    # getting score card of live match
    # api call
    import requests

    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{selected_matchid}/scard"

    headers = {
        "x-rapidapi-key": "cfc139f9acmsh9c243115962adf0p162b35jsn49345f34cdca",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    score_data = response.json()

    # nesting to exttract valuable information

    bat_stat1 = []
    bat_stat2 = []
    for s in score_data['scorecard']:
        if s['inningsid'] == 1:
            for ps in s['batsman']:
                name = ps['name']
                runs = ps['runs']
                balls = ps['balls']
                sixes = ps['sixes']
                fours = ps['fours']

                bat_stat1.append({
                    'name' : name,
                    'runs' : runs,
                    'balls' : balls,
                    'sixes' : sixes,
                    'fours' : fours
                })
        elif s['inningsid'] == 2:
            for ps in s['batsman']:
                name = ps['name']
                runs = ps['runs']
                balls = ps['balls']
                sixes = ps['sixes']
                fours = ps['fours']

                bat_stat2.append({
                    'name' : name,
                    'runs' : runs,
                    'balls' : balls,
                    'sixes' : sixes,
                    'fours' : fours
                })


    # for 1st inning
    cursor.execute("drop table if exists innings1_scorecard")
    cursor.execute("""
                create table innings1_scorecard(
                Name varchar(30),
                Runs smallint,
                Balls smallint,
                Sixes smallint,
                Fours smallint)
                """)

    query_scorecard = """
                    insert into innings1_scorecard(Name,Runs,Balls,Sixes,Fours) values
                    (%s,%s,%s,%s,%s)
    """
    for i in  bat_stat1:
        row = (i['name'],i['runs'],i['balls'],i['sixes'],i['fours'])
        cursor.execute(query_scorecard,row)


    # for 2nd inning
    cursor.execute("drop table if exists innings2_scorecard")
    cursor.execute("""
                create table innings2_scorecard(
                Name varchar(30),
                Runs smallint,
                Balls smallint,
                Sixes smallint,
                Fours smallint)
                """)

    query_scorecard = """
                    insert into innings2_scorecard(Name,Runs,Balls,Sixes,Fours) values
                    (%s,%s,%s,%s,%s)
    """
    for i in  bat_stat2:
        row = (i['name'],i['runs'],i['balls'],i['sixes'],i['fours'])
        cursor.execute(query_scorecard,row)

    # showing scorecard on webpage

     # scorecard team 1
    q1 = "select * from innings1_scorecard"
    sc1 = pd.read_sql(q1, con)
    st.subheader("Scorecard Team 1")
    st.dataframe(sc1, use_container_width=True,hide_index=True)

    # scorecard team 2
    q2 = "select * from innings2_scorecard"
    sc2 = pd.read_sql(q2, con)
    st.subheader("Scorecard Team 2")
    st.dataframe(sc2, use_container_width=True,hide_index=True)
