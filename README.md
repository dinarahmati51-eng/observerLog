\# Observer Log



\## Project Description



Observer Log is a Python application for recording and managing astronomical observations.



The application provides a graphical user interface that allows users to add, search, display, and visualize astronomical observations.



Observation records are stored in an SQLite database and can be imported from or exported to CSV files.



\## Features



\- Add astronomical observations

\- Store observations in an SQLite database

\- Search observations by target name

\- Display observations in a table

\- Visualize exposure times using Matplotlib

\- Import observations from CSV files

\- Export observations to CSV files

\- Prevent duplicate observations during CSV import

\- Use object-oriented programming and inheritance

\- Convert observation records into a Pandas DataFrame



\## Project Structure



\- `main.py`: Runs the graphical user interface

\- `Observation.py`: Contains observation classes

\- `database.py`: Manages the SQLite database and CSV import/export

\- `visual.py`: Displays observation tables and charts

\- `observations.db`: SQLite database

\- `observations.csv`: CSV file for importing and exporting observations

\- `README.md`: Project documentation



\## Requirements



\- Python 3

\- Pandas

\- Matplotlib

\- Tkinter

\- SQLite3



\## Installation



Install the required libraries using:



pip install pandas matplotlib



\## How to Run



Open a terminal in the project folder and run:



python main.py



\## Database



The application uses SQLite to store astronomical observation records.



Each record can contain a target name, observer name, filter name, exposure time, observation type, wavelength, and date.



\## CSV Import and Export



The application supports importing observations from CSV files and exporting database records to CSV files.



During CSV import, the application checks for duplicate records to avoid importing the same observation more than once.



\## Data Visualization



The application uses Pandas to organize observation records into a DataFrame and Matplotlib to visualize total exposure time by target.



\## Object-Oriented Programming



The project uses classes and inheritance to represent different types of astronomical observations.



\## Author



Student Project

