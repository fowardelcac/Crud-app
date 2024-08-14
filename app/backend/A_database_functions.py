from pydantic import BaseModel
from typing import Optional, Union
import sqlite3

BDD_PATH = "D:/Constructora/app/backend/dbb.db"

class CompanyModel(BaseModel):
    Company_name: str
    Location: str = None
    Company_phone: str = None
    Company_email: str = None


class ContactsModel(BaseModel):
    Contact_name: str
    Contact_phone: str
    Contact_email: str = None
    Job_position: str = None
    Company_id: int


class ConstructionsModel(BaseModel):
    Construction_name: str
    Description: str = None
    Type_of_task: str = None
    Direction: str = None
    Start_date: str = None
    Possible_end_date: str = None
    Budget: Optional[Union[float, int]] = 0.0
    Total_payment: Optional[Union[float, int]] = 0.0
    Partial_payment: Optional[Union[float, int]] = 0.0
    Company_id: int 


class ItemsModel(BaseModel):
    Item_name: str
    Description: str = None
    Start_date: str = None
    Possible_end_date: str = None
    Completed: str = "No"
    Construction_id: int


class MaintenancesModel(BaseModel):
    Type: str
    Description: str
    Last_maintenance: str
    Next_maintenance: str
    Item_id: int


##########################################################################################

# Table managers


class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect(database=BDD_PATH, check_same_thread=False)

    def get_table(self, query: str):
        with self.connection as con:
            cursor = con.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    # data_model es BaseModel
    def insert_table(self, query: str, data_model: tuple):
        with self.connection as con:
            cursor = con.cursor()
            cursor.execute(
                query,
                (data_model),
            )
            con.commit()

    # dentro de la tupla debe ider (data_model.... , id)
    def update_table(self, query: str, data_model: tuple):
        with self.connection as con:
            cursor = con.cursor()
            cursor.execute(
                query,
                (data_model),
            )
            con.commit()

    def delete_table(self, query: str, id: int):
        with self.connection as con:
            cursor = con.cursor()
            cursor.execute(query, (id,))
            con.commit()

    def get_company_keys(self):
        query = "SELECT * FROM Companies ORDER BY Company_id DESC"
        with self.connection as con:
            cursor = con.cursor()
            cursor.execute(query)
            query_result = cursor.fetchall()

        diccionario = {i[0]: i[1] for i in query_result}
        return diccionario
