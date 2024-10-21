

async def db_getsettings(connection)->list:
    return await connection.fetch(
        "select * from arbitration.settings"
    )
