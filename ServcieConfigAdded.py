


from db import Context
import ast
import asyncio
context = Context.DatabaseManager()

async def AddConfigs():
   services =  await context.execute_query_all("SELECT * FROM Service")

   for service in services:
     serverIds =  ast.literal_eval(service[17])
     for serverId in serverIds:
        await context.Query("INSERT INTO Configs(ServiceId,Name,uuid,Upload,Download,TotalUsed,TansformEnable,ServerId,State,isDelete,EndDate,CreateDate) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(service[0],service[3],str(service[4]),0,0,0,service[18],serverId,1,0,service[7],service[6]))
   print("End Process")
if __name__ == "__main__" :

   asyncio.run(AddConfigs()) 

