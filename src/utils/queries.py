get_user_in_db_by_name = """
        SELECT user_id
        FROM users
        WHERE username = $1;
        """

insert_user_in_users_table = """
        INSERT INTO
        users VALUES(DEFAULT, $1);
        """

get_user_in_db_by_id = """
        SELECT username
        FROM users
        WHERE user_id = $1
        """

insert_chat_in_chats_table = """
        INSERT INTO
        chats VALUES(DEFAULT, $1);
        """

get_chats_in_db = """
        SELECT chat_id, name
        FROM chats;
        """

get_chat_by_id = """
        SELECT name
        FROM chats
        WHERE chat_id = $1;
        """
