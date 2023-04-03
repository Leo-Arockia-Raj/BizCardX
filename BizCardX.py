import streamlit as st
import mysql.connector
import pandas as pd
import easyocr
import text_classifier
import numpy as np
from PIL import Image
from io import BytesIO

def extract_information(image):
    """ input : business card image
       output : extracted information of company name, cardholder name, designation, mobile number, email address,
       website URL, area, city, state, pin code"""
    if image:  # extract from image using easyocr
        input_image = Image.open(image)  # read image
        reader = easyocr.Reader(['en'])
        results = reader.readtext(np.array(input_image))
        extracted_words = []
        for text in results:
            extracted_words.append(text[1].strip())
        return extracted_words
        # # 1.png
        # return ('Selva', 'DATA MANAGER', '+123-456-7890', '+123-456-7891',
        #         'WWW XYZI.com', 'hello@XYZ1.com', '123 ABC St , Chennai;',
        #         'selva', 'TamilNadu 600113', 'digitals')
        # # 2.png
        # return ('Amit kumar', 'CEO & FOUNDER', '123-456-7569', 'hello@global.com', 'WWW', 'global.com',
        #         '123 global', 'Erode,', 'GLOBAL', 'TamilNadu 600115', 'INSURANCE', 'St ,')
        # # 3.png
        # return ('KARTHICK', 'General Manager', '123 ABC St , Salem,', 'TamilNadu 6004513', '+123-456-7890',
        #         'hello@Borcelle.com', 'www Borcelle.com', 'BORCELLE', 'AIRLINES')
        # # 4.png
        # return ('REVANTH', 'Marketing Executive', '123 ABC St,, HYDRABAD, TamilNadu;', '600001',
        #         '+91-456-1234', 'hello@CHRISTMAS.com', 'Family', 'wWW.CHRISTMAS.com', 'Restaurant')
        # # 5.png
        # return ('SANTHOSH', 'Technical Manager', '123 ABC St , Tirupur; TamilNadu,', '641603', '+123-456-1234',
        #         'hello@Sun.com', 'www.Suncom', 'Sun Electricals')
    else:  # Default display data
        return ('Xyz Company', 'Abcd', 'CEO', '+123-123-2345', 'business@gmail.com',
                'www.business_card.com', '123 Qwerty St.', 'Chennai', 'Tamil Nadu', '101010')


def create_database(host, user, password, database_name):
    """ Creates a Database named 'database_name' if database 'database_name' does not exist. """
    # Connect to the MySQL database
    mydb = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
    )
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]
    if database_name.lower() in databases:
        print(f"{database_name} already exists.")
    else:
        mycursor.execute(f"CREATE DATABASE {database_name}")
        mydb.close()


def connect_database(host, user, password, database):
    """"Establishes a connection with mysql database"""
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return mydb


def sql_table_creation(host, user, password, database, table_name):
    """ Creates a table in 'database' named 'table_name' if table 'table_name' does not exist. """
    mydb = connect_database(host=host, user=user, password=password, database=database)
    table_query = mydb.cursor()
    table_query.execute("show tables")
    tables = [table[0] for table in table_query.fetchall()]
    if table_name.lower() in tables:
        print(f"{table_name} table already exists")
    else:
        query = f"CREATE TABLE {table_name} (Company_Name varchar(255), Card_Holder_Name varchar(255), " \
                f"Designation varchar(255), Mobile_Number varchar(255), Email_Address varchar(255), " \
                f"Website_URL varchar(255), Area varchar(255), City varchar(255), State varchar(255)," \
                f" Pincode varchar(255), Card longblob)"
        table_query.execute(query)
        mydb.commit()
    table_query.close()
    mydb.close()


st.set_page_config(page_icon=":shark:", page_title="BizCardX", layout="wide")
st.title(":green[Business Card Reader|:shark:|]")

