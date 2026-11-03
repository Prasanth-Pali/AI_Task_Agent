from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

# 1. Database connection URL
connection_url = URL.create(
    "mssql+pyodbc",
    host=r"DESKTOP-8CEP79S\SQLEXPRESS",
    database="AITaskAssistantDB",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Trusted_Connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

# 2. Create database engine
engine = create_engine(
    connection_url,
    pool_pre_ping=True,
)

# 3. Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# 4. Test database connection
with engine.connect() as connection:
    database_name = connection.execute(
        text("SELECT DB_NAME()")
    ).scalar()

    print("Connected successfully to:", database_name)


# 5. Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()