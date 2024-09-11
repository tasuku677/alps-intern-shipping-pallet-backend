from fastapi import APIRouter, HTTPException
import pyodbc
from utils.constant_value import DEFAULT_CONFIG


router = APIRouter()

server = DEFAULT_CONFIG['DATABASE_SERVER']
database = DEFAULT_CONFIG['DATABASE_NAME'] 
username = DEFAULT_CONFIG['DATABASE_USERNAME']
password = DEFAULT_CONFIG['DATABASE_PASSWORD']
driver = "ODBC Driver 18 for SQL Server"

connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"TrustServerCertificate=yes;"
)

def get_db_connection():
    try: 
        connection = pyodbc.connect(connection_string)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def close_db_connection(connection):
    try:
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_data(connection):
    cursor = connection.cursor()
    query = f"""
    SELECT 
        PalletNo, 
        CreatedBy, 
        CONVERT(varchar, CreatedOn, 126) AS CreatedOn 
    FROM {DEFAULT_CONFIG['TABLE_NAME']}
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def add_data(connection, employeeId, palletID, timestamp):
    cursor = connection.cursor()
    query = f"""
    INSERT INTO {DEFAULT_CONFIG['TABLE_NAME']} (PalletNo, CreatedBy, CreatedOn) 
    VALUES (?, ?, CAST(? AS datetimeoffset))
    """
    # cursor.execute(query, (palletID, employeeId, "2024-09-09T11:29:11.65+00:00"))
    cursor.execute(query, (palletID, employeeId, timestamp))
    connection.commit()
    
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