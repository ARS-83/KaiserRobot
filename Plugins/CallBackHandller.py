from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup


import pyromod
import json

import aiofiles
import asyncio 
import datetime
import jdatetime
import qrcode
from io import BytesIO
from service import orm


Messages =  []


async def Canesel_Key(c:Client,m:Message,userid):
     
 Messages =await ReadFileText()

 await m.reply(Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(userid),resize_keyboard=True))


async def ReadFileConfig():
   
   async with aiofiles.open('Config/Config.json', mode='r',encoding='utf-8') as f: 
      res =   json.loads(await f.read())
   return res   

async def ReadFileText():
   
   async with aiofiles.open('Config/Messages.json', mode='r' , encoding='utf-8') as f: 
 
       return json.loads(await f.read())
   

async def CheckBlockUser(_,c:Client,m:Message):

  if await orm.CheckUserBlock(m.from_user.id)== True:
     Messages = await ReadFileText()
     await c.send_message(m.from_user.id,text=Messages['BlockUser'],reply_markup=ReplyKeyboardMarkup([["✅ درخواست"]],resize_keyboard=True))
     return False
  else:
     return True
  

async def CheckJoin(_,c:Client,m:Message):
   if await orm.IsChannelLock() == False:
       return True
   try:
      chanel  = await orm.GetChanellLock()
      await c.get_chat_member(chat_id=str(chanel),user_id=m.from_user.id)
      return True
      
   except:
      Messages = await ReadFileText()
      await c.send_message(m.from_user.id,Messages['lockchanel'],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ورود",url=f"https://t.me/{chanel}")]]))
      return False
      
async def CheckAdmin(_,c:Client,m:Message):
  
   if await orm.CheckAdmin(m.from_user.id) == True:
      return True
   else: 
      return False
   
   
async def CheckRun(_,c:Client,m:Message):
   if await orm.GetStateBot() == True:
      return True
   else:
      await m.reply("❤️‍🔥 بات در حال حاضر خاموش است کمی منتظر بمانید ")
      return False
async def CheckBtnsNot(_,c:Client,m:Message):
   btns = ["✅ درخواست","قطع","تست","📲 آموزش اتصال","⚙️ مدیریت ربات ⚙️","/start","🤝 همکاری","🔄 تمدید سرویس","🌟 تست رایگان","📥 اشتراک های من","🛍 خرید اشتراک","☎️ پشتیبانی","👤 حساب من","🔍 مشخصات اشتراک"]

   if m.text not in btns : 
       
       return True
   else:
       await orm.ChangeStep(m.from_user.id,"home")
       
       return False
  
    
    
blockCheck = filters.create(CheckBlockUser)
CheckLock = filters.create(CheckJoin)
Check_Admin = filters.create(CheckAdmin)
Check_Run = filters.create(CheckRun)
checkBtnsNot = filters.create(CheckBtnsNot)

@Client.on_message(filters.regex("✅ درخواست")&  CheckLock  & Check_Run) 
async def REQOnBlock(c:Client,m:Message):
    if await orm.CheckUserBlock(m.from_user.id) == True:
     if await orm.CheckReqUnblock(m.from_user.id) == True:
      await orm.ChangeStep(m.from_user.id,"requnblock")
      await m.reply(text="لطفا درخواست خود را ارسال کنید : "  )
    
     else:
        await m.reply("درخواست قبلی شما در دست بررسی میباشد لطفا صبر کنید ") 

    else:
       await m.reply("کاربر گرامی شما رفع مسدودیت شدید یا مسدود نیستید ! 🟢",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))




# answer = await pyromod.Chat.ask(text="🔻 لطفا شناسه کاربری کاربر مورد نظر  را ارسال فرمایید")


async def SendTiekt(c:Client,m:Message):

       res = await orm.AddTiket(m.text,m.from_user.id)
       if res[0] == True:
          try: 
           data = await ReadFileConfig()
           await c.send_message(data['ownerId'],f"""👤 کاربر {m.from_user.username} 
                                
☎️ درخواست تیکت به پشتیبانی ارسال کرده است  
                                
جزییات تیکت : 
{m.text}
                           
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("پاسخ ✍🏻",callback_data=f"answerTiket_{res[1]}")]]))
           admins = await orm.GetAdminList()
           if admins !=None :
               for admin in admins : 
                     await c.send_message(admin[1],f"""👤 کاربر {m.from_user.username} 
                                
☎️ درخواست تیکت به پشتیبانی ارسال کرده است  
                                
جزییات تیکت : 
{m.text}
                           
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("پاسخ ✍🏻",callback_data=f"answerTiket_{res[1]}")]]))
           await m.message.reply("✅ تیکت ثبت شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))
          
           return
          except:
           await m.message.reply("تیکت ثبت نشد ❌",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))
           
           return
       else:
           await m.message.reply("تیکت ثبت نشد ❌",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))


async def TransFormWallet(c:Client,m:Message,data):
           try :
             

                  
               UserId =int(m.text)
                     
               res = await orm.TranformData(data,UserId,m.from_user.id)
               if res[0] == True:
                         await m.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))
                         return
               else:
                         await m.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))    
                         return
                  
             
           except:
               await m.reply("لطفا فقط عدد")
               return




