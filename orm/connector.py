import aiomysql
import asyncio

class AsyncMySQLConnector:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            loop=asyncio.get_event_loop()
        )

    async def execute(self, query, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                result = await cur.fetchall()
                await conn.commit()
        return result

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()

# Пример использования:

async def main():
    connector = AsyncMySQLConnector(
        host='localhost',
        port=8081,  
        user='admin',
        password='admin',
        db='db'
    )
    try:
        await connector.connect()
        
        result = await connector.execute("""CREATE TABLE IF NOT EXISTS userss (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );""")
        
        insert_query = """INSERT INTO userss (username, email, password) 
                 VALUES ('john_doe', 'john@example.com', 'hashed_password');"""
        result = await connector.execute(insert_query)
        print(result)
        result2 = await connector.execute("SELECT * FROM userss")
        print("Select query result:", result2)
    except aiomysql.MySQLError as e:
        print(f"An error occurred: {e}")
    finally:
        await connector.close()

if __name__ == "__main__":
    asyncio.run(main())