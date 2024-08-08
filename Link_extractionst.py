import streamlit as st
import google.generativeai as genai
import serpapi
import mysql.connector as sql
import csv 
import re 
import pandas as pd
import base64
import datetime

# Initialize df as an empty DataFrame
df = pd.DataFrame(columns=['Name', 'Link', 'Query'])

# Function to generate boolean search query
def generate_search_query(user_input):
    # Configure GenerativeAI
    genai.configure(api_key="Gemini-API-Key")

    # Initialize the GenerativeAI model
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content(f'''Prompt: As an aspiring talent seeker, you're eager to find the perfect candidates for various roles. You've compiled a list of desired qualifications and universities. Your task is to craft Boolean search queries tailored to these criteria. Remember to focus solely on generating the search queries, excluding any additional information. Utilize LinkedIn platforms for your search.
                                      
                                      Desired Qualifications and Universities:

                                      Question : I need a MIT computer science graduate for python developer
                                      Answer : "MIT computer science" (software engineer OR python developer OR data scientist) site:linkedin.com

                                      Question :provide me data science student profiles from Harvard University in the US
                                      Answer : "data science " student Harvard University (US OR United States) site:linkedin.com

                                      Question : give me a undergraduate students with a passion for cybersecurity from Georgia Institute of Technology (GA) and University of Illinois Urbana-Champaign (IL)
                                      Answer : "cybersecurity" student ("Georgia Institute of Technology" OR "University of Illinois Urbana-Champaign") (US OR "United States") (club OR forum) site:linkedin.com

                                      Question: I need few profiles where data science is required as a skill.
                                      Answer: "data science" (required OR necessary OR must-have OR essential) site:linkedin.com

                                      Question: give me a technical intern profiles from pozent Labs 
                                      Answer : site:linkedin.com "company pozent Labs" "technical intern"

                                      Question : give me a Gen AI intern profiles from pozent Labs 
                                      Answer : site:linkedin.com "company pozent Labs" "Gen AI"

                                      Question :  provide me a Datascience profiles from harvard university
                                      Answer : "data science " student Harvard University (US OR United States) site:linkedin.com

                                      Question :  i need a bsc computer science students from gurunanak college of arts and science whose name is Nagarajan B J 
                                      Answer : "bsc computer science" student "Gurunanak College of Arts and Science" "Nagarajan B J" site:linkedin.com

                                      Question : Find a LinkedIn profile of a student named Easuraja A studying BSc Computer Science at the University of Madras.
                                      Answer : "bsc computer science" student "University of Madras" "Easuraja A" site:linkedin.com

                                      Question : give me data science profile from IIT madras
                                      Answer : "data science" student IIT Madras site:linkedin.com

                                      Question : give me python profile from IIT madras
                                      Answer : "python" student "IIT Madras" site:linkedin.com

                                      Question: provide me data science student profiles from Stanford University
                                      Answer: "data science" student Stanford University (US OR United States) site:linkedin.com

                                      Question: provide me data science student profiles from University of California, Berkeley
                                      Answer: "data science" student "University of California, Berkeley" (US OR United States) site:linkedin.com

                                      Question: provide me data science student profiles from University of Southern California
                                      Answer: "data science" student "University of Southern California" (US OR United States) site:linkedin.com

                                      Question: provide me data science student profiles from University of Texas at Austin
                                      Answer: "data science" student "University of Texas at Austin" (US OR United States) site:linkedin.com

                                      Question: provide me data science student profiles from University of Washington
                                      Answer: "data science" student "University of Washington" (US OR United States) site:linkedin.com

                                      Question :  i need a bsc computer science students from gurunanak college of arts and science 
                                      
                                      --- instructions : 
                                      1.Start with the academic qualification or course name enclosed in quotation marks, like: "academic qualification".
                                      2.Enclose the name of the educational institution or college in quotation marks, for example: "college name".
                                      3.Specify the name of the student enclosed in quotation marks, like: "full name".
                                      4.Specify the desired platform using the format: site:platformname.com.
                                      5.Combine all elements into a Boolean search query, for instance: "academic qualification" "college name" "full name" site:platformname.com.

                                      Answer : "bsc computer science" student "Gurunanak College of Arts and Science" site:linkedin.com

                                      
                                      Question : {user_input}
                                      Answer : 
                                      Modify this prompt to create a Boolean search query. Provide only the search query, excluding any additional details. Use sites as LinkedIn.
                                      ''')
    
    response_text = response.text
    response_text = response_text.replace("*", "").strip()
    print(response_text)
    st.write(f"Generated boolean query: ",{response_text})
    return response_text