async def ReqUnblock(c:Client,m:Message):
      try:
       adminAsli = await ReadFileConfig()
       await c.send_message(chat_id=adminAsli['ownerId'],text=f"""
درخواست رفع مسدودیت کاربر با ID : {m.from_user.id}

نام کاربری : @{m.from_user.username}

{m.text}


""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رفع مسدودیت 🟢",callback_data=f"Requnblock_{m.from_user.id}"),InlineKeyboardButton("رد",callback_data=f"radBlock_{m.from_user.id}")]]))
       admins = await orm.GetAdminList()
       if admins !=None or len(admins) != 0:
          for ad in admins:
            await c.send_message(chat_id=ad[1],text=f"""
درخواست رفع مسدودیت کاربر با ID : {m.from_user.id}

نام کاربری : @{m.from_user.username}

{m.text}


""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رفع مسدودیت 🟢",callback_data=f"Requnblock_{m.from_user.id}"),InlineKeyboardButton("رد",callback_data=f"radBlock_{m.from_user.id}")]]))
       await orm.UpdateReqBlock(m.from_user.id,1)  
       await m.reply("❤️‍🔥 درخواست ارسال و به زودی مورد بررسی قرار خواهد گرفت ")     
      except:

         pass








async def transWalletStepOne(c:Client,m:Message):
   
   if m.text.isdigit():
      if int(m.text)>=10000:
         await orm.ChangeStep(m.from_user.id,f"transWalletPriceTwo_{m.text}")
         await m.reply(text="🔻 لطفا شناسه کاربری کاربر مورد نظر را ارسال فرمایید")
      else:
          await m.reply("❤️ لطفا فقط بزرگتر از 10,000 تومان ارسال کنید")
            
   else:
       await m.reply("❤️ لطفا فقط عدد ارسال کنید")




async def EnterDiscount(c:Client,m:Message,orderId):
         
           dis = await orm.GetdisCountWithCode(m.text,orderId,m.from_user.id)
           if dis[0] == True:
                result = await orm.PlanidGetDiscountOrderDetails(orderId)
                plan = await orm.GetPlanById(result)
                orderBtns = await orm.GetBtnsSheldIScOUNT(orderId,plan[9])
                await orm.ChangeStep(m.from_user.id,'home') 
                await m.reply(f"""🎯 | در این بخش شیوه پرداخت خود را انتخاب کنید
                  
❤️‍🔥 | کد تخفیف تایید شد قیمت با تخفیف را واریز کنید                                             


🎛 | جزییات سرویس انتخابی :

🧩 | بسته انتخابی : {plan[0]}
💰 | قیمت : {plan[3]:,} تومان  ❌
🔥 | قیمت با تخفیف  : {dis[2]:,} ✅ 
📊 | حجم : {plan[4]} GB
⏰ | تعداد ماه : {plan[2]} ماه
🚀 | محدودیت سرعت : {'ندارد' if plan[6] == 0 else f'{plan[6]} Mb ' }
👥 | محدودیت کاربر : {'ندارد' if plan[7] == 0 else f'{plan[7]} نفر ' }

📑 | توضیحات :

{plan[1]}             

🔰 /start
""",reply_markup=InlineKeyboardMarkup(orderBtns))
                return
           else:
                   await m.reply(dis[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))    
                   await Canesel_Key(c,m,m.from_user.id)
                   return
           

async def  CardToCard(c:Client,m:Message,data):
      
       orderPrice = await orm.GetdataPriceOrder(data)
       res = await orm.GetDataForCardToCard()
       try:
        dataConfig =await ReadFileConfig()
        if   orderPrice[3] == "BuySingle" :
            
             await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=m.photo.file_id,caption=f"""🛍 خرید سرویس 
                                       
                                   
💳نوع خرید : کارت به کارت 
✍🏻 نام کاربر : {m.from_user.first_name}                                
👤 نام کاربری : @{m.from_user.username}                                  
👤 ای دی عددی : <code>{m.from_user.id}</code>        
💰 قیمت : {orderPrice[0]:,} تومان                  
☝🏻 خرید کانفیگ تکی 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {orderPrice[2]} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
        if   orderPrice[3] == "BuySub" :
            
             await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=m.photo.file_id,caption=f"""🛍 خرید سرویس 
                                        
                            
💳نوع خرید : کارت به کارت 
✍🏻 نام کاربر : {m.from_user.first_name}                                
👤 نام کاربری : @{m.from_user.username}                                  
👤 ای دی عددی : <code>{m.from_user.id}</code>        
💰 قیمت : {orderPrice[0]:,} تومان                  
🌐 خرید کانفیگ ساب 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {orderPrice[2]} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
               
        elif orderPrice[3] == "AddWallet" :      
                  await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=m.photo.file_id,caption=f"""💰 شارژ کیف پول 
                                       
                            
💳نوع خرید : کارت به کارت 
✍🏻 نام کاربر : {m.from_user.first_name}                                
👤 نام کاربری : @{m.from_user.username}                                  
👤 ای دی عددی : <code>{m.from_user.id}</code>        
💰 قیمت : {orderPrice[0]:,} تومان              
 

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
                  
        await m.reply("درخواست شما برای ادمین ارسال شد 🔰",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))    
        return
        
       except:
           await orm.ChangeStep(m.from_user.id,f"AgainCardToCard_{data}")
           await m.reply("🙏🏻 لطفا عکس ارسال کنید")
           await m.reply(text=f"""🔰 | لطفا ابتدا به این شماره کارت مبلغ را واریز کنید 
  
🔔 | دقت کنید بعد از پرداخت لطفا رسید خود را برای بات ارسال کنید سپس بعد از تایید ادمین سرویس برای شما ارسال خواهد شد   

{f"💰 | قیمت : {orderPrice[0]}" if orderPrice[1] == 0 else f"💰 | قیمت : {orderPrice[2]}"} 

💳 | شمارت کارت : {res[1]}  

👤 | نام : {res[0]} 

.
 """ )
           
        
       
            
           

async def AgainCardToCard(c:Client,m:Message,data):
      
       orderPrice = await orm.GetdataPriceOrder(data)
       try: 
           dataConfig =await ReadFileConfig()
           if   orderPrice[3] == "BuySingle" :
            
             await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=m.photo.file_id,caption=f"""🛍 خرید سرویس 
                                       
                                   
💳نوع خرید : کارت به کارت 
✍🏻 نام کاربر : {m.from_user.first_name}                                
👤 نام کاربری : @{m.from_user.username}                                  
👤 ای دی عددی : <code>{m.from_user.id}</code>        
💰 قیمت : {orderPrice[0]} تومان                  
☝🏻 خرید کانفیگ تکی 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {orderPrice[2]} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
           if   orderPrice[3] == "BuySub" :
            
             await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=m.photo.file_id,caption=f"""🛍 خرید سرویس 
                                       
                               
💳نوع خرید : کارت به کارت 
✍🏻 نام کاربر : {m.from_user.first_name}                                
👤 نام کاربری : @{m.from_user.username}                                  
👤 ای دی عددی : <code>{m.from_user.id}</code>        
💰 قیمت : {orderPrice[0]} تومان                  
🌐 خرید کانفیگ ساب 
 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {orderPrice[2]} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
   
           elif orderPrice[3] == "AddWallet" :      
                  await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=m.photo.file_id,caption=f"""💰 شارژ کیف پول 
                                       
                           
💳نوع خرید : کارت به کارت 
✍🏻 نام کاربر : {m.from_user.first_name}                                
👤 نام کاربری : @{m.from_user.username}                                  
👤 ای دی عددی : <code>{m.from_user.id}</code>        
💰 قیمت : {orderPrice[0]} تومان                  
 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {orderPrice[2]} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
           await m.reply("درخواست شما برای ادمین ارسال شد 🔰",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))    
        
           return
       except:
            
            await m.reply_video("https://media.giphy.com/media/edckP6sD9YyYxuQYpS/giphy.gif",caption="/:",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))    
            return


