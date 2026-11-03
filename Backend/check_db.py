from sqlalchemy import text
from database import engine

try:
    with engine.connect() as connection:

        # 1. Check total records
        count = connection.execute(
            text('SELECT COUNT(*) FROM "Tasks"')
        ).scalar()

        print("Total PostgreSQL records:", count)

        # 2. Display migrated records
        records = connection.execute(
            text("""
                SELECT
                    "TaskId",
                    "Title",
                    "Status",
                    "CreatedAtUtc"
                FROM "Tasks"
                ORDER BY "TaskId"
            """)
        ).mappings().all()

        for record in records:
            print(dict(record))

except Exception as e:
    print("Database error:", e)