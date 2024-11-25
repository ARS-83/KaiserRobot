# TODO : ADD TotalUsed > This TotalUsed Continue (:
from pyromod import listen
import asyncio
from pyrogram import Client
from pyrogram.types import  InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from uuid import uuid4
import aiofiles
import json
import string
import httpx
import time
import os
import random
from db import Context
from service import orm
import logging
import ast
logging.basicConfig(level=logging.WARNING, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('Kaiser.log'), logging.StreamHandler()])

logger = logging.getLogger(__name__)
context = Context.DatabaseManager()





async def SaveFileConfig(data):
 async with aiofiles.open('Config/Config.json', mode='w',encoding='utf-8') as f: 
      await f.write(json.dumps(data))
      


async def ReadFileText():
   async with aiofiles.open('Config/Messages.json', mode='r' , encoding='utf-8') as f: 
 
       return  json.loads(await f.read())
         
async def ReadFileConfig():
   async with aiofiles.open('Config/Config.json', mode='r',encoding='utf-8') as f: 
      res =   json.loads(await f.read())
   return res   



def get_random_string(length):
   
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generate_password(length):
    characters = [random.choice(string.ascii_letters +string.ascii_lowercase + string.digits ) for _ in range(length)]
    random.shuffle(characters)
    return ''.join(characters)



plugins = dict(root="Plugins")
app = Client("Kaiser_Robo23esfvdf23t", 
             api_id=27920385,
             plugins=plugins,
             api_hash="6ef7b57f85f5d96dfbde6b4fd36412be",
             bot_token="6489326673:AAF20M8j0FHspx1NyyMms4SHKrSYO3G3hGQ")

async def sendMessage():
 data = await ReadFileConfig()
 if data['SendingPublicMessage'] == 0:
 
  pm = await context.execute_query_one("SELECT * FROM PublicMessage WHERE IsSended = 0 AND IsDelete = 0")
  
  if pm != None:
    data['SendingPublicMessage'] = 1
    await SaveFileConfig(data)
    await app.send_message(pm[6] , f"🔔 شروع ارسال پیام {pm[1]}")
    Users = await context.execute_query_all("SELECT UserId FROM Users")
    
    counter  =pm[3]
    for user in Users:
      checkMes = await context.execute_query_one(f"SELECT IsDelete FROM PublicMessage WHERE Id = {pm[0]}")
      
      if checkMes[0] == 0:
        time.sleep(0.2)
        try:
         if pm[7] != 'empty':
           
           if pm[2]!= 'empty' :
              await app.send_cached_media(chat_id= user[0],file_id=pm[7],caption=pm[2])  
           else:
              await app.send_cached_media(chat_id= user[0],file_id=pm[7])  
         else:         
            await app.send_message(chat_id= user[0] ,text= f"""
{pm[2]}
""" )
        except Exception as e:
           logger.error("Error Send Message : {e}")
        counter += 1
        await context.QueryWidthOutValue(f"UPDATE PublicMessage SET CountSended = { counter } WHERE Id = {pm[0]}")
        
    await context.QueryWidthOutValue(f"UPDATE PublicMessage SET IsSended = 1 WHERE Id = {pm[0]}")  
   
    await app.send_message(pm[6] , f" ❤️  ارسال این پیام به پایان رسید {pm[1]}")

    data['SendingPublicMessage'] = 0
    await SaveFileConfig(data)
    
  return

async def CheckDiscount():
  
  # db = await aiosqlite.connect("db/ARSSub.db")
  # context  = await db.cursor()
  discountCheck = await context.execute_query_all("SELECT * FROM Discounts  WHERE Status = 1")
  # discountCheck =await context.fetchall()
  if len(discountCheck) != 0:
    for discount in discountCheck:
      dateEnd = datetime.datetime.fromtimestamp(discount[4]) 
      if datetime.datetime.now() >  dateEnd:
        await context.QueryWidthOutValue(f"UPDATE Discounts SET Status = 0 WHERE Id = {discount[0]}")
      
        data =await ReadFileConfig()
        await app.send_message(chat_id= data['ownerId'],text=f"زمان کد تخفیف {discount[2]} به پایان رسید ")
 
  return

