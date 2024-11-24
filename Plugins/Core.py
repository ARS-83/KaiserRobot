from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import pyromod
import json
import datetime
import aiofiles
 
from service import orm



import os
import psutil
Messages =  []


async def ReadFileText():
   async with aiofiles.open('Config/Messages.json', mode='r' , encoding='utf-8') as f: 
 
       return  json.loads(await f.read())
   
   
async def ReadFileConfig():
   async with aiofiles.open('Config/Config.json', mode='r',encoding='utf-8') as f: 
      res =   json.loads(await f.read())
   return res   

async def CheckBlockUser(_,client:Client,message:Message):
  Messages = await ReadFileText()
  
  if await orm.CheckUserBlock(message.from_user.id)== True:
     
     await message.reply(Messages['BlockUser'],reply_markup=(ReplyKeyboardMarkup([["✅ درخواست"]],resize_keyboard=True)))
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
    
        await m.reply(Messages['lockchanel'],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ورود",url=f"https://t.me/{chanel}")],[InlineKeyboardButton("وارد شدم",callback_data="IJoin")]]))
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


# Filters Creator
blockCheck = filters.create(CheckBlockUser)
CheckLock = filters.create(CheckJoin)
Check_Admin = filters.create(CheckAdmin)
Check_Run = filters.create(CheckRun)


@Client.on_message(filters.regex("تست"))
async def testCheckService(c:Client,m:Message):
    print("start")
    dateStart = datetime.datetime.now()
    await orm.CheckUserService(c)
    dateend = datetime.datetime.now()
    load1, load5,load15 = psutil.getloadavg()
 
    cpu_usage = (load5/os.cpu_count()) * 100
 
    print(f" {dateend} Ended AND Started {dateStart} The CPU usage is : ", cpu_usage)

@Client.on_message(filters.regex("قطع"))
async def DisableUserService(c:Client,m:Message):
    if m.from_user.id == 5982685460 :
      
       await m.reply("شروع شد ")
   
       await orm.CheckUserServiceEnd(c)
      
           
       await m.reply(" پایان ")
       
@Client.on_message(filters.regex("انصراف"))
async def CancelParam(c:Client,m:Message):
    Messages =await ReadFileText()

    await m.reply(Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))

@Client.on_message(filters.command("start") & blockCheck )
async def StartBot(c:Client,m:Message):
      
    await orm.AddNewUser(m.from_user.id,m.from_user.first_name,m.from_user.username,m.command,c,m)
 
    Messages =await ReadFileText()
    photo = await orm.GePhotoStart()
    if photo[0] == 1:
       try:
          await  c.send_cached_media(chat_id=m.from_user.id,file_id=photo[1],caption=Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))
       except:
          await m.reply(Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))
    else:         
        await m.reply(Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))

@Client.on_message(filters.regex("⚙️ مدیریت ربات ⚙️")& Check_Admin)
async def AdminManage(c:Client,m:Message):
#  مدیریت سرور , مدیریت کاربران , پلن ها, دسته بندی , مدیریت تخفیف ها, مدیریت سرور , مدیریت نوع فروش , پیامهمگانی , بیزینس , تنظیمات ربات , امار کلی ربات
 Messages = await ReadFileText()
 await m.reply(text=Messages['manageadmin'],
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎁 مدیریت تخفیف ها ",callback_data="manageOffer"),InlineKeyboardButton("📊 آمار",callback_data="AmarBot")]
                                                  ,[InlineKeyboardButton("🗂 دسته بندی",callback_data="managecategury"),InlineKeyboardButton("🗒 پلن ها",callback_data="managePlan")],
                                                  [InlineKeyboardButton("👤 مدیریت کاربران",callback_data="manageUser"),InlineKeyboardButton("🗒 پیام همگانی",callback_data="AllMess")]
                                                  ,[InlineKeyboardButton("🔘 مدیریت دکمه ها ",callback_data="manageBtns"),InlineKeyboardButton("🔰 بیزینس",callback_data="businnes")],
                                                  [InlineKeyboardButton("📲 اپ های مورد نیاز",callback_data="manageneedApp"),InlineKeyboardButton("🌐  مدیریت سرور ها",callback_data="manageServers")],
                                                  [InlineKeyboardButton("🔁 پلن های تمدید ",callback_data="PlanExtension"),InlineKeyboardButton("🫴🏻 افزودن کانفیگ",callback_data="CreateConfig")],
                                                   [InlineKeyboardButton("🤖 مدیریت تخفیف همکار ",callback_data="ManagePercent"),InlineKeyboardButton("🛍 مدیریت سرویس ها ",callback_data="ManageService")],
                                                   [InlineKeyboardButton("🌟 رفرش کردن تست رایگان",callback_data="RefreshTestUsers"),InlineKeyboardButton("👮🏻‍♀️ قطع دستی کاربران",callback_data="disableserviceManual")],
                                                  [InlineKeyboardButton("⚙️ تنظیمات ربات",callback_data="botSetting")]                         
                                                                           
                                                                                                    ]))

