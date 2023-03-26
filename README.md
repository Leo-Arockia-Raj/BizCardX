# BizCardX: Extracting Business Card Data with OCR

BizCardX is a project that uses OCR (Optical Character Recognition) to extract contact information from business cards. The tool is built using Python, streamlit GUI, SQL and Data Extraction technologies.

# Description:
BizCardX is a user-friendly tool for extracting contact information from business cards. The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. Users can access the extracted information using a GUI built using streamlit.

# Technologies:
BizCardX is built using the following technologies:
OCR - Optical Character Recognition technology for text extraction.
Python - Programming language used to build the tool.
Regular Expression – To classify the extracted data.
SQL - Database used to store the extracted data.
streamlit - Library used for building the user interface.

# Getting Started:
To get started with BizCardX, follow the steps below:

1.	Install the required libraries using the pip install command.
Streamlit, mysql.connector, pandas, easyocr.

2.	Execute the “BizCardX.py” using the streamlit run command.

A webpage is displayed in browser where user has the option to upload the respective Business Card whose information has to be extracted and stored.

•	Once user uploads a business card, the text present in the card is extracted by easyocr library.

•	The extracted text is sent to text_classifier() function present in text_classifier for respective text classification as  company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code using regular expression.

•	The classified data is displayed on screen which can be further edited by user based on requirement.

•	On Clicking Upload Button the data gets stored in the SQL Database. (Note: Provide respective host, user, password, database name in create_database, sql_table_creation and connect_database for establishing connection.)

•	Further the uploaded data’s in SQL Database can be accessed for Read, Update and Delete Operations.

The BizCardX application is a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button. Further the data stored in database can be easily Read, updated and deleted by user as per the requirement.