tab1, tab2 = st.tabs(["Upload New Business Card", "Modify Existing Business Card"])
# ------------------------------- Upload New Business Card : Start ------------------------------- #
with tab1:
    st.subheader("Business Card Upload : ")

    col1, col2, col3 = st.columns(3)
    with col1:  # Upload
        card_image = st.file_uploader("**:orange[Upload an Image of a Business Card]**", type=["jpg", "jpeg", "png"])
        if card_image:
            st.image(card_image)
        result = extract_information(card_image)
    (company_name, card_holder_name, designation, mobile_number, email_address,
     website_URL, area, city, state, pin_code) = text_classifier.text_classifier(result)

    with col2:  # Display classified data
        company_name = st.text_input("**:orange[Company Name:]**", company_name)
        card_holder_name = st.text_input("**:orange[Card Holder Name:]**", card_holder_name)
        designation = st.text_input("**:orange[Designation:]**", designation)
        mobile_number = st.text_input("**:orange[Mobile Number:]**", mobile_number)
        email_address = st.text_input("**:orange[email Address:]**", email_address)

    with col3:  # Display classified data
        website_URL = st.text_input("**:orange[Website URL:]**", website_URL)
        area = st.text_input("**:orange[Area:]**", area)
        city = st.text_input("**:orange[City:]**", city)
        state = st.text_input("**:orange[State:]**", state)
        pin_code = st.text_input("**:orange[Pin_code:]**", pin_code)

    # ----------------------- Database, Table Creation if not exist --------------------- #
    create_database(host="localhost", user="root", password="Philo@leo92", database_name='BusinessCardDb')
    sql_table_creation(host="localhost", user="root", password="Philo@leo92", database="BusinessCardDb", table_name='BusinessCards')

    if st.button("Click to Upload into Database"):  # Upload Card Data into Database.
        input_image = Image.open(card_image)  # read image
        mydb = connect_database(host="localhost", user="root", password="Philo@leo92", database="BusinessCardDb")
        query = mydb.cursor()
        query.execute(f"INSERT INTO BusinessCards(Company_Name, Card_Holder_Name, Designation, Mobile_Number, Email_Address, Website_URL, Area, City, State, Pincode, Card) VALUES ('{company_name}','{card_holder_name}','{designation}','{mobile_number}','{email_address}','{website_URL}','{area}','{city}','{state}','{pin_code}', '{input_image}')")
        mydb.commit()
        mydb.close()
        st.success("Upload Success!")
