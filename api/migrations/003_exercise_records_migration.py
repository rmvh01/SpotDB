steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE exercise_records (
            id SERIAL NOT NULL UNIQUE PRIMARY KEY,
            exercise_template_id INT REFERENCES exercise_templates(id) ON DELETE CASCADE,
            date DATE NOT NULL,
            time TIME NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE exercise_records;
        """,
    ],
]
