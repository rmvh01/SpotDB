import hashlib
from importlib import import_module
from itertools import zip_longest
import os.path
from pathlib import Path

from psycopg import AsyncConnection
from psycopg.rows import class_row
from pydantic import BaseModel

LATEST = {}
ZERO = {}


class MigrationRecord(BaseModel):
    name: str
    # hash associated with a given migration record
    digest: bytes

    # this dunder method deals with equality operations with objects of this class
    def __eq__(self, other):
        return (
            other
            and isinstance(other, MigrationRecord)
            and self.name == other.name
            and self.digest == other.digest
        )

    def __str__(self):
        digest = self.digest.hex()
        return f"<MigrationRecord {self.name}\n{digest}\n"


class MigrationStep(BaseModel):
    up: str
    down: str | None


class MigrationFile(MigrationRecord):
    steps: list[MigrationStep]


# reads and processes migration files from a directory "dir"
async def read_migrations(dir: str) -> list[MigrationFile]:
    # starts empty and will be populated
    migrations = []
    # makes this list of files sorted alpabetically and filters out the main/init files
    files = sorted(
        [
            file
            for file in Path(dir).iterdir()
            if not str(file.name).startswith("__")
        ]
    )
    # an instance of the sha256 hashing algorithm is created
    hash = hashlib.sha256()
    for file in files:
        if file.suffix == ".py":
            migration = import_module(f".{str(file.stem)}", package=__package__)
            # the "steps" lists in the migrations files are hashed and added to the larger hash
            hash.update(bytes(str(migration.steps), encoding="utf8"))
            migrations.append(
                MigrationFile(
                    name=str(file.stem),
                    digest=hash.digest(),
                    steps=[MigrationStep(up=step[0], down=step[1]) for step in migration.steps],
                )
            )
    return migrations


async def ensure_migrations_table(db_url: str):
    async with await AsyncConnection.connect(db_url) as conn:
        async with conn.cursor() as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS migrations (
                    name VARCHAR(300) PRIMARY KEY NOT NULL,
                    digest BYTEA NOT NULL
                );
                """
            )


async def current_migrations(db_url: str) -> list[MigrationRecord]:
    async with await AsyncConnection.connect(db_url) as conn:
        async with conn.cursor(row_factory=class_row(MigrationRecord)) as db:
            await db.execute(
                """
                SELECT name, digest
                FROM migrations
                ORDER BY name;
                """
            )
            return await db.fetchall()


async def up(db_url, to=LATEST, dir=os.path.dirname(__file__)):
    await ensure_migrations_table(db_url)
    migrations = await read_migrations(dir)
    applied = await current_migrations(db_url)
    migrations_to_run = zip_longest(migrations, applied)

    if to != ZERO:
        migrations_to_run = migrations_to_run[:to]

    for migration, record in migrations_to_run:
        if record and migration != record:
            message = f"Incompatible migration history at {migration.name}"
            raise RuntimeError(message)
        elif record and migration == record:
            continue
        async with await AsyncConnection.connect(db_url) as conn:
            async with conn.cursor() as db:
                for step in migration.steps:
                    await db.execute(step.up)
                await db.execute(
                    """
                    INSERT INTO migrations (name, digest)
                    VALUES (%s, %s)
                    """,
                    [migration.name, migration.digest],
                )


async def down(db_url, to=ZERO, dir=os.path.dirname(__file__)):
    await ensure_migrations_table(db_url)
    migrations = await read_migrations(dir)
    applied = await current_migrations(db_url)
    migrations_to_run = list(reversed(list(zip(migrations, applied))))
    if to != ZERO:
        migrations_to_run = migrations_to_run[:to]
    for migration, record in migrations_to_run:
        if migration != record:
            message = f"Incompatible migration history at {migration.name}"
            raise RuntimeError(message)
        async with await AsyncConnection.connect(db_url) as conn:
            async with conn.cursor() as db:
                for step in reversed(migration.steps):
                    await db.execute(step.down)
                await db.execute(
                    """
                    DELETE FROM migrations
                    WHERE name = %s;
                    """,
                    [migration.name],
                )
