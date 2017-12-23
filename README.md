# apc
A group project under the course of Advanced Programming Concepts. This project is about Facebook profile analysis

@FOR RETRIEVING DATA FROM FACEBOOK, STORING AND SECURING

>Version of Elnur:
    - Files: fbload.py
    - This is the most simplified version with only-one file with all neccessary functions and methods to retrieve data from FB
    - Includes a simplify retry control, which helps to re-connect to the server whenever there was a fail
    - People can easily and quickly deploy this.

>Version of Tien:
    - Files: Core.py, FileIO.py, Main.py, Run.py
    - The main data retrieving structures are inherited from Elnur and extending to data securing, clearer error handler and retrying controller
    - Everything you need is run the Run.py (this Run.py is just used to test, could be whatever the name...)
    - The FileIO include SHA256 and AES128 encryption and decryption methods, which you guys could implemented it separately whenever you want

@FOR DATA ANALYSIS, OUTPUTING CHARTS

>Version of Jan:
    - Files: charts.py, Extraction.py
    - Includes comments and reactions extraction
    - Summarizing all reactions and plotting graph

@FOR ONLINE TOKEN RETRIEVING

>Version of George:
    - Files: application.py, templates (folder)
    - As recommended by Facebook, Access Token should be retrieved directly from them and inputted directly into functions without storing


>There is a draft of Technical Specification docx file, please just feel free to play with it!