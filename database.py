# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 19:13:18 2023

@author: James
"""
from datetime import datetime
import sqlite3

"""
The below code initializes the creation of a database named 'RentalCompany'. 
This database is established to manage and store data important to a game rental business. 
It is constructed with several different tables, each with a unique purpose in the data management scheme.

1. 'Games' Table:
   - This table is made to store pertinent information about the games which can be rented. 
   - It includes columns for 'Game Id', 'Title', 'Platform', 'Genre', 'Purchase Price', and 'Purchase Date'.
   - These attributes provide unique game information.

2. 'Game Rentals' Table:
   - Specifically created to track the rental transactions.
   - It contains 'Rental Index', 'Customer Id', and 'Game Id' columns.
   - This table links customers to the games they rent, facilitating effective tracking and management of rentals.

3. 'Rental Periods' Table:
   - This table is dedicated to recording the duration of each game rental.
   - It includes 'Rental Index', 'Rental Start Date', and 'Rental End Date' columns.
   - By capturing the rental periods, the table assists in monitoring the availability and scheduling of games.

4. 'Game Catalogue' Table:
   - A unique table for keeping a catalogue of all games.
   - It features a 'Catalogue Index', 'Title', 'Platform', and 'Purchase Price'.

5. 'Game Genres' Table:
   - Tailored to classify games based on their genre.
   - It has 'Title' and 'Genre' columns.