async def SharjWallet(c:Client,m:Message):
        try: 
          res =  int(m.text)
          if res > 10000:
              result = await orm.CreateOrder(m.from_user.id,0,0,res,"AddWallet",0)
              if result[0] == True:
                  orderBtns = await orm.GetBtnsShellWallet(result[1])
                  await m.reply("⌛️",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))   

                  await m.reply(f"""💰 | شارژ کیف پول 
                  
🫴🏻 | در این بخش شیوه پرداخت خود را انتخاب کنید  

جزییات پرداخت 🫴🏻

افزایش کیف پول به مبلغ {res}  تومان                                 

🔰 /start
""",reply_markup=InlineKeyboardMarkup(orderBtns))
                  
              else:
                 await m.reply("فاکتور ساخته نشد...") 
                 await Canesel_Key(c,m,m.from_user.id)

                 return
          else:
            await m.reply("🤖 لطفا فقط بیشتر از 10000 تومان ارسال کنید ")  
            await Canesel_Key(c,m,m.from_user.id)
            return 
        except:
            await m.reply("🤖 لطفا فقط عدد ارسال کنید ")  
            await Canesel_Key(c,m,m.from_user.id)
            return

# commands = [
#     [r"انصراف",r".+",Canesel_Key],
#      [r".+", r"cardtocard_.+", CardToCard],
#      [r".+", r"AgainCardToCard_.+", AgainCardToCard],
#      [r".+", r"SharjWallet", SharjWallet],
#      [r".+", r"enterdiscountCode_.+", EnterDiscount],
#      [r".+", r"transWalletPrice", transWalletStepOne],
#      [r".+", r"transWalletPriceTwo_.+", TransFormWallet],
#      [r".+", r"sendTiket", SendTiekt],
#      [r".+", r"requnblock", ReqUnblock],

# ]


async def StartBot(c:Client,m:Message):
    command = m.text.split(" ")  
    await orm.AddNewUser(m.from_user.id,m.from_user.first_name,m.from_user.username,command,c,m)
 
    Messages =await ReadFileText()
    photo = await orm.GePhotoStart()
    if photo[0] == 1:
       try:
          await  c.send_cached_media(chat_id=m.from_user.id,file_id=photo[1],caption=Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))
       except:
          await m.reply(Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))
    else:         
        await m.reply(Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))
@Client.on_message(  checkBtnsNot &   CheckLock  & Check_Run)
async def STEPHandler(c:Client,m:Message):
  STEP = await orm.GetUserSTEP(m.from_user.id)
  if m.text != None:
   if "/start " in m.text :
     await StartBot(c,m)
     return
  if await orm.CheckUserBlock(m.from_user.id)== True:
      if STEP == "requnblock":
             await ReqUnblock(c,m)
             await orm.ChangeStep(m.from_user.id,"requnblock")

             return
      else:
        return
  if  m.text == "انصراف":
      await Canesel_Key(c,m,m.from_user.id)
      return
  elif "cardtocard_" in STEP:
        data = STEP.split("_")[1]
        await CardToCard(c,m,data)
        return
  
  elif "AgainCardToCard_" in STEP:
        data = STEP.split("_")[1]
        await AgainCardToCard(c,m,data)
        return
  elif STEP ==  "SharjWallet" :
        
        await SharjWallet(c,m)
        return
  elif "enterdiscountCode_" in STEP:
        data = STEP.split("_")[1]
        await EnterDiscount(c,m,data)
        return

  elif STEP ==  "transWalletPrice" :
       
        await transWalletStepOne(c,m)
        return

  elif "transWalletPriceTwo_" in STEP:
        data = STEP.split("_")[1]
        await TransFormWallet(c,m,data)
        return
  elif STEP == "sendTiket"  :
       
        await SendTiekt(c,m)
        return
   
  elif STEP =="getconfigdata":
      await GetConfig(c,m)
  else:
    await orm.ChangeStep(m.from_user.id,"home")








async def GetConfig(c:Client,m:Message): 
    await m.reply("⏳ | در حال جست و جو کمی صبور باشید")
    res = await orm.GetConfigInfo(m.text)
    if res[0]==True:
          toEnd = ""
          shamsi = "نامحدود"
          if  res[2]['expired_at'] != 0:
              
           date =  datetime.datetime.fromtimestamp(res[2]['expired_at']/1000)
           shamsi = jdatetime.datetime.fromgregorian(date =date)
           shamsi = shamsi.date()
           toEnd = ""
           if datetime.datetime.now() > date:
              toEnd = "زمان اشتراک شما به پایان رسیده"
              
           else:       
              toEnd = date - datetime.datetime.now()
              if toEnd.days == 0 and toEnd.seconds>0:
                   toEnd = "کمتر از یک روز مانده"
              else:
                   toEnd = str(toEnd.days)    
          else:
              toEnd = "نامحدود"

          total = ""    
          if res[2]['transfer_enable'] != 0:
                   
           total = round(res[2]['transfer_enable'] / 1024 / 1024 /1024,2)
          else:
              total = "نامحدود"
          download =round( res[2]['d']/ 1024 / 1024 /1024,2)
          upload =  round(res[2]['u']/ 1024 / 1024 /1024,2)
          used = download + upload 
          mande = total - (download + upload )
          qr_stream = BytesIO()
          qr = qrcode.make(res[2]['subscribe_url'])
          qr.save(qr_stream)
          qr_stream.seek(0)
          
          mes =f"""
✅ | اطلاعات اشتراک شما

👤 | نام اشتراک : {res[3]}
📊 | مقدار حجم : {total} GB
⏰ | مقدار زمان : {toEnd} روز

🔗 | کانفیگ شما :

<code>{res[2]['subscribe_url']}</code>

⚠️ | آموزش اتصال در ربات می‌باشد
"""


          await m.reply_photo(photo=qr_stream,caption=mes,reply_markup=InlineKeyboardMarkup(
              [  
                  [InlineKeyboardButton("🟢" if res[2]['state'] == 1 else "🔴",callback_data="ARS"),InlineKeyboardButton("🔔 وضعیت",callback_data="ARS")],
                  [InlineKeyboardButton(total,callback_data="ARS"),InlineKeyboardButton("🔋 حجم کل",callback_data="ARS")],
                  [InlineKeyboardButton(round(used,2),callback_data="ARS"),InlineKeyboardButton("🪫 حجم مصرفی  ",callback_data="ARS")],
                  [InlineKeyboardButton(round(mande,2),callback_data="ARS"),InlineKeyboardButton("🪫 حجم باقی مانده  ",callback_data="ARS")],

                  [InlineKeyboardButton(download,callback_data="ARS"),InlineKeyboardButton("📥 حجم دانلود ",callback_data="ARS")],
                  [InlineKeyboardButton(upload,callback_data="ARS"),InlineKeyboardButton("📤 حجم آپلود ",callback_data="ARS")],
                  [InlineKeyboardButton(str(shamsi),callback_data="ARS"),InlineKeyboardButton("📆 انقضا",callback_data="ARS")],
                  [InlineKeyboardButton(toEnd,callback_data="ARS"),InlineKeyboardButton("🕐 روز های باقی مانده",callback_data="ARS")],
                  
               
               ]))
          await Canesel_Key(c,m,m.from_user.id)
          return

    else:
            await orm.ChangeStep(m.from_user.id,'home') 
            
            await m.reply(res[1])     
            await Canesel_Key(c,m,m.from_user.id)
            return
    




