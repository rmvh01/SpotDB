steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE string_metric_values (
            id SERIAL NOT NULL UNIQUE PRIMARY KEY,
            value VARCHAR(100) NOT NULL,
            metric_id INT REFERENCES metric_templates(id)
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE string_metric_values;
        """,
    ],
]