"""

connection_to_sql_database=sqlite3.connect('RentalCompany.db')
cursor=connection_to_sql_database.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Games\
               ("Game Id" integer not null, \
                Title varchar(20),\
                    Platform varchar(20),\
                        Genre varchar(20),\
                            "Purchase Price" int, \
                                "Purchase Date" DATETIME)')
connection_to_sql_database.commit()
connection_to_sql_database.close()

connection_to_sql_database=sqlite3.connect('RentalCompany.db')
cursor=connection_to_sql_database.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS "Game Rentals" \
               ("Rental Index" integer,\
                "Customer Id" integer,\
                "Game Id" integer )')
connection_to_sql_database.commit()
connection_to_sql_database.close()

connection_to_sql_database=sqlite3.connect('RentalCompany.db')
cursor=connection_to_sql_database.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS "Rental Periods"\
               ("Rental Index" integer not null, \
                            "Rental Start Date" DATETIME, \
                                "Rental End Date" DATETIME)')
connection_to_sql_database.commit()
connection_to_sql_database.close()

connection_to_sql_database=sqlite3.connect('RentalCompany.db')
cursor=connection_to_sql_database.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS "Game Catalogue"\
               ("Catalogue Index" INTEGER PRIMARY KEY AUTOINCREMENT,\
                Title VARCHAR(20),\
                Platform VARCHAR(20),\
                "Purchase Price" INTEGER,\
                UNIQUE (Platform, Title, "Purchase Price"))')

connection_to_sql_database.commit()
connection_to_sql_database.close()

connection_to_sql_database=sqlite3.connect('RentalCompany.db')
cursor=connection_to_sql_database.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS "Game Genres"\
               (Title varchar(20),\
                    Genre varchar(20),\
                        UNIQUE (Title,Genre))')
connection_to_sql_database.commit()
connection_to_sql_database.close()

class GameCatalog:
    """
    Represents a single game in the rental business's game catalogue.

    This class is used to store and manage essential attributes of games.
    Each instance of this class represents a unique game, with its details such as game ID, 
    title, platform, genre, purchase price, and purchase date. These details 
    are intended to be temporarily held in this structure before being uploaded 
    into an SQL database for permanent storage and retrieval.
    """
    def __init__(self, game_id, title,platform,genre,purchase_price,purchase_date):
        
        self.game_id = game_id
        
        self.title = title
        
        self.genre = genre
        
        self.platform = platform
        
        self.purchase_price =purchase_price
        
        self.purchase_date = purchase_date

    def __str__(self):
        
        return f"{self.title} on {self.platform} for {self.purchase_price}"
        
    
"""
This code opens a text file that lists the games owned by a rental business. 
It reads and parses this data into objects, each representing a unique game copy. 
These objects are then added to a list named 'game_text_data', which is prepared 
for subsequent insertion into an SQL database.
"""
game_text_data = []
with open(r"Business Games_data.txt", "r") as file_data:
    next(file_data) 
    for line in file_data:  
        line = line.strip("\n")  
        line_elements = line.split("\t") 
        if line_elements: 
            game = GameCatalog(*line_elements)  
            game_text_data.append(game)  
            
class GameRentals:
    """
    Represents a single rental in the rental business's rental records.

    This class is used to store and manage essential attributes of rental records.
    Each instance of this class represents a unique game, with its details such as rental index,game ID, 
    rental start, rental end, and customer id. Rental index is the primary key.
    These details are intended to be temporarily held in this structure before being uploaded 
    into an SQL database for permanent storage and retrieval.
    """
    def __init__(self, rental_index,game_id, rental_start,rental_end,customer_id):
        
        self.rental_index=rental_index
        
        self.game_id = game_id
        
        self.rental_start = rental_start
        
        self.rental_end = rental_end
        
        self.customer_id = customer_id

    #This function is used to check that the generated object is not already present within our stored list
    def game_rental_duplicate_check(self,game_rental_list):
        """
        Involved in data cleaning this function removes duplicate entries of rental records.
        It takes the object as input and a list containing a list of all current rental records.
        It returns a boolean expression which if True implies that the rental record object of interest is a duplicate entry.
        """
        duplicates=0
        
        for game_rental in game_rental_list:
            
            is_same_game_id=game_rental.game_id == self.game_id
            
            is_same_game_rental_start=game_rental.rental_start==self.rental_start
            
            is_same_game_rental_end=game_rental.rental_end==self.rental_end
            
            is_same_customer_id=game_rental.customer_id==self.customer_id

            if is_same_game_id and is_same_game_rental_start and is_same_game_rental_end and is_same_customer_id:
                
                duplicates+=1
                
        game_rental_duplicate=(duplicates>0)
        
        return(game_rental_duplicate)
    
    def format_date_correctly(self):
        """
        Involved in data cleaning it ensures that the rental dates are in the correct datetime of a day,month and year.
        This function updates the values of the rental dates to be modified to the correct format.
        """
        self.rental_start = self._format_date(self.rental_start)
        
        if not(self.rental_end =="" or self.rental_end== None):
            
            self.rental_end = self._format_date(self.rental_end)

    def _format_date(self, date):
        """
        Involved in data cleaning, this changes the format of dates.
        It takes a date as input and returns a corrected date format.
        """
        if isinstance(date, str):
            # we need to add functionality to check the previous date too format.
            for fmt in ("%d/%m/%Y", "%d/%Y/%m", "%Y/%d/%m", "%m/%d/%Y", "%m/%Y/%d", "%Y/%m/%d","%m-%d-%Y", "%d-%Y-%m", "%Y-%d-%m", "%d-%m-%Y", "%m-%Y-%d", "%Y-%m-%d"):
                
                try:
                    
                    return datetime.strptime(date, fmt).strftime("%d-%m-%Y")
               
                except ValueError:
                    
                    continue
                
            raise ValueError(f"Date format for '{date}' is not recognized")
            
        elif isinstance(date, datetime):
            
            return date.strftime("%d-%m-%Y")
        
        else:
            
            raise TypeError("Date must be a string or a datetime object")


    def missing_data(self):
        """
        Involved in data cleaning, it identifies any missing data in any of the rental records.
        It takes it self as input and checks each of its attributes for the presence of a Null value.
        It returns a boolean expression, a True value indicates on of the columns has a missing value.
        """
        game_rental_removal=False
        
        is_game_id_absent= self.game_id==None or self.game_id==""
        
        is_rental_start_absent= self.rental_start== None or self.rental_start==""
        
        is_customer_id_absent= self.customer_id ==None or self.customer_id ==""
        
        if (is_game_id_absent or is_rental_start_absent or is_customer_id_absent):
            
            game_rental_removal=True
        
        return(game_rental_removal)
    
    #Determines if customer id is valid for database intialisation
    def customer_id_correct_size(self):
        """
        determines the size of a customer id.
        """
        id_size=len(str(self.customer_id))==4
        
        return(id_size)
        
    
"""
This code opens a text file that lists the rentals records a rental companys has. 
It reads and performs data cleaning operations like removing rental records with null data entries,
duplicate entries,customer id with invalid sizes, incorrect datetime formats.
It then parses the data into objects, each representing a unique rental transaction. 
These objects are then added to a list named 'rental_text_data', which is prepared 
for subsequent insertion into an SQL database.
"""
rental_text_data = []
with open (r"Customer Rental Data.txt","r") as file_data:
    
    next(file_data) 
    index=1
    for line in file_data:  
        
        line = line.strip("\n")  
        
        line_elements = line.split("\t") 
        
        if line_elements: 
            
            game = GameRentals(index,*line_elements)
            
            duplicates=game.game_rental_duplicate_check(rental_text_data)
            
            if (duplicates)==False and game.missing_data()==False and game.customer_id_correct_size()==True:
                
                index+=1
                game.format_date_correctly()
                rental_text_data.append(game)  
                
                
def insert_data_into_game_rentals(game_rental_data):
    
    """
    This function inserts new rental entries into the game rental table 
    within the rental company database.
    It takes paramater which is a tuple object as input, 
    this tuple consists of the rental index value, customer id and game id.
    """
    connection_to_sql_database=sqlite3.connect('RentalCompany.db')
    cursor=connection_to_sql_database.cursor()

    sqlite_insert_record_query="""Insert into 'Game Rentals' ('Rental Index','Customer Id','Game Id') VALUES (?,?,?)"""
    
    connection_to_sql_database.execute(sqlite_insert_record_query,game_rental_data)
    connection_to_sql_database.commit()
    connection_to_sql_database.close()

def insert_all_data_into_game_rentals(rental_text_data):
    """
    This converts rental transactions stored as a list of rental objects into a sql dataframe.
    It saves each of the rental transactions, each object encapsulates data about the rental records including
    the rental index, customer id and game id.
    """
    for rental in rental_text_data:
        insert_data_into_game_rentals((rental.rental_index,rental.customer_id,rental.game_id))
        

def insert_data_into_rental_periods(rental_period_data):
    """
    This function inserts new rental entries into the rental period table 
    within the rental company database.
    It takes a paramater which is a tuple object as input, 
    this tuple consists of the rental index value, rental start date and rental end date.
    """
    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()

    insert_query = """INSERT INTO 'Rental Periods' ('Rental Index', 'Rental Start Date', 'Rental End Date') VALUES (?,?,?)"""
    
    cursor.execute(insert_query, rental_period_data)
    connection.commit()
    connection.close()

def insert_all_data_into_rental_periods(rental_period_text_data):
   """This converts a list of rental period objects for insertion into the 'Rental Periods' table 
    of the rental company database. Each object in the list encapsulates data 
    about the rental periods, including the rental index, start date, and end date."""
   for period in rental_period_text_data:
        insert_data_into_rental_periods((period.rental_index, period.rental_start, period.rental_end))

def insert_data_into_game_catalogue(game_catalogue_data):
    """This insert game catalogue information like title,platform and purchase price into a game catalogue table within the
    sql database rental company."""

    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()

    insert_query = """INSERT OR IGNORE INTO 'Game Catalogue' ('Title', 'Platform', 'Purchase Price') VALUES (?,?,?)"""
    
    cursor.execute(insert_query, game_catalogue_data)
    connection.commit()
    connection.close()

def insert_all_data_into_game_catalogue(game_catalogue_text_data):
    """
    Iterates through a list of game catalogue entries and inserts each entry into the 
    'Game Catalogue' table in the database. Each entry in the list is a distinct object 
    containing data about a game, such as its title, platform, and purchase price. 
    """
    for catalogue in game_catalogue_text_data:
        insert_data_into_game_catalogue((catalogue.title, catalogue.platform, catalogue.purchase_price))

def insert_data_into_game_genres(game_genre_data):
    """"This function is responsible for inserting new genre entries into the 'Game Genres' table of the rental company database.
        It accepts a parameter in the form of a tuple, which includes the title of the game and its corresponding genre. 
        This information is then recorded into the database, enhancing the genre-specific data available for each game."
    """
    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()

    insert_query = """INSERT OR IGNORE INTO 'Game Genres' ('Title', 'Genre') VALUES (?,?)"""
    
    cursor.execute(insert_query, game_genre_data)
    connection.commit()
    connection.close()

def insert_all_data_into_game_genres(game_genre_text_data):
    """"Involved in transferring a list of game genre information into the 'Game Genres' table in the database. 
    Each object in the list represents a unique combination of a game's title and its genre. """
    for genre in game_genre_text_data:
        insert_data_into_game_genres((genre.title, genre.genre))

