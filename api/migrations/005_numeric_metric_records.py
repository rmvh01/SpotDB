steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE numeric_metric_values (
            id SERIAL NOT NULL UNIQUE PRIMARY KEY,
            value INT NOT NULL,
            metric_id INT REFERENCES metric_templates(id)
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE numeric_metric_values;
        """,
    ],
]
