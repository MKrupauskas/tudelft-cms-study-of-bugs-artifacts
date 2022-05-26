from datetime import datetime


def get_mysql_insert_query(category):
    """
    Retrieve the mysql query to use.

    :param category: The category to apply. 0 for "issue" and 1 for "pull_request".
    :return: The selected MySQL query.
    """
    if category == 1:
        return """INSERT INTO pull_request (
                            pull_request_id, title, url, created_at, number, body, closed_at, comments, comments_url, 
                            labels, pull_request, state, commits, additions, deletions, changed_files, 
                            commits_data, updated_at
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    else:
        return """INSERT INTO issue (
                            issue_id, title, url, created_at, number, body, closed_at, comments, comments_url, labels,
                            pull_request, state, commits, additions, deletions, changed_files, commits_data, updated_at
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """


def get_start_date(category, mysql_cursor):
    """
    Retrieve the start date to allow perceval to fetch data.

    :param category: The category to apply.
    :param mysql_cursor: MySQL connection cursor.
    :return: The year, month, day, hours and minutes.
    """
    year = 2017
    month = 1
    day = 1
    hours = 0
    minutes = 0

    try:
        select_query = f"SELECT `updated_at` FROM {category} ORDER BY `id` DESC LIMIT 1"
        mysql_cursor.execute(select_query)
        result = mysql_cursor.fetchall()

        for row in result:
            updated_at = row[0]
            datetime_object = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S%z")
            year = datetime_object.year
            month = datetime_object.month
            day = datetime_object.day
            hours = datetime_object.hour
            # Start from next minute from last recorded to avoid overlaps.
            minutes = datetime_object.minute + 1

    except Exception as err:
        print(err)

    return year, month, day, hours, minutes