def insert_data_into_sql(tuple_games):
    """This function undertakes the insertion of individual game records into the 'Games' table of the rental company database. 
    The input is a tuple containing all the essential game attributes like game ID, title, platform, genre, purchase price, and purchase date.
    """

    connection_to_sql_database=sqlite3.connect('RentalCompany.db')
    cursor=connection_to_sql_database.cursor()
    
    sqlite_insert_record_query="""Insert into Games ('Game id',Title,Platform,Genre,"Purchase Price", "Purchase Date") VALUES (?,?,?,?,?,?)"""
    
    cursor.execute(sqlite_insert_record_query, tuple_games)
    connection_to_sql_database.commit()
    connection_to_sql_database.close()
    
def insert_all_data_into_sql(game_data):
    """Efficiently processes a list of game data objects for bulk insertion into the 'Games' table in the database. 
    Each object in the list is a detailed representation of a game, inclusive of its ID, title, platform, genre, and other pertinent details.
    This sql table is used to generate a new sql table which links primary keys to foreign keys.
    """
    for game in game_data:
        insert_data_into_sql((game.game_id,game.title,game.platform, game.genre,game.purchase_price,game.purchase_date))

def create_game_rental_dates_table():
    """This generates a new table called game rental dates through an inner join between the Games table and Games Catalogue table
        it contains the following columns game id, catalogue index and purchase date."""
    conn = sqlite3.connect('RentalCompany.db')
    cursor = conn.cursor()
    
    sql_query = """
    CREATE TABLE "Game Rental Dates" AS
    SELECT 
        Games.'Game Id', 
        'Game Catalogue'.'Catalogue Index', 
        Games.'Purchase Date'
    FROM 
        Games 
    INNER JOIN 
        'Game Catalogue' 
    ON 
        Games.Title = 'Game Catalogue'.Title AND 
        Games.Platform = 'Game Catalogue'.Platform AND 
        Games.'Purchase Price' = 'Game Catalogue'.'Purchase Price';
    """
    
    cursor.execute(sql_query)
    conn.commit()
    conn.close()
    

try:
    """This process add alls the required data to the intialised tables of the rental company database."""
    insert_all_data_into_game_rentals(rental_text_data)
    
    insert_all_data_into_rental_periods(rental_text_data)
    
    insert_all_data_into_game_catalogue(game_text_data)
    
    insert_all_data_into_game_genres(game_text_data)
    
    insert_all_data_into_sql(game_text_data)
    
    create_game_rental_dates_table()
except:
    pass


#function type in game id to return game
from gameReturn import returning_game
#function type in customer id and game id to rent game
from gameRent import can_customer_rent_another_game
#function type in desired game title and platform to see avaliable games to give customers
from gameSearch import get_available_games_info
#function type in budget and month of choice for best game to buy
from gameSelect import games_to_buy,most_popular_title_for_month_graph