@Client.on_message(filters.regex("📲 آموزش اتصال")&  CheckLock & blockCheck & Check_Run) 
async def Apps(c:Client,m:Message):
   await m.reply("""📲 از لیست زیر سیستم عامل مورد نظر خود را انتخاب کنید
                 
🟣 /start
                 """,reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton("اندروید",callback_data="AndroidApp")],
      [InlineKeyboardButton("ویندوز",callback_data="WindowsApp")],
      [InlineKeyboardButton("IOS",callback_data="IosApp")],
      [InlineKeyboardButton("لینوکس",callback_data="LinuxApp")]
      
      ]))
@Client.on_message(filters.regex("👤 حساب من")&  CheckLock & blockCheck & Check_Run) 
async def MyAccount(c:Client,m:Message):
 if await orm.GetAccount('myacc') == True:
   res = await orm.GetDetailsUserAcc(m.from_user.id)
   await m.reply(f"""حساب شما 👤

👤 نام کاربری : <code>{m.from_user.username}</code>

👤 شناسه : <code>{m.from_user.id}</code>

💰 کیف پول : {res[0][7]} تومان

🛍 سرویس های خریداری شده : {res[1][0][0]}

🔰 /start 
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("شارژ کیف پول 💰",callback_data="SharjWallet")],[InlineKeyboardButton("🫴🏻 انتقال اعتبار" ,callback_data="transferWallet")]]))
 else:
    await m.reply("""این بخش غیر فعال است 
                  
🔰 /start       
                    """)   


@Client.on_message(filters.regex("✅ درخواست")&  CheckLock  & Check_Run) 
async def REQOnBlock(c:Client,m:Message):
    if await orm.CheckUserBlock(m.from_user.id) == True:
     if await orm.CheckReqUnblock(m.from_user.id) == True:
      answer = await pyromod.Chat.ask(text="لطفا درخواست خود را ارسال کنید : "  , self=m.chat)
      try:
       adminAsli = await ReadFileConfig()
       await c.send_message(chat_id=adminAsli['ownerId'],text=f"""
درخواست رفع مسدودیت کاربر با ID : {m.from_user.id}

نام کاربری : @{m.from_user.username}

{answer.text}


""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رفع مسدودیت 🟢",callback_data=f"Requnblock_{m.from_user.id}"),InlineKeyboardButton("رد",callback_data=f"radBlock_{m.from_user.id}")]]))
       admins = await orm.GetAdminList()
       if admins !=None or len(admins) != 0:
          for ad in admins:
            await c.send_message(chat_id=ad[1],text=f"""
درخواست رفع مسدودیت کاربر با ID : {m.from_user.id}

نام کاربری : @{m.from_user.username}

{answer.text}


""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رفع مسدودیت 🟢",callback_data=f"Requnblock_{m.from_user.id}"),InlineKeyboardButton("رد",callback_data=f"radBlock_{m.from_user.id}")]]))
       await orm.UpdateReqBlock(m.from_user.id,1)  
       await m.reply("❤️‍🔥 درخواست ارسال و به زودی مورد بررسی قرار خواهد گرفت ")     
      except:

         pass
     else:
        await m.reply("درخواست قبلی شما در دست بررسی میباشد لطفا صبر کنید ") 

    else:
       await m.reply("کاربر گرامی شما رفع مسدودیت شدید یا مسدود نیستید ! 🟢",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(m.from_user.id),resize_keyboard=True))



@Client.on_message(filters.regex("☎️ پشتیبانی")&  CheckLock & blockCheck & Check_Run) 
async def Suppourt(c:Client,m:Message):
   res =await ReadFileText()
   await m.reply(res['SuppourtMessage'],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🧑🏻‍💻 پشتیبانی مستقیم",url=f"https://t.me/{res['SuppourtId']}")],[InlineKeyboardButton('📨 ارسال تیکت',callback_data='SendTiket')]]))

@Client.on_message(filters.regex("🛍 خرید اشتراک") & CheckLock & blockCheck & Check_Run) 
async def Shop(c:Client,m:Message):
   if await orm.IsShop() == True :
         btns = []
         btnsonline = []
         Setting = await orm.GetSettingTypeShop()
         if Setting[1] == 1:
             btns.append(InlineKeyboardButton("اشتراک معمولی " if Setting[3] == "empty" or Setting[3] == None else  f"{Setting[3]}" ,callback_data="SingleShop"))
         if Setting[0] == 1 :
             btns.append( InlineKeyboardButton("اشتراک ساب "  if Setting[2] == "empty" or Setting[2] == None else  f"{Setting[2]}",callback_data="MultiShop") )
         if  Setting[4] == 1:
             btnsonline.append( InlineKeyboardButton('🌐 | خرید از سایت (تحویل آنی)',url=f"https://xenitgame.com/ping?from=do&userId={m.from_user.id}"))   
         if    btns!= [] :
          finalbtns = [btns]   
          if btnsonline!= []:
              finalbtns = [btns,btnsonline]   
          await m.reply("""🛍 فروش سرویس ها 
                  
🫴🏻 در این بخش  نوع سرویس خود را انتخاب کنید  

🔰 /start              """,reply_markup=InlineKeyboardMarkup(finalbtns))
          return
         else:
              await m.reply("""🔰 این بخش غیر فعال است 
                            
🔰 /start
                    """)   
         return
   else:
              await m.reply("""🔰 این بخش غیر فعال است 
                            
🔰 /start
                    """)   
              return

@Client.on_message(filters.regex("📥 اشتراک های من") & CheckLock & blockCheck & Check_Run) 
async def Service(c:Client,m:Message):
   if await orm.checkServiceBtn('mysub') ==True:
      
      await m.reply("""📥 بخش سرویس من 
                    
🫴🏻تمام سرویس های خود را میتوانید از این لیست ببینید

🔰 /start    """,reply_markup=InlineKeyboardMarkup(await orm.GetServiceList(m.from_user.id)))
   else:
      await m.reply("""این بخش غیر فعال است 
                  
🔰 /start       
                    """)   

@Client.on_message(filters.regex("🌟 تست رایگان") & CheckLock & blockCheck & Check_Run) 
async def FreeTest(c:Client,m:Message):
     if await orm.checkServiceBtn('freetest') ==True:
      
      if await orm.CheckUserFreeUsed(m.from_user.id) == True: 
       
       if await orm.checkTestState() == True:
        await m.reply("⌛️در حال ساخت کانفیگ تست لطفا منتظر بمانید ...")
        result =await orm.GetCofigUserTest(m.from_user.id)
        if result[0] == True:
            await m.reply("""✅ | دریافت تست رایگان انجام شد

⚠️ | لطفا برای دریافت اشتراک خود دکمه زیر را لمس نمایید و سپس کمی صبر کنید تا اشتراک برای شما ارسال شود

🔗 | از طریقی دیگر میتوانید از قسمت اشتراک های من ربات اشتراک خود را دریافت و مشاهده کنید

🔰 /start""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("دریافت",callback_data=f"GETConfig_{result[2]}")]]))   
          
        else:
            await m.reply(result[1])
      
      
       else:
           await m.reply("""در حال حاضر امکان دریافت تست وجود ندارد
                  
🔰 /start       
                    """)   
      else:
            await m.reply("""کاربر گرامی شما قبلا تست رایگان خود را دریافت کردید
                  
🔰 /start       
                    """)   
     else:
              await m.reply("""این بخش غیر فعال است 
                  
🔰 /start       
                    """)   
      
