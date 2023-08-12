get_user_in_db_by_name = \
        """
        SELECT user_id
        FROM users 
        WHERE username = $1;
        """

insert_user_in_users_table = \
        """
        INSERT INTO 
        users VALUES(DEFAULT, $1);
        """

get_user_in_db_by_id = \
        """
        SELECT username
        FROM users
        WHERE user_id = $1
        """

