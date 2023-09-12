steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE metric_templates (
            id SERIAL NOT NULL UNIQUE PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            unit VARCHAR(10)
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE metric_templates;
        """,
    ],
]
