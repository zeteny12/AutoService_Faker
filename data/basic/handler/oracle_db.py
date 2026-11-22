import os
import oracledb
from data.basic.model_dataclasses import Car, Mechanic, Service
from datetime import date
from data.basic.generator import generate_data


def test_connection() -> None:
    with oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM DUAL")
            result = cursor.fetchone()

            print("Oracle connection:", result[0] == 1)

def create_car_table() -> None:
    with oracledb.connect(
            user=os.environ["ORACLE_USER"],
            password=os.environ["ORACLE_PASSWORD"],
            dsn=os.environ["ORACLE_DSN"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM user_tables
                WHERE table_name = 'CAR'
            """)
            if cursor.fetchone() is not None:
                print("CAR table already exists.")
                return

            cursor.execute("""
                CREATE TABLE CAR (
                    plate VARCHAR2(20 CHAR) PRIMARY KEY,
                    car_type VARCHAR2(150 CHAR) NOT NULL,
                    year NUMBER(4) NOT NULL,
                    automatic NUMBER(1) NOT NULL CHECK (automatic IN (0, 1))
                )
            """)
            print("CAR table created successfully.")

def create_mechanic_table() -> None:
    with oracledb.connect(
            user=os.environ["ORACLE_USER"],
            password=os.environ["ORACLE_PASSWORD"],
            dsn=os.environ["ORACLE_DSN"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM user_tables
                WHERE table_name = 'MECHANIC'
            """)
            if cursor.fetchone() is not None:
                print("MECHANIC table already exists.")
                return

            cursor.execute("""
                CREATE TABLE MECHANIC (
                    id NUMBER(10) PRIMARY KEY,
                    name VARCHAR2(100 CHAR) NOT NULL,
                    experience_years NUMBER(2) NOT NULL,
                    specialization VARCHAR2(100 CHAR) NOT NULL
                )
            """)
            print("MECHANIC table created successfully.")

def create_service_table() -> None:
    with oracledb.connect(
            user=os.environ["ORACLE_USER"],
            password=os.environ["ORACLE_PASSWORD"],
            dsn=os.environ["ORACLE_DSN"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM user_tables
                WHERE table_name = 'SERVICE'
            """)
            if cursor.fetchone() is not None:
                print("SERVICE table already exists.")
                return

            cursor.execute("""  
                CREATE TABLE SERVICE (
                    id NUMBER(10) PRIMARY KEY,
                    car_plate VARCHAR2(20 CHAR) NOT NULL,
                    service_date DATE NOT NULL,
                    description VARCHAR2(100 CHAR) NOT NULL,
                    cost NUMBER(10) NOT NULL,
                    mechanic_id NUMBER(10) NOT NULL,
                
                    FOREIGN KEY (car_plate) REFERENCES CAR(plate),
                    FOREIGN KEY (mechanic_id) REFERENCES MECHANIC(id)
                )
            """)
            print("SERVICE table created successfully.")


def insert_cars(cars: list[Car], connection: oracledb.Connection) -> None:
    with connection.cursor() as cursor:
        for car in cars:
            cursor.execute("""
                INSERT INTO CAR (plate, car_type, year, automatic)                    
                VALUES (:plate, :car_type, :year, :automatic)
            """, {
                "plate": car.plate,
                "car_type": car.type,
                "year": car.year,
                "automatic": int(car.automatic)
            })
        print("Cars insert statements executed.")

def insert_mechanics(mechanics: list[Mechanic], connection: oracledb.Connection) -> None:
    with connection.cursor() as cursor:
        for mechanic in mechanics:
            cursor.execute("""
                INSERT INTO MECHANIC (id, name, experience_years, specialization)
                VALUES (:id, :name, :experience_years, :specialization)                
            """, {
                "id": mechanic.id,
                "name": mechanic.name,
                "experience_years": mechanic.experience_years,
                "specialization": mechanic.specialization
                })
        print("Mechanics insert statements executed.")

def insert_services(services: list[Service], connection: oracledb.Connection) -> None:
    with connection.cursor() as cursor:
        for service in services:
            cursor.execute("""
                INSERT INTO SERVICE (id, car_plate, service_date, description, cost, mechanic_id)
                VALUES (:id, :car_plate, :service_date, :description, :cost, :mechanic_id)
            """, {
                "id": service.id,
                "car_plate": service.car_plate,
                "service_date": date.fromisoformat(service.date),
                "description": service.description,
                "cost": service.cost,
                "mechanic_id": service.mechanic_id
            })
        print("Services insert statements executed.")


def check_table_counts() -> None:
    with oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"]
    ) as connection:
        with connection.cursor() as cursor:
            for table in ["CAR", "MECHANIC", "SERVICE"]:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]

                print(f"{table} records: {count}")


def insert_data(cars: list[Car], services: list[Service], mechanics: list[Mechanic]) -> None:
    with oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"]
    ) as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM SERVICE")
                cursor.execute("DELETE FROM MECHANIC")
                cursor.execute("DELETE FROM CAR")

            insert_cars(cars, connection)
            insert_mechanics(mechanics, connection)
            insert_services(services, connection)

            connection.commit()
            print("Database data replaced successfully.")

        except Exception as error:
            connection.rollback()
            print("Data replacement failed:", error)
            raise


if __name__ == "__main__":
    test_connection()
    create_car_table()
    create_mechanic_table()
    create_service_table()

    generated_cars, generated_services, generated_mechanics = generate_data(5)

    insert_data(generated_cars, generated_services, generated_mechanics)
    check_table_counts()