async def MessageChanell():
  
  # db = await aiosqlite.connect("db/ARSSub.db")
  # context  = await db.cursor()
  try:
   MessageChanell = await context.execute_query_all("SELECT * FROM MessageChanell  WHERE CanSend = 1")


   if len(MessageChanell) != 0:
    chanel =await context.execute_query_one("SELECT LockChanel FROM Setting  ")
    for Mes in MessageChanell:
     if Mes[2] + 1 >= Mes[3]:
       await app.forward_messages(chanel[0],Mes[5],Mes[1])
       await context.QueryWidthOutValue(f"UPDATE MessageChanell SET AfterTime = 0 WHERE Id = {Mes[0]}")
      
     else:
          await context.QueryWidthOutValue(f"UPDATE MessageChanell SET AfterTime = {Mes[2] + 1} WHERE Id = {Mes[0]}")
         
  except:
        data =await ReadFileConfig()
        await app.send_message(chat_id= data['ownerId'],text=f"هنگام ارسال پیامی به کانال به مشکل خوردیم لطفا بررسی کنید ") 
  
  return
       
async def QureKESHi():...
  # SELECT COUNT() FROM  Service WHERE UserId = {userId}
#     data = await context.execute_query_one("SELECT LotteryTime, LotteryState, LotteryTimeAfter,UserNumberLottery, LotteryPlan FROM Setting ")

#     if data[1] ==1:
#        if data[2]>= data[0]:
#          i = 1
#          users =await context.execute_query_all("SELECT * FROM Users")
        
#          plan = await context.execute_query_one(f"SELECT * FROM ServerPlans WHERE Id = {data[4]}")
        

#          while i <= data[3]:
#            usercount = len(users) - 1
#            radnUser = random.randint(0,usercount)
           
#            LockChanel  = await context.execute_query_one(f"SELECT LockChanel FROM Setting")
       
#            try:
            
#              await app.get_chat_member(chat_id=str(LockChanel[0]),user_id=users[radnUser][1])
#              try:
#                 await 
#                 await app.send_message(users[radnUser][1],f"""تبریک میگوییم 🔰❤️‍🔥
                                        
# شما برنده قرعه کشی شده اید 💰
                                        
# 🫴🏻 نام سابسکرایب شما : {email}

# میتوانید از قسمت اشتراک های من به ان دسترسی داشته باشید 😄
#                                       """)

#            except:
#              try: 
#               await app.send_message(users[radnUser][1],"""
# کاربر گرامی شما برنده قرعه کشی کانفیگ رایگان شدید 🔔
                                     
# اما چون از چنل لفت دادی دادیمش یکی دیگه اگه میخوای بازم شانس برنده شدن داشته باشی تو چنل باش ❤️
# """)
              
#              except: 
#               pass
           
           
                 
                    
         
               
               
        
#        else:
#            await context.QueryWidthOutValue(f"UPDATE Setting SET LotteryTimeAfter = {data[2] + 1} ")
           

   

async def CheckSubscribeUser():

  # try:
  #   print(f"Running CheckSubscribeUser\nTIME START : {datetime.datetime.now()}")

    await orm.CheckUserService(app)

  #   print(f"CheckSuccess Fully\nTIME END : {datetime.datetime.now()}")  
  # except Exception as e:
  #           print(f" Error in  CheckSubscribeUser: {str(e)}  {datetime.time.strftime()}")
 
