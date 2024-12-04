Instructions to Run the ILookUp Application
1. Required Software and Libraries
•	Python (version 3.7+)
•	Libraries:
o	tkinter (built-in with Python)
o	phonenumbers
o	Pillow
o	tkintermapview
o	opencage
•	OpenCage API key (for geocoding)
2. Installation Instructions
1.	Install Python: Download and install Python from python.org.
2.	Install required libraries by running
pip install phonenumbers, pillow, tkintermapview, opencage
3. Running the Application
1.	Save the code in a file named iLookUp.py, key.py, signIn.png, signUp.png. Therefore, datasheet.txt and myLocation.html will create automatically when you run the application, or you can download it as well. Note: You have to make sure all files are in the same folder.
2.	Create a key.py file and add your OpenCage API key: key = "YOUR_API_KEY"
3.	Run the application from the terminal:
python iLookUp.py
Alternatively, you can open the file in an IDE (like PyCharm) and run it.
4. Configuration Settings
•	Replace "YOUR_API_KEY" in key.py with a valid OpenCage API key (get it from OpenCage Geocoder).
5. Dependencies
•	OpenCage API: Used for geocoding phone locations.
•	Text File: datasheet.txt for storing user accounts. This file will be created automatically.
