from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup

import httpx
import pyromod
import json
import aiofiles

from service import orm
import datetime
import jdatetime
import qrcode
from io import BytesIO
cancelKey = "انصراف"
Messages =  []


async def ReadFileConfig():
   async with aiofiles.open('Config/Config.json', mode='r',encoding='utf-8') as f: 
      res =   json.loads(await f.read())
   return res   
   
async def ReadFileText():
   async with aiofiles.open('Config/Messages.json', mode='r' , encoding='utf-8') as f: 
 
       return   json.loads(await f.read())
   




async def CheckAdmin(_,c:Client,m:Message):
   Messages = await ReadFileText()
   if await orm.CheckAdmin(m.from_user.id) == True:
      return True
   else: 
      return False
   

async def Canesel_Key(c:Client,m:Message,userid):
     
 Messages =await ReadFileText()
 await orm.ChangeStep(m.from_user.id,"home")

 await m.reply(Messages["start"],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(userid),resize_keyboard=True))


Check_Admin = filters.create(CheckAdmin)


@Client.on_callback_query(Check_Admin)
async def onCallBackAdmin(c:Client,call:CallbackQuery):
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
         orderBtns.append([InlineKeyboardButton("دریافت رایگان",callback_data=f"GetFreeAdmin_{order[1]}")])
         if NewPrice != 0:
             await orm.UpdateorderPrice(order[1],NewPrice)
             await call.edit_message_text(f"""
🎯 | در این بخش شیوه پرداخت خود را انتخاب کنید

🎛 | جزییات سرویس انتخابی :

🧩 | بسته انتخابی : {plan[0]}
💰 | قیمت : {str(plan[3]):,} تومان  ❌
🤝 | قیمت همکاری  : {str(int(NewPrice)):,} ✅ 
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

   if call.data == "buyPanel":
       await call.edit_message_text("برای خرید پنل همکاری به پشتیبانی پیام بدهید",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("پشتیبانی",url="https://t.me/solartm")]]))

   if call.data == "buyBot":
       await call.edit_message_text("برای خرید ربات به پشتیبانی پیام بدهید",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("پشتیبانی",url="https://t.me/solartm")]]))   

   if "deatilApp_" in call.data :
       appId = call.data.split("_")[1]
       app = await orm.GetAppById(appId)
       await call.message.delete()
       if app[5] == "empty":
          await call.message.reply(app[3],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"دانلود {app[1]}",url=app[2])]]))
       else:
          await c.send_cached_media(chat_id=call.from_user.id,file_id=app[5],caption=app[3],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"دانلود {app[1]}",url=app[2])]]))
            
   if call.data == "mainApp":
        await call.edit_message_text("""📲 از لیست زیر سیستم عامل مورد نظر خود را انتخاب کنید
                 
🟣 /start
                 """,reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton("اندروید",callback_data="AndroidApp")],
      [InlineKeyboardButton("ویندوز",callback_data="WindowsApp")],
      [InlineKeyboardButton("IOS",callback_data="IosApp")],
      [InlineKeyboardButton("لینوکس",callback_data="LinuxApp")]
      
      ]))
   if call.data == "AndroidApp":
       btns = await orm.GetAppList('android')
       await call.edit_message_text("""
🔰لیست نرم افزار ها به شرح زیر است لطفا نرم افزار مورد نیاز سیستم عامل خود را انتخاب کنید

🔸پیشنهاد میشود از برنامه های پیشنهادی ما برای اتصال استفاده کنید تا به مشکل نخورید

🔰 /start
""",reply_markup=InlineKeyboardMarkup(btns))
   if call.data == "WindowsApp":
       btns = await orm.GetAppList('Windows')
       await call.edit_message_text("""
🔰لیست نرم افزار ها به شرح زیر است لطفا نرم افزار مورد نیاز سیستم عامل خود را انتخاب کنید

🔸پیشنهاد میشود از برنامه های پیشنهادی ما برای اتصال استفاده کنید تا به مشکل نخورید

🔰 /start
""",reply_markup=InlineKeyboardMarkup(btns))     
   if call.data == "IosApp":
       btns = await orm.GetAppList('IOS')
       await call.edit_message_text("""
🔰لیست نرم افزار ها به شرح زیر است لطفا نرم افزار مورد نیاز سیستم عامل خود را انتخاب کنید

🔸پیشنهاد میشود از برنامه های پیشنهادی ما برای اتصال استفاده کنید تا به مشکل نخورید

🔰 /start
""",reply_markup=InlineKeyboardMarkup(btns))     
   if call.data == "LinuxApp":
       btns = await orm.GetAppList('Linux')
       await call.edit_message_text("""
🔰لیست نرم افزار ها به شرح زیر است لطفا نرم افزار مورد نیاز سیستم عامل خود را انتخاب کنید

🔸پیشنهاد میشود از برنامه های پیشنهادی ما برای اتصال استفاده کنید تا به مشکل نخورید

🔰 /start
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
           await call.message.reply("✅ درخواست برای ادمین اصلی ارسال شد")
           await Canesel_Key(c,call.message,call.from_user.id)
           return
       except:
           await call.message.reply("❌ درخواست برای ادمین اصلی ارسال نشد")
           await Canesel_Key(c,call.message,call.from_user.id)
           return 
   if call.data == "Cooperationdiscount":
       btns = await orm.GetAllBtnsCooperation(call.from_user.id)
       userShop =await orm.GetCountShopUser(call.from_user.id)
       await call.edit_message_text(f"""  🤝 تخفیف همکاری
                                    
 🔰 شما پس از خرید تعداد بالا از ما میتوانید از خدمات همکاری ما استفاده کنید

تعداد خریداری شده : {userShop}                                    
                                    
🔰 /start""",reply_markup=InlineKeyboardMarkup(btns))

   if call.data == "SendTiket":
    await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    answer = await pyromod.Chat.ask(text="🔻 لطفا متن خود را ارسال کنید فرمایید" , self=call.message.chat)
    if answer.text!= "انصراف":
       res = await orm.AddTiket(answer.text,call.from_user.id)
       if res[0] == True:
          try: 
           data = await ReadFileConfig()
           await c.send_message(data['ownerId'],f"""👤 کاربر {call.from_user.username} 
                                
☎️ درخواست تیکت به پشتیبانی ارسال کرده است  
                                
جزییات تیکت : 
{answer.text}
                           
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("پاسخ ✍🏻",callback_data=f"answerTiket_{res[1]}")]]))
           admins = await orm.GetAdminList()
           if admins !=None :
               for admin in admins : 
                     await c.send_message(admin[1],f"""👤 کاربر {call.from_user.username} 
                                
☎️ درخواست تیکت به پشتیبانی ارسال کرده است  
                                
جزییات تیکت : 
{answer.text}
                           
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("پاسخ ✍🏻",callback_data=f"answerTiket_{res[1]}")]]))
           await call.message.reply("✅ تیکت ثبت شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          
           return
          except:
           await call.message.reply("تیکت ثبت نشد ❌",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
           
           return
       else:
           await call.message.reply("تیکت ثبت نشد ❌",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          
           return
    else:
        
        await Canesel_Key(c,call.message,call.from_user.id)
        return

#  NEW Features


   if call.data == "GetInviteLink":
      res = await c.get_me()
      link =  f"https://t.me/{res.username}?start=inv{call.from_user.id}"
      await orm.UpdateInviteLink(f"inv{call.from_user.id}",call.from_user.id)
      await call.message.reply(f"""✅ لینک دعوت ساخته شد 
                                   
لینک دعوت : {link}

🔰 تنها کافیست که کاربر اولین بار با لینک شما ربات را استارت بزند 

🔰 /start
                                   """)
   if  call.data == "mainCooperation":
       if await orm.checkServiceBtn('hamkarbtn') ==True:
            await call.edit_message_text("""🤝 بخش همکاری خوش آمدید

🔰 در این بخش میتوانید با همکاری کنید                 

🟣 | /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👤 زیر مجموعه گیری",callback_data="collection")],[InlineKeyboardButton("🤝 تخفیف همکاری",callback_data="Cooperationdiscount")],[InlineKeyboardButton("🛍 خرید پنل همکاری",callback_data="buyPanel")],[InlineKeyboardButton("🤖 دریافت ربات اختصاصی",callback_data="buyBot")]]))
       else:
              await call.message.reply("""این بخش غیر فعال است 
                  
🔰 /start       
                    """)     
   if call.data == "collection":
       btns = await orm.GetbtnsCollection(call.from_user.id)

       await call.edit_message_text("""👤 زیر مجموعه های شما 
       
اطلاعاتی درباره زیر مجموعه های شما 🔔
       
🟣 | /start
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
   if call.data == "extensionList" :
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
   












   
 #  new option
   if "RejectPerUse_" in call.data :
        userId = call.data.split("_")[1]
        await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بررسی شد !",callback_data="ARS")]]))

        await c.send_message(userId , " درخواست تخفیف همکاری شما توسط ادمین تایید نشد ")

   if "SuccessPerUse_" in call.data :
        userId = call.data.split("_")[2]
        perId = call.data.split("_")[1]
        userId = await orm.UpdatePerUser(userId,perId)
        await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بررسی شد !",callback_data="ARS")]]))
        await c.send_message(userId , "✅ درخواست تخفیف همکاری شما توسط ادمین تایید شد ")
        return
   if "transferWallet" in call.data:
       await call.message.delete()
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا قیمت را ارسال فرمایید" , self=call.message.chat)
       if answer.text != "انصراف":
           try :
               data =int(answer.text)
               if data > 1000:
                   answer = await pyromod.Chat.ask(text="🔻 لطفا شناسه کاربری کاربر مورد نظر  را ارسال فرمایید" , self=call.message.chat)
                   if answer.text != "انصراف":
                     UserId =int(answer.text)
                     
                     res = await orm.TranformData(data,UserId,call.from_user.id)
                     if res[0] == True:
                         await call.message.reply(res[1])
                         return
                     else:
                         await call.message.reply(res[1])    
                         return
                   else:
                     await Canesel_Key(c,call.message,call.from_user.id)
                     return 
               else:
                     await call.message.reply("بزرگ تر از 1000 لطفا فقط عدد")
                     await Canesel_Key(c,call.message,call.from_user.id)
                     return
           except:
               await call.message.reply("لطفا فقط عدد")
               await Canesel_Key(c,call.message,call.from_user.id)
               return
       else:
               await Canesel_Key(c,call.message,call.from_user.id)
               return
   if "WithCodeDis_" in call.data:
       orderId = call.data.split("_")[1]
       
       await call.message.delete()
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا کد تخفیف را ارسال فرمایید" , self=call.message.chat)
       if answer.text!= "انصراف":
           dis = await orm.GetdisCountWithCode(answer.text,orderId,call.from_user.id)
           if dis[0] == True:
                result = await orm.PlanidGetDiscountOrderDetails(orderId)
                plan = await orm.GetPlanById(result)
                orderBtns = await orm.GetBtnsSheldIScOUNT(orderId,plan[9])
                
                orderBtns.append([InlineKeyboardButton("دریافت رایگان",callback_data=f"GetFreeAdmin_{orderId}")])

                await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                await call.message.reply(f"""🎯 | در این بخش شیوه پرداخت خود را انتخاب کنید
                  
❤️‍🔥 | کد تخفیف تایید شد قیمت با تخفیف را واریز کنید                                             


🎛 | جزییات سرویس انتخابی :

🧩 | بسته انتخابی : {plan[0]}
💰 | قیمت : {str(plan[3])} تومان  ❌
🔥 | قیمت با تخفیف  : {dis[2]} ✅ 
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
                   await call.message.reply(dis[1])
                   return
       else:
          await Canesel_Key(c,call.message,call.from_user.id)
          return
   if "getOrder_" in call.data:
      data = call.data.split("_")[1]
      CatId = call.data.split("_")[2]
      plan = await orm.GetPlanById(data)

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
         orderBtns.append([InlineKeyboardButton("دریافت رایگان",callback_data=f"GetFreeAdmin_{order[1]}")])
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

   if  "payOnline_" in call.data :
       orderId = call.data.split("_")[1]
       text =await orm.GetTextAlertOnline()
       btns = await orm.GetOnlinePayBtns(orderId)
       await call.message.delete()
       await call.message.reply(text,reply_markup=InlineKeyboardMarkup(btns))
       return

   if "planshop_" in call.data:
      
      data = call.data.split("_")[1]
      await call.edit_message_text("""🛍 فروش سرویس ها 
                  
🫴🏻  در این بخش پلن خود را انتخاب کنید  

🔰  /start
""",reply_markup=InlineKeyboardMarkup(await orm.GetPlanCatShell(data)))
      return
   if "CardToCard_" in call.data:
       data = call.data.split("_")[1]
       orderPrice = await orm.GetdataPriceOrder(data)
       res  = await orm.GetDataForCardToCard()
       await call.answer(res[2],True)
       try:
        await call.message.delete()
        answer = await pyromod.Chat.ask(text=f"""🔰 | لطفا ابتدا به این شماره کارت مبلغ را واریز کنید 
  
🔔 | دقت کنید بعد از پرداخت لطفا رسید خود را برای بات ارسال کنید سپس بعد از تایید ادمین سرویس برای شما ارسال خواهد شد   

{f"💰 | قیمت : {orderPrice[0]}" if orderPrice[1] == 0 else f"💰 | قیمت : {orderPrice[2]}"} 

💳 | شمارت کارت : {res[1]}  

👤 | نام : {res[0]} 

.
                                       """ , self=call.message.chat)
        
        dataConfig =await ReadFileConfig()
        if   orderPrice[3] == "BuySingle" :
            
             await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=answer.photo.file_id,caption=f"""🛍 خرید سرویس 
                                       
                                   
💳نوع خرید : کارت به کارت 
✍🏻 نام کاربر : {call.from_user.first_name}                                
👤 نام کاربری : @{call.from_user.username}                                  
👤 ای دی عددی : <code>{call.from_user.id}</code>        
💰 قیمت : {orderPrice[0]} تومان                  
☝🏻 خرید کانفیگ تکی 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {orderPrice[2]} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
        if   orderPrice[3] == "BuySub" :
            
             await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=answer.photo.file_id,caption=f"""🛍 خرید سرویس 
                                       
                            
💳نوع خرید : کارت به کارت 
✍🏻 نام کاربر : {call.from_user.first_name}                                
👤 نام کاربری : @{call.from_user.username}                                  
👤 ای دی عددی : <code>{call.from_user.id}</code>        
💰 قیمت : {orderPrice[0]} تومان                  
🌐 خرید کانفیگ ساب 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {orderPrice[2]} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                      
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
               
        elif orderPrice[3] == "AddWallet" :      
                  await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=answer.photo.file_id,caption=f"""💰 شارژ کیف پول 
                                       
                              
💳نوع خرید : کارت به کارت 
✍🏻 نام کاربر : {call.from_user.first_name}                                
👤 نام کاربری : @{call.from_user.username}                                  
👤 ای دی عددی : <code>{call.from_user.id}</code>        
💰 قیمت : {orderPrice[0]} تومان                    
 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {orderPrice[2]} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
                  
        await call.message.reply("درخواست شما برای ادمین ارسال شد 🔰")
        return
        
       except:
         try:  
           await call.message.reply("🙏🏻 لطفا عکس ارسال کنید")
           answer = await pyromod.Chat.ask(text=f"""🔰 | لطفا ابتدا به این شماره کارت مبلغ را واریز کنید 
  
🔔 | دقت کنید بعد از پرداخت لطفا رسید خود را برای بات ارسال کنید سپس بعد از تایید ادمین سرویس برای شما ارسال خواهد شد   

{f"💰 | قیمت : {orderPrice[0]}" if orderPrice[1] == 0 else f"💰 | قیمت : {orderPrice[2]}"} 

💳 | شمارت کارت : {res[1]}  

👤 | نام : {res[0]} 

.
                                       """ , self=call.message.chat)
           
           dataConfig =await ReadFileConfig()
           
           if   orderPrice[3] == "BuySub" :
            
             await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=answer.photo.file_id,caption=f"""🛍 خرید سرویس 
                                       
                                   
💳نوع خرید : کارت به کارت 
نام کاربر : {call.from_user.first_name}                                
نام کاربری : {call.from_user.username}                                  
 ای دی عددی : {call.from_user.id}        
 قیمت : {str(orderPrice[0]):,} تومان                  
 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {str(orderPrice[2]):,} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
   
           elif orderPrice[3] == "AddWallet" :      
                  await c.send_cached_media(chat_id=dataConfig['ownerId'],file_id=answer.photo.file_id,caption=f"""💰 شارژ کیف پول 
                                       
                                   
💳نوع خرید : کارت به کارت 
نام کاربر : {call.from_user.first_name}                                
نام کاربری : {call.from_user.username}                                  
ای دی عددی : {call.from_user.id}        
قیمت : {str(orderPrice[0]):,} تومان                  
 
{f" از تخفیف استفاده شده  قیمت جدید 🫴🏻  {orderPrice[2]} " if orderPrice[1] != 0 else  "" }

🔰 /start                                 
                                  
                                  """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"SuccessCard_{data}"),InlineKeyboardButton("❌ رد کردن ",callback_data=f"aboveCard_{data}")]]))
           return
         except:
            
            await call.message.reply_video("https://media.giphy.com/media/edckP6sD9YyYxuQYpS/giphy.gif",caption="/:") 
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
⏰ | مقدار زمان : { f'{toEnd} روز ' if toEnd.isnumeric() == True else toEnd }

🔗 | کانفیگ شما :

<code>{res[2]['subscribe_url']}</code>

{f"🌐 | ادرس اتصال ساب : <code>{res[2]['subsingle']}</code>" if res[2]['subsingle'] != "" else "" }

⚠️ | آموزش اتصال در ربات می‌باشد
"""


          await call.message.reply_photo(photo=qr_stream,caption=mes,reply_markup=InlineKeyboardMarkup(
              [
                  [InlineKeyboardButton("🟢" if res[2]['state'] == 1 else "🔴",callback_data="ARS"),InlineKeyboardButton("🔔 وضعیت",callback_data="ARS")],

                  [InlineKeyboardButton(total,callback_data="ARS"),InlineKeyboardButton("🔋 حجم کل",callback_data="ARS")],
                  [InlineKeyboardButton(round(used,2),callback_data="ARS"),InlineKeyboardButton("🪫 مصرفی حجم  ",callback_data="ARS")],
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
✅ | اشتراک با موفقیت تغییر کرد
👤 | نام اشتراک : {res[3]}
📊 | مقدار حجم : {total} GB
⏰ | مقدار زمان : {toEnd} روز

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
       answer = await pyromod.Chat.ask(text="🔻(بیشتر از 10000 تومان) لطفا قیمت را حتما به عدد وارد کنید"  , self=call.message.chat)

       if answer.text!= "انصراف":
        try: 
          res =  int(answer.text)
          if res > 10000:
              result = await orm.CreateOrder(call.from_user.id,0,0,res,"AddWallet",0,0)
              if result[0] == True:
                  orderBtns = await orm.GetBtnsShellWallet(result[1])
                  await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

                  await call.message.reply(f"""💰 | شارژ کیف پول 
                  
🫴🏻 | در این بخش شیوه پرداخت خود را انتخاب کنید  

🫴🏻 | جزییات پرداخت 

افزایش کیف پول به مبلغ {res}  تومان                                 

🔰 /start
""",reply_markup=InlineKeyboardMarkup(orderBtns))
              else:
                 await call.answer("فاکتور ساخته نشد...") 
                 await Canesel_Key(c,call.message,call.from_user.id)

                 return
          else:
            await call.message.reply("🤖 لطفا فقط بیشتر از 10000 تومان ارسال کنید ")  
            await Canesel_Key(c,call.message,call.from_user.id)
            return 
        except:
            await call.message.reply("🤖 لطفا فقط عدد ارسال کنید ")  
            await Canesel_Key(c,call.message,call.from_user.id)
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
           await call.answer("اعتبار کیف پول شما کافی نیست 💰 ",True)    
           return
      
      
 #  just fro ADMINS
   if "GetFreeAdmin_" in call.data:
          orderId = call.data.split("_")[1]
          result = await orm.CreateSub(orderId,c,1)
          if result[0] == True:
             await call.message.reply("""✅ | خرید شما با موفقیت انجام شد 

⚠️ | لطفا برای دریافت اشتراک خود دکمه زیر را لمس نمایید و سپس کمی صبر کنید تا اشتراک برای شما ارسال شود

🔗 | از طریقی دیگر میتوانید از قسمت اشتراک های من ربات اشتراک خود را دریافت و مشاهده کنید

🔰 /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton( "دریافت",callback_data= f"GETConfig_{result[2]}")]]))
            #  await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بررسی شده !",callback_data="ARS")]]))

             await call.answer(result[1])
          else:
            await call.answer(result[1])
   if "aboveCard_" in call.data :
       orderId = call.data.split("_")[1]
        
       OrderCheck =  await orm.checkOrderCard(orderId)
       if OrderCheck[0] == True:
        await call.message.reply("⏳",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))    
        answer = await pyromod.Chat.ask(call.message.chat,"♦️ لطفا دلیل را ارسال نمایید")
        if answer.text != "انصراف":
           userId= await orm.GetUserIdByOrderId(orderId)
           await orm.UpdayeOrderReject(orderId)
           await c.send_message(userId ,f"""❌ | کاربر گرامی درخواست خرید شما رد شد 
علت : 
                                
{answer.text}
           
""" )
           await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بررسی شده !",callback_data="ARS")]]))
           await call.message.reply("دلیل رد برای کاربر ارسال شد ")
        else:
             await Canesel_Key(c,call.message,call.from_user.id)
             return    
       else:
         await call.answer("✅ | توسط ادمین دیگری این درخواست قبلا تایید یا رد شده",True)   
         await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بررسی شده !",callback_data="ARS")]]))
           
   if "DeleteDisCo_" in call.data:
        disId = call.data.split("_")[1]
        await call.message.delete()    
        await orm.DeleteDisCo(disId) 
        await call.message.reply("حذف موفقیت آمیز بود")

   if "EditCountDisCo_" in call.data :
          disId = call.data.split("_")[1]
          await call.message.reply("⏳",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))    
          answer = await pyromod.Chat.ask(call.message.chat,"♦️ لطفا تعداد جدید را ارسال نمایید")
          if answer.text != "انصراف":
              await orm.UpdateCountDisCo(disId,answer.text)
              await call.message.reply("✅ | با موفقیت ویرایش شد ")
              await Canesel_Key(c,call.message,call.from_user.id)
              return      
          else:    
                await Canesel_Key(c,call.message,call.from_user.id)
                return                   
   if "EditPerDisCo_" in call.data :
          disId = call.data.split("_")[1]
          await call.message.reply("⏳",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))    
          answer = await pyromod.Chat.ask(call.message.chat,"♦️ لطفا درصد را ارسال نمایید")
          if answer.text != "انصراف":
              await orm.UpdatePerDisCo(disId,answer.text)
              await call.message.reply("✅ با موفقیت ویرایش شد ")
              await Canesel_Key(c,call.message,call.from_user.id)
              return      
          else:    
                await Canesel_Key(c,call.message,call.from_user.id)
                return           
   if "DisCountper_" in call.data :
         disId = call.data.split("_")[1]
         btns = await orm.GetCooperationDiscount(disId) 
         await call.edit_message_text("""🫂 ویرایش تخفیف همکار 
                                      
💰 تخفیف خود را مدیریت کنید !
                                      """,reply_markup=InlineKeyboardMarkup(btns))
   if call.data == "AddPersentDis":
          await call.message.reply("⏳",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))    
          answer = await pyromod.Chat.ask(call.message.chat,"♦️ لطفا درصد را ارسال نمایید")
          if answer.text != "انصراف":
             try: 
              percent = int(answer.text)
              answer = await pyromod.Chat.ask(call.message.chat,"♦️ لطفا تعداد کانفیگ لازم را ارسال نمایید")
              if answer.text != "انصراف":
                     Count = int(answer.text)
                     await orm.AddNewPercentDis(percent , Count )
                     await call.message.reply("✅ با موفقیت اضافه شد ")
                     await Canesel_Key(c,call.message,call.from_user.id)
                     return      
              else:
                     await Canesel_Key(c,call.message,call.from_user.id)
                     return           
             except:
                     await call.message.reply("لطفا فقط عدد وارد کنید")
                     await Canesel_Key(c,call.message,call.from_user.id)
                     return  
          else:
                     await Canesel_Key(c,call.message,call.from_user.id)
                     return     

   if  call.data =="ManagePercent":
       btns = await orm.GetBtnsPercent()
       await call.edit_message_text("""⚙️ مدیریت درصد ها 
در این قسمت تخفیف همکار ها را ویرایش کنید
""",reply_markup=InlineKeyboardMarkup(btns))        
       return
   if "answerTiket_" in call.data:
            tiketId = call.data.split("_")[1]
            if await orm.CheckTiket(tiketId) == True:
                await call.message.reply("⏳",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))    
                answer = await pyromod.Chat.ask(call.message.chat,"♦️ لطفا پاسخ خود را ارسال نمایید")
                if answer.text != "انصراف":
                 data =  await orm.GetTiketById(tiketId)
                 await c.send_message(data[2],f"""
پاسخ ادمین به تیکت شما : 
                                      
{answer.text}                                      
                 
  """)
                 await orm.UpdateTiket(tiketId)
                 await call.message.reply("✅ پاسخ ارسال شد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

                else:
                     await Canesel_Key(c,call.message,call.from_user.id)
                     return


            else:
             await call.answer("✅ درخواست قبلا بررسی شده توسط ادمین دیگری",True)
             await  call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("! بررسی شده",callback_data="ARS")]]))       
             return   
   if "Requnblock_" in call.data:
        userId = call.data.split("_")[1]
        if  await orm.CheckReqUnblock(userId) != True:
            await orm.UnblockUser(userId)
            await  call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("! بررسی شده",callback_data="ARS")]]))    
            return
        else:
            await call.answer("✅ درخواست قبلا بررسی شده توسط ادمین دیگری",True)
            await  call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("! بررسی شده",callback_data="ARS")]]))       
            return   
   if "radBlock_" in call.data  :
        userId = call.data.split("_")[1]
        if  await orm.CheckReqUnblock(userId) != True:
            await orm.UpdateReqBlock(userId,0)
            await call.answer(" درخواست رد شد ",True)
            await  call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("! بررسی شده",callback_data="ARS")]]))    
            return
        else:
            await call.answer("✅ درخواست قبلا بررسی شده توسط ادمین دیگری",True)
            await  call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("! بررسی شده",callback_data="ARS")]]))    
            return
   if "SuccessCard_" in call.data :
      orderId = call.data.split("_")[1]
      OrderCheck =  await orm.checkOrderCard(orderId)
      if OrderCheck[0] == True:
         if OrderCheck[1] == "BuySub" or OrderCheck[1] == "BuySingle":
             
          result = await orm.CreateSub(orderId,c)
          if result[0] == True:
             await c.send_message(chat_id=result[3],text ="""✅ | خرید شما با موفقیت انجام شد 

⚠️ | لطفا برای دریافت اشتراک خود دکمه زیر را لمس نمایید و سپس کمی صبر کنید تا اشتراک برای شما ارسال شود

🔗 | از طریقی دیگر میتوانید از قسمت اشتراک های من ربات اشتراک خود را دریافت و مشاهده کنید

🔰 /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton( "دریافت اشتراک",callback_data= f"GETConfig_{result[2]}")]]))
             await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بررسی شده !",callback_data="ARS")]]))

             await call.answer(result[1])
          else:
            await call.answer(result[1])
         
         elif OrderCheck[1] == "AddWallet":
             ReturnData = await orm.SuccessWallet(orderId)
             if ReturnData[0] == True:
                 await c.send_message(chat_id=ReturnData[2],text=ReturnData[1])
             else:
                 await call.message.reply(ReturnData[1])    
      else:
         await call.answer("✅توسط ادمین دیگری این درخواست قبلا تایید یا رد شده",True)   
         await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بررسی شده !",callback_data="ARS")]]))
   if  "EditCodeManual_" in call.data :
     discountId = call.data.split("_")[1]
     await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
     anwser = await pyromod.Chat.ask(text="🔻 لطفا کد تخفیف را ارسال فرمایید", self=call.message.chat)
     if anwser.text!= "انصراف":
         await orm.UpdateCodeDiscountManual(discountId,anwser.text)
         await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
     else:
              await Canesel_Key(c,call.message,call.from_user.id)
              return
   if "EditDis_" in call.data:
       disId = call.data.split("_")[1]
       btns = await orm.GetDisBtns(disId)
       await call.edit_message_text("ویرایش کد تخفیف موجود",reply_markup=InlineKeyboardMarkup(btns))
   if call.data == "manageOffer":
        btns = await orm.GetAllDiscountBtn()
        await call.edit_message_text("به بخش مدیریت کد ها تخفیف خوش آمدید \n کد تخفیف خود را انتخاب کنید",
                                    reply_markup=InlineKeyboardMarkup(btns))
   if call.data =="SendAlertTimeFirst":
        await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
        anwser = await pyromod.Chat.ask(text="🔻 صفر خاموش است (فقط عدد) لطفا مقدار جدید خود را ارسال فرمایید" , self=call.message.chat)
        if anwser.text!= "انصراف":

          try:  
            await orm.UpdateSettingAlert("SendAlertTimeFirst",int(anwser.text))
            res=  await  orm.GetSettingBtns()
            await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

            await call.message.reply("🔻 به بخش مدیریت ربات خوش امدید\n\nتنظیمات دلخواه خود را اعمال کنید",reply_markup=InlineKeyboardMarkup(res))
            return
          except:
              await call.message.reply("لطفا فقط عدد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(),resize_keyboard=True)) 
              return
        else:
             await Canesel_Key(c,call.message,call.from_user.id)
             return
   if call.data =="SendAlertTimeTwo":
        await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
        anwser = await pyromod.Chat.ask(text="🔻 صفر خاموش است (فقط عدد) لطفا مقدار جدید خود را ارسال فرمایید" , self=call.message.chat)
        if anwser.text!= "انصراف" : 

          try:  
            if   int(anwser.text) >= 0 :
             await orm.UpdateSettingAlert("SendAlertTimeTwo",int(anwser.text))
             res=  await  orm.GetSettingBtns()
             await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

             await call.message.reply("🔻 به بخش مدیریت ربات خوش امدید\n\nتنظیمات دلخواه خود را اعمال کنید",reply_markup=InlineKeyboardMarkup(res))
             return
            else:
              await call.message.reply("بزرگتر از صفر لطفا فقط عدد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(),resize_keyboard=True)) 
              return

          except:
              await call.message.reply("لطفا فقط عدد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(),resize_keyboard=True)) 
              return
        else:
             await Canesel_Key(c,call.message,call.from_user.id)
             return     
   if call.data =="SendAlertVolumeFirst":
        await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
        anwser = await pyromod.Chat.ask(text="🔻صفر خاموش است  (فقط عدد) لطفا مقدار جدید خود را ارسال فرمایید" , self=call.message.chat)
        if anwser.text!= "انصراف"  and int(anwser.text) > 0:

          try:  
           if   int(anwser.text) >= 0 :
             await orm.UpdateSettingAlert("SendAlertVolumeFirst",int(anwser.text))
             res=  await  orm.GetSettingBtns()
             await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

             await call.message.reply("🔻 به بخش مدیریت ربات خوش امدید\n\nتنظیمات دلخواه خود را اعمال کنید",reply_markup=InlineKeyboardMarkup(res))
             return
           else:
              await call.message.reply("بزرگتر از صفر لطفا فقط عدد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(),resize_keyboard=True)) 
              return
          except:
              await call.message.reply("لطفا فقط عدد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(),resize_keyboard=True)) 
              return
        else:
             await Canesel_Key(c,call.message,call.from_user.id)
             return             
  
  
   if call.data =="SendAlertVolumeTwo":
        await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
        anwser = await pyromod.Chat.ask(text="🔻صفر خاموش است  (فقط عدد) لطفا مقدار جدید خود را ارسال فرمایید" , self=call.message.chat)
        if anwser.text!= "انصراف" and int(anwser.text) > 0:
             
          try:  
           if   int(anwser.text) >= 0 :
             await orm.UpdateSettingAlert("SendAlertVolumeTwo",int(anwser.text))
             res=  await  orm.GetSettingBtns()
             await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

             await call.message.reply("🔻 به بخش مدیریت ربات خوش امدید\n\nتنظیمات دلخواه خود را اعمال کنید",reply_markup=InlineKeyboardMarkup(res))
             return
           else:
              await call.message.reply("بزرگتر از صفر لطفا فقط عدد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(),resize_keyboard=True)) 
              return
          except:
              await call.message.reply("لطفا فقط عدد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(),resize_keyboard=True)) 
              return
        else:
             await Canesel_Key(c,call.message,call.from_user.id)
             return             
  
   if "StartAfterUse_" in call.data:
        state = call.data.split("_")[1]
        if state == '1':
            await orm.UpdateStateStartAfterUse(0)
        else:
            await orm.UpdateStateStartAfterUse(1)

        res=  await  orm.GetSettingBtns()
        await call.message.delete()
        await call.message.reply("🔻 به بخش مدیریت ربات خوش امدید\n\nتنظیمات دلخواه خود را اعمال کنید",reply_markup=InlineKeyboardMarkup(res))
        return
   if  "SendPhotoWithStartBot_" in call.data:
       sendPhototState = call.data.split("_")[1]
  
       if sendPhototState == '1' :
           await orm.UpdateSettingPhotoStart(0,"empty")
           res=  await  orm.GetSettingBtns()
           await call.message.delete()
           await call.message.reply("🔻 به بخش مدیریت ربات خوش امدید\n\nتنظیمات دلخواه خود را اعمال کنید",reply_markup=InlineKeyboardMarkup(res))

           return
       else:
               
        await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
        anwser = await pyromod.Chat.ask(text="🔻 لطفا تصویر خود را ارسال فرمایید" , self=call.message.chat)
        if anwser.text!= "انصراف":
            await orm.UpdateSettingPhotoStart(1,anwser.photo.file_id)
            res=  await  orm.GetSettingBtns()
            await call.message.reply("✅ ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

            await call.message.reply("🔻 به بخش مدیریت ربات خوش امدید\n\nتنظیمات دلخواه خود را اعمال کنید",reply_markup=InlineKeyboardMarkup(res))

        else:
             await Canesel_Key(c,call.message,call.from_user.id)
             return
   if call.data == "EditDomainConfig":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       anwser = await pyromod.Chat.ask(text="🔻 لطفا  دامنه جدید خود را ارسال فرمایید" , self=call.message.chat)
       if anwser.text!= "انصراف":
            await orm.UpdateDomainConfig(anwser.text)
            await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
       else:
         await Canesel_Key(c,call.message,call.from_user.id)
         return    
   if call.data == "ChangePGMad":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       anwser = await pyromod.Chat.ask(text="🔻 لطفا توکن درگاه MadPal خود را ارسال فرمایید" , self=call.message.chat)
       if anwser.text!= "انصراف":
            await orm.UpdatePaymentGatewayMad(anwser.text)
            await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
       else:
         await Canesel_Key(c,call.message,call.from_user.id)
         return        
   if call.data == "ChangePG":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       anwser = await pyromod.Chat.ask(text="🔻 لطفا توکن درگاه خود را ارسال فرمایید" , self=call.message.chat)
       if anwser.text!= "انصراف":
            await orm.UpdatePaymentGateway(anwser.text)
            await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
       else:
         await Canesel_Key(c,call.message,call.from_user.id)
         return
   if "AddDis" == call.data:     
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       anwser = await pyromod.Chat.ask(text="🔻 لطفا درصد تخفیف را ارسال فرمایید" , self=call.message.chat)
       if anwser.text!= "انصراف":
           percent = 0
           try:
               percent = int(anwser.text)
           except:    
             await call.message.reply("لطفا فقط عدد")
             await Canesel_Key(c,call.message,call.from_user.id)
             return
           anwser = await pyromod.Chat.ask(text="🔻 لطفا تعداد تخفیف را ارسال فرمایید" , self=call.message.chat)
           if anwser.text!= "انصراف":
              count = 0 
              try:
                 count = int(anwser.text)
              except:    
                 await call.message.reply("لطفا فقط عدد")
                 await Canesel_Key(c,call.message,call.from_user.id)
                 return
              anwser = await pyromod.Chat.ask(text="🔻 لطفا تعداد خرید تخفیف برای هر کاربر را ارسال فرمایید" , self=call.message.chat)
              if anwser.text!= "انصراف":   
                   canUse = 0 
                   try:
                      canUse = int(anwser.text)
                   except:    
                      await call.message.reply("لطفا فقط عدد")
                      await Canesel_Key(c,call.message,call.from_user.id)
                      return
                   anwser = await pyromod.Chat.ask(text="🔻 لطفا تعداد روز تخفیف را ارسال فرمایید" , self=call.message.chat)
                   if anwser.text!= "انصراف":   
                        days = 0
                        try:
                            days = int(anwser.text)
                            res = await orm.AddDisCount(percent,count,canUse,days)
                            if res[0] == True:
                                await call.message.reply("✅ با موفقیت اضافه شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
                                btns = await orm.GetDisBtns(res[1])
                                await call.message.reply(f" <code>{res[2]}</code> ویرایش کد تخفیف موجود",reply_markup=InlineKeyboardMarkup(btns))

                            else:
                                await call.message.reply("❌ هنگام اضافه کردن مشکلی پیش آمد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
                                return
                                
                                   
                        except:
                          await call.message.reply("لطفا فقط عدد")
                          await Canesel_Key(c,call.message,call.from_user.id)
                          return
                   else:
                          await Canesel_Key(c,call.message,call.from_user.id)
                          return
              else:
                          await Canesel_Key(c,call.message,call.from_user.id)
                          return
           else:
                          await Canesel_Key(c,call.message,call.from_user.id)
                          return
       else:
                          await Canesel_Key(c,call.message,call.from_user.id)
                          return
   if "EditCountDis_" in call.data:
       disId = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا  تعداد جدید را ارسال فرمایید" , self=call.message.chat)
       if answer.text!= "انصراف":
        countNew = 0
        try:
           countNew = int(answer.text)
        except:
               await call.message.reply("لطفا فقط عدد وارد کنید",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
               return
        await orm.EditCountDsicount(disId,countNew)
        btns = await orm.GetDisBtns(disId)
        dis = await orm.GetDiscountCode(disId)
        await call.message.reply("✅ ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

        await call.message.reply(f"<code>{dis}</code> ویرایش کد تخفیف موجود",reply_markup=InlineKeyboardMarkup(btns))   
       else:
                 
          await Canesel_Key(c,call.message,call.from_user.id)
          return
   if  "EditCanUserDis_" in call.data:
       disId = call.data.split("_")[1]

       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا  تعداد جدید کاربر را ارسال فرمایید" , self=call.message.chat)
       if answer.text!= "انصراف":
        countNewUser = 0
        try:
           countNewUser = int(answer.text)
        except:
               await call.message.reply("لطفا فقط عدد وارد کنید",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
               return
        dis = await orm.GetDiscountCode(disId)
        
        await orm.EditCountUserDsicount(disId,countNewUser)
        btns = await orm.GetDisBtns(disId)
        await call.message.reply("✅ ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

        await call.message.reply(f"<code>{dis}</code> ویرایش کد تخفیف موجود",reply_markup=InlineKeyboardMarkup(btns))   
       else:
                 
          await Canesel_Key(c,call.message,call.from_user.id)
          return   
       
   if "EditDateDis_" in call.data:
       disId = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا زمان جدید را وارد کنید زمان شروع زمان اضافه شدن است و این زمان جهت تمدید است" , self=call.message.chat)
       if answer.text!= "انصراف":
        DaysNew = 0
        try:
           DaysNew = int(answer.text)
        except:
               await call.message.reply("لطفا فقط عدد وارد کنید",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
               return
        await orm.EditDaysDsicount(disId,DaysNew)
        btns = await orm.GetDisBtns(disId)
        dis = await orm.GetDiscountCode(disId)
        await call.message.reply("✅ ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

        await call.message.reply(f"<code>{dis}</code> ویرایش کد تخفیف موجود",reply_markup=InlineKeyboardMarkup(btns))   
       else:
                 
          await Canesel_Key(c,call.message,call.from_user.id)
          return
   if "EditPercentDis_" in call.data:
       disId = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا درصد جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
        Percent = 0
        try:
           Percent = int(answer.text)
        except:
               await call.message.reply("لطفا فقط عدد وارد کنید",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
               return
        await orm.EditPercentDsicount(disId,Percent)
        btns = await orm.GetDisBtns(disId)
        dis = await orm.GetDiscountCode(disId)
        await call.message.reply("✅ ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

        await call.message.reply(f"<code>{dis}</code> ویرایش کد تخفیف موجود",reply_markup=InlineKeyboardMarkup(btns))   
        
       else:
                 
          await Canesel_Key(c,call.message,call.from_user.id)
          return
   if "DeletePlan_" in call.data:
      data = call.data.split("_")[1]
      await orm.DeletePlan(data)
      await call.message.delete()
      await call.message.reply("✅ حذف موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

   if "EditStateDis_" in call.data:
       data = call.data.split("_")
       if data[2] == '0':
           await orm.EditStatusDiscount(data[1],1)
       else:
           await orm.EditStatusDiscount(data[1],0)
               
       dis =  await orm.GetDiscountCode(data[1])
       await call.message.delete()
       btns = await orm.GetDisBtns(data[1])
       await call.message.reply(f"<code>{dis}</code> ویرایش کد تخفیف موجود",reply_markup=InlineKeyboardMarkup(btns)) 
   if "EditCode_" in call.data:
       disId = call.data.split("_")[1]
       dis =  await orm.UpdateDisCode(disId)
       await call.message.delete()
       btns = await orm.GetDisBtns(disId)
       await call.message.reply(f"<code>{dis}</code> ویرایش کد تخفیف موجود",reply_markup=InlineKeyboardMarkup(btns))   
   if call.data == "mainAdmin":
      Messages =await ReadFileText()
      await call.edit_message_text(text=Messages['manageadmin'],
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
      return
   if call.data == "disableserviceManual":
             
       await call.message.reply("""فرایند غیرفعال سازی کاربرانی که بیشتر مصرف میکنند اغاز شد   

این فرایند باعث کاهش سرعت بات خواهد بود
                                
                                """)
   
       await orm.CheckUserServiceEnd(c)
      
           
       await call.message.reply(" پایان ")
   if  call.data ==  "ManageService" :
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       uuid = ""
       answer = await pyromod.Chat.ask(text="🙏🏻 | لطفا سرویس مورد نظر را ارسال کنید" , self=call.message.chat)
       if answer.text != "انصراف":
           Service = await orm.SearchConfigUser(answer.text)
           if Service[0] ==True :
               await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
               date =  datetime.datetime.fromtimestamp(Service[1][7]/1000)
               shamsi = jdatetime.datetime.fromgregorian(date =date)
               username = await orm.GetUserNameByUserId(Service[1][1])
               usernamedef = "دریافت نشد"
               if username != None :
                   usernamedef= username[0]
                   
                   
               await call.message.reply(f"""✅ | جزییات سرویس یافت شده 
                                        
🔰 | نوع : {'ساب' if Service[1][24] == "sub" else 'معمولی'}
👾 | نام : {Service[1][3]}
🔋 | حجم : {round((Service[1][18] / 1024 /1024 /1024),2)} GB
🚀 | حجم مصرفی : {round((Service[1][14] / 1024 /1024 /1024),2)} GB
📆 | تاریخ : {str(shamsi)} 
💠 | وضعیت : {'غیرفعال' if Service[1][16] == 0 else 'فعال'}
👤 | مالک : <code>{Service[1][1]}</code>
👤 | نام مالک : @{usernamedef}

⚠️ | برای انجام تغییرات یکی از گزینه های زیر را انتخاب کنید

.
                                        
                                        """,reply_markup=InlineKeyboardMarkup([
                                            
                                                                               [InlineKeyboardButton("ویرایش حجم ✍🏻" ,callback_data=f"EditVolumeConfigUser_{Service[1][0]}"),InlineKeyboardButton("تعویض لینک 🔁" ,callback_data=f"Changelink_{Service[1][0]}")],                                                                               
                                                                               [InlineKeyboardButton("کاهش روز ➖" ,callback_data=f"MDConfigUser_{Service[1][0]}"),InlineKeyboardButton("➕ افزودن روز" ,callback_data=f"ADConfigUser_{Service[1][0]}")],
                                                                               [InlineKeyboardButton(" فعال کردن 🟢" ,callback_data=f"EnableConfigUser_{Service[1][0]}"),InlineKeyboardButton("غیرفعال کردن 🔴" ,callback_data=f"DisableConfigUser_{Service[1][0]}")],
                                                                               [InlineKeyboardButton("حذف ❌" ,callback_data=f"DeleteConfigUser_{Service[1][0]}")]
                                                                               
                                                                               ]) )
           else:    
               await call.message.reply("🫗🫗 | ادمین گرامی سرویس شما یافت نشد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
       else:
                       await Canesel_Key(c,call.message,call.from_user.id)
                       return   
   if "ADConfigUser_" in call.data:
         serviceId = call.data.split("_")[1]
         await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
         
         answer = await pyromod.Chat.ask(text="""🙏🏻 | لطفا روز سرویس مورد نظر را ارسال کنید
                                         
⚠️ | به تاریخ انقضا حال اضافه خواهد شد
.
                                         """ , self=call.message.chat)
         if answer.text != "انصراف":
            days = 0
            try:
                days = int( answer.text) 
            except:
               await call.message.reply("🙏🏻 | لطفا فقط عدد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
               return     
           
            res =  await orm.EditDateConfig(serviceId,c,days,True)  
          
            if res ==True :
                
             await call.message.delete()     
           
               
             await call.message.reply("✅ زمان ویرایش شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
             await orm.mainManageService(serviceId,call)
             return
                    
            else :
                 await call.message.reply("هنگام ویرایش مشکلی پیش آمد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
                 return       
         else:
                       await Canesel_Key(c,call.message,call.from_user.id)
                       return  
  
   if "MDConfigUser_" in call.data:
         serviceId = call.data.split("_")[1]
         await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
         
         answer = await pyromod.Chat.ask(text="""🙏🏻 | لطفا روز سرویس مورد نظر را ارسال کنید
                                         
⚠️ | از تاریخ انقضا حال کم خواهد شد
.
                                         """ , self=call.message.chat)
         if answer.text != "انصراف":
            days = 0
            try:
                days = int( answer.text) 
            except:
               await call.message.reply("🙏🏻 | لطفا فقط عدد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
               return     
           
            res =  await orm.EditDateConfig(serviceId,c,days,False)  
          
            if res ==True :
                
             await call.message.delete()     
           
               
             await call.message.reply("✅ زمان ویرایش شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
             await orm.mainManageService(serviceId,call)
             return
                    
            else :
                 await call.message.reply("هنگام ویرایش مشکلی پیش آمد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
                 return       
         else:
                       await Canesel_Key(c,call.message,call.from_user.id)
                       return                                 
   if "EditVolumeConfigUser_" in call.data :
                  
         serviceId = call.data.split("_")[1]
         await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
         
         answer = await pyromod.Chat.ask(text="🙏🏻 | لطفا حجم سرویس مورد نظر را ارسال کنید" , self=call.message.chat)
         if answer.text != "انصراف":
            volume = 0
            try:
                volume = int( answer.text) 
            except:
               await call.message.reply("🙏🏻 | لطفا فقط عدد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
               return     
            res =  await orm.EditVolumeConfig(serviceId,c,volume)  
          
            if res ==True :
                
             await call.message.delete()     
           
               
             await call.message.reply("✅ حجم ویرایش شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
             await orm.mainManageService(serviceId,call)
             return
                    
            else :
                 await call.message.reply("هنگام ویرایش مشکلی پیش آمد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
                 return  
         else:
                       await Canesel_Key(c,call.message,call.from_user.id)
                       return  
   if "EnableConfigUser_" in call.data :
      
     
            serviceId = call.data.split("_")[1]
            res =  await orm.DisableOrEnableConfig(serviceId,c,'true')  
          
            if res ==True :
                
             await call.message.delete()     
            
               
             await call.message.reply("✅ فعال شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
             await orm.mainManageService(serviceId,call)
             return
                         
            else :
                 await call.message.reply("هنگام ویرایش مشکلی پیش آمد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 

                 return 
   if "DisableConfigUser_" in call.data :
      
     
            serviceId = call.data.split("_")[1]
            res =  await orm.DisableOrEnableConfig(serviceId,c,'false')  
          
            if res ==True :
                
             await call.message.delete()     
            
               
             await call.message.reply("✅ غیرفعال شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
             await orm.mainManageService(serviceId,call)
             return
             
                     
            else :
                 await call.message.reply("هنگام ویرایش مشکلی پیش آمد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 

                 return           
   if "DeleteConfigUser_" in call.data :
      
     
            serviceId = call.data.split("_")[1]
            res =  await orm.DeleteConfig(serviceId,c)  
            await call.message.delete()     
            if res[0] == True:
               
              await call.message.reply("✅ حذف شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
              return
            else:
                 await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
                 return
             
   if call.data == "AcceptResetTest":
      res = await orm.RefreshAllTest()
      if res ==True:
        await call.answer("✅ از سرگیری موفقیت آمیز بود ",True)
        Messages =await ReadFileText()
        await call.edit_message_text(text=Messages['manageadmin'],
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
        return
      else:
          await call.answer("❌ از سرگیری موفقیت آمیز نبود ",True)
          return
   if call.data == "RefreshTestUsers":
       await call.edit_message_text("""⚠️ | توجه 
                                    
با زدن دکمه تایید تمامی کاربرانی که قبلا تست رایگان دریافت کرده اند مجدد میتوانند دریافت کنند 
                                    
.                                    
                                    """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data="AcceptResetTest")],[InlineKeyboardButton("🔙 بازگشت",callback_data="mainAdmin")]]))
       return
   if  call.data == "CreateConfig":
      await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
      serverId = 0
      numberOfConf = 0
      answer = await pyromod.Chat.ask(text="🔻 ترجیحا کمتر از 10 تعداد اکانت را وارد کنید:" , self=call.message.chat)
      if answer.text != "انصراف":
        try:
            numberOfConf =int(answer.text)
            if numberOfConf <= 0 :
                 await call.message.reply("لطفا فقط عدد بزرگ تر از 0 وارد  کنید",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
                 return   
        except:
              await call.message.reply("لطفا فقط عدد وارد کنید") 
              return
        await call.message.reply("🫴🏻 دسته بندی را انتخاب کنید ",reply_markup=ReplyKeyboardMarkup(await orm.GetCatBtnsSelect(),resize_keyboard=True))
        answer = await pyromod.Chat.ask(call.message.chat,"♦️ در صورتی که در لیست موجود نیست ابتدا باید دسته بندی ایجاد کنید") 
        if answer.text != "انصراف":
          catId = await orm.GetCatByName(answer.text)   
          if catId != None: 
               catType = await orm.GetCatType(catId[0])
               if catType == "normal":
                await call.message.reply("🫴🏻 سرور را انتخاب کنید ",reply_markup=ReplyKeyboardMarkup(await orm.GetServerBtnsSelect(),resize_keyboard=True))
                answer = await pyromod.Chat.ask(call.message.chat,"♦️ در صورتی که در لیست سروری موجود نیست ابتدا سرور به دسته بندی اضافه کنید") 
                if answer.text == "انصراف":
                        await Canesel_Key(c,call.message,call.from_user.id)
                        return
                serverId = await orm.GetServerByName(answer.text)   
                if serverId == None :
                    await call.message.reply("این سرور پیدا نشد")
                    return
               answer = await pyromod.Chat.ask(text="🔻 حجم را به گیگ وارد کنید:(نامحدود=0)" , self=call.message.chat)
               if answer.text != "انصراف":
                volume = 0
                try:
                 volume =  float(answer.text) * 1024 * 1024 *1024
                except:
                                      await call.message.reply("لطفا فقط عدد وارد کنید") 
                                      await Canesel_Key(c,call.message,call.from_user.id)
                                      return
                answer = await pyromod.Chat.ask(text="🔻 روز را وارد کنید:(نامحدود=0)" , self=call.message.chat)
                if answer.text != "انصراف":
                  days = 0
                  endTimeMikro = 0
                  if answer.text != '0':  
                   try:
                    days = int(answer.text) 
                   except:
                                      await call.message.reply("لطفا فقط عدد وارد کنید") 
                                      await Canesel_Key(c,call.message,call.from_user.id)
                                      return
                   monthCount = datetime.datetime.now() + datetime.timedelta(days=days)
                   endTimeMikro =int(datetime.datetime.timestamp(monthCount) ) * 1000
                
                  configName = ""    
                  answer = await pyromod.Chat.ask(text="🔻 پیشوند اکانت ها را وارد کنید:" , self=call.message.chat)
                  if answer.text != "انصراف":
                   configName = answer.text
                  else:
                        await Canesel_Key(c,call.message,call.from_user.id)
                        return
                  
                  answer = await pyromod.Chat.ask(text="🔻 شماره شروع را وارد کنید:" , self=call.message.chat)
                  if answer.text == "انصراف":
                         await Canesel_Key(c,call.message,call.from_user.id)
                         return
                  nmuberStart = 0
                  try:
                    nmuberStart = int(answer.text)    
                  except:
                     await call.message.reply("لطفا فقط عدد وارد کنید") 
                     return


                  res = await orm.AddConfigUserManual(nmuberStart,endTimeMikro,configName,volume,numberOfConf,catId[0],call.message,call.from_user.id,serverId)      
                else:
                       await Canesel_Key(c,call.message,call.from_user.id)
                       return  
               else:
                          await Canesel_Key(c,call.message,call.from_user.id)
                          return  
             
          else:
               await call.message.reply("دسته بندی یافت نشد")
               await Canesel_Key(c,call.message,call.from_user.id)
               return  
        else:
                           await Canesel_Key(c,call.message,call.from_user.id)
                           return  
      else:
               await Canesel_Key(c,call.message,call.from_user.id)
               return    
   if call.data ==  "PlanExtension":
        btns = await orm.GetAllPlanExtension()
        await call.edit_message_text("""🔁 مدیریت پلن های تمدید 
                                     
ℹ️ پلنی را انتخاب کنید و برای ویرایش اقدام کنید                                     
                                     
🔰 /start
                                     
                                     """,reply_markup=InlineKeyboardMarkup(btns))
        return
   if call.data ==  "addplanExtension" :
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا نام پلن را ارسال فرمایید" , self=call.message.chat)
       if answer.text!= "انصراف":
        PlanName = answer.text   
        answer = await pyromod.Chat.ask(text="🔻 لطفا قیمت را ارسال فرمایید" , self=call.message.chat)
        if answer.text!= "انصراف":
         try:
          Price =  int(answer.text)   
          answer = await pyromod.Chat.ask(text="🔻 لطفا حجم را ارسال فرمایید" , self=call.message.chat)
          if answer.text!= "انصراف":
              Volume =  float(answer.text)   
              answer = await pyromod.Chat.ask(text="🔻 لطفا ماه را ارسال فرمایید" , self=call.message.chat)
              if answer.text!= "انصراف":
                 Month = int(answer.text) 
                 await orm.AddExtension(PlanName,Price,Volume,Month)
                 await call.message.reply("✅")
                 await Canesel_Key(c,call.message,call.from_user.id)

              else:
                    await Canesel_Key(c,call.message,call.from_user.id)
                    return
          else:
                    await Canesel_Key(c,call.message,call.from_user.id)
                    return
         except:
           await call.message.reply("عدد وارد کنید , یا هنگام وارد کردن اطلاعات مشکلی پیش آمد ❌")
           await Canesel_Key(c,call.message,call.from_user.id)
           return
        else:
           await Canesel_Key(c,call.message,call.from_user.id)
           return
       else:
            
           await Canesel_Key(c,call.message,call.from_user.id)
           return
   if "EditPlanExt_" in call.data:
       planId = call.data.split("_")[1]        
       btns = await orm.GetBtnEXT(planId)  
       await call.edit_message_text("🔄 ویرایش پلن تمدید مورد نظر",reply_markup=InlineKeyboardMarkup(btns))
   if "EditNamePlanExt_" in call.data : 
       planId  = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       Email = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا نام جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
              await orm.UpdateNameExtPlan(planId , answer.text)
              await call.message.reply("✅ ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
              return
       else:  
          await Canesel_Key(c,call.message,call.from_user.id) 
          return  
   if "EditPricePlanExt_" in call.data : 
       planId  = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       Email = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا قیمت جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
        try:
              Price = int(answer.text)
              await orm.UpdatePiceExtPlan(planId , Price)
              await call.message.reply("✅ ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
              return
        except:
              await call.message.reply(" لطفا فقط عدد وارد کنید ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
              return
       else:  
          await Canesel_Key(c,call.message,call.from_user.id) 
          return  
   if "EditVolumePlanExt_" in call.data : 
       planId  = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       Email = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا حجم جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
        try:
              Volume = float(answer.text)
              await orm.UpdateVolumeExtPlan(planId , Volume)
              await call.message.reply("✅ ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
              return
        except:
              await call.message.reply(" لطفا فقط عدد وارد کنید ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
              return
       else:  
          await Canesel_Key(c,call.message,call.from_user.id) 
          return  
   if "EditMonthCountPlanExt_" in call.data:
       planId  = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       Email = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا ماه جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
        try:
              Month = int(answer.text)
              await orm.UpdateMonthExtPlan(planId , Month)
              await call.message.reply("✅ ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
              return
        except:
              await call.message.reply(" لطفا فقط عدد وارد کنید ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
              return
       else:  
          await Canesel_Key(c,call.message,call.from_user.id) 
          return  
   if "DeletePlanExt_" in call.data:
      planId = call.data.split("_")[1]
      await orm.DeleteExtPlan(planId)
      await call.message.delete()
      await call.message.reply("✅")
   if "BtnShop_" in call.data:
       state = call.data.split("_")[1]
       await orm.UpdateBtns('btnshop','on' if state == 'off' else 'off')
       btns =  await  orm.GetBtnsSetting()
       await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))
   if "BtnTest_" in call.data:
       state = call.data.split("_")[1]
       await orm.UpdateBtns('freetest','on' if state == 'off' else 'off')
       btns =  await  orm.GetBtnsSetting()
       await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))    
   if "BtnAccount_" in call.data:
       state = call.data.split("_")[1]
       await orm.UpdateBtns('myacc','on' if state == 'off' else 'off')
       btns =  await  orm.GetBtnsSetting()
       await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))
   if "BtnSub_" in call.data:
       state = call.data.split("_")[1]
       await orm.UpdateBtns('mysub','on' if state == 'off' else 'off')
       btns =  await  orm.GetBtnsSetting()
       await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))    
   if "Hamkarbtn_" in call.data:
       state = call.data.split("_")[1]
       await orm.UpdateBtns('hamkarbtn','on' if state == 'off' else 'off')
       btns =  await  orm.GetBtnsSetting()
       await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))       
   if "Tamdidbtn_" in call.data:
       state = call.data.split("_")[1]
       await orm.UpdateBtns('tamdidbtn','on' if state == 'off' else 'off')
       btns =  await  orm.GetBtnsSetting()
       await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))  
   if "GetConfigData_" in call.data:
       state = call.data.split("_")[1]
       await orm.UpdateBtns('configdata','on' if state == 'off' else 'off')
       btns =  await  orm.GetBtnsSetting()
       await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))    
              
   if call.data == "manageBtns":
      btns =  await  orm.GetBtnsSetting()
      await call.edit_message_text("""🔘مدیریت دکمه ها 
                                   
  بخش مدیریت دکمه های ربات 🔘 
""",reply_markup=InlineKeyboardMarkup(btns))
      return
   if call.data == "AmarBot":
       btns  = await orm.GetBtnsAmar()
       await call.edit_message_text("""
☄️ به بخش آمار ربات خوش آمدید
                                    
☺️ در این بخش شما میتوانید آماری از وضعیت ربات داشته باشید
                                    
/start
                                    """,reply_markup=InlineKeyboardMarkup(btns))
       return
   if call.data == "manageUser":
    
      Messages =await ReadFileText()
      config = await ReadFileConfig()
      if config['ownerId'] == call.from_user.id:
            
       await call.edit_message_text(Messages["manageuser"],reply_markup=
                                   InlineKeyboardMarkup(
                                      [
                                      [InlineKeyboardButton("👤 لیست ادمین ها",callback_data="adminManage"),InlineKeyboardButton("🆕 افزودن ادمین",callback_data="AddNewAdmin")] , 
                                      [InlineKeyboardButton("✅ کاربران مسدود شده",callback_data="BlockedUser")],
                                      [InlineKeyboardButton("🔍 تنظیمات کاربر",callback_data="settingUser")],
                                      [InlineKeyboardButton("🔙 بازگشت",callback_data="mainAdmin")]
                                      ]
                                      ))
      else:
         await call.edit_message_text(Messages["manageuser"],reply_markup=
                                   InlineKeyboardMarkup(
                                      [
                                      [InlineKeyboardButton("✅ کاربران مسدود شده",callback_data="BlockedUser")],
                                      [InlineKeyboardButton("🔍 تنظیمات کاربر",callback_data="settingUser")],
                                      [InlineKeyboardButton("🔙 بازگشت",callback_data="mainAdmin")]
                                      ]
                                      ))
   if call.data == "adminManage":
      Messages =await ReadFileText()
      admins = await orm.GetAdminList()
      btns = []
      print(admins)
      if admins != []:
         
       for admin in admins:
         btns.append([InlineKeyboardButton(admin[2],callback_data="ARS"),InlineKeyboardButton("❌",callback_data=f"DeleteAdmin_{admin[0]}")])
      else:
        btns.append([InlineKeyboardButton("خالی" , callback_data="ARS")])   
             
      btns.append([InlineKeyboardButton("🔙 بازگشت 🔙" , callback_data="manageUser")])   
      await call.edit_message_text(f"""🧑🏼‍💻 به بخش مدیریت ادمین ها خوش امدید 
تعداد : {len(admins)}

▪️▫️▪️▫️▪️▫️                        
           """,reply_markup=InlineKeyboardMarkup(btns))
   if call.data == "BlockedUser":
       await call.edit_message_text("لیست کاربران مسدود شده ! ",reply_markup=InlineKeyboardMarkup(await orm.GetbtnUserBlocks()))
       return
   if "BlockUser_" in call.data:
         userId = call.data.split("_")[1]
         user = await orm.GetUserByUserId(userId)
         countConfig = await orm.GetConfigUserCount(user[1])
         currentUser = await ReadFileConfig()
         if user != None:

          await call.message.reply(f"""مدیریت کاربر {user[2]} 🔰
                                   

🆔 : <code>{user[1]}</code>

تعداد کانفیگ : {countConfig[0][0]}

کیف پول : {user[7]} تومان

تست گرفته ؟: {"❌" if user[8] == 0 else "✅"}

ادمین میباشد ؟ : {"❌" if user[3] == 0 else "✅"}

▫️▪️▫️▪️▫️

""",reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton("➕" , callback_data=f"aaw_{user[0]}"),InlineKeyboardButton("➖" , callback_data=f"amw_{user[0]}"), InlineKeyboardButton("کیف پول ",callback_data="ARS")]
 ,[InlineKeyboardButton(  "❌" if user[3] == 0  else  "✅"  if currentUser['ownerId'] == call.from_user.id else  "شما ادمین اصلی نیستید" , callback_data=f"aaa_{user[0]}" if currentUser['ownerId'] == call.from_user.id else "ARS" ),InlineKeyboardButton("👤 ادمین 👤",callback_data="ARS")]

                                       ,[InlineKeyboardButton("✅" if user[4] == 1 else "❌",callback_data=f"aub_{user[0]}"),InlineKeyboardButton("👮🏻‍♂️ مسدودیت 👮🏻‍♂️",callback_data="ARS")]
                                       ,[InlineKeyboardButton("لیست کانفیگ ها",callback_data=f"lcau_{user[1]}")]
                                       ,[InlineKeyboardButton("🔙 بازگشت 🔙",callback_data="BlockedUser")]]))
          return  

   if "DeleteConfig_" in call.data:
     serviceId = call.data.split("_")[1]
     res =  await orm.DeleteConfig(serviceId,c)       
     if res[0] == True:
      await call.message.delete()
      await call.message.reply("✅ حذف شد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
     else:
         await call.message.reply(res[1])
   if "DeleteAdmin_" in call.data:
        UserId = call.data.split("_")[1]
        await orm.DeleteAdmin(UserId)
        admins = await orm.GetAdminList()

        await call.edit_message_text("✅ موفقیت امیز بود" ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت 🔙" , callback_data="adminManage")]]))
   if call.data == "settingUser":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       anwser = await pyromod.Chat.ask(text="🔻 لطفا ای دی عدد کاربر یا نام کاربری یا نام را ارسال فرمایید" , self=call.message.chat)
       if anwser.text!= "انصراف":
         user = await orm.GetUserByUserDeatails(anwser.text)
         countConfig = await orm.GetConfigUserCount(user[1])
         currentUser = await ReadFileConfig()
         #TODO Create UserManage 
         if user != None:

          await call.message.reply(f"""مدیریت کاربر {user[2]} 🔰
                                   

🆔 : <code>{user[1]}</code>

تعداد کانفیگ : {countConfig[0][0]}

کیف پول : {user[7]} تومان

تست گرفته ؟: {"❌" if user[8] == 0 else "✅"}

ادمین میباشد ؟ : {"❌" if user[3] == 0 else "✅"}

▫️▪️▫️▪️▫️

""",reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton("➕" , callback_data=f"aaw_{user[0]}"),InlineKeyboardButton("➖" , callback_data=f"amw_{user[0]}"), InlineKeyboardButton("کیف پول ",callback_data="ARS")]
    ,[InlineKeyboardButton(  "❌" if user[3] == 0  else  "✅"  if currentUser['ownerId'] == call.from_user.id else  "شما ادمین اصلی نیستید" , callback_data=f"aaa_{user[0]}" if currentUser['ownerId'] == call.from_user.id else "ARS" ),InlineKeyboardButton("👤 ادمین 👤",callback_data="ARS")]

                                       ,[InlineKeyboardButton("✅" if user[4] == 1 else "❌",callback_data=f"aub_{user[0]}"),InlineKeyboardButton("👮🏻‍♂️ مسدودیت 👮🏻‍♂️",callback_data="ARS")]
                                       ,[InlineKeyboardButton("لیست کانفیگ ها",callback_data=f"lcau_{user[1]}")]
                                       ,[InlineKeyboardButton("🔙 بازگشت 🔙",callback_data="manageUser")]]))

          
         else:
          await call.answer("کاربری با این مشخصات یافت نشد",False)

         await Canesel_Key(c,call.message,call.from_user.id)
       else:
            
           await Canesel_Key(c,call.message,call.from_user.id)
   if "lcau_" in  call.data:
       userId = call.data.split("_")[1]
       btns  = await orm.GetServiceListForAdmin(userId)
       
       await call.edit_message_text("""لیست کانفیگ های کاربر مورد نظر شما """,reply_markup=InlineKeyboardMarkup(btns))
   if call.data == "AddNewAdmin":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا ای دی عدد کاربر را ارسال فرمایید" , self=call.message.chat)
       if answer.text!= "انصراف":
         
         res = await orm.AddNewAdmin(answer.text)
         if res == True:
          await call.message.reply("✅ افزودن موفقیت امیز")
          user = await orm.GetUserByUserId(answer.text)
          countConfig = await orm.GetConfigUserCount(user[1])
          currentUser = await ReadFileConfig()
          await call.message.reply(f"""مدیریت کاربر {user[2]} 🔰

    
🆔 : <code>{user[1]}</code>

تعداد کانفیگ : {countConfig[0][0]}

کیف پول : {user[7]} تومان

تست گرفته ؟: {"❌" if user[8] == 0 else "✅"}

ادمین میباشد ؟ : {"❌" if user[3] == 0 else "✅"}

▫️▪️▫️▪️▫️
""",reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton("➕" , callback_data=f"aaw_{user[0]}"),InlineKeyboardButton("➖" , callback_data=f"amw_{user[0]}"), InlineKeyboardButton("کیف پول ",callback_data="ARS")]
   ,[InlineKeyboardButton(  "❌" if user[3] == 0  else  "✅"  if currentUser['ownerId'] == call.from_user.id else  "شما ادمین اصلی نیستید" , callback_data=f"aaa_{user[0]}" if currentUser['ownerId'] == call.from_user.id else "ARS" ),InlineKeyboardButton("👤 ادمین 👤",callback_data="ARS")]

                                       ,[InlineKeyboardButton("✅" if user[4] == 1 else "❌",callback_data=f"aub_{user[0]}"),InlineKeyboardButton("👮🏻‍♂️ مسدودیت 👮🏻‍♂️",callback_data="ARS")]
                                       ,[InlineKeyboardButton("لیست کانفیگ ها",callback_data=f"lcau_{user[1]}")]
                                       ,[InlineKeyboardButton("🔙 بازگشت 🔙",callback_data="manageUser")]]))
          await Canesel_Key(c,call.message)
         else:
          await call.message.reply("کاربری با این مشخصات یافت نشد")
          await Canesel_Key(c,call.message,call.from_user.id)

       else:
            
          await Canesel_Key(c,call.message,call.from_user.id)
   if "aub_" in call.data:
      data = call.data.split("_")[1]
      user = await orm.GetUserById(int(data))
      currentUser = await ReadFileConfig()
      change = 0
      if user[4] == 0 :
         await orm.BlockUser(int(data),1)
         change = 1
      else:
         await orm.BlockUser(int(data),0)
        
      user = await orm.GetUserById(int(data))

      await call.answer("✅ ویرایش موفقیت امیز",False)
     
         #TODO Create UserManage 
    
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton("➕" , callback_data=f"aaw_{user[0]}"),InlineKeyboardButton("➖" , callback_data=f"amw_{user[0]}"), InlineKeyboardButton("کیف پول ",callback_data="ARS")]
    ,[InlineKeyboardButton(  "❌" if user[3] == 0  else  "✅"  if currentUser['ownerId'] == call.from_user.id else  "شما ادمین اصلی نیستید" , callback_data=f"aaa_{user[0]}" if currentUser['ownerId'] == call.from_user.id else "ARS" ),InlineKeyboardButton("👤 ادمین 👤",callback_data="ARS")]

                                       ,[InlineKeyboardButton("✅" if user[4] == 1 else "❌",callback_data=f"aub_{user[0]}"),InlineKeyboardButton("👮🏻‍♂️ مسدودیت 👮🏻‍♂️",callback_data="ARS")]
                                       ,[InlineKeyboardButton("لیست کانفیگ ها",callback_data=f"lcau_{user[1]}")]
                                       ,[InlineKeyboardButton("🔙 بازگشت 🔙",callback_data="manageUser")]]))
   if "aaw_" in call.data:
      data = call.data.split("_")[1]
      await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
      answer = await pyromod.Chat.ask(text="🔻 لطفا مقدار را به تومان ارسال کنید فرمایید" , self=call.message.chat)
      if answer.text!= "انصراف":
          res=  await orm.AddToUserWallet(int(data),int(answer.text))
          if res == True:
            await call.message.reply("✅ افزودن موفقیت امیز",False)
            await Canesel_Key(c,call.message,call.from_user.id)
            return
          else:
              await call.message.reply("کاربر پیدا نشد یا مشکلی پیش آمده",False)
              await Canesel_Key(c,call.message,call.from_user.id)
              return
   if "amw_" in call.data:
      data = call.data.split("_")[1]
      await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
      answer = await pyromod.Chat.ask(text="🔻 لطفا مقدار را به تومان ارسال کنید فرمایید" , self=call.message.chat)
      if answer.text!= "انصراف":
          res=  await orm.MinusToUserWallet(int(data),int(answer.text))
          if res == True:
            await call.message.reply("✅ کاهش موفقیت امیز")
            await Canesel_Key(c,call.message,call.from_user.id)

          else:
              await call.message.reply("کاربر پیدا نشد یا مشکلی پیش امده")
              await Canesel_Key(c,call.message,call.from_user.id)
   if "aaa_" in call.data:
      data = call.data.split("_")[1]
      user = await orm.GetUserById(int(data))
      change = 0
      if user[3] == 0 :
         await orm.AdminUser(int(data),1)
         change = 1
      else:
         await orm.AdminUser(int(data),0)
        
      user = await orm.GetUserById(int(data))
      currentUser = await ReadFileConfig()
      await call.answer("✅ ویرایش موفقیت امیز",False)
     
         #TODO Create UserManage 
    
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton("➕" , callback_data=f"aaw_{user[0]}"),InlineKeyboardButton("➖" , callback_data=f"amw_{user[0]}"), InlineKeyboardButton("کیف پول ",callback_data="ARS")]
     ,[InlineKeyboardButton(  "❌" if user[3] == 0  else  "✅"  if currentUser['ownerId'] == call.from_user.id else  "شما ادمین اصلی نیستید" , callback_data=f"aaa_{user[0]}" if currentUser['ownerId'] == call.from_user.id else "ARS" ),InlineKeyboardButton("👤 ادمین 👤",callback_data="ARS")]

                                       ,[InlineKeyboardButton("✅" if user[4] == 1 else "❌",callback_data=f"aub_{user[0]}"),InlineKeyboardButton("👮🏻‍♂️ مسدودیت 👮🏻‍♂️",callback_data="ARS")]
                                       ,[InlineKeyboardButton("لیست کانفیگ ها",callback_data=f"lcau_{user[1]}")]
                                       ,[InlineKeyboardButton("🔙 بازگشت 🔙",callback_data="manageUser")]]))
   if call.data == "manageneedApp":
      apps =   await orm.GetAllApp()    
      btns = []
      btns.append([InlineKeyboardButton("📲 افزودن به لیست ",callback_data="AddApp")])
      print(apps)
      if apps!= None:
         for app in apps:
            if "https://" in app[2] or "http://" in app[2] :
              btns.append([InlineKeyboardButton(text = app[1],url=app[2])])
              btns.append([InlineKeyboardButton("🗑" , callback_data=f"deleteapp_{app[0]}"),InlineKeyboardButton("✍🏻",callback_data=f"EditApp_{app[0]}")])
            else: 
              btns.append([InlineKeyboardButton(text = app[1],callback_data="لینک مشکل دارد")])
              btns.append([InlineKeyboardButton("🗑" , callback_data=f"deleteapp_{app[0]}"),InlineKeyboardButton("✍🏻",callback_data=f"EditApp_{app[0]}")])
      btns.append([InlineKeyboardButton("🔙 بازکشت ",callback_data="mainAdmin")])
      await call.edit_message_text("""
🔰لیست نرم افزار ها به شرح زیر است لطفا یکی از موارد را انتخاب کنید

🔸می توانید به راحتی همه فایل ها را به صورت رایگان دریافت کنید
""",reply_markup= InlineKeyboardMarkup(btns))
   if call.data == "AddApp":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       nameApp = ""
       link = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا نام اپلیکیشن را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         nameApp =  answer.text
         answer = await pyromod.Chat.ask(text="🔻 لطفا لینک اپلیکیشن را وارد کنید" , self=call.message.chat)
         if answer.text!= "انصراف":
             link  = answer.text
             answer = await pyromod.Chat.ask(text="🔻 لطفا توضیحات اپلیکیشن را وارد کنید" , self=call.message.chat)
             if answer.text!= "انصراف":
              Description  = answer.text
              answer = await pyromod.Chat.ask(text="🔻درصورتی که میخواهید عکس یا فیلم نداشته باشد (empty) لطفا عکس یا فیلم اموزش اپلیکیشن را وارد کنید" , self=call.message.chat)
              if answer.text!= "انصراف":
               photo =  "empty"
               if answer.text == "empty":
                     photo = "empty"
               else:
                  try:      
                    photo = answer.photo.file_id 
                  except:
                     try:
                       photo = answer.video.file_id 
                     except:
                        photo = "empty"

               await call.message.reply("🗒 دسته بندی را انتخاب کنید ",reply_markup=ReplyKeyboardMarkup([["اندروید","IOS"],["ویندوز","لینوکس"],["انصراف"]],resize_keyboard=True))
               answer = await pyromod.Chat.ask(text="🔻 لطفا دسته بندی اپلیکیشن را وارد کنید" , self=call.message.chat)
               if answer.text!= "انصراف":

                if answer.text=="اندروید":
                     
                     await orm.AddApp(link , nameApp,"android",Description,photo)
                     await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                     return
                elif answer.text=="IOS":
                     
                     await orm.AddApp(link , nameApp,"IOS",Description,photo)
                     await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                     return
                elif answer.text=="ویندوز":
                     
                     await orm.AddApp(link , nameApp,"Windows",Description,photo)
                     await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                     return
                     
                elif answer.text=="لینوکس":
                     await orm.AddApp(link , nameApp,"Linux",Description,photo)
                     await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                     return
                else:
                    await call.message.reply("مقادیر وارد نشده به درستی ")
                    return
          
               else:
                 await Canesel_Key(c,call.message,call.from_user.id)  
                 return
                   
              else:
                 await Canesel_Key(c,call.message,call.from_user.id)  
                 return
             else:
                 await Canesel_Key(c,call.message,call.from_user.id)   
                 return
         



             apps =   await orm.GetAllApp()    
             btns = []
             btns.append([InlineKeyboardButton("📲 افزودن به لیست ",callback_data="AddApp")])

             if apps!=[] or None:
                for app in apps:
                   btns.append([InlineKeyboardButton(app[1],url=app[2])])
                   btns.append([InlineKeyboardButton("🗑" , callback_data=f"deleteapp_{app[0]}"),InlineKeyboardButton("✍🏻",callback_data=f"EditApp_{app[0]}")])
             btns.append([InlineKeyboardButton("🔙 بازکشت ",callback_data="mainAdmin")])
             await call.edit_message_text("""
🔰لیست نرم افزار ها به شرح زیر است لطفا یکی از موارد را انتخاب کنید

🔸می توانید به راحتی همه فایل ها را (به صورت رایگان) دریافت کنید
""",reply_markup= InlineKeyboardMarkup(btns))
             await Canesel_Key(c,call.message,call.from_user.id)   
             
         else:
           await Canesel_Key(c,call.message,call.from_user.id)   

       else:
            
          await Canesel_Key(c,call.message,call.from_user.id)   
   if "deleteapp_" in call.data:
      appId =  call.data.split("_")[1]
      await orm.DeleteApp(appId)
      apps =   await orm.GetAllApp()    
      btns = []
      btns.append([InlineKeyboardButton("📲 افزودن به لیست ",callback_data="AddApp")])
      print(apps)
      if apps!= None:
         for app in apps:
            btns.append([InlineKeyboardButton(text = app[1],url=app[2])])
            btns.append([InlineKeyboardButton("🗑" , callback_data=f"deleteapp_{app[0]}"),InlineKeyboardButton("✍🏻",callback_data=f"EditApp_{app[0]}")])
      btns.append([InlineKeyboardButton("🔙 بازکشت ",callback_data="mainAdmin")])
      await call.edit_message_reply_markup(reply_markup= InlineKeyboardMarkup(btns))
   if "EditApp_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       nameApp = ""
       link = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا نام اپلیکیشن را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         nameApp =  answer.text
         answer = await pyromod.Chat.ask(text="🔻 لطفا لینک اپلیکیشن را وارد کنید" , self=call.message.chat)
         if answer.text!= "انصراف":
             link  = answer.text
             answer = await pyromod.Chat.ask(text="🔻 لطفا توضیحات اپلیکیشن را وارد کنید" , self=call.message.chat)
             if answer.text!= "انصراف":
              Description  = answer.text
              photo =  "empty"
              answer = await pyromod.Chat.ask(text="🔻درصورتی که میخواهید عکس یا فیلم نداشته باشد (empty) لطفا عکس یا فیلم اموزش اپلیکیشن را وارد کنید" , self=call.message.chat)
              if answer.text!= "انصراف":
               if answer.text == "empty":
                     photo = "empty"
               else:
                  try:      
                    photo = answer.photo.file_id 
                  except:
                     try:
                       photo = answer.video.file_id 
                     except:
                        photo = "empty"
              else: 
                          await Canesel_Key(c,call.message,call.from_user.id)   
                          return
              await call.message.reply("🗒 دسته بندی را انتخاب کنید ",reply_markup=ReplyKeyboardMarkup([["اندروید","IOS"],["ویندوز","لینوکس"],["انصراف"]],resize_keyboard=True))
              answer = await pyromod.Chat.ask(text="🔻 لطفا دسته بندی اپلیکیشن را وارد کنید" , self=call.message.chat)
              if answer.text!= "انصراف":
                if answer.text=="اندروید":
                     await orm.EditApp(link , nameApp,data,"android",Description,photo)
                     await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                     return
                elif answer.text=="IOS":
                    await orm.EditApp(link , nameApp,data,"IOS",Description,photo)
                    await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                    return
                elif answer.text=="ویندوز":
                     await orm.EditApp(link , nameApp,data,"Windows",Description,photo) 
                     await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                     return
                elif answer.text=="لینوکس":
                     await orm.EditApp(link , nameApp,data,"Linux",Description,photo) 
                     await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

                     return
                else:
                    await call.message.reply("مقادیر وارد نشده به درستی ")
                    return
                apps =   await orm.GetAllApp()    
                btns = []
                btns.append([InlineKeyboardButton("📲 افزودن به لیست ",callback_data="AddApp")])

                if apps!=[] or None:
                   for app in apps:
                     btns.append([InlineKeyboardButton(app[1],url=app[2])])
                     btns.append([InlineKeyboardButton("🗑" , callback_data=f"deleteapp_{app[0]}"),InlineKeyboardButton("✍🏻",callback_data=f"EditApp_{app[0]}")])
                btns.append([InlineKeyboardButton("🔙 بازکشت ",callback_data="mainAdmin")])
                print(btns)
                try :
                  await call.message.reply("""
🔰لیست نرم افزار ها به شرح زیر است لطفا یکی از موارد را انتخاب کنید

🔸می توانید به راحتی همه فایل ها را (به صورت رایگان) دریافت کنید
""",reply_markup= InlineKeyboardMarkup(btns))
                  await Canesel_Key(c,call.message,call.from_user.id)   
                except:
                 await call.answer("در دریافت اطلاعات مشکلی پیش امده")
         else: 
           await Canesel_Key(c,call.message,call.from_user.id)   
           return
       else:
            
          await Canesel_Key(c,call.message,call.from_user.id)
          return
   if call.data =="botSetting":
     try:   
       res=  await  orm.GetSettingBtns()
       await call.edit_message_text("""🔻 به بخش مدیریت ربات خوش امدید
       
تنظیمات دلخواه خود را اعمال کنید
                                    
⚠️ | معمولا مقدار empty درصورت نیاز تغییر دهید مقدار از پیش در نظر گرفته است   

                       
                                    """,reply_markup=InlineKeyboardMarkup(res))
     except  :
         
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")
   if "esa_" in call.data :
     try: 
      res = call.data.split("_")[1]
      print(res)
      await orm.EditEsa(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")
         return
   if "SingleSubShopSetting_" in call.data:
     try: 
      res = call.data.split("_")[1]
      
      await orm.EditChangeSingleShopSub(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")  
         return           
   if "BuyAgainService_" in call.data:
     try: 
      res = call.data.split("_")[1]
      
      await orm.BuyAgainService(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")  
         return              
   if "SubShopSetting_" in call.data:
     try: 
      res = call.data.split("_")[1]
      
      await orm.EditChangeShopSub(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")  
         return         
   if "SingleShopSetting_" in call.data:
     try: 
      res = call.data.split("_")[1]
      
      await orm.EditChangeShopSingle(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")  
         return      
   if "ChangeShop_" in call.data :
     try: 
      res = call.data.split("_")[1]
      print(res)
      await orm.EditChangeShop(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")  
         return    
   if "ChangeTEST_" in call.data :
     try: 
      res = call.data.split("_")[1]
      print(res)
      await orm.EditChangeTEST(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")     
         return
   if "ChangeWallet_" in call.data:
     try: 
      res = call.data.split("_")[1]
      print(res)
      await orm.EditChangeWallet(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")  
         return   
   if "CardToCardChange_" in call.data:
     try: 
      res = call.data.split("_")[1]
  
      await orm.EditCardToCardChange(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")     
         return

   if "changeXenitGame_" in call.data:
          
     try: 
      res = call.data.split("_")[1]
    
      await orm.changeXenit(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")   
         return        
   if "chengenotifState_" in call.data:
          
     try: 
      res = call.data.split("_")[1]
    
      await orm.changeStateNotif(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")   
         return           
   if "changelink_" in call.data:
          
     try: 
      res = call.data.split("_")[1]
    
      await orm.ChangeLinkConf(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")   
         return             
   if "chanelLock_" in call.data:
          
     try: 
      res = call.data.split("_")[1]
    
      await orm.ChannelLock(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")   
         return                  
   if "SafeMode_" in call.data:
          
     try: 
      res = call.data.split("_")[1]
    
      await orm.SafeMode(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")   
         return                       
   if "onlinPay_" in call.data:
     
     try: 
      res = call.data.split("_")[1]
    
      await orm.EditonlinPay(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")   
         return  
   if "onlinPayMad_" in call.data:
     
     try: 
      res = call.data.split("_")[1]
    
      await orm.EditonlinPayMad(res)
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")   
         return    
   if "DisManageState_" in call.data:
     try: 
      res = call.data.split("_")[1]

      if res == '0':
         await orm.EditDiscountStateManage(1)
      else:
         await orm.EditDiscountStateManage(0)
             
      res=  await  orm.GetSettingBtns()
      
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
      return
     except:
         await call.answer("در دریافت اطلاعات مشکلی پیش امده")     
         return
   if call.data == "alertCard":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا متن را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editalertCardp(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return
   if call.data == "alertWebsite":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا جدید متن را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editalertWebsite(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return   
       
   if call.data == "NameBot":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا  نام کاربری بات را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editNameBot(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return      
   if call.data == "NameSingle":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا  نام فروش معمولی را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editNameSingle(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return           
   if call.data == "NameSub":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا  نام فروش ساب  را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editNameSub(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return               
   if call.data == "NameSubService":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا  نام سرویس ساب  را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editNameSubService(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return                   
   
   if call.data == "NameSingleService":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا  نام سرویس معمولی را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editNameSingleService(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return                        

   if call.data == "ChangeSafeConfig":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا کانفیگ جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          config = answer.text

          
          catbtns = await orm.GetBtnCat() 
           
          await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup(catbtns))
          answer = await pyromod.Chat.ask(text="دسته بندی خود را انتخاب کنید" , self=call.message.chat)
          if answer.text== "انصراف":
              await Canesel_Key(c,call.message,call.from_user.id)   
              return
          try:
             catId = answer.text.split(":")[0]
             await orm.UpdateConfigSafe(config,catId) 
          except:
                     await call.message.reply("هنگام ویرایش اطلاعات مشکلی پیش آمد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
                     return
    
          res=  await orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return                               
   if call.data == "ChangeSupportId":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا شناسه پشتیبانی را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editSupportId(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return                               
   if call.data == "NameTestService":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا  نام سرویس تست  را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editNameTestService(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return                       
   if  call.data == "editTimeBackUp":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا زمان جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editTimeBackUp(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return
   if  call.data == "RewardInvite":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا درصد سود کاربر دعوت کننده را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editRewardInvite(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)   
              return
   if   call.data == "editTimeQuartz":
       
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا زمان جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.TimeSendQuartz(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)    
              return        
 
   if call.data == "editChanelLock":
       
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا چنل جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editChanelLock(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))

          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)       
              return    
   if call.data == "editChanelQuartz"     :
       
       
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا چنل بکاپ جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editChanelQuartz(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))

          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)     
              return         
   if call.data == "editChanelQuartzQuartz"     :
       
       
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا چنل گزارش جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.editChanelQuartzQuartz(answer.text)
          res=  await  orm.GetSettingBtns()
      
          await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
          await call.message.reply("تغییر کرد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))

          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)     
              return                  
   if "ServerEdit_" in call.data :
                   serverId = call.data.split("_")[1]
                   await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
                   answer =  await pyromod.Chat.ask(call.message.chat,"""♦️ لطفا ادرس ورود سرور را وارد کنید 
مثال :
                                              
http://127.0.0.1:8083/path
https://lochalhost:8083/path
http://127.0.0.1:8083
https://lochalhost:8083

وارد کنید ❤️                                                  

                                              """) 
                   if answer.text != "انصراف":
                        UrlPanel = answer.text
                        answer =  await pyromod.Chat.ask(call.message.chat,"♦️ لطفا نام کاربری ورود سرور را وارد کنید ") 
                        if answer.text != "انصراف":
                            userName = answer.text 
                            answer =  await pyromod.Chat.ask(call.message.chat,"♦️ لطفا InboundID کانفیگ های درون سرور را وارد کنید ")
                            
                            if answer.text != "انصراف":    
                                 
                                 inboundId = answer.text
                                 try:
                                  inboundId = int(inboundId)
                                 except:
                                     await call.message.reply("لطفا فقط عدد وارد کنید",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
                                     return   
                                 
                                 answer =  await pyromod.Chat.ask(call.message.chat,"♦️ لطفا رمز عبور ورود سرور را وارد کنید ") 
                                 if answer.text != "انصراف":
                                              Password = answer.text
                                              await call.message.reply("🫴🏻 نوع پنل را انتخاب کنید ",reply_markup=ReplyKeyboardMarkup([['ثنایی','علیرضا'],['ساده','انصراف']],resize_keyboard=True))
                                              answer = await pyromod.Chat.ask(call.message.chat,"♦️  لطفا از دکمه هایزیر انتخاب کنید") 
                                              if answer.text != "انصراف":
                                                  if answer.text == "ثنایی":
                                                      res = await orm.UpdateServerLogin(UrlPanel,userName,Password,"sanaei",serverId,inboundId)
                                                      if res[0]== True:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))      
                                                        return  
                                                      else:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                                                        return 
                                                  elif answer.text == "علیرضا":
                                                      res = await orm.UpdateServerLogin(UrlPanel,userName,Password,"alireza",serverId,inboundId)
                                                      if res[0]== True:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))      
                                                        return   
                                                      else:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                                                        return
                                                  elif answer.text ==  'ساده':
                                                      res = await orm.UpdateServerLogin(UrlPanel,userName,Password,"normal",serverId,inboundId)
                                                      if res[0]== True:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))      
                                                        return
                                                      else:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                                                        return 
                                                      
                                 else:
                                    await Canesel_Key(c,call.message,call.from_user.id)     
                                    return  
                        else:
                            await Canesel_Key(c,call.message,call.from_user.id)     
                            return   

   if "GetInfoServer_" in call.data:
    serverId = call.data.split("_")[1]
    ServerData =  await  orm.GetServerData(serverId)
    if ServerData[0] == True:
        btns = await orm.GetBtnsServerData(ServerData[1],serverId)
        await call.edit_message_text("وضعیت سرور انتخابی شما 🔰" ,reply_markup=InlineKeyboardMarkup(btns))
    else:
        await call.answer("هنگام ارتباط با سرور مشکلی پیش آمد لطفا بررسی کنید",True)    

   if "EditStateSr_" in call.data:
     serverId = call.data.split("_")[1]        
     state = call.data.split("_")[2]
     if int(state) == 1 :
         await orm.EditServerState(serverId,0)
     else:                 
          await orm.EditServerState(serverId,1)
     await call.message.delete()     
     await call.message.reply("""مدیریت سرور 🌐
                                    
سرور  این بخش مدیریت کنید 🌐
                                    
🌐 /start                                    
                                    """,reply_markup=InlineKeyboardMarkup(await orm.GetServerById(serverId)))     
     return
   if "ChangeServerSafe_" in call.data:
     serverId = call.data.split("_")[1]        
     state = call.data.split("_")[2]
     if int(state) == 1 :
         await orm.EditServerSafe(serverId,0)
     else:                 
          await orm.EditServerSafe(serverId,1)
     await call.message.delete()     
     await call.message.reply("""مدیریت سرور 🌐
                                    
سرور  این بخش مدیریت کنید 🌐
                                    
🌐 /start                                    
                                    """,reply_markup=InlineKeyboardMarkup(await orm.GetServerById(serverId)))     
     return   
   if "EditCatSR_" in call.data:
       serverId = call.data.split("_")[2]
       catId = call.data.split("_")[1]
       await orm.UpdateCatServer(serverId,catId)
       await call.edit_message_text("✅ موفقیت امیز بود ",reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton("🔙بازگشت به سرور",callback_data=f"EditServer_{serverId}")]]))
   if "editCatServer_" in call.data:
       serverId= call.data.split("_")[1]
       btns =await orm.GetAllCatBtnsInline(serverId)
       await call.edit_message_text("✍🏻 ویرایش دسته بندی سرور انتخابی",reply_markup=InlineKeyboardMarkup(btns))
   if "ServerName_"in call.data :
       serverId = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا  نام جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.UpdateServerName(answer.text,serverId)
          await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)     
              return                     
   if "DomainServer_"in call.data :
       serverId = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا  نام دامنه جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          await orm.UpdateServerDomainName(answer.text,serverId)
          await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
          return
       else:
              await Canesel_Key(c,call.message,call.from_user.id)     
              return    

   if "AddCatToServer_" in call.data :
        serverId = call.data.split("_")[1]
        CatId = call.data.split("_")[2]
        res = await orm.AddCatToServer(serverId,CatId)
        if res ==True:
              await call.answer("با موفقیت اضافه شد ✅",True)
              btns = await orm.GetServerCatFortManage(serverId)
              await call.message.delete()
              await call.message.reply("لطفا دسته بندی خود را برای افزودن انتخاب کنید",reply_markup=InlineKeyboardMarkup(btns))
              return
        else:
            await call.answer("یا هنگام افزودن مشکلی آمد این دسته بندی از قبل اضافه شده است",True)  
            return  
   if "catListserver_" in call.data : 
       serverId = call.data.split("_")[1]
       btns = await orm.GetCatforSelectServer(serverId)
       await call.edit_message_text("لطفا دسته بندی خود را برای افزودن انتخاب کنید",reply_markup=InlineKeyboardMarkup(btns))
       return
   if "deletecatServer_" in call.data :
        serverId = call.data.split("_")[1]
        res = await orm.DeleteCatServer(serverId)
        if res ==True:
           await call.answer("✅ با موفقیت حذف شد",True)
           await call.message.delete()
           return
        else:
            await call.answer("هنگام حذف مشکلی پیش آمد") 
   if "CatServerManage_" in call.data :                         
     serverId = call.data.split("_")[1]
     btns = await orm.GetServerCatFortManage(serverId)
     await call.edit_message_text("دسته بندی های انتخابی شما برای سرور",reply_markup=InlineKeyboardMarkup(btns))
     return
   if "EditServer_" in call.data:
       serverId = call.data.split("_")[1]
       serverBtns = await orm.GetServerById(serverId)
       await call.edit_message_text("""مدیریت سرور 🌐
                                    
سرور  این بخش مدیریت کنید 🌐
                                    
🌐 /start                                    
                                    """,reply_markup=InlineKeyboardMarkup(serverBtns))
       return

   if call.data == "AddNewServer" :
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([['انصراف']],resize_keyboard=True))
       answer =  await pyromod.Chat.ask(call.message.chat,"♦️ لطفا نام سرور را وارد کنید ") 
       if answer.text != "انصراف":
             Name = answer.text
             answer =  await pyromod.Chat.ask(call.message.chat,"♦️ لطفا دامنه سرور را وارد کنید ") 
             if answer.text != "انصراف":
                   domain = answer.text
                   answer =  await pyromod.Chat.ask(call.message.chat,"""♦️ لطفا ادرس ورود سرور را وارد کنید 
مثال :
                                              
http://127.0.0.1:8083/path
https://lochalhost:8083/path
http://127.0.0.1:8083
https://lochalhost:8083

وارد کنید ❤️                                                  

                                              """) 
                   if answer.text != "انصراف":
                        UrlPanel = answer.text
                        answer =  await pyromod.Chat.ask(call.message.chat,"♦️ لطفا نام کاربری ورود سرور را وارد کنید ") 
                        if answer.text != "انصراف":
                            userName = answer.text
                            answer =  await pyromod.Chat.ask(call.message.chat,"♦️ لطفا رمز عبور ورود سرور را وارد کنید ") 
                            if answer.text != "انصراف":    
                                 Password = answer.text
                                 answer =  await pyromod.Chat.ask(call.message.chat,"♦️ لطفا InboundID کانفیگ های درون سرور را وارد کنید ") 
                                 if answer.text != "انصراف":
                                    
                                                        
                                         inboundId = answer.text
                                         try:
                                            inboundId = int(inboundId)
                                         except:
                                            await call.message.reply("لطفا فقط عدد وارد کنید",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True)) 
                                            return
                                         await call.message.reply("🫴🏻 دسته بندی را انتخاب کنید ",reply_markup=ReplyKeyboardMarkup(await orm.GetCatBtnsSelect(),resize_keyboard=True))
                                         answer = await pyromod.Chat.ask(call.message.chat,"♦️ در صورتی که در لیست موجود نیست ابتدا باید دسته بندی ایجاد کنید") 
                                         if answer.text != "انصراف":
                                           catId = None
                                           IsAddToUsers = False
                                           if answer.text != "♦️ کانفیگ تکی ♦️️":
                                               
                                             Cat = await orm.GetCatByName(answer.text)  
                                             catId = Cat[0] 
                                             await call.message.reply("✍🏻 ایا قصد دارید با افزودن سرور به کاربران این دسته بندی نیز اضافه شود؟",reply_markup=ReplyKeyboardMarkup([['خیر','بله'],['انصراف']],resize_keyboard=True))
                                             answer = await pyromod.Chat.ask(call.message.chat,"♦️ در انتظار ارسال") 
                                             if answer.text == "بله":
                                                 
                                                 IsAddToUsers = True

                                             elif answer.text == "خیر":
                                                 
                                                 IsAddToUsers = False

                                             elif answer.text == "انصراف":
                                                  
                                                  await Canesel_Key(c,call.message,call.from_user.id)     
                                                  return    
                                                 
                                           else:
                                              catId = 0
                                           if catId != None: 
                                            #   ساده
                                              await call.message.reply("🫴🏻 نوع پنل را انتخاب کنید ",reply_markup=ReplyKeyboardMarkup([['ثنایی','علیرضا'],['انصراف']],resize_keyboard=True))
                                              answer = await pyromod.Chat.ask(call.message.chat,"♦️ در انتظار ارسال") 
                                              if answer.text != "انصراف":
                                                  
                                                  if answer.text == "ثنایی":
                                                      if IsAddToUsers == True :
                                                        await call.message.reply("کمی صبور باشید افزودن کاربران چندین ثانیه طول خواهد کشید لطفا ")
                                                      res = await orm.AddServer(Name,domain,UrlPanel,userName,Password,"sanaei",catId,inboundId,IsAddToUsers)
                                                      if res[0]== True:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))      
                                                        return  
                                                      else:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                                                        return 
                                                  elif answer.text == "علیرضا":
                                                      if IsAddToUsers == True :
                                                        await call.message.reply("کمی صبور باشید افزودن کاربران چندین ثانیه طول خواهد کشید لطفا ")
                                                      res = await orm.AddServer(Name,domain,UrlPanel,userName,Password,"alireza",catId,inboundId,IsAddToUsers)
                                                      if res[0]== True:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))      
                                                        return   
                                                      else:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                                                        return
                                                  elif answer.text ==  'ساده':
                                                      if IsAddToUsers == True :
                                                        await call.message.reply("کمی صبور باشید افزودن کاربران چندین ثانیه طول خواهد کشید لطفا ")
                                                      res = await orm.AddServer(Name,domain,UrlPanel,userName,Password,"normal",catId,IsAddToUsers)
                                                      if res[0]== True:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))      
                                                        return
                                                      else:
                                                        await call.message.reply(res[1],reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                                                        return 
                                              else:
                                                  await Canesel_Key(c,call.message,call.from_user.id)     
                                                  return              
                                           else:
                                                await call.message.reply("دسته بندی پیدا نشد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(),resize_keyboard=True))
                                         else:
                                            await Canesel_Key(c,call.message,call.from_user.id)     
                                            return               
                                 else:
                                    await Canesel_Key(c,call.message,call.from_user.id)     
                                    return  
                        
                            else:
                                            await Canesel_Key(c,call.message,call.from_user.id)     
                                            return              
                        else:
                            await Canesel_Key(c,call.message,call.from_user.id)     
                            return   

                   else:
                          await Canesel_Key(c,call.message,call.from_user.id)     
                          return    
             else:
                        await Canesel_Key(c,call.message,call.from_user.id)     
                        return                          
       else:
              await Canesel_Key(c,call.message,call.from_user.id)     
              return         
   if call.data == "manageServers":
       serversbtns = await orm.GetAllServersBtns()
       await call.edit_message_text("""مدیریت سرور ها 🌐
                                    
سرور های خود را در این بخش مدیریت کنید 🌐
                                    
🌐 /start                                    
                                    """,reply_markup=InlineKeyboardMarkup(serversbtns))
       return
       
#    if "manageServer_" in call.data :
#     serverId = call.data.split("_")[1]
#     server =   await orm.GetServer(serverId)
#     btns = []
    
       
    
#     btns.append([InlineKeyboardButton("نام کاربری 👤 ",callback_data="ARS"),InlineKeyboardButton(server[1],callback_data="EditEmailS")])   
#     btns.append([InlineKeyboardButton("کلمه عبور 👤 ",callback_data="ARS"),InlineKeyboardButton(server[2],callback_data="EditPassS")])   
#     btns.append([InlineKeyboardButton("آدرس",callback_data="ARS"),InlineKeyboardButton(server[3],callback_data="EditUrlS")])   
#     btns.append([InlineKeyboardButton("Authentication key",callback_data="ARS"),InlineKeyboardButton(server[3],callback_data="EditAuth")])   
#     btns.append([InlineKeyboardButton("Background Path",callback_data="ARS"),InlineKeyboardButton(server[4],callback_data="EditkeyS")])   
#     btns.append([InlineKeyboardButton("بازگشت",callback_data="mainAdmin")])
#     await call.edit_message_text("به بخش مدیریت سرور خوش آمدید در این قسمت میتوانید تنظیمات اتصال سرور خود را مدیریت کنید",reply_markup=InlineKeyboardMarkup(btns))  
#     return
   if "AcceptDeleteServer_" in call.data:
       serverId = call.data.split("_")[1]
       res =await orm.DeleteServer(serverId)
       if res ==True:
           await call.edit_message_text("✅ حذف موفقیت آمیز بود",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت",callback_data="manageServers")]]))
           return
       else:
              await call.answer("هنگام پاک کردن مشکلی پیش آمد",True)
              return
   if "DeleteServer_" in call.data:
     serverId = call.data.split("_")[1]
     await call.edit_message_text("""⚠️ | آیا از حذف سرور خود مطمئن هستید؟ 
     
در صورتی که سرور شما جزوی از مجموعه ساب باشد در محاسبه سرویس های کاربران به مشکل خواهیم خورد  

/start                                      
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ تایید",callback_data=f"AcceptDeleteServer_{serverId}"),InlineKeyboardButton("بازگشت",callback_data="manageServers")]]))
     return
   if call.data =="EditEmailS" :
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       Email = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا ایمیل را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         Email =  answer.text
         if await orm.EditEmailServer(Email) == True:
           await call.message.reply("ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
           return
         else:
            
            await call.message.reply("ویرایش موفقیت امیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
            return
       else:  
          await Canesel_Key(c,call.message,call.from_user.id) 
          return  
   if call.data =="EditPassS" :
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       password = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا پسورد را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         password =  answer.text
         if await orm.EditpasswordServer(password) == True:
             await call.message.reply("ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
             return
         else:
            
            await call.message.reply("ویرایش موفقیت امیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
            return
       else:  
          await Canesel_Key(c,call.message,call.from_user.id)   
          return
   if call.data =="EditUrlS":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       Url = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا آدرس جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         Url =  answer.text
         if await orm.EditUrlServer(Url) == True:
          await call.message.reply("ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
         else:
            
            await call.message.reply("ویرایش موفقیت امیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
            
       else:  
          await Canesel_Key(c,call.message,call.from_user.id)   
   if call.data =="arddServer":
       
       
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       Email = ""
       Password = ""
       Url =""
       answer = await pyromod.Chat.ask(text="🔻 لطفا ایمیل را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         Email =  answer.text
         answer = await pyromod.Chat.ask(text="🔻 لطفا کلمه عبور را وارد کنید" , self=call.message.chat)
         if answer.text!= "انصراف":
          Password= answer.text
          answer = await pyromod.Chat.ask(text="🔻 لطفا ادرس را وارد کنید" , self=call.message.chat)
          if answer.text!= "انصراف":
           Url = answer.text
           try: 
            headers = {"Content-Type" :"application/x-www-form-urlencoded","Cookie":"dark_mode=1; i18n=en-US"}
           
            data = {"email":f"{Email}",
                "password":f"{Password}"}
            async with httpx.AsyncClient() as client:
            
              response = await client.post(f'https://{Url.split("/")[2]}/api/v1/passport/auth/login',data=data,headers=headers)

              if response.status_code == 200:
                 
                auth = json.loads(response.content)['data']['auth_data']
                await orm.AddServer(Email,Password, f"https://{Url.split('/')[2]}",auth,Url.split("/")[3])
                await call.message.reply("سرور اضافه شد")  
                await Canesel_Key(c,call.message,call.from_user.id)   
                return
              else:
                 await call.message.reply("درخواست موفقیت امیز نبود")  
                 
                 await Canesel_Key(c,call.message,call.from_user.id)   
                 return
           except :
              await call.message.reply("درخواست موفقیت امیز نبود")  

              await Canesel_Key(c,call.message,call.from_user.id)   

              return
          else:
           await Canesel_Key(c,call.message,call.from_user.id)   


         else:
           await Canesel_Key(c,call.message,call.from_user.id)   
           return
       else:
            
          await Canesel_Key(c,call.message,call.from_user.id)
          return
   if call.data =="EditAuth":
   
      await call.answer("کمی صبر کنید")
      result = await orm.ChangeServerAuth()
      if result == True :
         btns =  await orm.GetServerManageBtns()
         await call.answer("ویرایش موفقیت امیز بود")
         await  call.edit_message_reply_markup(InlineKeyboardMarkup(btns))
         return
      else:
               await call.answer("اتصال را بررسی کنید , تغییر موفقیت امیز نبود ",True)
               return

   if call.data =="EditkeyS":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       Key = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا Background Path  جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         Background =  answer.text
         if await orm.EditBackgroundServer(Background) == True:
            await call.message.reply("ویرایش موفقیت امیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
            return
         else:
            
            await call.message.reply("ویرایش موفقیت امیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
            
            return
       else:  
          await Canesel_Key(c,call.message,call.from_user.id)   
          return
   if call.data == "businnes":
       await call.edit_message_text("""🔰 بخش بیزینس 

شما میتونید تو این بخش تنظیمات خودکاری را کانفیگ کنید که به کسب و کار شما رونق بدهد !
                                    
♦️ /start                                    
""",reply_markup= InlineKeyboardMarkup( [
        [InlineKeyboardButton("🌟 تست رایگان",callback_data="FreeTestManage"),InlineKeyboardButton("(به زودی) 🎁 قرعه کشی",callback_data="ARS")],
        [InlineKeyboardButton("🗒 مدیریت ارسال پیام",callback_data="sendChanellMes")],
        [InlineKeyboardButton("منو ادمین🔙 ",callback_data="mainAdmin")]


    ]))
   if call.data == "FreeTestManage":
       res= await orm.GetManageTestBtn()
       await call.edit_message_text(""" 🌟 تست رایگان
به بخش مدیریت تست رایگان خوش آمدید
 
Admin Panel /start
 """,reply_markup=InlineKeyboardMarkup(res))
   if call.data ==  "LotteryManage":
          btns = await orm.LotteryManageBtns()
          await call.edit_message_text("""💥 به بخش مدیریت قرعه کشی خوش آمدید
                                       
🔰 /start                                     
                                       """,reply_markup=InlineKeyboardMarkup(btns))
   if call.data =="sendChanellMes":
         btns =await orm.GetmesChanell()
         await call.edit_message_text("""🔰 تنظیمات ارسال پیام
                                      
در این بخش میتوانید تنظیماتی را برای ارسال پیام در چنل خود به صورت مکرر به انجام برسانید تا نیازی به ادمین نباشد!
                                      
🔰 /start                                    
""",reply_markup=InlineKeyboardMarkup(btns))  
   if "LotteryStateEdit_" in call.data:
       
       stat = 0
       if int(call.data.split("_")[1])== 0:
           stat =1
       await orm.UpdateLotteryState(stat)
       await call.message.delete()

       btns = await orm.LotteryManageBtns()
       await call.message.reply("""💥 به بخش مدیریت قرعه کشی خوش آمدید
                                       
🔰 /start                                     
                                       """,reply_markup=InlineKeyboardMarkup(btns))
   if call.data =="UserNumberLottery":
       await call.message.delete()
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا تعداد جدید را ارسال کنید" , self=call.message.chat)
       
       if answer.text!= "انصراف":      
         try:
               number = int(answer.text)  
               if number <= 0:
                  await call.message.reply("بزرگتر از صفر فقط عدد")
                  return
                   
               await orm.UpdateLotteryUserNumber(number)
               btns = await orm.LotteryManageBtns()
               await call.message.reply("""💥 به بخش مدیریت قرعه کشی خوش آمدید
                                       
🔰 /start                                     
                                       """,reply_markup=InlineKeyboardMarkup(btns))
         except:
               await call.message.reply("فقط عدد")
               await Canesel_Key(c,call.message,call.from_user.id)   
            
               return   
   if call.data == "AddPlanLottery":
      plans = await orm.GetAllPlanName()
      btns = []
      if plans !=None:
          for plan in plans:
              btns.append([InlineKeyboardButton(plan[0],callback_data=f"AddFinalyLottery_{plan[1]}")])
      else:
          btns.append([InlineKeyboardButton("پلنی موجود نیست",callback_data="ARS")])
      await call.edit_message_text("لطفا پلن قرعه کشی را انتخاب کنید",reply_markup=InlineKeyboardMarkup(btns))
   if "AddFinalyLottery_" in call.data:
         planId =call.data.split("_")[1]
         await orm.UpdatePlanIdLottery(planId)
         await call.message.delete()

         btns = await orm.LotteryManageBtns()
         await call.message.reply("""💥 به بخش مدیریت قرعه کشی خوش آمدید
                                       
🔰 /start                                     
                                       """,reply_markup=InlineKeyboardMarkup(btns))
   if call.data =="LotteryTimeEdit":
       await call.message.delete()
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا زمان جدید را ارسال کنید" , self=call.message.chat)
       
       if answer.text!= "انصراف":      
         try:
             days = int(answer.text)
             await orm.UpdateDaysLottery(days)
             btns = await orm.LotteryManageBtns()
             await call.message.reply("""💥 به بخش مدیریت قرعه کشی خوش آمدید
                                       
🔰 /start                                     
                                       """,reply_markup=InlineKeyboardMarkup(btns))
         except:
               await call.message.reply("فقط عدد")
               await Canesel_Key(c,call.message,call.from_user.id)   
            
               return  
       else:
           await Canesel_Key(c,call.message,call.from_user.id)   
           return 
   if call.data =="AddMesChanel":
       await call.message.delete()
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       mesId =""
    
       answer = await pyromod.Chat.ask(text=""" 🔻 لطفا متن را ارسال کنید

درصورتی که متن نیاز نداری خالی بگذارید                                                                              
                                       """ , self=call.message.chat)

       if answer.text!= "انصراف":
              mesId = answer.id
              
              res = await orm.addMessageChanell(mesId,call.from_user.id)
              if res[0] ==True:
                  btns = await orm.GetMessageSettingBtns(res[1])
                  await call.message.reply("✅ اضافه شد ",reply_markup=InlineKeyboardMarkup(btns))
                  return
              else:
                  await call.message.reply("❌ اضافه نشد ")
       else:
           await Canesel_Key(c,call.message,call.from_user.id)   
           return    
   if "GetMesCahnell_" in call.data:
       data = call.data.split("_")[1]
       btns = await orm.GetMessageSettingBtns(data)
       await call.edit_message_text("ویرایش مسیج زمان بندی شده",reply_markup=InlineKeyboardMarkup(btns))
   if "GetmessageShow_" in call.data:
       data = await orm.GetMessageDetails(call.data.split("_")[1])
       await c.forward_messages(call.from_user.id,data[5],data[1])
   if "ChangeStatMes_" in call.data:
       data = call.data.split("_")
       stat = 0
       if int(data[2]) == 0:
           stat = 1
       await orm.ChangeStatMessage(data[1],stat)
       btns = await orm.GetMessageSettingBtnsEditStat(data[1],stat)
       await call.message.delete()

       await call.message.reply("ویرایش مسیج زمان بندی شده",reply_markup=InlineKeyboardMarkup(btns))    
       return
   if "EditMesChanell_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا پیام جدید را ارسال کنید" , self=call.message.chat)
       mesId = 0  
       if answer.text!= "انصراف":      
           try:
               mesId = answer.id
               await orm.EditMessageChanell(mesId,call.from_user.id,data)
           except:
               await call.message.reply("هنگام ویرایش مشکلی پیش آمد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
               return   
   if "ChangetimeSendMes_" in call.data :
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       answer = await pyromod.Chat.ask(text="🔻 لطفا روز جدید را ارسال کنید" , self=call.message.chat)
       newDays = 0  
       if answer.text!= "انصراف":      
           try:
               newDays = int(answer.text)
               if newDays <= 0:
                  await call.message.reply("❌ بزرگتر از صفر لطفا فقط عدد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                  return
               
               await orm.EditMessageDays(newDays,data)
               btns = await orm.GetMessageSettingBtns(data)
               await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))    
               return
           except:
               await call.message.reply("❌ لطفا فقط عدد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
               return
       else:
               await Canesel_Key(c,call.message,call.from_user.id)   
               return    
   if call.data == "AddTest":
       await call.message.delete()
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       
       Volume = ""
       Days = ""
       countGet = 0
       try:
        answer = await pyromod.Chat.ask(text="🔻 لطفا تعداد را ارسال کنید" , self=call.message.chat)

        if answer.text!= "انصراف":
         countGet = int(answer.text)
         answer = await pyromod.Chat.ask(text="🔻 لطفا حجم را ارسال کنید" , self=call.message.chat)

         if answer.text!= "انصراف":
            Volume = float(answer.text)
            answer = await pyromod.Chat.ask(text="🔻 لطفا روز را ارسال کنید" , self=call.message.chat)
            if answer.text!= "انصراف":
                Days = int(answer.text)
                await call.message.reply("🫴🏻 دسته بندی را انتخاب کنید ",reply_markup=ReplyKeyboardMarkup(await orm.GetCatBtnsSelect(),resize_keyboard=True))
                answer = await pyromod.Chat.ask(call.message.chat,"♦️ در صورتی که در لیست موجود نیست ابتدا باید دسته بندی ایجاد کنید") 
                if answer.text != "انصراف":
                 catId = await orm.GetCatByName(answer.text)   
                 if catId == None:
                       await call.message.reply("دسته بندی یافت نشد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
    
                       return    
                 CatType = await orm.GetCatType(catId[0])
                 serverId = 0
                 if CatType == "normal" : 
                      await call.message.reply("🫴🏻  سرور را انتخاب کنید ",reply_markup=ReplyKeyboardMarkup(await orm.GetServerCatForTest(catId[0]),resize_keyboard=True))
                      answer = await pyromod.Chat.ask(call.message.chat,"♦️ در صورتی که در لیست موجود نیست ابتدا باید دسته بندی ایجاد کنید") 
                      if answer.text != "انصراف":
                          serverId = await orm.GetServerByName(answer.text) 
                          if serverId == 0:
                               await call.message.reply(" سرور یافت نشد")  
                               await Canesel_Key(c,call.message,call.from_user.id)   
                               return    
                      else:
                       await Canesel_Key(c,call.message,call.from_user.id)   
                       return   
                      
                 res = await orm.AddTest(Days,Volume,countGet,serverId,catId[0]) 
                 if res == True:
                    res= await orm.GetManageTestBtn()
                    await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
                    await call.message.reply(""" 🌟 تست رایگان
به بخش مدیریت تست رایگان خوش آمدید
 
Admin Panel /start
 """,reply_markup=InlineKeyboardMarkup(res))
                 else:
                       await call.message.reply("هنگام افزودن مشکلی پیش امده",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
                       
                       return    
                else:

                        await Canesel_Key(c,call.message,call.from_user.id)  
                        return
            else:
                
             await Canesel_Key(c,call.message,call.from_user.id)   
             return
         else:
           await Canesel_Key(c,call.message,call.from_user.id)   
           return
        else:
           await Canesel_Key(c,call.message,call.from_user.id)   
           return
       except:
           await call.message.reply("لطفا فقط عدد",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))

           return
   if "DeleteTest_" in call.data:
       data =call.data.split("_")[1]
       res = await orm.DeleteTestFree(data)
       if res == True:
                 await call.answer("🟢 حذف موفقیت آمیز بود")
                 res= await orm.GetManageTestBtn()
                 await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(res))
       else:
         await call.answer("حذف موفقیت امیز نبود")    
   if call.data == "AllMess":
      res = await orm.GetPublicMessage()
      btns=[]
      if res == None:
         btns.append([InlineKeyboardButton("افزودن پیام همگانی",callback_data="AddMessage")])
      else:
            btns.append([InlineKeyboardButton(res[1],callback_data="ARS"),InlineKeyboardButton("🟢" if res[4] == 0 else "🔴",callback_data=f"ARS")])
            btns.append([InlineKeyboardButton("❌",callback_data=f"DelMessage_{res[0]}"),InlineKeyboardButton(f"ارسال شده : {res[3]}",callback_data=f"ARS")])
      btns.append([InlineKeyboardButton("بازگشت",callback_data="mainAdmin")])      
      await call.edit_message_text(""" 🗒به بخش مدیریت پیام همگانی خوش امدید
      
                                   
▫️▪️▫️▪️▫️
                                   """,reply_markup=InlineKeyboardMarkup(btns))
      return
   if call.data =="AddMessage":
       res = await orm.GetPublicMessage()
       btns=[]
       if res != None:
          await call.answer("یک پیام در صف ارسال میباشد")
          return
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       Title = ""
       Description = ""
       answer = await pyromod.Chat.ask(text="🔻 لطفا عنوان را ارسال کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         Title =  answer.text
         answer = await pyromod.Chat.ask(text="🔻 لطفا متن یا تصویر را ارسال کنید" , self=call.message.chat)
         if answer.text!= "انصراف":
          photo = "empty"   
          Description = "empty"
          if answer.photo != None:
              photo = answer.photo.file_id
              if answer.caption != None:
                  Description = answer.caption
                  
          elif answer.text != None : 
            Description= answer.text
          else:
             await call.message.reply("لطفا به درستی ارسال کنید")
             await Canesel_Key(c,call.message,call.from_user.id)   
             return
          await orm.AddNewPublicMessage(Title ,Description,call.from_user.id,photo)
          await call.message.reply("✅ اضافه شد",reply_markup = ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          return
         else:
             await Canesel_Key(c,call.message,call.from_user.id)   
             return

       else:
            
          await Canesel_Key(c,call.message,call.from_user.id)
          return
   if "EditNameCat_" in call.data:
      data = call.data.split("_")[1]
      await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
      answer = await pyromod.Chat.ask(text="🔻 لطفا نام جدید را وارد کنید" , self=call.message.chat)
      if answer.text!= "انصراف":
        await call.message.delete()

        await orm.UpdateCatName(data, answer.text)

        await call.message.reply("✅ ویرایش موفقیت امیز",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
        return
      else:
             await Canesel_Key(c,call.message,call.from_user.id)   
             return
   
   if "DelMessage_" in call.data:
    data = call.data.split("_")[1]
    await orm.DeletePublicMess(data)
    res = await orm.GetPublicMessage()
    btns=[]
    if res == None:
         btns.append([InlineKeyboardButton("افزودن پیام همگانی",callback_data="AddMessage")])
    else:
            btns.append([InlineKeyboardButton(res[1],callback_data="ARS"),InlineKeyboardButton("🟢" if res[4] == 0 else "🔴")])
            btns.append([InlineKeyboardButton("❌",callback_data=f"DelMessage_{res[0]}"),InlineKeyboardButton(f"ارسال شده : {res[3]}")])
    btns.append([InlineKeyboardButton("بازگشت",callback_data="mainAdmin")])      
    await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))
    return
   if "EditCatSett_" in call.data:
        catId = call.data.split("_")[1]
        btns = await orm.GetCatEditBtns(catId)
        await call.edit_message_text("🗒 سرور های این دسته بندی",reply_markup=InlineKeyboardMarkup(btns))

   if call.data == "managecategury" :
      catbtns = await orm.GetCatBtns()
      await call.edit_message_text("🗂 به بخش مدیریت دسته بندی ها خوش امدید\n\n ▪️▫️▪️▫️▪️▫️ ",reply_markup=InlineKeyboardMarkup(catbtns))
      return
   if call.data == "AddCat":
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا نام دسته بندی را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
        await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["سابسکرایب","معمولی"],["انصراف"]],resize_keyboard=True))
        titleCat = answer.text
        answer = await pyromod.Chat.ask(text="🔻 لطفا نوع دسته بندی را وارد کنید" , self=call.message.chat)
        if answer.text != "انصراف":
          if answer.text == "سابسکرایب" :
           if await orm.addCat(titleCat,"sub") == True:
             await call.message.reply("با موفقیت اضافه شد ✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
             return
           else:
            
            await call.message.reply("هنگام افزودن مشکلی پیش امده")
            return
          elif answer.text == "معمولی":
           if await orm.addCat(titleCat,"normal") == True:
             await call.message.reply("با موفقیت اضافه شد ✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
             return
           else:
            
            await call.message.reply("هنگام افزودن مشکلی پیش امده")
            return
       else:
             await Canesel_Key(c,call.message,call.from_user.id)   
             return
   
   if "StateCat_" in call.data:
         try:  
           await call.answer("کمی صبر کنید...")
           catId = call.data.split("_")[1]
           show = int(call.data.split("_")[2])
           show  = 0 if show ==1 else 1
           await orm.UpdateCatState(catId,show)
           await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(await orm.GetCatBtns()))    
           return       
         except:
             await call.answer("هنگام تغییر مشکلی پیش آمد",True)
   if "DeleteCat_"  in call.data:
      data = call.data.split("_")[1]
      await orm.DeleteCat(data)
      await call.answer("✅")
      await call.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(await orm.GetCatBtns()))
      return
   if call.data == "managePlan":
      btns = await orm.GetAllPlansList()
      await call.edit_message_text(  "🔺 به بخش مدیریت پلن ها خوش امدید \n\n ▫️▪️▫️▪️▫️▪️▫️  ",  reply_markup=InlineKeyboardMarkup(btns))
  
   if call.data ==  "AddPlan":
       if await orm.IsServerAny() == False:
          await call.answer("سرور یافت نشد..")
          return 
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       planName = ""
       DescriptionPlan = ""
       monthCount = 0
       Price = 0
       Valume = 0
       countShell = 0
       answer = await pyromod.Chat.ask(text="🔻 لطفا نام پلن را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          planName = answer.text
          answer = await pyromod.Chat.ask(text="🔻 لطفا توضیحات را وارد کنید" , self=call.message.chat)
          if answer.text!= "انصراف":
            DescriptionPlan = answer.text
            answer = await pyromod.Chat.ask(text="🔻 لطفا تعداد ماه را وارد کنید" , self=call.message.chat)
            if answer.text!= "انصراف":
                #   try:
                   monthCount = int(answer.text)
                   answer = await pyromod.Chat.ask(text="🔻 لطفا قیمت را وارد کنید" , self=call.message.chat)
                   if answer.text!= "انصراف":
                    Price  = int(answer.text)
                    answer = await pyromod.Chat.ask(text="🔻 لطفا حجم را وارد کنید" , self=call.message.chat)
                    if answer.text!= "انصراف":
                       
                       Valume  = float(answer.text)
                     
                       answer = await pyromod.Chat.ask(text="🔻 لطفا تعداد فروش را وارد کنید" , self=call.message.chat)
                       if answer.text!= "انصراف":
                          countShell =  answer.text
                          
                          btns =  await orm.GetCatBtnsReply()
                          await call.message.reply("لطفا لیست دسته بندی انتخاب کنید",reply_markup=ReplyKeyboardMarkup(btns,resize_keyboard=True)) 
                          answer = await pyromod.Chat.ask(text="🔻 لطفا از لیست انتخاب کنید" , self=call.message.chat)
                          if answer.text!= "انصراف":
                             CatId = await orm.GetCatByName(answer.text)
                             if CatId == None:
                                await call.message.reply("دسته بندی یافت نشد...")
                                await Canesel_Key(c,call.message,call.from_user.id)    
                                return
                             else:
                               
                                answer = await pyromod.Chat.ask(text="🔻 0 نامحدود است* \n لطفا محدودیت کاربر را وارد کنید" , self=call.message.chat)
                                if answer.text!= "انصراف":
                                 userlimit ="" if answer.text == "0" else answer.text
                                 added = await orm.AddPlan(planName,DescriptionPlan,monthCount,Price,Valume,countShell,CatId[0],0,userlimit)
                                 if added == True:
                                     await call.message.reply("پلن ثبت شد ...",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
                                     return
                                 else:
                                  await call.message.reply("پلن ثبت نشد ...")
                                  await Canesel_Key(c,call.message,call.from_user.id)    
                                  return
                                else:
                                   await Canesel_Key(c,call.message,call.from_user.id)       
                                   return
                              
                                   

                             
                       else:
                          await Canesel_Key(c,call.message,call.from_user.id) 
                          return    
                    else:
                     await Canesel_Key(c,call.message,call.from_user.id)  
                     return    
                   else:
                    await Canesel_Key(c,call.message,call.from_user.id)      
                    return

                #   except:
                #     await call.message.reply("لطفا فقط عدد")
                #     await Canesel_Key(c,call.message,call.from_user.id)      
                #     return 
                  
            else:
                await Canesel_Key(c,call.message,call.from_user.id)      
                return
          else:
             await Canesel_Key(c,call.message,call.from_user.id)      
             return
       else:
             await Canesel_Key(c,call.message,call.from_user.id)      
             return
   if "EditPlan_" in call.data:
      data = call.data.split("_")[1]
      btns =await orm.GetEditPlansBtns(data)
      await call.edit_message_text("به بخش ویرایش پلن مورد نظر خود خوش امدید",reply_markup=InlineKeyboardMarkup(btns))
      return
   if "EditPName_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا نام جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         
          if await orm.EditPlanName(answer.text,data) == True:
            await call.message.reply("✅ ویرایش موفقیت آمیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
          else:
                         await call.message.reply("❌ ویرایش موفقیت آمیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         return
       else:   

             await Canesel_Key(c,call.message,call.from_user.id)      
             return

   if "EditDPlane_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا توضیحات جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         
          if await orm.EditPlanDescription(answer.text,data) == True:
            await call.message.reply("✅ ویرایش موفقیت آمیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
            return
          else:
                         await call.message.reply("❌ ویرایش موفقیت آمیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         return
       else:   

             await Canesel_Key(c,call.message,call.from_user.id)      
             return

   if "EditMPlan_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       
       answer = await pyromod.Chat.ask(text="🔻 لطفا ماه جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          try:
             month  = int(answer.text)
          except:
                await call.message.reply("لطفا فقط عدد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         
                return
          if await orm.EditPlanMonth(month,data) == True:
              await call.message.reply("✅  ویرایش موفقیت آمیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

          else:
                         await call.message.reply("❌ ویرایش موفقیت آمیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         return
       else:   

             await Canesel_Key(c,call.message,call.from_user.id)      
             return
   if "EditPricePlan_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       
       answer = await pyromod.Chat.ask(text="🔻 لطفا قیمت جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          try:
             month  = int(answer.text)
          except:
                await call.message.reply("لطفا فقط عدد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         
                return
          if await orm.EditPlanPrice(month,data) == True:
              await call.message.reply("✅  ویرایش موفقیت آمیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

          else:
                         await call.message.reply("❌ ویرایش موفقیت آمیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         return
       else:   

             await Canesel_Key(c,call.message,call.from_user.id)      
             return       
   if "EditVPlan_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       
       answer = await pyromod.Chat.ask(text="🔻 لطفا حجم جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
          try:
             vloume  = float(answer.text)
          except:
                await call.message.reply("لطفا فقط عدد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         
                return
          if await orm.EditPlanVloume(vloume,data) == True:
              await call.message.reply("✅  ویرایش موفقیت آمیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

          else:
                         await call.message.reply("❌ ویرایش موفقیت آمیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         return
       else:   

             await Canesel_Key(c,call.message,call.from_user.id)      
   if "CatListToPlan_" in call.data:
    planId = call.data.split("_")[1]
    btns = await orm.GetCatPlanbtnsSelect(planId)
    await call.edit_message_text("دسته بندی که میخواهید به پلن شما اضافه شود را انتخاب کنید",reply_markup= InlineKeyboardMarkup(btns)) 
    return
   if "DeleteCatPlan_" in call.data :
        serverId = call.data.split("_")[1]
        res = await orm.DeleteCatPlan(serverId)
        if res ==True:
           await call.answer("✅ با موفقیت حذف شد",True)
           await call.message.delete()
           return
        else:
            await call.answer("هنگام حذف مشکلی پیش آمد") 
   if "AddCatToPlan_" in call.data:
       PlanId = call.data.split("_")[1]
       CatId = call.data.split("_")[2]
       res = await orm.AddCatToPlan(PlanId,CatId)
       if res == True:
           await call.answer("✅ با موفقیت افزوده شد ")
           btns = await orm.GetCatsPlan(PlanId)
           await call.message.delete()
           await call.message.reply("لیست دسته بندی های پلن انتخابی",reply_markup=InlineKeyboardMarkup(btns))
           return
       else:
           await call.answer("این دسته بندی قبلا افزوده شده یا هنگام افزودن مشکلی پیش آمد",True) 
           return
   if "DeleteCatPlan_" in call.data:
           PlanId = call.data.split("_")[1]
   if "EditCPlan_" in call.data:
    PlanId = call.data.split("_")[1]
    btns = await orm.GetCatsPlan(PlanId)
    await call.edit_message_text("لیست دسته بندی های پلن انتخابی",reply_markup=InlineKeyboardMarkup(btns))
    return
   if "EditSPlan_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
       
       answer = await pyromod.Chat.ask(text="🔻 لطفا تعداد فروش جدید را وارد کنید" , self=call.message.chat)

       if answer.text!= "انصراف":
          try:
             month  = int(answer.text)
          except:
                await call.message.reply("لطفا فقط عدد ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         
                return
          if await orm.EditPlanCountShel(month,data) == True:
              await call.message.reply("✅  ویرایش موفقیت آمیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   

          else:
                         await call.message.reply("❌ ویرایش موفقیت آمیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         return
       else:   

             await Canesel_Key(c,call.message,call.from_user.id)      
             return       
       
   if "EditSpeedPlan_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا سرعت جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         
          if await orm.EditPlanSpeed(answer.text,data) == True:
            await call.message.reply("✅ ویرایش موفقیت آمیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
          else:
                         await call.message.reply("❌ ویرایش موفقیت آمیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         return
       else:   

             await Canesel_Key(c,call.message,call.from_user.id)      
             return    
   if "EditUserPlan_" in call.data:
       data = call.data.split("_")[1]
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا کاربران جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
         
          if await orm.EditPlanUser(answer.text,data) == True:
            await call.message.reply("✅ ویرایش موفقیت آمیز بود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
          else:
                         await call.message.reply("❌ ویرایش موفقیت آمیز نبود",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                         return
       else:   

             await Canesel_Key(c,call.message,call.from_user.id)      
             return     
   if "editCardAdminNumber" == call.data:
      
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا شماره کارت جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
        await orm.EditCardNumber(answer.text)

        await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
        return
       else:
           await Canesel_Key(c,call.message,call.from_user.id)      
           return     
   if "CardAdminName" == call.data:
      
       await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
    
       answer = await pyromod.Chat.ask(text="🔻 لطفا به نام شماره کارت جدید را وارد کنید" , self=call.message.chat)
       if answer.text!= "انصراف":
        await orm.EditCardNamerName(answer.text)
        
        await call.message.reply("✅",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))
        return
       else:
           await Canesel_Key(c,call.message,call.from_user.id)      
           return     
         
   if "autoCard_" in call.data:
      onOroff = call.data.split("_")[1] 
      await call.edit_message_text("""
پرداخت خودکار کارت به کارت توسط سوپال 
                                   
میباشد ابتدا درون سایت  ثبت نام کنید 
      
جزییات بیشتر 
👇🏻👇🏻👇🏻
https://sopall.solarteam.site/info
""")
      await call.message.reply("⌛️",reply_markup=ReplyKeyboardMarkup([["انصراف"]],resize_keyboard=True))
      answer = await pyromod.Chat.ask(text="🔻 لطفا ایمیل را وارد کنید" , self=call.message.chat)
      email = ""
      password = ""
      apiKey = ""
      if answer .text != "انصراف":
         email = answer.text
         answer = await pyromod.Chat.ask(text="🔻 لطفا پسورد را وارد کنید" , self=call.message.chat)
         if answer.text != "انصراف":
            password = answer.text
            answer = await pyromod.Chat.ask(text="🔻 لطفا APIkEY را وارد کنید" , self=call.message.chat)
            if answer .text != "انصراف":
                apiKey = answer.text
                res =  await orm.ChangeCardAutoData(email,password,apiKey,onOroff)
                if res ==True :
                    await call.message.reply("✅ فعال سازی موفقیت آمیز بود ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                else:
                    await call.message.reply("❌ فعال سازی موفقیت آمیز نبود ",reply_markup=ReplyKeyboardMarkup(await orm.GetMainKeys(call.from_user.id),resize_keyboard=True))   
                  
                try:   
                     res=  await  orm.GetSettingBtns()
                     await call.message.reply("🔻 به بخش مدیریت ربات خوش امدید\n\nتنظیمات دلخواه خود را اعمال کنید",reply_markup=InlineKeyboardMarkup(res))
                     return
                except  :
         
                          await call.message.reply("هنگام دریافت اطلاعات مشکلی پیش امد")  
                          return
         else:
            await Canesel_Key(c,call.message,call.from_user.id)      
            return 
      else :
              
           await Canesel_Key(c,call.message,call.from_user.id)      
           return    