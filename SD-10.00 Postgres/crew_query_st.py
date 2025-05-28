import streamlit as st 
import os 
import pandas as pd  
from crew_query import SQLQueryCrew
from postgres_connection import PostgresConnection
from postgres_db import PostgresDB

root = os.path.dirname(os.path.abspath(__file__))

sql_crew = SQLQueryCrew()

st.title("AI - Query")
st.sidebar.header("Query Config")

database_type = st.sidebar.selectbox("Banco:",['Postgres','MySQL','SQLite'], index=0)

database_name = st.sidebar.selectbox("Nome do banco:",["ecommerce","clinica"],index=0)

schema_path = os.path.join(root, "schemas",f"schema_{database_name}.yaml")

user_request = st.text_area("You question?","")

exibir_grafico = st.checkbox("Show results in chart?")

if st.button("Run query"):
    if not user_request.strip():
        st.warning("Question is empty.")
    else: 
        inputs = {
            "database_type": database_type,
            "database_name": database_name,
            "yaml_path": schema_path,
            "user_request": user_request,
            "json_output": False 
        }

        sql_query = sql_crew.kickoff(inputs)
        
        st.subheader("SQL Query Crew finished its work...")
        
        if sql_query:
            selected_database = PostgresDB.get_database_uri(database_name)
            conn = PostgresConnection(db_uri=selected_database)
            conn.connect()
            
            cursor = conn.cursor
            cursor.execute(sql_query)
            
            results = cursor.fetchall()
            colunas = conn.get_colunas()
            
            conn.disconnect()
            df = pd.DataFrame(results, columns=colunas)
            
            st.subheader("Query results:")
            
            if exibir_grafico:
                #tratamento de regionalismo: . e , como separadores decimais
                for col in df.columns:
                    try:
                        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",","."))
                    except ValueError:
                        pass
                
                numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
                
                if len(numeric_columns) >= 1:
                    st.bar_chart(df.set_index(df.columns[0]))
                else:
                    st.warning("No numerical values to be shown in a chart")
            st.dataframe(df)
        else:
            st.warning("Crew generated no results") 
            