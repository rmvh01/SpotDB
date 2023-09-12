steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE exercise_templates (
            id SERIAL NOT NULL UNIQUE PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            type VARCHAR(100) NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE exercise_templates;
        """,
    ],
]
