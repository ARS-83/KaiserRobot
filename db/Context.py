import aiosqlite
import json
import asyncio

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    async def connect(self):
        if self._connection is None:
            self._connection = await aiosqlite.connect('db/ARSSub.db')
    async def Query(self,query,value):
          if self._connection is None:
            await self.connect()

          res =await self._connection.execute(query,value)
          await self._connection.commit()
          return res

   
    async def QueryWidthOutValue(self,query):
          if self._connection is None:
            await self.connect()
          
          await self._connection.execute(query)
          await self._connection.commit()

          
    async def execute_query_all(self, query):
        if self._connection is None:
            await self.connect()
        
        async with self._connection.execute(query) as cursor:
            result = await cursor.fetchall()
            return result
    async def execute_query_one(self, query):
        if self._connection is None:
            await self.connect()
        result = None
        async with self._connection.execute(query) as cursor:
           result  = await cursor.fetchone()
        return result

    async def close_connection(self):
        if self._connection is not None:
            await self._connection.close()
            self._connection = None





class ServerDataManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    async def connect(self):
        if self._connection is None:
            self._connection = await aiosqlite.connect('db/DataServers.db')
    async def Query(self,query,value):
          if self._connection is None:
            await self.connect()

          res =await self._connection.execute(query,value)
          await self._connection.commit()
          return res

   
    async def QueryWidthOutValue(self,query):
          if self._connection is None:
            await self.connect()
          
          await self._connection.execute(query)
          await self._connection.commit()

          
    async def execute_query_all(self, query):
        if self._connection is None:
            await self.connect()
        
        async with self._connection.execute(query) as cursor:
            result = await cursor.fetchall()
            return result
    async def execute_query_one(self, query):
        if self._connection is None:
            await self.connect()
        result = None
        async with self._connection.execute(query) as cursor:
           result  = await cursor.fetchone()
        return result

    async def close_connection(self):
        if self._connection is not None:
            await self._connection.close()
            self._connection = None



