#Stephanie Wang
import sqlite3
import random
import json

from User_Model import User
from Game_Model import Game

class Scorecard:
    def __init__(self, db_name, scorecard_table_name, user_table_name, game_table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = scorecard_table_name 
        self.user_table_name = user_table_name
        self.game_table_name = game_table_name
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name, )
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    game_id INTEGER,
                    user_id INTEGER,
                    categories TEXT,
                    turn_order INTEGER,
                    name TEXT,
                    FOREIGN KEY(game_id) REFERENCES {self.game_table_name}(id) ON DELETE CASCADE,
                    FOREIGN KEY(user_id) REFERENCES {self.user_table_name}(id) ON DELETE CASCADE
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        cursor.execute(f"DROP TABLE scorecards;")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create(self, game_id, user_id, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            existing_ids_query = cursor.execute(f"SELECT id FROM {self.table_name};")
            existing_ids = existing_ids_query.fetchall()
            
            #CHECK IF ID EXISTS AND REROLL IF IT DOES
            card_id_exists = True
            while card_id_exists == True:
                card_id = random.randint(0, self.max_safe_id)
                if ((card_id,) not in existing_ids) == True:
                    card_id_exists = False
                else:
                    card_id_exists = True

            #INSERT BLANK TEMPLATE OF CATEGORIES
            categories = json.dumps(self.create_blank_score_info())

            #TURN ORDER
            existing_scorecards_for_game_query = cursor.execute(f"SELECT * FROM {self.table_name} WHERE game_id={game_id};")
            existing_scorecards_for_game = existing_scorecards_for_game_query.fetchall()

            turn_order = len(existing_scorecards_for_game)+1

            if turn_order > 4:
                return {"status": "error",
                        "data": "There are already 4 scorecards for this game!"
                        }
            
            #CHECK IF USER ALREADY HAS SCORECARD IN THIS GAME
            existing_scorecards_for_user_query = cursor.execute(f"SELECT * FROM {self.table_name} WHERE game_id={game_id} AND user_id = {user_id};")
            existing_scorecards_for_user = existing_scorecards_for_user_query.fetchall()
            
            if len(existing_scorecards_for_user) > 0:
                return {"status": "error",
                        "data": "There is already a scorecard for this user!"
                        }

            card_data = (card_id,game_id,user_id,categories,turn_order,name)
            card_data_dict = self.to_dict(card_data)

            #print("passed")
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?);", card_data)
            db_connection.commit()
            
            return {"status": "success",
                    "data": card_data_dict
                    }
   
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get(self, name=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if name != None:
                specific_card_query = cursor.execute(f'''
                                                    SELECT * FROM {self.table_name} 
                                                    WHERE name = '{name}';''')
                specific_card = specific_card_query.fetchall()
                if specific_card != []:
                    return {"status":"success",
                    "data":self.to_dict(specific_card[0])}
                else:
                    return {"status":"error",
                    "data":"Scorecard does not exist!"}
            elif id != None:
                specific_card_query = cursor.execute(f'''
                                                    SELECT * FROM {self.table_name} 
                                                    WHERE id = {id};''')
                specific_card = specific_card_query.fetchall()
                if specific_card != []:
                    return {"status":"success",
                    "data":self.to_dict(specific_card[0])}
                else:
                    return {"status":"error",
                    "data":"Scorecard does not exist!"}
            else:
                return {"status":"error",
                    "data":"No scorecard name or id entered!"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            all_cards_query = cursor.execute(f'''SELECT * FROM {self.table_name};''')
            all_cards = all_cards_query.fetchall()

            all_cards_list = []
            for card_tup in all_cards:
                all_cards_list.append(self.to_dict(card_tup))
            
            return {"status":"success",
                        "data":all_cards_list}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all_game_scorecards(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            all_cards_query = cursor.execute(f'''SELECT * FROM {self.table_name};''')
            all_cards = all_cards_query.fetchall()

            game_cards_list = []
            for card_tup in all_cards:
                if (card_tup[5].split("|"))[0] == game_name:
                    game_cards_list.append(self.to_dict(card_tup))
            
            return {"status":"success",
                        "data":game_cards_list}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_game_usernames(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            all_cards_query = cursor.execute(f'''SELECT * FROM {self.table_name};''')
            all_cards = all_cards_query.fetchall()

            game_cards_list = []
            for card_tup in all_cards:
                if (card_tup[5].split("|"))[0] == game_name:
                    game_cards_list.append(self.to_dict(card_tup))

            game_usernames_list = []
            for card_dict in game_cards_list:
                game_usernames_list.append(card_dict["name"].split("|")[1])
            
            return {"status":"success",
                        "data":game_usernames_list}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_user_game_names(self, username:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            all_cards_query = cursor.execute(f'''SELECT * FROM {self.table_name};''')
            all_cards = all_cards_query.fetchall()

            user_game_names_list = []
            for card_tup in all_cards:
                print(card_tup)
                if (card_tup[5].split("|"))[1] == username:
                    user_game_names_list.append((card_tup[5].split("|"))[0])
            
            return {"status":"success",
                        "data":user_game_names_list}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, id, name=None, categories=None): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            all_ids_query = cursor.execute(f'''SELECT id FROM {self.table_name};''')
            all_ids = all_ids_query.fetchall()

            #check if id exists
            if (id,) not in all_ids:
                return {"status":"error",
                        "data":"Id does not exist!"}
            #if id does exist
            else:
                #update id's info, need to convert categories to a string
                cursor.execute(f'''
                UPDATE {self.table_name}
                SET categories = '{json.dumps(categories)}',
                name = '{name}'
                WHERE id = {id};
                ''')
                db_connection.commit()

                updated_card_query = cursor.execute(f'''SELECT * FROM {self.table_name}
                                                        WHERE id = {id};''')
                updated_card = updated_card_query.fetchall()
                return {"status":"success",
                    "data":self.to_dict(updated_card[0])}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, id): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            card_results = []
            card_id_results = cursor.execute(f'''
                SELECT * FROM {self.table_name}
                WHERE id = {id};
            ''')
            card_results = card_id_results.fetchall()
            
            if (len(card_results) == 1):
                original_card_info = self.get(id=id)

                cursor.execute(f'''
                DELETE FROM {self.table_name}
                WHERE id = {id};
                ''')
                db_connection.commit()

                return {"status":"success",
                    "data":original_card_info["data"]}
            else:
                return {"status":"error",
                    "data":"Scorecard does not exist!"}
            
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, card_tuple):
        game_dict={}
        if card_tuple:
            game_dict["id"]=card_tuple[0]
            game_dict["game_id"]=card_tuple[1]
            game_dict["user_id"]=card_tuple[2]
            game_dict["categories"]=json.loads(card_tuple[3])
            game_dict["turn_order"]=card_tuple[4]
            game_dict["name"]=card_tuple[5]
        return game_dict
    
    def create_blank_score_info(self):
        return {
            "rolls_remaining":3,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }

    def tally_score(self, score_info):
        total_score = 0
        upper_score = 0

        for key in score_info["upper"]:
            if score_info["upper"][key] != -1:
                print (key,score_info["upper"][key])
                upper_score += score_info["upper"][key]
        if upper_score >= 63:
            total_score += upper_score + 35
        else:
            total_score += upper_score
        for key in score_info["lower"]:
            if score_info["lower"][key] != -1:
                print (key,score_info["lower"][key])
                total_score+= score_info["lower"][key]
                print(total_score)
   
        return total_score

if __name__ == '__main__':
    import os
    #print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/yahtzeeDB.db"
    #print("location", DB_location)
    Users = User(DB_location, "users")
    Users.initialize_table()
    Games = Game(DB_location, "games")
    Games.initialize_table()
    Scorecards = Scorecard(DB_location, "scorecards", "users", "games")
    Scorecards.initialize_table()