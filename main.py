from fastapi import FastAPI
from database import engine
import pandas as pd
from schemas import Donor
from sqlalchemy import text

app = FastAPI()

@app.get("/")
def home():
    return {
        "message":"Blood Bank API Running"
    }

@app.get("/test-db")
def test_db():

    try:
        connection = engine.connect()
        connection.close()

        return {
            "status":"Database Connected"
        }

    except Exception as e:

        return {
            "error":str(e)
        }

@app.get("/donors")
def get_donors():

    query = """
    SELECT * FROM donors
    """

    data = pd.read_sql(
        query,
        engine
    )

    return data.to_dict(
        orient="records"
    )
@app.get("/donor/{donor_id}")
def get_donor(donor_id:str):

    query = f"""
    SELECT *
    FROM donors
    WHERE donor_id='{donor_id}'
    """

    data = pd.read_sql(
        query,
        engine
    )

    return data.to_dict(
        orient="records"
    )

@app.post("/add-donor")
def add_donor(donor:Donor):

    new_donor = pd.DataFrame(
        [donor.dict()]
    )

    new_donor.to_sql(
        "donors",
        engine,
        if_exists="append",
        index=False
    )

    return {
        "message":"Donor Added Successfully"
    }

@app.put("/update-donor/{donor_id}")
def update_donor(
    donor_id:str,
    donor:Donor
):

    query = text("""
    UPDATE donors
    SET
        name=:name,
        age=:age,
        gender=:gender,
        blood_group=:blood_group,
        weight=:weight,
        city=:city
    WHERE donor_id=:donor_id
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "name": donor.name,
                "age": donor.age,
                "gender": donor.gender,
                "blood_group": donor.blood_group,
                "weight": donor.weight,
                "city": donor.city,
                "donor_id": donor_id
            }
        )

    return {
        "message":"Donor Updated Successfully"
    }

@app.delete("/delete-donor/{donor_id}")
def delete_donor(donor_id:str):

    query = text("""
    DELETE
    FROM donors
    WHERE donor_id=:donor_id
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "donor_id": donor_id
            }
        )

    return {
        "message":"Donor Deleted Successfully"
    }

@app.get("/donor-count")
def donor_count():

    query = """
    SELECT COUNT(*) AS total
    FROM donors
    """

    result = pd.read_sql(
        query,
        engine
    )

    return result.to_dict(
        orient="records"
    )