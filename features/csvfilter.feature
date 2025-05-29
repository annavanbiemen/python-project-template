Feature: CSV File Filtering
    As a user
    I want to filter CSV files based on specific criteria
    So that I can extract relevant data from CSV files

    Background:
        Given the following input
            """
            Name,Age
            Julia,28
            Bob,44
            """

    Scenario: Select one field without filtering
        Given the field "Name"
        When I run the CSV filter
        Then the output should be
        """
        Name
        Julia
        Bob
        """

    Scenario: Select one field with lowercase filter
        Given the field "Name.lower"
        When I run the CSV filter
        Then the output should be
        """
        Name
        julia
        bob
        """
