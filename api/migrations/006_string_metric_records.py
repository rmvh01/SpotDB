steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE string_metric_records (
            id SERIAL NOT NULL UNIQUE PRIMARY KEY,
            value VARCHAR(100),
            metric_template_id INT REFERENCES metric_templates(id),
            exercise_record_id INT NOT NULL REFERENCES exercise_records(id) ON DELETE CASCADE
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE string_metric_records;
        """,
    ],
]
