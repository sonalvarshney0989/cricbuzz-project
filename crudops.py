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
    st.markdown("#### 🗒️ Create, Read, Update, Delete Player records")

def create():
    cursor.execute("drop table if exists cruds_table")
    cursor.execute("""
        create table cruds_table (
        id int,
        name varchar(50),
        matches int,
        overs float,
        wickets int,
        economy float
        )                
    """)
    insertCRUDs = """
        insert into cruds_table values
        (%s,%s,%s,%s,%s,%s)
    """

    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

    querystring = {"statsType":"lowestEcon","matchType":"1"}

    headers = {
        "x-rapidapi-key": "26ac642350msh32a0dd01efaadf5p102886jsnc1f3d91af0ab",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    datacruds = response.json()

    for i in datacruds.get('values', []):
        row = i.get('values', [])
        cursor.execute(insertCRUDs, row)

def add():
    st.markdown("#### ➕ Add a new player")

    col1, col2 = st.columns(2)

    with col1:
        id = st.number_input("Player ID", min_value=0, step=1)
        name = st.text_input("Player Name", placeholder= "enter player name")
        matches = st.number_input("Matches", min_value=0, step=1)
    
    with col2:
        overs = st.number_input("Overs")
        wickets = st.number_input("Wickets", min_value=0, step=1)
        economy = st.number_input("Economy")
    
    if st.button("➕Add Player"):
        insertCRUDs = """
            insert into cruds_table values
        (%s,%s,%s,%s,%s,%s)
        """
        row = (id, name, matches, overs, wickets, economy)
        
        cursor.execute(insertCRUDs, row)


def read():
    st.markdown("#### 📖 View All Players")

    if st.button("📊 Load All Players", ):
        query = "select * from cruds_table"

        data = pd.read_sql(query, con)

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

def update():
    st.markdown("##### Update player information")

    player = st.text_input(
        "🔍Search for player to update:",
        placeholder= "enter player name"
    )
    
    if player:
        queryget2 = f"""
                select name, id, wickets, matches, economy, overs
                from cruds_table
                where  name = %s
        """
        df1 = pd.read_sql(queryget2, con, params=(player,))
        if not df1.empty:

            df = df1.iloc[0]
            pname = df['name']
            pmatches = df['matches']
            povers = df['overs']
            pwickets = df['wickets']
            peco = df['economy']
            Id = df['id']

            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Player Name", value= pname)
                matches = st.number_input("Matches", value=pmatches, step=1 )
                overs = st.number_input("Overs", value= povers)
            
            with col2:
                wickets = st.number_input("Wickets", value=pwickets, step=1)
                economy = st.number_input("Economy", value= peco)

            if st.button("Update Player"):
                update = f"""
                        update cruds_table
                        set 
                            name = '{name}',
                            matches = '{matches}',
                            overs = '{overs}',
                            wickets = '{wickets}',
                            economy = '{economy}'
                        where id = '{Id}'
                    """
                cursor.execute(update)

                st.write("Updated")
        else:
            st.write("No player with this name")
        




def delete():

    player = st.text_input(
        "🔍Search Player to delete",
        placeholder= "enter full name of player"
    )

    queryget = f"""
        select name, id, wickets
        from cruds_table
        where  name = '{player}'
    """

    df = pd.read_sql(queryget, con)

    df['disp'] = (
        df['name'] + 
        " (ID : " + df['id'].astype(str) + ")" +
        " - " + df['wickets'].astype(str) + "wickets"
    )

    selected = st.selectbox(
        "Select player to delete:",
        df['disp']
    )

    confirmation = st.text_input(
        f"Type Delete to delete: {player}"
    )

    if confirmation == 'Delete':
        del_query = f"""
            delete from cruds_table
            where name = '{player}'
            """
        cursor.execute(del_query)

        st.write("Player Removed")

    
    