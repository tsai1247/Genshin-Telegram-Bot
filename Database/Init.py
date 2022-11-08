from Database.Sql import Sql

def init_table():
    if not Sql.exists('Config'):
        Sql.create("Config", 
            ['Name', 'Val'], 
            [Sql.Type.TEXT, Sql.Type.INTEGER]
        )

    if not Sql.exists('Cookie'):
        Sql.create("Cookie", 
            ['userID', 'ltuid', 'ltoken', 'cookie_token', 'account_id'], 
            [Sql.Type.INTEGERUNIQUE, Sql.Type.TEXT, Sql.Type.TEXT, Sql.Type.TEXT, Sql.Type.TEXT],
            ['userID']
        )

    if not Sql.exists('Daily'):
        Sql.create("Daily", 
            ['userID', 'autoDaily'], 
            [Sql.Type.INTEGERUNIQUE, Sql.Type.INTEGER]
        )