async def SendBackUp():
   
   chanel =  await context.execute_query_one("SELECT QuartzChanell,TimeSendQuartz,TimeSendBackUp,TimeAfterSendBackUp,TimeAfterSendQuartz,ChanelQuartzQuartz FROM Setting")
   if chanel[2] <= (chanel[3] + 1):
       try:
            
             await app.send_message(chat_id=str(chanel[0]),text="🔸 ارسال بکاپ بات  ")
             try:
                await app.send_document(f"{chanel[0]}","db/ARSSub.db")
                await app.send_document(f"{chanel[0]}","db/DataServers.db")
                servers = await context.execute_query_all("SELECT * FROM Server")
    
          
   
                await app.send_message(chat_id=str(chanel[0]),text="🔸 ارسال بکاپ سرور های بات  ")

                for server in servers:
                 try:       
                   origin= server[3].split("/")
                   headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
  'X-Requested-With': 'XMLHttpRequest',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': f'{origin[0]}://{origin[2]}',
  'Connection': 'keep-alive',
  'Referer': f'{server[3]}/panel/inbounds',
  'Cookie': ''
}

               
             
                   async with httpx.AsyncClient() as client:
                      response =  await client.post(url=f"{server[3]}/login",data={"username":f"{server[1]}","password":f"{server[2]}"})

                      session = response.headers.get("Set-Cookie").split("; ")[0]   
                      headers['Cookie'] = f"lang=en-US; {session}"
                      res =await client.get(server[3] + "/server/getDb", headers=headers, timeout=6)
                      file = open(f"backUp/x-ui.db","wb")
                      file.write(res.content)
                      file.close()
  
                      await app.send_document(f"{chanel[0]}",document='backUp/x-ui.db',caption=f"بکاپ پنل {server[6]}")
    
                      os.remove('backUp/x-ui.db')   
                 except :
                     adminId =await ReadFileConfig()
                     await app.send_message(chat_id=adminId['ownerId'],text=f"هنگام دریافت بکاپ  سرور {server[6]} به مشکل خوردیم")
            
                
             except:
                   data = await ReadFileConfig()
                   await app.send_message(data['ownerId'],"هنگام ارسال بکاپ بات مشکلی پیش آمد")

       except:
          data = await ReadFileConfig()
          await app.send_message(data['ownerId'],"""
لطفا بات را در چنل بکاپ ادمین کنید
""")
               
       await context.QueryWidthOutValue("UPDATE Setting SET TimeAfterSendBackUp = 0 ")      
   else:
      await context.QueryWidthOutValue(f"UPDATE Setting SET TimeAfterSendBackUp = {chanel[3] + 1}")   
   if chanel[1] <= (chanel[4] + 1):
        try:
         
             dateAgo = datetime.datetime.now() - datetime.timedelta(hours=chanel[1])
             OrderCount = await context.execute_query_all(f"SELECT COUNT() FROM OrdersList WHERE DateTime > {datetime.datetime.timestamp(dateAgo)} ")
             Pays = await context.execute_query_all(f"SELECT COUNT() FROM Service WHERE CreateDate > {datetime.datetime.timestamp(dateAgo)} AND ServiceTest = 'empty'")
             Tests = await context.execute_query_one(f"SELECT COUNT() FROM Service WHERE CreateDate > {datetime.datetime.timestamp(dateAgo)} AND ServiceTest = 'ok'")
             user = await context.execute_query_all(f"SELECT COUNT() FROM Users WHERE TimeJoin > {datetime.datetime.timestamp(dateAgo)} ")
             ShopedPrice = await context.execute_query_all(f"SELECT SUM(Price) FROM OrdersList WHERE DateTime > {datetime.datetime.timestamp(dateAgo)} AND State = 1 AND DiscountId = 0")
             ShopedPriceDis = await context.execute_query_all(f"SELECT SUM(PriceAfterDiscount) FROM OrdersList WHERE DateTime > {datetime.datetime.timestamp(dateAgo)} AND State = 1 AND DiscountId != 0")
             


             me =await app.get_me()
             await app.send_message(chat_id=str(chanel[5]),text=f"""📊 | گزارش بات در {chanel[1]} ساعت گذشته 

💰 | درآمد : { f'{ShopedPrice[0][0] + ShopedPriceDis[0][0] if ShopedPriceDis[0][0] != None else ShopedPrice[0][0] :,}' if ShopedPrice[0][0] != None or ShopedPriceDis[0][0] != None else 0 } تومان

🎁 | اشتراک تست دریافت شده : {Tests[0]}

🛍 | فروش اشتراک ها : {Pays[0][0]}

👤 |  تعداد کاربران اضافه شده : {user[0][0]}

@{me.username}
                                     """)
             
        except:
          data = await ReadFileConfig()
          await app.send_message(data['ownerId'],"""
لطفا بات را در چنل بکاپ ادمین کنید
""")
        await context.QueryWidthOutValue("UPDATE Setting SET TimeAfterSendQuartz = 0 ")      
               

      #TODO
      
   else:
      await context.QueryWidthOutValue(f"UPDATE Setting SET TimeAfterSendQuartz = {chanel[4] + 1}")   
         
      
async def CheckTimeSub():
   await orm.CheckServiceTime(app)