# Function to perform Google search with fallback mechanism for multiple API keys
def search_google(query, num_results, api_keys):
    for api_key in api_keys:
        print(f"Using API Key: {api_key}")
        params = {
            "api_key": api_key,
            "q": query,
            "engine": "google",
            "num": num_results
        }
        try:
            results = serpapi.search(params)
            if results.get("search_metadata"):
                return results
        except Exception as e:
            print(f"API Key {api_key} failed with error: {e}")
            continue
    return {"error": "All API keys failed"}

# Function to save data to MySQL database 
# store in local database
def save_to_database(name, link, user_query):
    db = sql.connect(
        host="localhost",
        user="root",
        password="root123",
        database="tth"
    )
    cursor = db.cursor()
    sql_query = "INSERT INTO link_extractor (name, link, jd, Event_Timestamp) VALUES (%s, %s, %s, %s)"
    sql_values = (name, link, user_query,datetime.datetime.now())
    cursor.execute(sql_query, sql_values)
    db.commit()

# store in common database
def connect_to_mysql(name, link, user_query):
    db = sql.connect(
        host="192.168.0.172",
        user="root",
        password="root123",
        database="data"
    )
    cursor = db.cursor()
    sql_query = "INSERT INTO link_extractor (name, link, jd, Event_Timestamp) VALUES (%s, %s, %s, %s)"
    sql_values_THH = (name, link, user_query,datetime.datetime.now())
    cursor.execute(sql_query, sql_values_THH)
    db.commit()

def save_to_csv(results):
    with open('search_results.csv', mode='w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Snippet', 'Link'])
        if "organic_results" in results:
            for result in results["organic_results"]:
                writer.writerow([result.get('title', ''), result.get('snippet', ''), result.get('link', '')])

# Streamlit UI
def main():
    global df  # Accessing the global variable df
    st.title("THH Link Extractor")
    user_input = st.text_input("Enter your prompt:")
    file_name = st.text_input("Enter the file name to save : ")
    if st.button("Search"):
        boolean_query = generate_search_query(user_input)
        api_keys = [
            "Serp-API-Key",
        ]
        results = search_google(boolean_query, num_results=300, api_keys=api_keys)
        if "error" not in results:
            if "organic_results" in results:
                for result in results["organic_results"]:
                    name = result.get('title', '')
                    link = result.get('link', '')
                    if re.match(r"https://(www|in|uk|us|ca|au|fr|de|es|it|cn|jp|br|mx|sg|nz|za|ae|sa|hk|my|id|th|ph|vn|kr|tw|se|no|fi|dk|nl|be|ch|at|pl|cz|hu|tr|il|ru|ie|pt|gr)\.linkedin\.com/in/.*", link):

                        # Append data as a dictionary to a list
                        df_list = [{'Name': name, 'Link': link, 'Query': user_input}]
                        # Concatenate the list of dictionaries with the existing DataFrame
                        df = pd.concat([df, pd.DataFrame(df_list)], ignore_index=True)
                        save_to_database(name, link, user_input)
                        # try:
                        #     connect_to_mysql(name,link,user_input)
                        # except:
                        #     pass

        # Display output
        st.subheader("Search Results")
        if not df.empty:
            st.dataframe(df)  # Display data as DataFrame

            # Save data as CSV
            csv_filename = f"{file_name}.csv"
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to bytes
            href = f'<a href="data:file/csv;base64,{b64}" download="{csv_filename}">Download CSV file</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