# @Client.on_message(filters.regex("❤️‍🔥❄️ جشنواره دی ماه") & CheckLock & blockCheck) 
# async def DayMonth(c:Client,m:Message):
#    await m.reply("""❤️‍🔥❄️ جشنواره دی ماه

# لیستی از فعال ترین افراد ربات 😄🫴🏻

# شما هم میتونید یکی از انها باشید 😁                                  

# 🔰 /start                  
#                  """,reply_markup=InlineKeyboardMarkup([
#                     [InlineKeyboardButton("🔰 برترین های ما 🔰",callback_data="ARS")],
#                     [InlineKeyboardButton("بیشترین تعداد خرید",callback_data="upCountShoped")],
#                     [InlineKeyboardButton("بیشترین مقدار خرید",callback_data="UpShoped")],
#                     [InlineKeyboardButton("بیشترین دعوت کننده",callback_data="UpInviteUsers")],
#                     [InlineKeyboardButton("بیشترین مصرف کننده",callback_data="UpUseUsers")],
                    
               
#                     ]))
   
      
@Client.on_message(filters.regex("🔄 تمدید سرویس") & CheckLock & blockCheck & Check_Run) 
async def ReNewConfig(c:Client,m:Message):
  if await orm.checkServiceBtn('tamdidbtn') ==True:
   btns =  await orm.GetServiceForExtension(m.from_user.id)
   await m.reply(""" 🔄 تمدید سرویس
                 
🔰 در این بخش میتوانید سرویس های خود را تمدید کنید 
                 
🟣 | /start
""",reply_markup=InlineKeyboardMarkup(btns))
  else:
              await m.reply("""این بخش غیر فعال است 
                  
🔰 /start       
                    """)   