async def SendConfigUser():
  data = await context.execute_query_all("SELECT * FROM SendConfOnline WHERE State = 0")
  for d in data:
    try:  
     res = await orm.CreateSub(d[2],app)
     if res[0]==True:
        await app.send_message(chat_id=res[3],text ="""♦️ سرویس شما افزوده شد ✅

کاربر گرامی توجه ! ⚠️
لطفا برای دریافت ادرس اتصال خود دکمه زیر را لمس نمایید سپس کمی صبر کنید تا سرویس برای شما ارسال شود 🫴🏻
یا میتوانید از قسمت اشتراک های من اشتراک خود را دریافت و مشاهده کنید 🫳🏻

🔰 /start

""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton( "دریافت",callback_data= f"GETConfig_{res[2]}")]]))
        await  context.QueryWidthOutValue(f"UPDATE SendConfOnline SET State = 1 WHERE Id ={d[0]}")
     else:
            data = await ReadFileConfig()
            await app.send_message(chat_id= data['ownerId'], text=res[1]) 
            
    except:
            data =await ReadFileConfig()
            # await app.send_message(chat_id= data['ownerId'], text="هنگام افزودن سرویس مشکللی پیش آمد") 

async def DeleteOrderNoneState():
   date = datetime.datetime.now() - datetime.timedelta(weeks=1)
   convert = datetime.datetime.timestamp(date)
   await context.QueryWidthOutValue(f"DELETE FROM OrdersList WHERE State = 0 AND DateTime < {convert}") 


async def CheckServerState():
   
   data = await ReadFileConfig()
   servers = await context.execute_query_all("SELECT * FROM Server ")
   disableServer=[]
   setting = await context.execute_query_one("SELECT alertTimeOut FROM Setting")
   for server in servers:
      async with httpx.AsyncClient() as client:
        try:  
          response = None
          try:

           response = await client.post(f"{server[3]}/login",data={"username": f"{server[1]}", "password": f"{server[2]}"})
          except:
           response = await client.post(f"{server[3]}/login",data={"username": f"{server[1]}", "password": f"{server[2]}"})


          session = ""
          if len(response.headers.get("Set-Cookie").split("; ") )>= 6:
      
             session =  response.headers.get("Set-Cookie").split("; ")[4]  
             session =session.split(", ")[1]
          else:
            session =  response.headers.get("Set-Cookie").split("; ")[0]  

          await context.QueryWidthOutValue(f"UPDATE Server SET Session = '{session}' ,Connection= 1 WHERE Id = {server[0]}"  ) 
          if server[13] == 0 and setting[0] != 0:
              await  app.send_message(chat_id= data['ownerId'], text=f"""
اتصال با سرور {server[6]} مجدد برقرار شد ✅

""") 
        except:
            if server[13] != 0 :
               
          
              
             await context.QueryWidthOutValue(f"UPDATE Server SET Connection = 0 , DateConnectionLost = {int(datetime.datetime.timestamp(datetime.datetime.now()))} WHERE Id = {server[0]} " ) 

             disableServer.append({
               "name":server[6],
               "Id" : server[0]

            })

   if len(disableServer) != 0 and setting[0] != 0:

      
    text ="""
🔴 | لیست سرور هایی که ارتباط با انها برقرار نشد  :

"""
    for disabel in disableServer:
      text +=f"""
{disabel['name']}

"""
    
    await app.send_message(chat_id= data['ownerId'], text=f"""
{text}
ℹ️ | سرور هایی که در لیست بالا قرار داشتند در ارتباط با ربات به مشکل خورده اند در صورتی که اتصال مجدد برقرار شد اطلاعیه برای شما ارسال خواهد شد

""") 

async def imperfectComplete():
  imperfects =  await context.execute_query_all("SELECT * FROM imperfect WHERE IsCompleted = 0 ORDER BY DateCreateImperfect")
  for imperfect in  imperfects:
   try:

     if imperfect[1] == "extension":
      try:
       config = await context.execute_query_one(f"SELECT * FROM Configs WHERE Id= {imperfect[3]}")
       server = await context.execute_query_one(f"SELECT * FROM Server WHERE Id = {config[8]} ")
       service = await context.execute_query_one(f"SELECT * FROM Service WHERE Id = {config[1]}")
       origin= server[3].split("/")
       headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
  'X-Requested-With': 'XMLHttpRequest',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': f'{origin[0]}://{origin[2]}',
  'Connection': 'keep-alive',
  'Referer': f'{server[3]}/{"panel"if server[4] == "sanaei" else "xui" }/inbounds',
  'Cookie': ''
}

       data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ config[3] +'", "alterId": 0, "email": "'+ config[2] +'", "totalGB": '+ str(int(imperfect[5])) +', "expiryTime": '+str(int(imperfect[6]))+', "enable": true, "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
}
       async with httpx.AsyncClient() as client:
         response = None
         headers['Cookie'] = f"lang=en-US; {server[8]}"
         try:
           response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{imperfect[8]}',data=data,headers=headers)
         except:
           response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{imperfect[8]}',data=data,headers=headers)
               
         data = json.loads(response.text)
         
         if data['success'] != False:
            
            
            await context.QueryWidthOutValue(f"UPDATE Configs SET TansformEnable = {imperfect[5]} , State = 1 , EndDate = {imperfect[6]} ")
            await app.send_message(service[1],f"""
👮🏻 | کاربر گرامی اطلاعیه تمدید سرور درون سرویس {config[2]}  

⛑ | هنگام برقراری ارتباط با سرور {server[6]} هنگام درخواست تمدید سرویس شما به مشکل خورده بودیم که با موفقیت رفع شد و اشتراک شما درون این سرور تمدید شد ✅

⚡️ | برای استفاده از این سرور اشتراک خودتون رو مجدد به روز رسانی کنید

🔰 /start
""")
            await context.QueryWidthOutValue(f"UPDATE imperfect SET IsCompleted = 1 WHERE Id = {imperfect[0]}")
         else:
             await context.QueryWidthOutValue(f"DELETE FROM imperfect WHERE Id = {imperfect[0]}")
             configFile = await ReadFileConfig()  
             await app.send_message(chat_id=configFile['ownerId'],text= f"""🔄 تمدید در سرور {server[5]}

👤 نام کانفیگ : {config[2]}

UUID جدید : {str(imperfect[8])}
حجم : {(imperfect[5] / 1024 / 1024 /1024)}
تاریخ انقضا : {datetime.datetime.fromtimestamp(int(imperfect[6]) / 1000)}

جزییات سرور : {str(response.text)}

**عملیات از ربات حذف شد لطفا به صورت دستی اقدام به تغییرات کنید**
""")
      except:
         pass        
     elif imperfect[1] == "disable":
       try:
          config = await context.execute_query_one(f"SELECT * FROM Configs WHERE Id = {imperfect[3]}")
          server = await context.execute_query_one(f"SELECT * FROM Server WHERE Id = {config[8]}")
          service = await context.execute_query_one(f"SELECT * FROM Service WHERE Id = {config[1]}")
          if server == None:
              return
          origin= server[3].split("/")
          headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
  'X-Requested-With': 'XMLHttpRequest',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': f'{origin[0]}://{origin[2]}',
  'Connection': 'keep-alive',
  'Referer': f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbounds',
  'Cookie': ''
}

          data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ config[3] +'", "alterId": 0, "email": "'+ config[2] +'", "totalGB": '+ str(int(config[7])) +', "expiryTime": '+str(config[12])+', "enable": false, "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
}
          limits = httpx.Limits(max_connections=3)
          async with httpx.AsyncClient(limits=limits) as client:
           response = None

     
           headers['Cookie'] = f"lang=en-US; {server[8]}"
           try:

              response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{config[3]}',data=data,headers=headers)
           except:
              response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{config[3]}',data=data,headers=headers)

           data = json.loads(response.text)
           if data['success'] == True:
               await context.QueryWidthOutValue(f"UPDATE imperfect SET IsCompleted = 1 WHERE Id = {imperfect[0]}")
               await context.QueryWidthOutValue(f"UPDATE Configs SET State = 0 WHERE ServiceId = {config[1]} AND ServerId = {server[0]}")
           else:
             await context.QueryWidthOutValue(f"DELETE FROM imperfect WHERE Id = {imperfect[0]}")
             configFile = await ReadFileConfig()  
             await app.send_message(chat_id=configFile['ownerId'],text= f"""🔄 غیرفعال کردن کانفیگ در سرور {server[5]}

👤 نام کانفیگ : {config[2]}
UUID کانفیگ : {config[3]}

جزییات سرور : {str(response.text)}

عملیات از ربات حذف شد لطفا به صورت دستی اقدام به تغییرات کنید
""")      
       except: 
          pass
     elif imperfect[1] == "change" :
         try: 
          config = await context.execute_query_one(f"SELECT * FROM Configs WHERE Id= {imperfect[3]}")
          server = await context.execute_query_one(f"SELECT * FROM server WHERE Id = {config[8]}")
          service = await context.execute_query_one(f"SELECT * FROM Service WHERE Id = {config[1]}")
          origin= server[3].split("/")
          headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
  'X-Requested-With': 'XMLHttpRequest',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': f'{origin[0]}://{origin[2]}',
  'Connection': 'keep-alive',
  'Referer': f'{server[3]}/{"panel"if server[4] == "sanaei" else "xui" }/inbounds',
  'Cookie': ''
}
          
          data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ str(imperfect[8]) +'", "alterId": 0, "email": "'+ config[2] +'", "totalGB": '+ str(int(config[7])) +', "expiryTime": '+str(config[12])+', "enable": true, "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
}
        
          async with httpx.AsyncClient() as client:
           response = None

         
           headers['Cookie'] = f"lang=en-US; {server[8]}"

           try:
            response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{config[3]}',data=data,headers=headers)
           except:
            response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{config[3]}',data=data,headers=headers)
               
           data = json.loads(response.text)
           
           if data['success'] ==True :
               await context.QueryWidthOutValue(f"UPDATE imperfect SET IsCompleted = 1 WHERE Id = {imperfect[0]}")
               await context.QueryWidthOutValue(f"UPDATE Configs SET uuid = '{str(imperfect[8])}' WHERE ServerId = {server[0]} AND ServiceId = {config[1]} ")       
               await app.send_message(imperfect[9],f"""
👮🏻 | کاربر گرامی اطلاعیه تغییر سرور درون سرویس {config[2]}  

⛑ | هنگام برقراری ارتباط با سرور {server[6]} هنگام درخواست تغییر لینک سرویس شما به مشکل خورده بودیم که با موفقیت رفع شد و اشتراک شما درون این سرویس تعویض شد ✅

⚡️ | برای استفاده از این سرور اشتراک خودتون رو مجدد به روز رسانی کنید

🔰 /start
""")
           else:
             await context.QueryWidthOutValue(f"DELETE FROM imperfect WHERE Id = {imperfect[0]}")
             configFile = await ReadFileConfig()  
             await app.send_message(chat_id=configFile['ownerId'],text= f"""🔄 تغییر در سرور {server[5]}

👤 نام کانفیگ : {config[2]}
UUID قبل : {config[3]}
UUID جدید : {str(imperfect[8])}

جزییات سرور : {str(response.text)}

عملیات از ربات حذف شد لطفا به صورت دستی اقدام به تغییرات کنید
""")
         except:
            pass
     elif imperfect[1] =="insert":
      try:     
       server = await context.execute_query_one(f"SELECT * FROM Server WHERE Id = {imperfect[11]}")
       service = await context.execute_query_one(f"SELECT * FROM Service WHERE Id = {imperfect[4]}")
       if service[14] >=service[18] : 
          await context.QueryWidthOutValue(f"UPDATE imperfect SET IsCompleted = 1 WHERE Id = {imperfect[0]}")
          continue
       data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ str({service[4]}) +'", "alterId": 0, "email": "'+ service[3] +'", "totalGB": '+ str(int(service[18])) +', "expiryTime": '+str(service[7]) + ', "enable": true, "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
}
       origin= server[3].split("/")
       headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
  'X-Requested-With': 'XMLHttpRequest',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': f'{origin[0]}://{origin[2]}',
  'Connection': 'keep-alive',
  'Referer': f'{server[3]}/{"panel"if server[4] == "sanaei" else "xui" }/inbounds',
  'Cookie': ''
}

       async with httpx.AsyncClient() as client:
         response = None
      
         
         
         
         headers['Cookie']  = f"lang=en-US; {server[8]}"
         try:
          response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers)
         except:
          response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers)
              
         data = json.loads(response.text)
         
         if data['success'] == False:
                           
             await context.QueryWidthOutValue(f"DELETE FROM imperfect WHERE Id = {imperfect[0]}")
             configFile = await ReadFileConfig()  
             await app.send_message(chat_id=configFile['ownerId'],text= f"""🔄 افزودن در سرور {server[5]}

👤 نام کانفیگ : {service[3]}

جزییات سرور : {str(response.text)}

عملیات از ربات حذف شد لطفا به صورت دستی اقدام به تغییرات کنید
""")

         

          
             
         else:
             serverIdS = ast.literal_eval(service[17])
             serverIdS.append(server[0])
             await context.QueryWidthOutValue(f"UPDATE imperfect SET IsCompleted = 1 WHERE Id = {imperfect[0]}")
             await context.QueryWidthOutValue(f"UPDATE Service SET ServerIds = '{str(serverIdS)}' WHERE Id = {service[0]}")
             await context.Query("INSERT INTO Configs(ServiceId,Name,uuid,Upload,Download,TotalUsed,TansformEnable,ServerId,State,isDelete,EndDate,CreateDate) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(service[0],service[3],str(service[4]),0,0,0,service[18],server[0],1,0,service[7],service[6]))
             await app.send_message(service[1] ,f"""
👮🏻 | کاربر گرامی اطلاعیه افزایش سرور به سرویس {service[3]}  

⛑ | هنگام برقراری ارتباط با سرور {server[6]} به مشکل خوردیم که به سرویس شما اضافه نشده بود هم اکنون اضافه شد ✅

⚡️ | برای استفاده از این سرور اشتراک خودتون رو مجدد به روز رسانی کنید

🔰 /start
""")
             
             
      except:

        ...
   except:
    ...

async def MessageStateServers():
  setting = await context.execute_query_one("SELECT alertTimeOut FROM Setting")
  data = await ReadFileConfig()

  servers = await context.execute_query_all("SELECT * FROM Server WHERE Connection = 0")
  text = """
سرور هایی که در ساعت گذشته اتصالی نداشته اند ℹ️

"""
  if len(servers) == 0:
     return
  counter = 0 
  for server in servers:
      if (date + datetime.timedelta(hours=1)) < datetime.datetime.now():
         counter +=1
  if counter == 0:
     return       
  for server in servers:
     date = datetime.datetime.fromtimestamp(server[14])
     if (date + datetime.timedelta(hours=1)) < datetime.datetime.now():
        text += f"""
        
{server[6]}

        """
  if  setting[0] == 1:
        await app.send_message(chat_id= data['ownerId'], text=text)
# TODO CREATE FIRST Shop
async def disableConfig(server_id,service):


     
         try:

          server = await context.execute_query_one(f"SELECT * FROM Server WHERE Id = {server_id}")
          if server == None:
              return
          origin= server[3].split("/")
          headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
  'X-Requested-With': 'XMLHttpRequest',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': f'{origin[0]}://{origin[2]}',
  'Connection': 'keep-alive',
  'Referer': f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbounds',
  'Cookie': ''
}

          data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ service[4] +'", "alterId": 0, "email": "'+ service[3] +'", "totalGB": '+ str(int(service[18])) +', "expiryTime": '+str(service[7])+', "enable": false, "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
}
          limits = httpx.Limits(max_connections=3)
          async with httpx.AsyncClient(limits=limits) as client:
           response = None

     
           headers['Cookie'] = f"lang=en-US; {server[8]}"
           try:

              response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{service[4]}',data=data,headers=headers)
           except:
              response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{service[4]}',data=data,headers=headers)

           data = json.loads(response.text)
           if data['success'] == True:
               await context.QueryWidthOutValue(f"UPDATE Configs SET State = 0 WHERE ServiceId = {service[0]} AND ServerId = {server[0]}")
 
             
           else:
              config = await context.execute_query_one(f"SELECT * FROM Configs WHERE ServerId = {server[0]} AND ServiceId = {service[0]}")
              await context.Query("INSERT INTO imperfect(Type,ConfigId,UserId,DateCreateImperfect) VALUES(?,?,?,?)",("disable",config[0],service[1],datetime.datetime.now().timestamp()))   
             
         except:

              config = await context.execute_query_one(f"SELECT * FROM Configs WHERE ServerId = {server[0]} AND ServiceId = {service[0]}")
              await context.Query("INSERT INTO imperfect(Type,ConfigId,UserId,DateCreateImperfect) VALUES(?,?,?,?)",("disable",config[0],service[1],datetime.datetime.now().timestamp()))   
             
           
        
async def checkOnlineUsers():
   servers = await context.execute_query_all("SELECT * FROM Server")
   for server in servers : 
      async with httpx.AsyncClient() as client:
       try:
        origin= server[3].split("/")
        headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
  'X-Requested-With': 'XMLHttpRequest',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': f'{origin[0]}://{origin[2]}',
  'Connection': 'keep-alive',
  'Referer': f'{server[3]}/{"panel"if server[4] == "sanaei" else "xui" }/inbounds',
  'Cookie': ''
}
        headers['Cookie']  = f"lang=en-US; {server[8]}"

        response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/onlines',headers=headers)
        dataLoaded = json.loads(response.text)

        if dataLoaded['success'] == True:
           await context.QueryWidthOutValue(f"UPDATE Server SET Onlines = '{json.dumps(dataLoaded['obj'])}' WHERE Id = {server[0]}")
        else:
           logger.error(f"Server Response Has Problem : {e}")   
     
       except Exception as e:
          
         logger.error(f"Error In Checker Onlines : {e}")

   Services = await context.execute_query_all("SELECT * FROM Service WHERE isDelete = 0 AND UserLimit != 0 AND State = 1 AND Warning > 0")
   for service in Services :
      counter = 0
      warning = service[29]
      serverIds = ast.literal_eval(service[17])
      for serverId in serverIds:
         serverOnlens = await context.execute_query_one(f"SELECT Onlines FROM Server WHERE Id = {serverId}")
         datalistLoad = json.loads(serverOnlens[0])
         if datalistLoad == None:
            continue
         for online in datalistLoad:
            if online == service[3]:
               counter +=1
      if counter > service[28]:
            try:
             warning -= 1
             if warning == 2:
                await app.send_message(chat_id=service[1] , text=f"""⚠️ | توجه کاربر گرامی!!!
                                       
**🙏🏼 | سرویس {service[3]} شما دارای محدودیت کاربر است لطفا از استفاده بیش از حد مجاز خودداری کنید**

👥 تعداد مجاز : {service[28]}                                       
👮🏻‍♀️ کاربران متصل : {counter}

⚠️ | درصورتی که به هشدار ها توجه نکنید سرویس شما از سرور های ما قطع خواهد شد 

❤️ | همچنین اگر احساس میکنید که شما از سرویس استفاده نمیکنید از قابلیت تعویض لینک استفاده کنید و سرویس خود را مجدد دریافت کنید        

/start
                                           """)
             if warning == 1: 
                 await app.send_message(chat_id=service[1] , text=f"""⚠️ | (اخطار نهایی) توجه کاربر گرامی!!!
                                       
**🙏🏼 | سرویس {service[3]} شما دارای محدودیت کاربر است لطفا از استفاده بیش از حد مجاز خودداری کنید**

👥 تعداد مجاز : {service[28]}                                       
👮🏻‍♀️ کاربران متصل : {counter}

⚠️ | درصورتی که به هشدار ها توجه نکنید سرویس شما از سرور های ما قطع خواهد شد 

❤️ | همچنین اگر احساس میکنید که شما از سرویس استفاده نمیکنید از قابلیت تعویض لینک استفاده کنید و سرویس خود را مجدد دریافت کنید        

/start
                                           """)
             if warning == 0:
                for serverId in serverIds:
                   await disableConfig(serverId,service)
                await app.send_message(chat_id=service[1] , text=f"""⚠️ | (اخطار قطعی) توجه کاربر گرامی!!!

⚠️ | به دلیل توجه نکردن به اخطار های قطعی سرویس شما غیرفعال شد

/start
                                           """)    
                await context.QueryWidthOutValue(f"UPDATE Service SET State = 0 WHERE Id = {service[0]}")
             await context.QueryWidthOutValue(f"UPDATE Service SET Warning = {warning} WHERE Id = {service[0]}")
            except Exception as e:
               logger.error(f"Error In Check Online : {e}")  




scheduler = AsyncIOScheduler()
scheduler.add_job(checkOnlineUsers,"interval",seconds=150) #150
scheduler.add_job(sendMessage, "interval",seconds=360) # 360
scheduler.add_job(CheckDiscount, "interval",seconds=21600) # 21600
scheduler.add_job(MessageChanell, "interval",seconds=86400) # 86400
scheduler.add_job(QureKESHi  , "interval",seconds=86400) # 86400
scheduler.add_job(CheckSubscribeUser  , "interval",seconds=350) # 360
scheduler.add_job(SendBackUp  , "interval",seconds=3600) # 3600
scheduler.add_job(CheckTimeSub  , "interval",seconds=43200) # 43200
scheduler.add_job(SendConfigUser  , "interval",seconds=80) # 20
scheduler.add_job(DeleteOrderNoneState  , "interval",seconds=604800) # 604,800
scheduler.add_job(CheckServerState,"interval",seconds=60)
scheduler.add_job(MessageStateServers,"interval",seconds=3600)
scheduler.add_job(imperfectComplete,"interval",seconds=360)# 3600

scheduler.start()
logger.info("Scheduler Started")
app.run()
   