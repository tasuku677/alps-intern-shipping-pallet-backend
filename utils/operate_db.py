from fastapi import APIRouter, HTTPException
import pymssql
from config.configurable_value import get_config # type: ignore


import logging
router = APIRouter()

server = get_config('DATABASE_SERVER')
database = get_config('DATABASE_NAME')
username = get_config('DATABASE_USERNAME')
password = get_config('DATABASE_PASSWORD')
TABLE_NAME = get_config('TABLE_NAME')

logger = logging.getLogger('db')

def get_db_connection():
    try: 
        connection = pymssql.connect(server, username, password, database)
        return connection
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

def close_db_connection(connection):
    try:
        connection.close()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

def get_data(connection):
    cursor = connection.cursor(as_dict=True)
    query = f"""
    SELECT 
        PalletNo, 
        CreatedBy, 
        CONVERT(varchar, CreatedOn, 126) AS CreatedOn 
    FROM {TABLE_NAME}
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def add_data(connection, employeeId, palletID, timestamp):
    query = f"""
        INSERT INTO {TABLE_NAME} (PalletNo, CreatedBy, CreatedOn) 
        VALUES ('{palletID}','{employeeId}',CAST('{timestamp}' AS datetimeoffset))
    """
    logger.info(query)
    # cursor.execute(query, (palletID, employeeId, "2024-09-09T11:29:11.65+00:00"))
    connection.execute_non_query(query)
    
if __name__ == "__main__":
    connection = get_db_connection()
    add_data(connection, "Ic980", "ALPS8092", "2024-09-09T11:29:11.65+00:00")
    data = get_data(connection)
    print(data)
    close_db_connection(connection)

# @router.get("/photos_db/{employee_id}")
# def get_photos_by_employee_id(employee_id: str):
#     try:
#         conn = pyodbc.connect(connection_string)
#         cursor = conn.cursor()
#         cursor.execute(f"SELECT * FROM Photos WHERE EmployeeId = '{employee_id}'")
#         photos = cursor.fetchall()
#         return photos
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#         return None
