import sqlite3
from contextlib import closing
from pathlib import Path


DATABASE_PATH = Path("data") / "facilitators.db"


def get_connection():

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def table_exists(connection, table_name):

    return connection.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
            AND name = ?
        """,
        (table_name,)
    ).fetchone() is not None


def table_has_column(connection, table_name, column_name):

    columns = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    return any(column["name"] == column_name for column in columns)


def create_schema(connection):

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS facilitators (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            facilitated_before INTEGER NOT NULL DEFAULT 0,
            confidence INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS facilitator_availability (
            student_id TEXT NOT NULL,
            day TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            PRIMARY KEY (student_id, day, time_slot),
            FOREIGN KEY (student_id)
                REFERENCES facilitators (student_id)
                ON DELETE CASCADE
        );
        """
    )


def migrate_legacy_schema(connection):

    if not table_exists(connection, "facilitators"):
        return

    if table_has_column(connection, "facilitators", "student_id"):
        return

    has_availability = table_exists(
        connection,
        "facilitator_availability"
    )

    connection.execute("PRAGMA foreign_keys = OFF")

    connection.execute(
        """
        ALTER TABLE facilitators
        RENAME TO facilitators_old
        """
    )

    if has_availability:

        connection.execute(
            """
            ALTER TABLE facilitator_availability
            RENAME TO facilitator_availability_old
            """
        )

    create_schema(connection)

    connection.execute(
        """
        INSERT INTO facilitators (
            student_id,
            name,
            facilitated_before,
            confidence,
            created_at,
            updated_at
        )
        SELECT
            CAST(id AS TEXT),
            name,
            facilitated_before,
            confidence,
            created_at,
            updated_at
        FROM facilitators_old
        """
    )

    if has_availability:

        connection.execute(
            """
            INSERT OR IGNORE INTO facilitator_availability (
                student_id,
                day,
                time_slot
            )
            SELECT
                CAST(facilitator_id AS TEXT),
                day,
                time_slot
            FROM facilitator_availability_old
            """
        )

        connection.execute("DROP TABLE facilitator_availability_old")

    connection.execute("DROP TABLE facilitators_old")
    connection.execute("PRAGMA foreign_keys = ON")


def init_db():

    with closing(get_connection()) as connection:

        with connection:

            migrate_legacy_schema(connection)
            create_schema(connection)


def save_facilitators(facilitators):

    init_db()

    with closing(get_connection()) as connection:

        with connection:

            for facilitator in facilitators:

                connection.execute(
                    """
                    INSERT INTO facilitators (
                        student_id,
                        name,
                        facilitated_before,
                        confidence
                    )
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(student_id) DO UPDATE SET
                        name = excluded.name,
                        facilitated_before = excluded.facilitated_before,
                        confidence = excluded.confidence,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        facilitator["student_id"],
                        facilitator["name"],
                        int(facilitator["facilitated_before"]),
                        facilitator["confidence"],
                    )
                )

                connection.execute(
                    """
                    DELETE FROM facilitator_availability
                    WHERE student_id = ?
                    """,
                    (facilitator["student_id"],)
                )

                for day, time_slots in facilitator["availability"].items():

                    for time_slot in time_slots:

                        connection.execute(
                            """
                            INSERT OR IGNORE INTO facilitator_availability (
                                student_id,
                                day,
                                time_slot
                            )
                            VALUES (?, ?, ?)
                            """,
                            (
                                facilitator["student_id"],
                                day,
                                time_slot
                            )
                        )

    return len(facilitators)


def get_facilitators():

    init_db()

    facilitators = {}

    with closing(get_connection()) as connection:

        rows = connection.execute(
            """
            SELECT
                facilitators.student_id,
                facilitators.name,
                facilitators.facilitated_before,
                facilitators.confidence,
                facilitator_availability.day,
                facilitator_availability.time_slot
            FROM facilitators
            LEFT JOIN facilitator_availability
                ON facilitator_availability.student_id =
                    facilitators.student_id
            ORDER BY facilitators.name, facilitator_availability.day
            """
        ).fetchall()

    for row in rows:

        facilitator = facilitators.setdefault(
            row["student_id"],
            {
                "student_id": row["student_id"],
                "name": row["name"],
                "facilitated_before": bool(row["facilitated_before"]),
                "confidence": row["confidence"],
                "availability": {},
            }
        )

        if row["day"] and row["time_slot"]:

            facilitator["availability"].setdefault(
                row["day"],
                []
            ).append(row["time_slot"])

    return list(facilitators.values())
