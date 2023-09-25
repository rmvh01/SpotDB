steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE numeric_metric_records (
            id SERIAL NOT NULL UNIQUE PRIMARY KEY,
            value INT,
            metric_template_id INT REFERENCES metric_templates(id),
            exercise_record_id INT NOT NULL REFERENCES exercise_records(id) ON DELETE CASCADE
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE numeric_metric_records;
        """,
    ],
]
