
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from database import engine as postgres_engine

# 1. Connect to existing local SQL Server
sqlserver_url = URL.create(
    "mssql+pyodbc",
    host=r"DESKTOP-8CEP79S\SQLEXPRESS",
    database="AITaskAssistantDB",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Trusted_Connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

sqlserver_engine = create_engine(
    sqlserver_url,
    pool_pre_ping=True,
)

try:
    # 2. Read all records from SQL Server
    with sqlserver_engine.connect() as source:
        records = source.execute(
            text("""
                SELECT
                    TaskId,
                    Title,
                    Status,
                    CreatedAtUtc,
                    Description,
                    DueDateUtc,
                    UpdatedAtUtc
                FROM dbo.Tasks
                ORDER BY TaskId
            """)
        ).mappings().all()

    print(f"SQL Server records found: {len(records)}")

    if not records:
        print("No records found. Migration stopped.")
        raise SystemExit(0)

    # 3. Insert records into PostgreSQL
    with postgres_engine.begin() as target:

        existing_count = target.execute(
            text('SELECT COUNT(*) FROM "Tasks"')
        ).scalar()

        if existing_count > 0:
            raise RuntimeError(
                "PostgreSQL table is not empty. Migration cancelled "
                "to prevent duplicate records."
            )

        insert_query = text("""
            INSERT INTO "Tasks" (
                "TaskId",
                "Title",
                "Status",
                "CreatedAtUtc",
                "Description",
                "DueDateUtc",
                "UpdatedAtUtc"
            )
            VALUES (
                :TaskId,
                :Title,
                :Status,
                :CreatedAtUtc,
                :Description,
                :DueDateUtc,
                :UpdatedAtUtc
            )
        """)

        target.execute(
            insert_query,
            [dict(record) for record in records]
        )

        # 4. Synchronize PostgreSQL identity sequence
        target.execute(text("""
            SELECT setval(
                pg_get_serial_sequence('"Tasks"', 'TaskId'),
                (SELECT MAX("TaskId") FROM "Tasks")
            )
        """))

    # 5. Verify migration
    with postgres_engine.connect() as target:
        migrated_count = target.execute(
            text('SELECT COUNT(*) FROM "Tasks"')
        ).scalar()

    print(f"PostgreSQL records migrated: {migrated_count}")

    if migrated_count == len(records):
        print("Migration completed successfully!")
    else:
        print("Record count mismatch. Please investigate.")

finally:
    sqlserver_engine.dispose()
    postgres_engine.dispose()