@Client.on_callback_query(blockCheck & CheckLock )
async def CallBackHandler(c: Client, call: CallbackQuery):
   if call.data == "ARS":
       return
   if call.data == "mainservice" :
        if await orm.IsShop() == True :
         btns = []
         btnsonline=[]
         Setting = await orm.GetSettingTypeShop()
         if Setting[1] == 1:
             btns.append(InlineKeyboardButton("اشتراک معمولی " if Setting[3] == "empty" or Setting[3] == None else  f"{Setting[3]}" ,callback_data="SingleShop"))
         if Setting[0] == 1 :
             btns.append( InlineKeyboardButton("اشتراک ساب "  if Setting[2] == "empty" or Setting[2] == None else  f"{Setting[2]}",callback_data="MultiShop") )
         if  Setting[4] == 1:
             btnsonline.append( InlineKeyboardButton('🌐 | خرید از سایت (تحویل آنی)',url=f"https://xenitgame.com/ping?from=do&userId={call.from_user.id}"))   
         if    btns!= [] :
          finalbtns = [btns]   
          if btnsonline!= []:
              finalbtns = [btns,btnsonline]                
         if    btns!= [] :
             
          await call.edit_message_text("""🛍 فروش سرویس ها 
                  
🫴🏻 در این بخش  نوع سرویس خود را انتخاب کنید  

🔰 /start              """,reply_markup=InlineKeyboardMarkup(finalbtns))
          return
         else:
              await call.edit_message_text("""🔰 این بخش غیر فعال است 
                            
🔰 /start
                    """)   
         return
        else:
              await call.edit_message_text("""🔰 این بخش غیر فعال است 
                            
🔰 /start
                    """)   
              return

   if "OrderSingle_" in call.data:
      data = call.data.split("_")[1]
      ServerId = call.data.split("_")[2]
      plan = await orm.GetPlanById(data)
      catId = call.data.split("_")[3]
      if plan[5] <= plan[8]:
         await call.answer("🙏🏻 موجودی این پلن به پایان رسیده ",True)
         return
      user= await orm.GetUserPerId(call.from_user.id)
      NewPrice = 0
      Per = None
      if user!= 0:
           Per =  await orm.GetPercentById(user)
           if Per != None:
               
              NewPrice =   plan[3] - ( Per[2] * plan[3] / 100 )
           else:
                  NewPrice = plan[3]
           order = await orm.CreateOrderSingle(call.from_user.id ,data  , 0 ,NewPrice ,  "BuySingle",plan[2],ServerId,catId)
      else: 
           order = await orm.CreateOrderSingle(call.from_user.id ,data  , 0 ,plan[3] ,  "BuySingle",plan[2],ServerId,catId)
      
      if order[0] ==True:
         orderBtns = await orm.GetBtnsShel(order[1],plan[9])
         
         if NewPrice != 0:
             await orm.UpdateorderPrice(order[1],NewPrice)
             await call.edit_message_text(f"""
🎯 | در این بخش شیوه پرداخت خود را انتخاب کنید

🎛 | جزییات سرویس انتخابی :

🧩 | بسته انتخابی : {plan[0]}
💰 | قیمت : {str(plan[3])} تومان  ❌
🤝 | قیمت همکاری  : {str(int(NewPrice)) } ✅ 
📊 | حجم : {plan[4]} GB
⏰ | تعداد ماه : {plan[2]} ماه
🚀 | محدودیت سرعت : {'ندارد' if plan[6] == 0 else f'{plan[6]} Mb ' }
👥 | محدودیت کاربر : {'ندارد' if plan[7] == 0 else f'{plan[7]} نفر ' }

📑 | توضیحات :

{plan[1]}             

🔰 /start    

""",reply_markup=InlineKeyboardMarkup(orderBtns))
             return
         await call.edit_message_text(f"""
🎯 | در این بخش شیوه پرداخت خود را انتخاب کنید

🎛 | جزییات سرویس انتخابی :

🧩 | بسته انتخابی : {plan[0]}
💰 | قیمت : {str(plan[3])} تومان
📊 | حجم : {plan[4]} GB
⏰ | تعداد ماه : {plan[2]} ماه
🚀 | محدودیت سرعت : {'ندارد' if plan[6] == 0 else f'{plan[6]} Mb ' }
👥 | محدودیت کاربر : {'ندارد' if plan[7] == 0 else f'{plan[7]} نفر ' }

📑 | توضیحات :

{plan[1]}             

🔰 /start    
""",reply_markup=InlineKeyboardMarkup(orderBtns))
         return
      else: 
        await call.answer("فاکتور ساخته نشد...")   
        return
   if "GetPlanCat_" in call.data:
       ServerId= call.data.split("_")[2]
       CatId= call.data.split("_")[1]
       btns = await orm.GetPlanCatShellSingle(CatId,ServerId)
       await call.edit_message_text("""🛍 فروش سرویس ها 
                  
🫴🏻  در این بخش پلن خود را انتخاب کنید  

🔰  /start
""",reply_markup=InlineKeyboardMarkup(btns))
       return
        
   if "GetServers_" in call.data :
       catId = call.data.split("_")[1]
       Servers = await orm.GetServerCatForShop(catId)
       await call.edit_message_text("""🛍 فروش سرویس ها 
                  
🫴🏻  در این بخش سرور خود را انتخاب کنید  

🔰  /start
""",reply_markup=InlineKeyboardMarkup(Servers))
   if call.data == "MultiShop":
       if await orm.IsShop() == True :
         
         await call.edit_message_text("""🛍 فروش سرویس ها 
                  
🫴🏻 در این بخش دسته بندی خود را انتخاب کنید  

🔰 /start              """,reply_markup=InlineKeyboardMarkup(await orm.GetCatBtnsShell()))
         return
       else:
              await call.answer("""🔰 این بخش غیر فعال است 
                    """,True)   
              return
       
   if  call.data == "SingleShop":   
        if await orm.IsShop() == True :
         btns = await orm.SingleServers()
         if btns == [] :
             await call.answer("در حال حاضر امکان خرید کانفیگ تکی نمیباشد",True)
             return
         await call.edit_message_text("""🛍 فروش سرویس ها 
                  
🫴🏻 در این بخش سرور خود را انتخاب کنید  

🔰 /start              """,reply_markup=InlineKeyboardMarkup(btns))
         return
        else:
              await call.answer("""🔰 این بخش غیر فعال است 
                    """,True)   
              return
   if  "payOnline_" in call.data :
       orderId = call.data.split("_")[1]
       text =await orm.GetTextAlertOnline()
       btns = await orm.GetOnlinePayBtns(orderId)
       await call.message.delete()
       await call.message.reply(text,reply_markup=InlineKeyboardMarkup(btns))
       return
   if call.data == "buyPanel":
       await call.edit_message_text("برای خرید پنل همکاری به پشتیبانی پیام بدهید",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("پشتیبانی",url="https://t.me/AR_S_83")]]))

   if call.data == "buyBot":
       await call.edit_message_text("برای خرید ربات به پشتیبانی پیام بدهید",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("پشتیبانی",url="https://t.me/AR_S_83")]]))   

   if "deatilApp_" in call.data :
       appId = call.data.split("_")[1]
       app = await orm.GetAppById(appId)
       await call.message.delete()
       if app[5] == "empty":
          await call.message.reply(app[3],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"دانلود {app[1]}",url=app[2])]]))
       else:
          await c.send_cached_media(chat_id=call.from_user.id,file_id=app[5],caption=app[3],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"دانلود {app[1]}",url=app[2])]]))

   if call.data == "mainApp":
        await call.edit_message_text("""📲 | از لیست زیر سیستم عامل مورد نظر خود را انتخاب کنید
                 
🔰 | /start
                 """,reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton("اندروید",callback_data="AndroidApp")],
      [InlineKeyboardButton("ویندوز",callback_data="WindowsApp")],
      [InlineKeyboardButton("IOS",callback_data="IosApp")],
      [InlineKeyboardButton("لینوکس",callback_data="LinuxApp")]
      
      ]))
   if call.data == "AndroidApp":
       btns = await orm.GetAppList('android')
       await call.edit_message_text("""
🔰 | لیست نرم افزار ها به شرح زیر است لطفا نرم افزار مورد نیاز سیستم عامل خود را انتخاب کنید

🔸 | پیشنهاد میشود از برنامه های پیشنهادی ما برای اتصال استفاده کنید تا به مشکل نخورید

🔰 | /start
""",reply_markup=InlineKeyboardMarkup(btns))
   if call.data == "WindowsApp":
       btns = await orm.GetAppList('Windows')
       await call.edit_message_text("""
🔰 | لیست نرم افزار ها به شرح زیر است لطفا نرم افزار مورد نیاز سیستم عامل خود را انتخاب کنید

🔸 | پیشنهاد میشود از برنامه های پیشنهادی ما برای اتصال استفاده کنید تا به مشکل نخورید

🔰 | /start
""",reply_markup=InlineKeyboardMarkup(btns))     
   if call.data == "IosApp":
       btns = await orm.GetAppList('IOS')
       await call.edit_message_text("""
🔰 | لیست نرم افزار ها به شرح زیر است لطفا نرم افزار مورد نیاز سیستم عامل خود را انتخاب کنید

🔸 | پیشنهاد میشود از برنامه های پیشنهادی ما برای اتصال استفاده کنید تا به مشکل نخورید

🔰 | /start
""",reply_markup=InlineKeyboardMarkup(btns))     
   if call.data == "LinuxApp":
       btns = await orm.GetAppList('Linux')
       await call.edit_message_text("""
🔰 | لیست نرم افزار ها به شرح زیر است لطفا نرم افزار مورد نیاز سیستم عامل خود را انتخاب کنید

🔸 | پیشنهاد میشود از برنامه های پیشنهادی ما برای اتصال استفاده کنید تا به مشکل نخورید

🔰 | /start
""",reply_markup=InlineKeyboardMarkup(btns))   
   if "ReqCooperation_" in call.data:
       perId = call.data.split("_")[1]
       user = await orm.GetUserByUserId(call.from_user.id)
       per = await orm.GetPercentById(perId)
       await call.message.delete() 
       try: 
           data = await ReadFileConfig()
           await c.send_message(data['ownerId'],f"""👤 کاربر {call.from_user.username} 
                                
🫴🏻 درخواست دریافت  تخفیف همکاری  داشته است
                                
🔰 جزییات کاربر  

 💰 کیف پول  : {user[7]}

 🛍 خرید کرده  : {user[10]}

 👤  دعوت کرده  : {user[11]}
                           
🔰 /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessPerUse_{perId}_{user[0]}"),InlineKeyboardButton("❌ رد",callback_data=f"RejectPerUse_{user[1]}")]]))
           await call.message.reply("✅ | درخواست برای ادمین اصلی ارسال شد")
           await Canesel_Key(c,call.message,call.from_user.id)
           return
       except:
           await call.message.reply("❌ | درخواست برای ادمین اصلی ارسال نشد")
           await Canesel_Key(c,call.message,call.from_user.id)
           return 
   if call.data == "Cooperationdiscount":
       btns = await orm.GetAllBtnsCooperation(call.from_user.id)
       await call.edit_message_text("""🤝 تخفیف همکاری
                                    
 🔰 شما پس از خرید تعداد بالا از ما میتوانید از خدمات همکاری ما استفاده کنید
🔰 /start""",reply_markup=InlineKeyboardMarkup(btns))

   if call.data == "SendTiket":
    await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    await orm.ChangeStep(call.from_user.id,"sendTiket")
    await call.message.reply(text="🔻 لطفا متن خود را ارسال کنید فرمایید" )
    return
#  NEW Features


   if call.data == "GetInviteLink":
      res = await c.get_me()
      link =  f"https://t.me/{res.username}?start=inv{call.from_user.id}"
      await orm.UpdateInviteLink(f"inv{call.from_user.id}",call.from_user.id)
      await call.message.reply(f"""✅ لینک دعوت ساخته شد 
                                   
لینک دعوت : {link}

🔰 | تنها کافیست که کاربر اولین بار با لینک شما ربات را استارت بزند 

🔰 | /start
                                   """)
   if  call.data == "mainCooperation":
       if await orm.checkServiceBtn('hamkarbtn') ==True:
            await call.edit_message_text("""🤝 | بخش همکاری خوش آمدید

🔰 | در این بخش میتوانید با همکاری کنید                 

🔰 | /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👤 زیر مجموعه گیری",callback_data="collection")],[InlineKeyboardButton("🤝 تخفیف همکاری",callback_data="Cooperationdiscount")],[InlineKeyboardButton("🛍 خرید پنل همکاری",callback_data="buyPanel")],[InlineKeyboardButton("🤖 دریافت ربات اختصاصی",callback_data="buyBot")]]))
       else:
              await call.message.reply("""این بخش غیر فعال است 
                  
🔰 | /start       
                    """)     
   if call.data == "collection":
       btns = await orm.GetbtnsCollection(call.from_user.id)

       await call.edit_message_text("""👤 زیر مجموعه های شما 
       
اطلاعاتی درباره زیر مجموعه های شما 🔔
       
🔰 | /start
                                    """,reply_markup=InlineKeyboardMarkup(btns))


   if "ExtensionFinall" in call.data :
        planId =  call.data.split("_")[1]
        Service =  call.data.split("_")[2]
        if await orm.CheckWalletForExtension(planId,call.from_user.id)== True:
          res=  await orm.ExtensionFinall(planId,call.from_user.id ,Service)
          
          if res[0] == True:
              await call.message.reply(res[1])
          else:
              await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
              return 
        else:
           await  call.answer("😂 موجودی کیف پول شما کافی نیست",True)    
   if call.data ==  "extensionList" :
    btns =  await orm.GetServiceForExtension(call.from_user.id)
    await call.edit_message_text("""🔄 تمدید سرویس
                 
🔰 در این بخش میتوانید سرویس های خود را تمدید کنید 
                 
🟣 | /start
""",reply_markup=InlineKeyboardMarkup(btns))
    return
   if call.data == "MainDays":
         await call.edit_message_text("""❤️‍🔥❄️ جشنواره دی ماه

لیستی از فعال ترین افراد ربات 😄🫴🏻

شما هم میتونید یکی از انها باشید 😁                                  

🔰 /start                  
                 """,reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔰 برترین های ما 🔰",callback_data="ARS")],
                    [InlineKeyboardButton("بیشترین تعداد خرید",callback_data="upCountShoped")],
                    [InlineKeyboardButton("بیشترین مقدار خرید",callback_data="UpShoped")],
                    [InlineKeyboardButton("بیشترین دعوت کننده",callback_data="UpInviteUsers")],
                    [InlineKeyboardButton("بیشترین مصرف کننده",callback_data="UpUseUsers")],
                    
               
                    ]))
         return
   if call.data ==  "upCountShoped" :
        btns =await orm.getbtnsCountShpped()
        await call.edit_message_text("""❤️‍🔥❄️ جشنواره دی ماه
                                     
🔰 بیشترین تعداد خرید 
                                     
🔰 /start                                     
                                     """,reply_markup=InlineKeyboardMarkup(btns))



   if call.data == "UpShoped":
       
        btns =await orm.GetTopShopped()
        await call.edit_message_text("""❤️‍🔥❄️ جشنواره دی ماه
                                     
🔰 بیشترین مقدار خرید 
                                     
🔰 /start                                     
                                     """,reply_markup=InlineKeyboardMarkup(btns))

   if call.data == "UpInviteUsers":
       
        btns = await orm.getbtnsCountInvitedBest()
        await call.edit_message_text("""❤️‍🔥❄️ جشنواره دی ماه
                                     
🔰 بیشترین تعداد دعوت 
                                     
🔰 /start                                     
                                     """,reply_markup=InlineKeyboardMarkup(btns))
   
   if "extension_" in call.data :
      if await orm.checkServiceBtn('tamdidbtn') ==True:   
         serviceId = call.data.split("_")[1]
         btns = await orm.GetPlanExtForExt(serviceId)
         await call.edit_message_text("لطفا پلن خود را انتخاب کنید و برای پرداخت اقدام کنید ",reply_markup=InlineKeyboardMarkup(btns))
      else:
              await call.message.reply("""این بخش غیر فعال است """)
 
   if call.data == "UpUseUsers":
        btns = await orm.GetTopUseUsers()
        await call.edit_message_text("""❤️‍🔥❄️ جشنواره دی ماه
                                     
🔰 بیشترین مصرف کننده 
                                     
🔰 /start                                     
                                     """,reply_markup=InlineKeyboardMarkup(btns))
        return
   

   if "transferWallet" in call.data:
       await call.message.delete()
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       await orm.ChangeStep(call.from_user.id,"transWalletPrice")
    
       await call.message.reply(text="🔻بزرگتر از  تومان 10,000 لطفا قیمت را ارسال فرمایید")
       return
           
       
   if "WithCodeDis_" in call.data:
       orderId = call.data.split("_")[1]
       
       await call.message.delete()
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       await orm.ChangeStep(call.from_user.id,f"enterdiscountCode_{orderId}")
 
       await call.message.reply(text="🔻 لطفا کد تخفیف را ارسال فرمایید")
       return
   if "getOrder_" in call.data:
      data = call.data.split("_")[1]
      plan = await orm.GetPlanById(data)
      CatId = call.data.split("_")[2]
      print(plan)
      if plan[5] <= plan[8]:
         await call.answer("🙏🏻 موجودی این پلن به پایان رسیده ",True)
         return
      user= await orm.GetUserPerId(call.from_user.id)
      NewPrice = 0
      Per = None
      
      if user!= 0:
           Per =  await orm.GetPercentById(user)
           if Per != None:
               
              NewPrice =   plan[3] - ( Per[2] * plan[3] / 100 )
           else:
                  NewPrice = plan[3]
           order = await orm.CreateOrder(call.from_user.id ,data  , 0 ,NewPrice ,  "BuySub",plan[2],CatId)
      else: 
           order = await orm.CreateOrder(call.from_user.id ,data  , 0 ,plan[3] ,  "BuySub",plan[2],CatId)
      
      if order[0] ==True:
         orderBtns = await orm.GetBtnsShel(order[1],plan[9])
         if NewPrice != 0:
             await orm.UpdateorderPrice(order[1],NewPrice)
             await call.edit_message_text(f"""
🎯 | در این بخش شیوه پرداخت خود را انتخاب کنید

🎛 | جزییات سرویس انتخابی :

🧩 | بسته انتخابی : {plan[0]}
💰 | قیمت : {str(plan[3])} تومان  ❌
🤝 | قیمت همکاری  : {str(int(NewPrice)) } ✅ 
📊 | حجم : {plan[4]} GB
⏰ | تعداد ماه : {plan[2]} ماه
🚀 | محدودیت سرعت : {'ندارد' if plan[6] == 0 else f'{plan[6]} Mb ' }
👥 | محدودیت کاربر : {'ندارد' if plan[7] == 0 else f'{plan[7]} نفر ' }

📑 | توضیحات :

{plan[1]}             

🔰 /start    
""",reply_markup=InlineKeyboardMarkup(orderBtns))
             return
         await call.edit_message_text(f"""
🎯 | در این بخش شیوه پرداخت خود را انتخاب کنید

🎛 | جزییات سرویس انتخابی :

🧩 | بسته انتخابی : {plan[0]}
💰 | قیمت : {str(plan[3])} تومان
📊 | حجم : {plan[4]} GB
⏰ | تعداد ماه : {plan[2]} ماه
🚀 | محدودیت سرعت : {'ندارد' if plan[6] == 0 else f'{plan[6]} Mb ' }
👥 | محدودیت کاربر : {'ندارد' if plan[7] == 0 else f'{plan[7]} نفر ' }

📑 | توضیحات :

{plan[1]}             

🔰 /start    
""",reply_markup=InlineKeyboardMarkup(orderBtns))
         return
      else: 
        await call.answer("فاکتور ساخته نشد...")   
        return
   if call.data == "IJoin":
    #   await orm.AddNewUser(call.from_user.id,call.from_user.first_name,call.from_user.username)
   
      Messages =await ReadFileText()

      await call.message.delete()
      await call.message.reply(Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
      return
   if "planshop_" in call.data:
      
      data = call.data.split("_")[1]
      await call.edit_message_text("""🛍 فروش سرویس ها 
                  
🫴🏻 در این بخش پلن خود را انتخاب کنید  

🔰 /start
""",reply_markup=InlineKeyboardMarkup(await orm.GetPlanCatShell(data)))
      return
   if "CardToCard_" in call.data:
       data = call.data.split("_")[1]
       orderPrice = await orm.GetdataPriceOrder(data)
       res  = await orm.GetDataForCardToCard()
       await call.answer(res[2],True)
       await call.message.delete()
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       await orm.ChangeStep(call.from_user.id,f"cardtocard_{data}")
       await orm.ChangeStep(call.from_user.id,f"cardtocard_{data}")
       await call.message.reply(text=f"""🔰 | لطفا ابتدا به این شماره کارت مبلغ را واریز کنید 
  
🔔 | دقت کنید بعد از پرداخت لطفا رسید خود را برای بات ارسال کنید سپس بعد از تایید ادمین سرویس برای شما ارسال خواهد شد   

{f"💰 | قیمت : {orderPrice[0]}" if orderPrice[1] == 0 else f"💰 | قیمت : {orderPrice[2]}"} 

💳 | شمارت کارت : {res[1]}  

👤 | نام : {res[0]} 

.
                                       """ )
       return 
 
   if "GETConfig_" in call.data:
        data = call.data.split("_")[1]
        res = await orm.GetCofigUser(data) 
        if res[0]==True:
          date =  datetime.datetime.fromtimestamp(res[2]['expired_at']/1000)
          shamsi = jdatetime.datetime.fromgregorian(date =date)
          toEnd = ""
          if datetime.datetime.now() > date:
              toEnd = "زمان اشتراک شما به پایان رسیده"
              
          else:       
              toEnd = date - datetime.datetime.now()
              if toEnd.days == 0 and toEnd.seconds>0:
                   toEnd = "کمتر از یک روز مانده"
              else:
                   toEnd = str(toEnd.days)    
          total = round(res[2]['transfer_enable'] / 1024 / 1024 /1024,2)
          download =round( res[2]['d']/ 1024 / 1024 /1024,2)
          upload =  round(res[2]['u']/ 1024 / 1024 /1024,2)
          used = download + upload 
          mande = total - (download + upload )
          qr_stream = BytesIO()
          qr = qrcode.make(res[2]['subscribe_url'])
          qr.save(qr_stream)
          qr_stream.seek(0)
          await call.message.delete()
          mes =f"""
✅ | اطلاعات اشتراک شما

👤 | نام اشتراک : {res[3]}
📊 | مقدار حجم : {total} GB
⏰ | مقدار زمان : { f'{toEnd} روز ' if toEnd.isnumeric()  == True else toEnd }

🔗 | کانفیگ شما :

<code>{res[2]['subscribe_url']}</code>

{f"🌐 | ادرس اتصال ساب : <code>{res[2]['subsingle']}</code>" if res[2]['subsingle'] != "" else "" }

⚠️ | آموزش اتصال در ربات می‌باشد
"""


          await call.message.reply_photo(photo=qr_stream,caption=mes,reply_markup=InlineKeyboardMarkup(
              [  
                  [InlineKeyboardButton("🟢" if res[2]['state'] == 1 else "🔴",callback_data="ARS"),InlineKeyboardButton("🔔 وضعیت",callback_data="ARS")],
                  [InlineKeyboardButton(total,callback_data="ARS"),InlineKeyboardButton("🔋 حجم کل",callback_data="ARS")],
                  [InlineKeyboardButton(round(used,2),callback_data="ARS"),InlineKeyboardButton("🪫 حجم مصرفی   ",callback_data="ARS")],
                 [InlineKeyboardButton(round(mande,2),callback_data="ARS"),InlineKeyboardButton("🪫  حجم باقی مانده  ",callback_data="ARS")],

                  [InlineKeyboardButton(download,callback_data="ARS"),InlineKeyboardButton("📥 حجم دانلود ",callback_data="ARS")],
                  [InlineKeyboardButton(upload,callback_data="ARS"),InlineKeyboardButton("📤 حجم آپلود ",callback_data="ARS")],
                  [InlineKeyboardButton(str(shamsi.date()),callback_data="ARS"),InlineKeyboardButton("📆 انقضا",callback_data="ARS")],
                  [InlineKeyboardButton(toEnd,callback_data="ARS"),InlineKeyboardButton("🕐 روز های باقی مانده",callback_data="ARS")],
                  [InlineKeyboardButton("تعویض لینک سرویس",callback_data=f"Changelink_{data}"),InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{data}")],[InlineKeyboardButton("منو سرویس ها",callback_data="menuService")]
               
               ]))
          return

        else:
            await call.answer(res[1])     
            return
   if "Changelink_" in call.data:
      if await orm.CanUserChangeLinkConf() == True:  
        data = call.data.split("_")[1]

        res = await orm.GetCofigUserANDChange(data,c) 
        if res[0]==True:
          date =  datetime.datetime.fromtimestamp(res[2]['expired_at']/1000)
          shamsi = jdatetime.datetime.fromgregorian(date =date)
          toEnd = ""
          if datetime.datetime.now() > date:
              toEnd = "زمان اشتراک شما به پایان رسیده"
              
          else:       
              toEnd = date - datetime.datetime.now()
              if toEnd.days == 0 and toEnd.seconds>0:
                   toEnd = "کمتر از یک روز مانده"
              else:
                   toEnd = str(toEnd.days)    
          total = res[2]['transfer_enable'] / 1024 / 1024 /1024
          download = res[2]['d']/ 1024 / 1024 /1024
          upload = res[2]['u']/ 1024 / 1024 /1024
          used = download + upload 
          mande = total - (download + upload )
          qr_stream = BytesIO()
          qr = qrcode.make(res[2]['subscribe_url'])
          qr.save(qr_stream)
          qr_stream.seek(0)
          await call.message.delete()
          mes =f"""
✅ | اطلاعات کانفیگ شما

👤 | نام کانفیگ : {res[3]}

📊 | مقدار حجم : {total}

⏰ | مقدار زمان : {toEnd} 

🔗 | کانفیگ شما :

<code>{res[2]['subscribe_url']}</code>

{f"🌐 | ادرس اتصال ساب : <code>{res[2]['subsingle']}</code>" if res[2]['subsingle'] != "" else "" }

⚠️ | آموزش اتصال در ربات می‌باشد
"""

          await call.message.reply_photo(photo=qr_stream,caption=mes,reply_markup=InlineKeyboardMarkup(
              [
                  [InlineKeyboardButton("🟢" if res[2]['state'] == 1 else "🔴",callback_data="ARS"),InlineKeyboardButton("🔔 وضعیت",callback_data="ARS")],
                  
                  [InlineKeyboardButton(total,callback_data="ARS"),InlineKeyboardButton("🔋 حجم کل",callback_data="ARS")],
                  [InlineKeyboardButton(round(used,2),callback_data="ARS"),InlineKeyboardButton("🪫 حجم مصرفی   ",callback_data="ARS")],
                  [InlineKeyboardButton(round(mande,2),callback_data="ARS"),InlineKeyboardButton("🪫  حجم باقی مانده  ",callback_data="ARS")],

                  [InlineKeyboardButton(download,callback_data="ARS"),InlineKeyboardButton("📥 حجم دانلود ",callback_data="ARS")],
                  [InlineKeyboardButton(upload,callback_data="ARS"),InlineKeyboardButton("📤 حجم آپلود ",callback_data="ARS")],
                  [InlineKeyboardButton(str(shamsi.date()),callback_data="ARS"),InlineKeyboardButton("📆 انقضا",callback_data="ARS")],
                  [InlineKeyboardButton(toEnd,callback_data="ARS"),InlineKeyboardButton("🕐 روز های باقی مانده",callback_data="ARS")],
                  [InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{data}")],[InlineKeyboardButton("منو سرویس ها",callback_data="menuService")]
               
               ]))
          return

        else:
            await call.answer(res[1])     
            return
      else:
        await call.answer("🙏🏻 این بخش غیر فعال میباشد ",True)   
   if call.data == "menuService":
       await call.message.delete()
       await call.message.reply("""📥 بخش سرویس من 
                    
🫴🏻تمام سرویس های خود را میتوانید از این لیست ببینید

🔰 /start    """,reply_markup=InlineKeyboardMarkup(await orm.GetServiceList(call.from_user.id)))   
       return
   if "GETConfigTest_" in call.data:
        data = call.data.split("_")[1]
        res = await orm.GetCofigUserTest(data) 
        if res[0]==True:
          date =  datetime.datetime.fromtimestamp(res[2]['expired_at'])
          shamsi = jdatetime.datetime.fromgregorian(date =date)
          toEnd = ""
          if datetime.datetime.now() > date:
              toEnd = "زمان اشتراک شما به پایان رسیده"
              
          else:       
              toEnd = date - datetime.datetime.now()
              if toEnd.days == 0 and toEnd.seconds>0:
                   toEnd = "کمتر از یک روز مانده"
              else:
                   toEnd = str(toEnd.days)    
          total = res[5] / 1024 / 1024 /1024
          download = res[2]['d']/ 1024 / 1024 /1024
          upload = res[2]['u']/ 1024 / 1024 /1024
          used = download + upload 
          qr_stream = BytesIO()
          qr = qrcode.make(res[4])
          qr.save(qr_stream)
          qr_stream.seek(0)
          await call.message.delete()
          mes =f"🔸 نام کاربری: {res[3]}\n🔸 وضعیت: 0\n🔸 حجم کل: {total}\n🔸 حجم مصرفی: {used}\n🔸 حجم دانلود: {download}GB\n🔸 حجم اپلود: {upload}GB\n📆 انقضا: {str(shamsi)} \n🕐 روز های باقی مانده: {toEnd}\nتست رایگان 🌟\n\n\n\n🔗 کانفیگ شما:\n <code>{res[4]}</code>"

          await call.message.reply_photo(photo=qr_stream,caption=mes,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تعویض لینک سرویس",callback_data=f"Changelink_{data}")]]))
          return
        else:
            await call.answer(res[1])
            return     
      
   if call.data == "SharjWallet":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       await orm.ChangeStep(call.from_user.id,f"SharjWallet")

       await call.message.reply(text="🔻(بیشتر از 10000 تومان) لطفا قیمت را حتما به عدد وارد کنید" )
       return
      
      
   if "PayWallet_" in call.data:
       orderId = call.data.split("_")[1]
       res =await orm.ShopANDGetSubscribe(orderId,call.from_user.id)
       if res == True :
          result = await orm.CreateSub(orderId,c)
          if result[0] == True:
             
             await c.send_message(chat_id=result[3],text ="""✅ | سرویس شما اضافه با موفقیت خریداری شد 

کاربر گرامی توجه ! ⚠️
لطفا برای دریافت ادرس اتصال خود دکمه زیر را لمس نمایید سپس کمی صبر کنید تا سرویس برای شما ارسال شود 🫴🏻
یا میتوانید از قسمت اشتراک های من اشتراک خود را دریافت و مشاهده کنید 🫳🏻

🔰 /start

""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton( "دریافت",callback_data= f"GETConfig_{result[2]}")]]))
             
             await call.answer(result[1])
             return
          else:
            await call.answer(result[1])
            return
       else:
           await call.answer("اعتبار کیف پول شما کافی نیست | 💰 ",True)    
           return
      
      

