#Stephanie Wang
import sqlite3
import random
import datetime

class Game:
    def __init__(self, db_name, table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = table_name #"games"
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    name TEXT UNIQUE,
                    created DATE,
                    finished DATE
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, game_name=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            game_name_results = []

            if game_name != None:
                game_name_results = cursor.execute(f'''
                    SELECT * FROM {self.table_name}
                    WHERE name = '{game_name}';
                ''')
                game_name_results = game_name_results.fetchall()
            else:
                return {"status":"error",
                    "data":"No game name entered!"}

            if len(game_name_results) != 1:
                return {"status": "success",
                    "data": False
                    }
            else:
                return {"status": "success",
                    "data": True
                    }
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def create(self, game_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            existing_ids_query = cursor.execute(f"SELECT id FROM {self.table_name};")
            existing_ids = existing_ids_query.fetchall()
            
            #CHECK IF ID EXISTS AND REROLL IF IT DOES
            game_id_exists = True
            while game_id_exists == True:
                game_id = random.randint(0, self.max_safe_id)
                #user_id = 1 #(used for testing)
                if ((game_id,) not in existing_ids) == True:
                    game_id_exists = False
                else:
                    game_id_exists = True

            #MAKE SURE NAME IS IN VALID FORMAT
            if (self.exists(game_name=game_info["name"]))["data"] == True: 
                return {"status":"error",
                    "data":"Game name already exists!"}
            elif game_info["name"].isalnum() == False:
                if "-" not in game_info["name"] and "_" not in game_info["name"]:
                    return {"status":"error",
                            "data":"Game name contains forbidden characters!"}
                
            #MAKE CREATED/FINISHED TIMESTAMPS (should be the same here)
            raw_timestamp = datetime.datetime.now()
            #formatted_timestamp = raw_timestamp.strftime("%B %d, %Y %X") more readable format 
            formatted_timestamp = str(datetime.datetime.now())

            game_data = (game_id, game_info["name"], formatted_timestamp, formatted_timestamp)
            game_data_dict = self.to_dict(game_data)

            #print("passed")
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", game_data)
            db_connection.commit()
            
            return {"status": "success",
                    "data": game_data_dict
                    }
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, game_name=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if game_name != None:
                specific_game_query = cursor.execute(f'''
                                                    SELECT * FROM {self.table_name} 
                                                    WHERE name = '{game_name}';''')
                specific_game = specific_game_query.fetchall()
                if specific_game != []:
                    return {"status":"success",
                    "data":self.to_dict(specific_game[0])}
                else:
                    return {"status":"error",
                    "data":"Game does not exist!"}
            elif id != None:
                specific_game_query = cursor.execute(f'''
                                                    SELECT * FROM {self.table_name} 
                                                    WHERE id = {id};''')
                specific_game = specific_game_query.fetchall()
                if specific_game != []:
                    return {"status":"success",
                    "data":self.to_dict(specific_game[0])}
                else:
                    return {"status":"error",
                    "data":"Game does not exist!"}
            else:
                return {"status":"error",
                    "data":"No game name or id entered!"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            all_games_query = cursor.execute(f'''SELECT * FROM {self.table_name};''')
            all_games = all_games_query.fetchall()

            all_games_list = []
            for game_tup in all_games:
                all_games_list.append(self.to_dict(game_tup))
            
            return {"status":"success",
                        "data":all_games_list}
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, game_info): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            all_ids_query = cursor.execute(f'''SELECT id FROM {self.table_name};''')
            all_ids = all_ids_query.fetchall()
            #print(all_ids)

            original_game_query = cursor.execute(f'''SELECT * FROM {self.table_name} WHERE id = {game_info["id"]};''')
            original_game = original_game_query.fetchone()

            #check if id exists
            if (game_info["id"],) not in all_ids:
                return {"status":"error",
                        "data":"Id does not exist!"}
            #if id does exist
            else:
                #check if game name is unique
                if (self.exists(game_name=game_info["name"]))["data"] == True and game_info["name"] != original_game[1]:
                    return {"status":"error",
                            "data": "Game name already exists!"}
                else:
                    #update id's info
                    cursor.execute(f'''
                    UPDATE {self.table_name}
                    SET name = '{game_info["name"]}',
                    created = '{game_info["created"]}',
                    finished = '{game_info["finished"]}'
                    WHERE id = {game_info["id"]};
                    ''')
                    db_connection.commit()

                    updated_game_query = cursor.execute(f'''SELECT * FROM {self.table_name}
                                                            WHERE id = {game_info["id"]};''')
                    updated_game = updated_game_query.fetchall()
                    return {"status":"success",
                        "data":self.to_dict(updated_game[0])}
            
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, game_name): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if (self.exists(game_name=game_name)["data"] == True):
                original_game_info = self.get(game_name=game_name)

                cursor.execute(f'''
                DELETE FROM {self.table_name}
                WHERE name = '{game_name}';
                ''')
                db_connection.commit()

                return {"status":"success",
                       "data":original_game_info["data"]}
            else:
                return {"status":"error",
                    "data":"Game does not exist!"}
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def is_finished(self, game_name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            if (self.exists(game_name=game_name)["data"] == True):
                original_game_info = self.get(game_name=game_name)["data"]
                
                if original_game_info["created"] == original_game_info["finished"]:
                    return {"status":"success",
                       "data":False}
                else:
                    return {"status":"success",
                       "data":True}
            else:
                return {"status":"error",
                    "data":"Game does not exist!"}
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, game_info):
        '''Utility function which converts the tuple returned from a SQLlite3 database
           into a dictionary
        '''
        game_dict={}
        if game_info:
            game_dict["id"]=game_info[0]
            game_dict["name"]=game_info[1]
            game_dict["created"]=game_info[2]
            game_dict["finished"]=game_info[3]
        return game_dict

if __name__ == '__main__':
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db"

    Games = Game(DB_location, "games")
    Games.initialize_table()

    games =[]
    for i in range(5):
        games.append({"name":f"ourGame{i}"})

    original_games = {}
    for i in range(len(games)):
        game = Games.create(games[i])
        print(game)
        original_games[game['data']["name"]] = game["data"] #game name maps to game object
            
    updated_game = original_games[games[3]["name"]]
    updated_game["finished"]=str(datetime.datetime(2020, 5, 17))

    print(updated_game)
    
    returned_game = Games.update(updated_game)