# ------------------------------- Upload New Business Card : End ------------------------------- #
# ------------------------------ View, Update, Delete Existing Cards : Start --------------------- #
with tab2:
    st.subheader("Business Card Update : ")
    mydb = connect_database(host="localhost", user="root", password="Philo@leo92", database="BusinessCardDb")
    tab1m, tab2m, tab3m = st.tabs(["Read", "Update", "Delete"])
    # ------------------------------- View Record : Start -------------------------------------- #
    with tab1m:
        if st.button("Click to Read"):
            qry = "select * from BusinessCards"
            dfm = pd.read_sql_query(qry, mydb)
            st.dataframe(dfm)
    # ------------------------------- View Record : End ----------------------------------------- #
    # -------------------------------Update Record : Start -------------------------------------- #
    with tab2m:
        Name_M = st.text_input("Enter Card Holder Name:", 'Mark Zuckerberg')

        qry = f"select * from BusinessCards where Card_Holder_Name = '{Name_M}'"
        df = pd.read_sql_query(qry, mydb)
        if len(df) == 0:
            st.markdown(f":red[Card_Holder_Name {Name_M} does not Exist.]")
            (fetch_company_name, fetch_card_holder_name, fetch_designation, fetch_mobile_number, fetch_email_address,
             fetch_website_URL, fetch_area, fetch_city, fetch_state, fetch_pin_code) = ('-', '-', '-', '-', '-', '-',
                                                                                        '-', '-', '-', '-')
        elif len(df) == 1:
            (fetch_company_name, fetch_card_holder_name, fetch_designation, fetch_mobile_number, fetch_email_address,
             fetch_website_URL, fetch_area, fetch_city, fetch_state, fetch_pin_code) = \
            (df.iloc[0, 0], df.iloc[0, 1], df.iloc[0, 2], df.iloc[0, 3], df.iloc[0, 4],
             df.iloc[0, 5], df.iloc[0, 6], df.iloc[0, 7], df.iloc[0, 8], df.iloc[0, 9])
            Mobile_Number_M = df.iloc[0, 3]

        else:
            Mobile_Number_M = st.text_input("Enter Mobile_Number:", "123456789")
            qry = f"select * from BusinessCards where Card_Holder_Name = '{Name_M}'and Mobile_Number ='{Mobile_Number_M}' "
            df = pd.read_sql_query(qry, mydb)
            st.dataframe(df)
            try:
                (fetch_company_name, fetch_card_holder_name, fetch_designation, fetch_mobile_number, fetch_email_address,
                 fetch_website_URL, fetch_area, fetch_city, fetch_state, fetch_pin_code) = \
                (df.iloc[0, 0], df.iloc[0, 1], df.iloc[0, 2], df.iloc[0, 3], df.iloc[0, 4],
                 df.iloc[0, 5], df.iloc[0, 6], df.iloc[0, 7], df.iloc[0, 8], df.iloc[0, 9])
            except:
                st.write("Enter Correct Mobile Number")
                (fetch_company_name, fetch_card_holder_name, fetch_designation, fetch_mobile_number,
                 fetch_email_address, fetch_website_URL, fetch_area, fetch_city, fetch_state,
                 fetch_pin_code) = ('-', '-', '-', '-', '-', '-', '-', '-', '-', '-')

            # (fetch_company_name, fetch_card_holder_name, fetch_designation, fetch_mobile_number, fetch_email_address,
            #  fetch_website_URL, fetch_area, fetch_city, fetch_state, fetch_pin_code) = ('Pinapple','Mark Zuckerberg', 'CEO', '+123-123-2345','mark@gmail.com',
            # 'www.apple.com','27 raman st.', 'kodabakam', 'USA', '624339')

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**:orange[Business Card:]**")
            # st.image(Image.frombytes(data=df.iloc[0, 10]))

        with col2:
            company_name_m = st.text_input("**:orange[Modify Company Name:]**", fetch_company_name)
            card_holder_name_m = st.text_input("**:orange[Modify Card Holder Name:]**", fetch_card_holder_name)
            designation_m = st.text_input("**:orange[Modify Designation:]**", fetch_designation)
            mobile_number_m = st.text_input("**:orange[Modify Mobile Number:]**", fetch_mobile_number)
            email_address_m = st.text_input("**:orange[Modify email Address:]**", fetch_email_address)
        with col3:
            website_URL_m = st.text_input("**:orange[Modify Website URL:]**", fetch_website_URL)
            area_m = st.text_input("**:orange[Modify Area:]**", fetch_area)
            city_m = st.text_input("**:orange[Modify City:]**", fetch_city)
            state_m = st.text_input("**:orange[Modify State:]**", fetch_state)
            pin_code_m = st.text_input("**:orange[Modify Pin_code:]**", fetch_pin_code)

            query = mydb.cursor()

            qry = f"update BusinessCards SET Company_Name='{company_name_m}', Card_Holder_Name='{card_holder_name_m}' , " \
                  f"Designation='{designation_m}', Mobile_Number='{mobile_number_m}', Email_Address='{email_address_m}'," \
                  f" Website_URL='{website_URL_m}', Area='{area_m}', City='{city_m}', State='{state_m}', Pincode='{pin_code_m}' " \
                  f"where Card_Holder_Name = '{Name_M}' and Mobile_Number = '{Mobile_Number_M}';"
            #
            # qry = f"update BusinessCards SET Company_Name='{company_name_m}', Card_Holder_Name='{card_holder_name_m}' , " \
            #       f"Designation='{designation_m}', Mobile_Number='{mobile_number_m}', Email_Address='{email_address_m}'," \
            #       f" Website_URL='{website_URL_m}', Area='{area_m}', City='{city_m}', State='{state_m}', Pincode='{pin_code_m}' " \
            #       f"where Card_Holder_Name = '{Name_M}';"
        if st.button("Modify Changes"):  # Acknowledge Update
            query.execute(qry)
            st.success("Modified Successfully")
            mydb.commit()
    # -------------------------------Update Record : End -------------------------------------- #
    # -------------------------------Delete Record : Start ------------------------------------ #
    with tab3m:  # Delete Record
        Name_D = st.text_input("Enter Card_Holder_Name:", "ABC")
        qry_D = f"select * from BusinessCards where Card_Holder_Name = '{Name_D}'"
        df = pd.read_sql_query(qry_D, mydb)
        if len(df) == 0:
            st.markdown(f":red[Card_Holder_Name '{Name_D}' does not Exist.]")
        elif len(df) == 1:
            st.dataframe(df)
            if st.button("Delete"):
                qry = f"delete from BusinessCards where Card_Holder_Name = '{Name_D}';"
                query = mydb.cursor()
                query.execute(qry)
                mydb.commit()
                mydb.close()
                st.success("Deletion Successful!")
        else:
            Mobile_Number_D = st.text_input(f"Enter Mobile_Number of {Name_D}:")
            qry = f"select * from BusinessCards where Card_Holder_Name = '{Name_D}'" \
                  f"and Mobile_Number ='{Mobile_Number_D}';"
            df = pd.read_sql_query(qry, mydb)
            st.dataframe(df)
            if st.button("Delete"):
                qry = f"delete from BusinessCards where Card_Holder_Name = '{Name_D}'" \
                      f"and Mobile_Number ='{Mobile_Number_D}';"
                query = mydb.cursor()
                query.execute(qry)
                mydb.commit()
                mydb.close()
                st.success("Deletion Successful!")
    # ------------------------------- Delete Record : End --------------------------------------- #