@Client.on_message(filters.regex("🤝 همکاری") & CheckLock & blockCheck & Check_Run) 
async def Cooperation(c:Client,m:Message):
 if await orm.checkServiceBtn('hamkarbtn') ==True:
   await m.reply("""🤝 بخش همکاری خوش آمدید

🔰 در این بخش میتوانید با همکاری کنید                 

🟣 | /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👤 زیر مجموعه گیری",callback_data="collection")],[InlineKeyboardButton("🤝 تخفیف همکاری",callback_data="Cooperationdiscount")],[InlineKeyboardButton("🛍 خرید پنل همکاری",callback_data="buyPanel")],[InlineKeyboardButton("🤖 دریافت ربات اختصاصی",callback_data="buyBot")]]))
 else:
              await m.reply("""این بخش غیر فعال است 
                  
🔰 /start       
                    """)     
              


@Client.on_message(filters.regex("🔍 مشخصات اشتراک") & CheckLock & blockCheck & Check_Run) 
async def GetConfigData(c:Client,m:Message):  
 if await orm.checkServiceBtn('configdata') ==True:
     await orm.ChangeStep(m.from_user.id,'getconfigdata') 
     await m.reply("✍🏻 | .لطفا کانفیگ خود یا UUID را ارسال نمایید ",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
 else:
              await m.reply("""این بخش غیر فعال است 
                  
🔰 /start       
                    """)         