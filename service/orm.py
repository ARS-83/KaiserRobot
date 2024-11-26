from pyrogram.types import  InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from db import Context
import json
import aiofiles
db_manager = Context.DatabaseManager()
ServerManager = Context.ServerDataManager()
import datetime
import httpx
from uuid import uuid4
import random
import ast
import string
import asyncio
import base64
import time
import jdatetime
import qrcode
from io import BytesIO

async def DeleteUserService(app):
    
    
    services =  await db_manager.execute_query_all("SELECT * FROM Service WHERE State = 0 and isDelete = 0")
    for service in services:
      
        serverIds  = ast.literal_eval(service[17])
        noneTrue = False
        try:
          
          for serverid in serverIds:
            server = await db_manager.execute_query_one(f'SELECT * FROM Server WHERE Id = {serverid}')
            try:   
             origin = server[3].split("/")
             limits = httpx.Limits(max_connections=1)  
             async with httpx.AsyncClient(limits=limits) as client:
              response = None 
           
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
                    'Cookie': f'lang=en-US; {server[8]}'
                }
        # https://adminmain.panelshams.site:8383/navid-shams-ali-8383-root/panel/inbound/1/delClient/948ac7a2-91a7-47b9-8c6e-2f7bd9c85744
              try:
               response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/{server[10]}/delClient/{service[4]}',headers=headers)
              except:
               response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/{server[10]}/delClient/{service[4]}',headers=headers)
                  
            except:
                noneTrue = True
          if noneTrue == False:
              
            await db_manager.QueryWidthOutValue(f'UPDATE Service SET isDelete = 1 WHERE Id = {service[0]}')              
        except:
                pass
async def ReadFileText():
   async with aiofiles.open('Config/Messages.json', mode='r',encoding='utf-8') as f: 
      res =   json.loads(await f.read())
   return res   
   
def convert_link_vless(vless_account: str):
    content = vless_account[8:]
    Id = content.split("@")[0]
    return Id
def convert_link_vmess(vmess_account: str):
    try:
        base64_content = vmess_account[8:]
        base64_bytes = base64_content.encode("ascii")

        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        x = sample_string.replace("\'", "\"")
        if "b{" in str(x):
          x= x[1:]
        return json.loads(str(x))["id"]
  
    except:
        return "configKosSher"
    
def wings(vmess_account: str):
    base64_content = vmess_account[8:]
    base64_decoded_content = base64.b64decode(
        base64_content.encode('utf-8')).decode('utf-8', 'ignore')
    return json.loads(base64_decoded_content)





def GetConfig(stream:str, uuid: str, email: str, port: str, protocol: str, serverName: str):
    # Your Remark
    inboundSetting = json.loads(stream)
  
    remark = email

    path = None
    host = "none"
    domainName = None
    serviceName = None
    headerType = None
    alpn = None
    kcpType = None
    grpcSecurity = None
    
   # Get Security 
    fingerPrint = ""
   
    tls = inboundSetting["security"]

    if  tls == "reality":
      
 
      fingerPrint = inboundSetting['realitySettings']['settings']['fingerprint']
      global publicKey 
      publicKey =  inboundSetting['realitySettings']['settings']['publicKey']
      global shortIds
      shortIds = inboundSetting['realitySettings']['shortIds'][0]
      global spiderX
      spiderX = inboundSetting['realitySettings']['settings']['spiderX']
      global sni
      sni = inboundSetting['realitySettings']['serverNames'][0]
  
    if tls == "tls":
        domainName = inboundSetting["tlsSettings"]["serverName"]
    elif tls == "xtls":
        domainName = inboundSetting["xtlsSettings"]["serverName"]
        alpn =  inboundSetting["tlsSettings"][0]["certificates"]["alpn"][0]
        global allowInsecure 

        allowInsecure = inboundSetting["tlsSettings"][0]["certificates"]["allowInsecure"]
   
   
   #    Get Net Type Setting
    netType = inboundSetting["network"]
    if netType == "grpc":
        serviceName = inboundSetting["grpcSettings"]["serviceName"]
        grpcSecurity = inboundSetting["security"]
    elif netType == "tcp":
        headerType = inboundSetting["tcpSettings"]["header"]["type"]
        if headerType != 'none':
            
          path = inboundSetting["tcpSettings"]["header"]["request"]["path"][0]
          try:
           try:
              
             host = inboundSetting["tcpSettings"]["header"]["request"]["headers"]["host"][0]
           except:
             host = inboundSetting["tcpSettings"]["header"]["request"]["headers"]["Host"][0]
          except:  
              host = ""       
                 
    elif netType == "ws":
       
        path = inboundSetting["wsSettings"]["path"]
        try:
            host = inboundSetting["wsSettings"]["headers"]["host"]
        except:
            host=""    
    elif netType == "kcp":
        kcpType = inboundSetting["kcpSettings"]["header"]["type"]
        kcpSeed = inboundSetting["kcpSettings"]["seed"]




    #  Get Protocol . Final Step 
    if protocol == "shadowsocks":
       setting = json.loads(stream['settings'])
       confFirst = f"{setting['method']}:{setting['password']}:{uuid}"
       Clients = ""
       decoded_bytes = base64.urlsafe_b64encode(confFirst )
       if tls == "tls":
             conf += f"&security={tls}&fp={fingerPrint}&alpn={alpn}{'&allowInsecure=1' if allowInsecure ==True else'' }&sni={sni}"
       if netType == "tcp" : 
         return (
    f"{protocol}://{decoded_bytes}@{serverName}:{port}?type={netType}"
    + (
        f"&headerType={headerType}&path={path if path != '' else '/'}&host={host}"
        if headerType != "none"
        else ""
    )
    + f"{conf}#{remark}"
)


       elif netType == "ws" or netType == "httpupgrade" or netType == "splithttp" :
           return  f"{protocol}://{uuid}@{serverName}:{port}?type={netType}&path={path if path!='' else '/'}&host={host}{conf}#{remark}"
                      
       elif netType == "kcp":
           return  f"{protocol}://{decoded_bytes}@{serverName}:{port}?type={netType}&security={tls}&headerType={kcpType}&seed={kcpSeed}#{remark}"             
            
       if netType == "grpc":
            
            authority = inboundSetting['grpcSettings']['authority']
           
            conf  = f"&serviceName={serviceName}&authority={authority}" + conf
            

            return (
    f"{protocol}://{uuid}@{serverName}:{port}?type={netType}"
    + (
        f"&headerType={headerType}&path={path if path != '' else '/'}&host={host}"
        if headerType != "none"
        else ""
    )
    + f"{conf}#{remark}"
)



 
 
    if protocol == "trojan":
        conf = ""
        if tls == "reality":
               conf += f"&security={tls}&pbk={publicKey}&fp={fingerPrint}&sni={sni}&sid={shortIds}&spx={spiderX}"             
        if tls == "tls":
             conf += f"&security={tls}&fp={fingerPrint}&alpn={alpn}{'&allowInsecure=1' if allowInsecure ==True else'' }&sni={sni}"
        if netType == "tcp" : 
           return (
    f"{protocol}://{uuid}@{serverName}:{port}?type={netType}"
    + (
        f"&headerType={headerType}&path={path if path != '' else '/'}&host={host}"
        if headerType != "none"
        else ""
    )
    + f"{conf}#{remark}"
)


        elif netType == "ws" or netType == "httpupgrade" or netType == "splithttp" : return  f"{protocol}://{uuid}@{serverName}:{port}?type={netType}&path={path if path!='' else '/'}&host={host}{conf}#{remark}"
                      
        elif netType == "kcp": return  f"{protocol}://{uuid}@{serverName}:{port}?type={netType}&security={tls}&headerType={kcpType}&seed={kcpSeed}#{remark}"             
            
        if netType == "grpc":
            
            authority = inboundSetting['grpcSettings']['authority']
           
            conf  = f"&serviceName={serviceName}&authority={authority}" + conf
            

            return (
    f"{protocol}://{uuid}@{serverName}:{port}?type={netType}"
    + (
        f"&headerType={headerType}&path={path if path != '' else '/'}&host={host}"
        if headerType != "none"
        else ""
    )
    + f"{conf}#{remark}"
)

    elif protocol == "vless":
        conf = ""
        if netType == "tcp":

            if tls == "xtls":
                conf += f"&security={tls}&flow=xtls-rprx-direct"
            if tls == "reality":
               conf += f"&security={tls}&pbk={publicKey}&fp={fingerPrint}&sni={sni}&sid={shortIds}&spx={spiderX}"     
            if tls == "tls":
             conf += f"&security={tls}&fp={fingerPrint}&alpn={alpn}{'&allowInsecure=1' if allowInsecure ==True else'' }&sni={sni}"
            if host =="none" :
                host=""    
            newConfig = (
    f"{protocol}://{uuid}@{serverName}:{port}?type={netType}"
    + (
        f"&headerType={headerType}&path={path if path != '' else '/'}&host={host}"
        if headerType != "none"
        else ""
    )
    + f"{conf}#{remark}"
)

        elif netType == "ws":
            if tls == "tls":
             
             conf += f"&security={tls}&fp={fingerPrint}&alpn={alpn}{'&allowInsecure=1' if allowInsecure == True else'' }&sni={sni}"

            newConfig = f"{protocol}://{uuid}@{serverName}:{port}?type={netType}&path={path if path!='' else '/'}&host={host}{conf}#{remark} "
        elif netType == "kcp":
            newConfig = f"{protocol}://{uuid}@{serverName}:{port}?type={netType}&security={tls}&headerType={kcpType}&seed={kcpSeed}#{remark}"
        elif netType == "grpc":
             
            authority = inboundSetting['grpcSettings']['authority']
           
            conf  = f"&serviceName={serviceName}&authority={authority}" + conf
            if tls == "xtls":
                conf += "&flow=xtls-rprx-direct"
            if tls == "reality":
               conf += f"&security={tls}&pbk={publicKey}&fp={fingerPrint}&sni={sni}&sid={shortIds}&spx={spiderX}"     
            if tls == "tls":
             conf += f"&security={tls}&fp={fingerPrint}&alpn={alpn}{'&allowInsecure=1' if allowInsecure ==True else'' }&sni={sni}"
            newConfig = f"{protocol}://{uuid}@{serverName}:{port}?type={netType}&serviceName={serviceName}#{remark}"
    elif protocol == "vmess":
        vmessConf = {
            "v": "2",
            "ps": f"{remark}",
            "add": serverName,
            "port": int(port),
            "id": uuid,
            "aid": 0,
            "net": netType,
            "type": "none",
            "tls": "none",
            "path": "",
            "host":  ""

        }
     
   
        if headerType != None:
            vmessConf["type"] = headerType
        elif kcpType != None:
            vmessConf["type"] = kcpType
        else:
            vmessConf["type"] = "none"

        if host != None or host != "none":
            vmessConf["host"] = host
        if path == None or path == '':
            vmessConf["path"] = "/"
        else:
            vmessConf["path"] = path
        if  tls == "" or tls =="none":
            vmessConf["tls"] = "none"

        else:
            vmessConf["tls"] = tls
        if headerType == "http":
            vmessConf["path"] = "/"
            vmessConf["type"] = headerType
        if netType == "kcp":
            if kcpSeed != None or kcpSeed != "":
                vmessConf["path"] = kcpSeed

        if netType == "grpc":
            vmessConf['type'] = grpcSecurity
            vmessConf['scy'] = 'auto'
        if netType == "httpupgrade" or netType == "splithttp":
              vmessConf['scy'] = 'auto'
        res = json.dumps(vmessConf)
        res =res[1:]

        res = "{\n"  +  res.replace("}","\n}")
        res = res.replace("," ,",\n ")
        sample_string_bytes = res.encode("ascii")
    
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        
        newConfig = f"vmess://{base64_string}"
    return newConfig



async def ReadFileConfig():
   async with aiofiles.open('Config/Config.json', mode='r',encoding='utf-8') as f: 
      res =   json.loads(await f.read())
   return res   
   
async def CheckAdmin(userId:int):
   
    res = await db_manager.execute_query_one(f'SELECT IsAdmin FROM Users WHERE UserId = {userId}')
    
    configFile = await ReadFileConfig()
    ownerId = configFile['ownerId']
    if  ownerId == userId : 
        return True 
    if res != None:
     if  res[0]==1:
        
        return True 
     else:
        return False
    else:
        return False 


async def CheckUserBlock(UserId:int):
  

    result = await db_manager.execute_query_one(f'SELECT IsBlock FROM Users WHERE UserId = {UserId} ')
    configFile = await ReadFileConfig()
    ownerId = configFile['ownerId']
    if  ownerId == UserId : 
        return False 
    if result == None :
        return False
    if result[0] == 0:
        return False
    else:
        return True
   
async def AddNewUser(userId:int,Name:str,UserName:str,command,client,message):
  
  result = await db_manager.execute_query_one(f'SELECT IsBlock FROM Users WHERE UserId = {userId} ')
  
  
  if result != None :
        return 
  else:
      if len(command) !=1 :
          try:
              inviterId =  command[1].split("inv")[1]
              user = await db_manager.execute_query_one(f'SELECT * FROM Users WHERE UserId = {inviterId} ')
              if user != None:
               rew = await db_manager.execute_query_one("SELECT RewardInvite FROM Setting ")
              
               await db_manager.QueryWidthOutValue(f"UPDATE Users SET Invited = {user[11] + 1}  , Wallet = { user[7] + rew[0]} WHERE UserId = {user[1]} ")
               timeJoin =datetime.datetime.timestamp(datetime.datetime.now())
               await db_manager.Query("INSERT INTO Users(UserId,UserName,Name,InvitedFrom,TimeJoin,IsAdmin,CountShopped,Invited,CooperationId,UseFreeTrial,Wallet,STEP) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(userId,UserName,Name,inviterId,timeJoin,0,0,0,0,0,0,"home"))
               await client.send_message(user[1] , f""" 🔔 کاربر گرامی 
                                         
🤝 کاربری با کد دعوت شما ربات را استارت زد   

👤 نام کاربری :  {message.from_user.username} 

👤 شناسه کاربری :  {message.from_user.id} 

🎁 سود شما : {rew[0]}% هر خرید این کاربر



🔰 /start

                                          """)
              else:
                  timeJoin =datetime.datetime.timestamp(datetime.datetime.now())
                  await db_manager.Query("INSERT INTO Users(UserId,UserName,Name,TimeJoin,IsAdmin,CountShopped,Invited,CooperationId,UseFreeTrial,Wallet,STEP) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(userId,UserName,Name,timeJoin,0,0,0,0,0,0,"home"))

          except:
                    pass
      else:
         timeJoin =datetime.datetime.timestamp(datetime.datetime.now())
          
         await db_manager.Query("INSERT INTO Users(UserId,UserName,Name,TimeJoin,IsAdmin,CountShopped,Invited,CooperationId,UseFreeTrial,Wallet,STEP) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(userId,UserName,Name,timeJoin,0,0,0,0,0,0,"home"))

async def UnblockUser(userId):
    await db_manager.QueryWidthOutValue(f"UPDATE Users SET ReqUnblock = 0 , IsBlock = 0 WHERE UserId = {userId}")   

async def CheckReqUnblock(UserId):
  result = await db_manager.execute_query_one(f'SELECT ReqUnblock FROM Users WHERE UserId = {UserId} ')
  if result[0] == 0:
      return True
  else:
      return False
async def GetbtnUserBlocks():
    res = await db_manager.execute_query_all("SELECT * FROM Users WHERE IsBlock = 1")
    btns =[]   
    if res !=None or len(res)!=0:
      for r in res:
          btns.append([InlineKeyboardButton(r[2] + "نام کاربری : ",callback_data=f"BlockUser_{r[1]}")])
    else:
        btns.append([InlineKeyboardButton("بچه های خوبی بودن",callback_data="ARS")])

    btns.append([InlineKeyboardButton("بازگشت🔙",callback_data="manageUsers")])
    return btns
async def AddNewAdmin(userId:int):
  result = await db_manager.execute_query_one(f'SELECT * FROM Users WHERE UserId = {userId} ')
  if result == None:
      return False
  
  
  await db_manager.QueryWidthOutValue(f"UPDATE Users SET IsAdmin = 1 WHERE UserId = {userId}")
  
  
  return True

async def DeleteAdmin(userId:int):
  
  await db_manager.QueryWidthOutValue(f"UPDATE Users SET IsAdmin = 0 WHERE Id = {userId}")
  
  

async def GetChanellLock():

    lock = await db_manager.execute_query_one("SELECT LockChanel FROM Setting")
    return lock[0]

async def GetMainKeys(userId:int):
    data  = await ReadFileText()
    dataConfig = await ReadFileConfig()
    data = data['mainKey']
    
    result = await db_manager.execute_query_one(f'SELECT * FROM Users WHERE UserId = {userId} ')
    setting =  await db_manager.execute_query_one(f'SELECT * FROM Setting')
    await ChangeStep(userId,"home")

    btns = []
    btntate = json.loads(setting[4])
    print(result)

    if   userId != dataConfig['ownerId']:
    # {"btnshop":"off","freetest":"off","myacc":"on","mysub":"off"}
    #  btns.append([data['offer']])
     if btntate['btnshop'] == "on":
        if btntate['freetest'] == "on":
            btns.append([data['freetest'],data['shop']])
          
        else:
            btns.append([data['shop']])
     if btntate['mysub'] == "on":
           if   btntate['configdata'] == "on":
              btns.append([data['GetConfigData'],data['mysubscribe']])
           else:
                btns.append([data['mysubscribe']])
     else:
          if  btntate['configdata'] == "on": 
             btns.append([data['GetConfigData']])
     
    
     if btntate['hamkarbtn'] == "on":
        if btntate['tamdidbtn']  =="on":
            
           btns.append([data['hamkar'],data['tamdid']])              
        else:
           btns.append([data['hamkar']])              

     else:
          if btntate['tamdidbtn']  =="on":
              btns.append([data['tamdid']])         
     btns.append([data['needapp'],data['suppourt']])      
     if result[3] == 1 :
        btns.append([data['manageadmin']])                   
    else:
        # [data['offer']]
        btns =[[data['freetest'],data['shop']],[data['GetConfigData'],data['mysubscribe']],[data['hamkar'],data['tamdid']],[data['needapp'],data['suppourt']],[data['myaccount']],[data['manageadmin']]]
        
        return btns
    

   
    
    return btns
    return btns
# "{"btnshop":"off","freetest":"off","myac,"myacc":"on","mysub":"off"}"
async def GetAdminList():
     result = await db_manager.execute_query_all(f'SELECT * FROM Users WHERE IsAdmin = 1 ')
     
     return result

async def GetConfigUserCount(userId):
     count =await db_manager.execute_query_all(f"SELECT COUNT() FROM  Service WHERE UserId = {userId}")
     return count 
async def GetUserByUserId(userId:int):
     result = await db_manager.execute_query_one(f'SELECT * FROM Users WHERE UserId = {userId} ')
     return result      
     
async def GetUserByUserDeatails(userId):
     result = None
     if userId.isnumeric():
         

      result = await db_manager.execute_query_one(f'SELECT * FROM Users WHERE UserId = {userId}  ')
     else:
          result = await db_manager.execute_query_one(f"SELECT * FROM Users WHERE UserName LIKE '%{userId}%' OR Name LIKE '%{userId}%'")
     return result      
async def GetUserNameByUserId(userId:int):
     result = await db_manager.execute_query_one(f'SELECT UserName FROM Users WHERE UserId = {userId} ')
     return result 
async def UpdateReqBlock(userId,blockState):
    await db_manager.QueryWidthOutValue(f"UPDATE Users SET ReqUnblock = {blockState} WHERE UserId = {userId}")
    return
async def GetUserById(Id:int):
     result = await db_manager.execute_query_one(f'SELECT * FROM Users WHERE Id = {Id} ')
     return result      
         
    
async def AddToUserWallet(id:int,AddWallet:int):
   try:  
     result = await db_manager.execute_query_one(f'SELECT Wallet FROM Users WHERE Id = {id} ')
  
     if result ==  None:
         return False
     final =  int(result[0]) + AddWallet
      
     await db_manager.QueryWidthOutValue(f"UPDATE Users SET Wallet = {final} WHERE Id = {id}")
  
     
     return True
   except:
        return False
   
async def MinusToUserWallet(id:int,AddWallet:int):
   try:  
     result = await db_manager.execute_query_one(f'SELECT Wallet FROM Users WHERE Id = {id} ')
  
     if result ==  None:
         return False
     final =  int(result[0]) - AddWallet
     if final < 0:
         final = 0
     await db_manager.QueryWidthOutValue(f"UPDATE Users SET Wallet = {final} WHERE Id = {id}")
  
     
     return True
   except:
        return False
async def BlockUser(id:int,type:int):
     await db_manager.QueryWidthOutValue(f"UPDATE Users SET IsBlock = {type} WHERE Id = {id}")
  
     
async def AdminUser(id:int,type:int):
     await db_manager.QueryWidthOutValue(f"UPDATE Users SET IsAdmin = {type} WHERE Id = {id}")
  
     
async def GetAllApp():
     
     result = await db_manager.execute_query_all('SELECT * FROM AppSuggestment')

     return result      
async def AddApp(link:str,Name:str,type,descrition,photo):
      await db_manager.Query("INSERT INTO AppSuggestment(Name,URl,appType,Description,photo) VALUES(?,?,?,?,?)",(Name,link,type,descrition,photo))

      
async def GetAppList(type):
    res = await db_manager.execute_query_all(f"SELECT * FROM AppSuggestment WHERE appType = '{type}'")
    btns =[]
    if len(res) != 0:
        for r in res :
          btns.append([InlineKeyboardButton(r[1],callback_data=f"deatilApp_{r[0]}")])   
    else:
          btns.append([InlineKeyboardButton("یافت نشد",callback_data=f"ARS")])   
    btns.append([InlineKeyboardButton("🔙 بازگشت",callback_data="mainApp")])      

    return btns
async def GetAppById(appId):
    res= await db_manager.execute_query_one(f"SELECT * FROM AppSuggestment WHERE Id = {appId}")
    return res
async def UpdatePaymentGateway(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET PaymentGateway = '{data}' ")
async def UpdatePaymentGatewayMad(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET TokenMadPal = '{data}' ")
async def DeleteApp(appId):
    await db_manager.QueryWidthOutValue(f"DELETE FROM AppSuggestment WHERE Id = {appId}")
    
async def EditApp(link:str,Name:str,id:int,type,descrition,photo):

    await db_manager.QueryWidthOutValue(f"UPDATE AppSuggestment SET Photo = '{photo}' , URL = '{link}' , Name = '{Name}' , appType = '{type}' , Description = '{descrition}'   WHERE Id = {id}")
    
async def editalertCardp(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET AlertCard = '{data}'")    


async def editalertWebsite(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET AlertOnline = '{data}'")    


async def editNameSingle(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET MessageSingle = '{data}'")           
async def editNameSub(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET MessageSub = '{data}'")    
async def editNameSubService(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET SubName = '{data}'")   
async def editNameSingleService(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET SingleName = '{data}'")   

async def editSupportId(data):
   message = await ReadFileText()    
   message['SuppourtId'] = data
   await SaveFileMessage(message)
   
async def editNameTestService(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET TestName = '{data}'")               
async def editNameBot(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET UserBot = '{data}'")            
async def GetSettingBtns():
    
    result = await db_manager.execute_query_all(f'SELECT * FROM Setting')
    if result[0][38] == 0 and result[0][37] == 0:
        await db_manager.QueryWidthOutValue("UPDATE Setting SET Shop = 0 ")
        result = await db_manager.execute_query_all(f'SELECT * FROM Setting')

    res = result[0]
    messages = await ReadFileText()
    btns =[ 
        
    [InlineKeyboardButton("✅" if res[0] == 1 else "❌",callback_data=f"esa_{res[0]}"),InlineKeyboardButton("وضعیت ربات",callback_data="ARS")],
           
    [InlineKeyboardButton("✅" if res[8] == 1 else "❌",callback_data=f"ChangeShop_{res[8]}"),InlineKeyboardButton("فروش",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[38] == 1 else "❌",callback_data=f"SingleShopSetting_{res[38]}"),InlineKeyboardButton("فروش معمولی",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[37] == 1 else "❌",callback_data=f"SubShopSetting_{res[37]}"),InlineKeyboardButton(" فروش ساب",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[41] == 1 else "❌",callback_data=f"SingleSubShopSetting_{res[41]}"),InlineKeyboardButton("ساب برای کانفیگ معمولی ",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[45] == 1 else "❌",callback_data=f"BuyAgainService_{res[45]}"),InlineKeyboardButton("خرید مجدد",callback_data="ARS")],

    [InlineKeyboardButton("✅" if res[9] == 1 else "❌",callback_data=f"ChangeTEST_{res[9]}"),InlineKeyboardButton("تست",callback_data="ARS")],

    [InlineKeyboardButton("✅" if res[5] == 1 else "❌",callback_data=f"ChangeWallet_{res[5]}"),InlineKeyboardButton("کیف پول",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[2] == 1 else "❌",callback_data=f"CardToCardChange_{res[2]}"),InlineKeyboardButton("کارت به کارت",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[3] == 1 else "❌",callback_data=f"onlinPay_{res[3]}"),InlineKeyboardButton("خرید انلاین",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[32] == 1 else "❌",callback_data=f"onlinPayMad_{res[32]}"),InlineKeyboardButton("مدپال",callback_data="ARS")],

    # [InlineKeyboardButton("✅" if res[11] == 1 else "❌",callback_data=f"autoCard_{res[11]}"),InlineKeyboardButton("کارت به کارت خودکار",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[19] == 1 else "❌",callback_data=f"DisManageState_{res[19]}"),InlineKeyboardButton("کد تخفیف",callback_data="ARS")],
      [InlineKeyboardButton("✅" if res[43] == 1 else "❌",callback_data=f"changeXenitGame_{res[43]}"),InlineKeyboardButton("پرداخت XG",callback_data="ARS")],
    

    [InlineKeyboardButton("✅" if res[28] == 1 else "❌",callback_data=f"SendPhotoWithStartBot_{res[28]}"),InlineKeyboardButton("ارسال تصویر هنگام استارت",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[44] == 1 else "❌",callback_data=f"chengenotifState_{res[44]}"),InlineKeyboardButton(" نوتیف وضعیت سرور ها",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[46] == 1 else "❌",callback_data=f"changelink_{res[46]}"),InlineKeyboardButton("تعویض لینک",callback_data="ARS")],
    [InlineKeyboardButton("✅" if res[50] == 1 else "❌",callback_data=f"chanelLock_{res[50]}"),InlineKeyboardButton("قفل چنل (اد اجباری)",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[33]}",callback_data=f"ChangePGMad"),InlineKeyboardButton("توکن مادپال",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[31]}",callback_data=f"ChangePG"),InlineKeyboardButton("توکن درگاه",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[20]}",callback_data=f"RewardInvite"),InlineKeyboardButton("درصد همکاری ",callback_data="ARS")],

    [InlineKeyboardButton(f"{res[6]}ساعت",callback_data="editTimeBackUp"),InlineKeyboardButton("زمان بک اپ",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[7]}ساعت",callback_data="editTimeQuartz"),InlineKeyboardButton("زمان گزارش در آمد",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[1]}",callback_data="editChanelLock"),InlineKeyboardButton("قفل چنل",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[10]}",callback_data="editChanelQuartz"),InlineKeyboardButton("چنل بکاپ",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[42]}",callback_data="editChanelQuartzQuartz"),InlineKeyboardButton("چنل گزارش",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[12]}",callback_data="editCardAdminNumber"),InlineKeyboardButton("شماره کارت",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[13]}",callback_data="CardAdminName"),InlineKeyboardButton("به نام",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[21]}",callback_data="EditDomainConfig"),InlineKeyboardButton("دامنه ساب",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[26]} Days",callback_data="SendAlertTimeFirst"),InlineKeyboardButton("زمان باقی مانده هشدار اول",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[27]} Days",callback_data="SendAlertTimeTwo"),InlineKeyboardButton("زمان باقی مانده هشدار دوم",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[24]} GB",callback_data="SendAlertVolumeFirst"),InlineKeyboardButton("حجم باقی مانده هشدار اول",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[25]} GB",callback_data="SendAlertVolumeTwo"),InlineKeyboardButton("حجم باقی مانده هشدار دوم",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[34]}",callback_data="alertCard"),InlineKeyboardButton("آلرت کارت به کارت",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[35]}",callback_data="alertWebsite"),InlineKeyboardButton("الرت خرید آنلاین",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[36]}",callback_data="NameBot"),InlineKeyboardButton("(برای درگاه)  نام کاربری بات",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[40]}",callback_data="NameSingle"),InlineKeyboardButton("نام فروش معمولی",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[39]}",callback_data="NameSub"),InlineKeyboardButton("نام فروش ساب",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[48]}",callback_data="NameSubService"),InlineKeyboardButton(" نام ساب ها",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[47]}",callback_data="NameTestService"),InlineKeyboardButton("نام تست ها",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[49]}",callback_data="NameSingleService"),InlineKeyboardButton(" نام فروش معمولی",callback_data="ARS")],
    [InlineKeyboardButton(f"{messages['SuppourtId']}",callback_data="ChangeSupportId"),InlineKeyboardButton("شناسه پشتیبانی",callback_data="ARS")],
    [InlineKeyboardButton(f"{res[53]}",callback_data=f"ChangeSafeConfig"),InlineKeyboardButton("کانفیگ اضطراری",callback_data="ARS")],
  
    [InlineKeyboardButton("بازگشت",callback_data="mainAdmin")]]

    return btns     

async def GetBtnCat():


    Cats = await db_manager.execute_query_all("SELECT * FROM category ")
    btns=[]
    for cat in Cats:
        btns.append([f'{cat[0]}:{cat[1]}'])

    btns.append(['انصراف'])
    return   btns   

async def changeXenit(data):
    data = int(data)
    if data==0:
        data = 1
    else:
      data = 0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET OnlineXG = {data}")  
async def CanUserChangeLinkConf():
    setting =  await db_manager.execute_query_one("SELECT changelink FROM Setting")
    if setting[0] == 0:
        return False
    else :
        return True
async def ChangeLinkConf(data):
    data = int(data)
    if data==0:
        data = 1
    else:
      data = 0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET changelink = {data}")  

async def ChannelLock(data):
    data = int(data)
    if data==0:
        data = 1
    else:
      data = 0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET chanelLock = {data}")  
async def UpdateConfigSafe(config,catId):

    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET SafeModCat = {catId} , SafeMode = '{config}'")

async def changeStateNotif(data):
    data = int(data)
    if data==0:
        data = 1
    else:
      data = 0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET alertTimeOut = {data}")  
async def UpdateDomainConfig(data ):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET  SubDomain = '{data}'")
async def UpdateSettingAlert(Name , Value):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET {Name} = {Value}")

async def UpdateStateStartAfterUse(state ):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET StartAfterUse = {state}")
    
async def UpdateSettingPhotoStart(State,Photo):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET SendPhotoWithStartBot = {State}, PhotoStart = '{Photo}' ")     
async def EditDiscountStateManage(state):
        await db_manager.QueryWidthOutValue(f"UPDATE Setting SET Discount = {state}")  

async def EditEsa(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data =0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET Status = {data}")  
    

async def EditChangeShop(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data =0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET Shop = {data}")  
    
 
async def EditChangeSingleShopSub(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data =0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET SubSingle = {data}")  

async def BuyAgainService(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data =0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET buyagain = {data}")      

async def EditChangeShopSub(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data =0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET SubShop = {data}")  
async def GetSettingTypeShop():
    data = await db_manager.execute_query_one("SELECT SubShop , SingleShop , MessageSub , MessageSingle,OnlineXG FROM Setting ")
    return data
async def EditChangeShopSingle(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data = 0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET SingleShop = {data}")  
async def EditChangeTEST(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data =0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET Test = {data}")  
    

async def EditChangeWallet(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data =0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET Wallet = {data}")  
    

async def EditCardToCardChange(data:str):
    data = int(data)
    if data==0:
        data = 1
        await db_manager.QueryWidthOutValue(f"UPDATE Setting SET CardToCard = {data} ,CardToCardAutomatically = 0 ") 
    else:
      data =0
      await db_manager.QueryWidthOutValue(f"UPDATE Setting SET CardToCard = {data} ")  
    
    

async def EditonlinPay(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data =0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET OnlinePayment = {data}")  


async def EditonlinPayMad(data:str):
    data = int(data)
    if data==0:
        data = 1
    else:
      data =0
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET madpal = {data}")     


async def editTimeBackUp(time):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET TimeSendBackUp = {time}") 

    
async def editRewardInvite(reward):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET RewardInvite = {reward}") 


async def TimeSendQuartz(time):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET TimeSendQuartz = {time}") 

    

async def editChanelLock(time):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET LockChanel = '{time}'") 

    
 
async def editChanelQuartz(time):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET QuartzChanell = '{time}'") 
    

 
async def editChanelQuartzQuartz(time):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET ChanelQuartzQuartz = '{time}'") 
    
       
async def GetServer():
    res =await db_manager.execute_query_one(f"SELECT * FROM Server")
    return res
    
async def UpdateServerLogin(UrlPanel,userName,Password,typeServer,serverId,inbound):
 
 try:   
    async with httpx.AsyncClient() as client:
          response =  await client.post(url=f"{UrlPanel}/login",data={"username":f"{userName}","password":f"{Password}"})

          if  response.status_code == 200:
           session =""
           if len(response.headers.get("Set-Cookie").split("; ") )>= 6:
      
             session =  response.headers.get("Set-Cookie").split("; ")[4]  
             session =session.split(", ")[1]
           else:
             session =  response.headers.get("Set-Cookie").split("; ")[0]  
           await db_manager.QueryWidthOutValue(f"UPDATE Server SET Url = '{UrlPanel}', User = '{userName}' , Password = '{Password}', PanelType = '{typeServer}' , Session  = '{session}' , InboundId = {inbound} WHERE Id = {serverId} ")
           return [True,"✅ سرور با موفقیت ویرایش شد"]
          else:
               return [False,"هنگام ویرایش سرور مشکلی پیش آمده و اطلاعاتی از سرور دریافت نشد"]           


 except:
     return [False,"هنگام ویرایش سرور مشکلی پیش آمده و اطلاعاتی از سرور دریافت نشد"]   
async def AddServer(Name,domain,UrlPanel,userName,Password,typeServer,catId,inboundId,IsAddToUsers):
 try:   
    text = ""
    response = ""
    async with httpx.AsyncClient() as client:
          response =  await client.post(url=f"{UrlPanel}/login",data={"username":f"{userName}","password":f"{Password}"})

    if  response.status_code == 200:
        session = ""
        if len(response.headers.get("Set-Cookie").split("; ") ) >= 6:
      
             session =  response.headers.get("Set-Cookie").split("; ")[4]  
             session =session.split(", ")[1]
        else:
             session =  response.headers.get("Set-Cookie").split("; ")[0]  
        if IsAddToUsers == True :
          Services = await db_manager.execute_query_all(f"SELECT * FROM Service WHERE CatId = {catId} ")     
          clients = ""
          for Service in Services:
    
              clients+=('{"id": "'+ Service[4] + '", "alterId": 0, "email": "'+Service[3]+'", "totalGB": '+str(Service[18])+' , "expiryTime": '+str(Service[7])+', "enable": true, "tgId": "", "subId": ""},')
           
          clients = clients[:-1] 
          data={"settings":'{"clients": [' + clients+ ']}',
                
                "id":f"{inboundId}"
                }
   
          response = ""
          origin= UrlPanel.split("/")
          headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate',
'X-Requested-With': 'XMLHttpRequest',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Origin': f'{origin[0]}://{origin[2]}',
'Connection': 'keep-alive',
'Referer': f'{UrlPanel}/{"panel" if typeServer=="sanaei" else "xui"}/inbounds',
'Cookie': ''
}
          headers['Cookie']  = f"lang=en-US; {session}"
          response = None
          async with httpx.AsyncClient() as client:

            response = await client.post(UrlPanel+f"/{'panel' if typeServer=='sanaei' else 'xui'}/inbound/addClient",headers=headers,data=data)  
          reponseData = json.loads(response.text)
          
          if  reponseData['success'] == True:
              data = await db_manager.Query("INSERT INTO Server(User,Password,Url,PanelType,Name,Domain,Session,CatId,InboundId) VALUES(?,?,?,?,?,?,?,?,?)",(userName,Password,UrlPanel,typeServer,Name,domain,session,catId,inboundId))
              await ServerManager.QueryWidthOutValue(f"INSERT INTO ServerData(ServerId) VALUES({data.lastrowid})")
              await ServerManager.QueryWidthOutValue(f"INSERT INTO ServerCat(ServerId,CatId) VALUES({data.lastrowid},{catId})")
              
              text = "کانفیگ ها با موفقیت اضافه شدند"
              for service in Services:
                  ServerService =  ast.literal_eval(service[17]) 
                  ServerService.append(data.lastrowid) 
                  await db_manager.QueryWidthOutValue(f"UPDATE Service SET ServerIds = '{ServerService}'")
                  
              return [True,"✅ سرور با موفقیت اضافه شد" + text ]


          else:
              data = await db_manager.Query("INSERT INTO Server(User,Password,Url,PanelType,Name,Domain,Session,CatId,InboundId) VALUES(?,?,?,?,?,?,?,?,?)",(userName,Password,UrlPanel,typeServer,Name,domain,session,catId,inboundId))
              await ServerManager.QueryWidthOutValue(f"INSERT INTO ServerData(ServerId) VALUES({data.lastrowid})")
              await db_manager.QueryWidthOutValue(f"INSERT INTO ServerCat(ServerId,CatId) VALUES({data.lastrowid},{catId})")

              text = "⚠️ هنگام افزودن کلاینت ها به مشکل خوردیم"
              return [True,"✅ سرور با موفقیت اضافه شد" + text ]
        else:

         data = await db_manager.Query("INSERT INTO Server(User,Password,Url,PanelType,Name,Domain,Session,CatId,InboundId) VALUES(?,?,?,?,?,?,?,?,?)",(userName,Password,UrlPanel,typeServer,Name,domain,session,catId,inboundId))
         await ServerManager.QueryWidthOutValue(f"INSERT INTO ServerData(ServerId) VALUES({data.lastrowid})")
         await db_manager.QueryWidthOutValue(f"INSERT INTO ServerCat(ServerId,CatId) VALUES({data.lastrowid},{catId})")

         return [True,"✅ سرور با موفقیت اضافه شد" ]
    else:
        return [False,"هنگام افزودن سرور مشکلی پیش آمده و اطلاعاتی از سرور دریافت نشد"]           


 except:
     return [False,"هنگام افزودن سرور مشکلی پیش آمده و اطلاعاتی از سرور دریافت نشد"]   

async def GetPublicMessage():
    res = await db_manager.execute_query_one("SELECT * FROM PublicMessage WHERE IsSended = 0")
    
    return res    
async def AddNewPublicMessage(title , mes,idUser,photo):
    await db_manager.Query("INSERT INTO PublicMessage(Title , Description, AddUser,photo) VALUES(?, ?, ?,?)",(title,mes,int(idUser),photo))
    
async def DeletePublicMess(data):
    await db_manager.QueryWidthOutValue(f"DELETE FROM PublicMessage WHERE Id = {data}")
    
async def GetCatBtnsReply():
    resualt = await db_manager.execute_query_all("SELECT * FROM category")
    btns = []

    if resualt != None:
          count = 0
          btnOdd = []
          for data  in resualt:
           count += 1
           btnOdd.append(data[1])
           if count == 2:
                btns.append(btnOdd)    
                count = 0
                btnOdd = []
          if count != 0:      
           btns.append(btnOdd)  
    btns.append(["انصراف"])
    return btns
async def GetCatBtns():
    resualt = await db_manager.execute_query_all("SELECT * FROM category")
    btns = []
    
    if resualt != None:
        btns.append([InlineKeyboardButton("سرور ها",callback_data="ARS"),InlineKeyboardButton("حذف",callback_data="ARS"),InlineKeyboardButton("وضعیت",callback_data="ARS"),InlineKeyboardButton("نام",callback_data="ARS")])
        for res in resualt:
            btns.append([InlineKeyboardButton("⚙️",callback_data=f"EditCatSett_{res[0]}"),InlineKeyboardButton("❌",callback_data=f"DeleteCat_{res[0]}"),InlineKeyboardButton(  "🔴" if res[3] == 0 else "🟢" ,callback_data = f"StateCat_{res[0]}_{res[3]}"),InlineKeyboardButton(res[1],callback_data=f"EditNameCat_{res[0]}")])
       
    btns.append([InlineKeyboardButton("افزودن",callback_data="AddCat")])            
    btns.append([InlineKeyboardButton("بازگشت",callback_data="mainAdmin")])
    return btns


async def UpdateCatName(catId , Name):
    await db_manager.QueryWidthOutValue(f"UPDATE category SET Title  = '{Name}' WHERE Id = {catId}")
async def GetCatBtnsShell():
    resualt = await db_manager.execute_query_all("SELECT * FROM category WHERE Show = 1 AND TypeServices = 'sub' ")
    

    btns = []
    
    if resualt != []:
        for res in resualt:
            btns.append([InlineKeyboardButton(res[1],callback_data=f"planshop_{res[0]}")])
       
    else:
        btns.append([InlineKeyboardButton("🔻 دسته بندی موجود نیست 🔻",callback_data="ARS" )])   
    btns.append([InlineKeyboardButton("بازگشت",callback_data="mainservice" )])
    return btns
async def SingleServers():
    resualt = await db_manager.execute_query_all("SELECT * FROM category WHERE Show = 1 AND TypeServices = 'normal' ")
    
    btns = []
    if resualt != []:
        for res in resualt:
            btns.append([InlineKeyboardButton(res[1],callback_data=f"GetServers_{res[0]}")])
       
    else:
        btns.append([InlineKeyboardButton("🔻 دسته بندی موجود نیست 🔻",callback_data="ARS" )])   

    btns.append([InlineKeyboardButton("بازگشت",callback_data="mainservice" )])
    return btns
async def DeleteCat(data):
    await db_manager.QueryWidthOutValue(f"DELETE FROM category WHERE Id = {data} ")
    
async def GetAllPlansList():
     btns = []
     datas =  await db_manager.execute_query_all("SELECT * FROM ServerPlans")
     
     btns.append([InlineKeyboardButton("حذف",callback_data="ARS"),InlineKeyboardButton("نام پلن",callback_data="ARS")])
     if datas != None:
         
      for data in datas:
          btns.append([InlineKeyboardButton("❌",callback_data=f"DeletePlan_{data[0]}"),InlineKeyboardButton(f"{data[1]}",callback_data=f"EditPlan_{data[0]}")])
     btns.append([InlineKeyboardButton("افزودن پلن",callback_data="AddPlan"),InlineKeyboardButton("بازگشت 🔙",callback_data="mainAdmin")])
     return btns
async def AddPlan(planName,DescriptionPlan,monthCount,Price,Valume,countShell,CatId,speed_limit,userlimit):
    try:
     if userlimit =='':
       userlimit = 0
  
     lastRowId = await db_manager.Query(f"INSERT INTO ServerPlans(PlanName , Description, MonthCount, Price , Volume, CatId , CountSell, SpeedLimit, UserLimit, PlanServerId,DataServer) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(f'{planName}',f'{DescriptionPlan}',monthCount,Price,Valume,CatId,countShell,0,userlimit,0,'0'))
     await db_manager.Query("INSERT INTO PlanCat(CatId,PlanId) VALUES(?,?)",(CatId,lastRowId.lastrowid))
     
     
     return True
    except:
        return False
    
async def DeletePlan(data):
     await db_manager.QueryWidthOutValue(f"DELETE FROM ServerPlans WHERE Id = {data}")
async def IsServerAny():
        res=  await db_manager.execute_query_one("SELECT * FROM Server")
        
        if res ==None:
            return False
        else: return True


async def ChangeServerAuth():

   server=  await db_manager.execute_query_one("SELECT * FROM Server")
   
   try:  
            headers = {"Content-Type" :"application/x-www-form-urlencoded","Cookie":"dark_mode=1; i18n=en-US"}
           
            data = {"email":f"{server[0]}",
                "password":f"{server[1]}"}
            async with httpx.AsyncClient() as client:
            
              response = await client.post(f'{server[2]}/api/v1/passport/auth/login',data=data,headers=headers)
              if response.status_code==200:
                  auth = json.loads(response.content)['data']['auth_data']
                  await db_manager.QueryWidthOutValue(f"UPDATE Server SET url  = '{server[2]}' , authorize = '{auth}' ")
                  
                  return True
              else:
                      

                       return False
   except:
   
         return False   
   

async def GetServerManageBtns():
    server =   await GetServer()
    btns = []
  
    if server == None:
       btns.append([InlineKeyboardButton("اضافه کردن سرور",callback_data="arddServer")])
    else:
       btns.append([InlineKeyboardButton("ایمیل 👤 ",callback_data="ARS"),InlineKeyboardButton(server[0],callback_data="EditEmailS")])   
       btns.append([InlineKeyboardButton("کلمه عبور 👤 ",callback_data="ARS"),InlineKeyboardButton(server[1],callback_data="EditPassS")])   
       btns.append([InlineKeyboardButton("آدرس",callback_data="ARS"),InlineKeyboardButton(server[2],callback_data="EditUrlS")])   
       btns.append([InlineKeyboardButton("Authentication key",callback_data="ARS"),InlineKeyboardButton(server[3],callback_data="EditAuth")])   
       btns.append([InlineKeyboardButton("Background Path",callback_data="ARS"),InlineKeyboardButton(server[4],callback_data="EditkeyS")])   
    btns.append([InlineKeyboardButton("بازگشت",callback_data="mainAdmin")])
    return btns
async def EditBackgroundServer(back):
      
                  await db_manager.QueryWidthOutValue(f"UPDATE Server SET  Key ='{back}' ")
                  
                  return True
             
async def GetCatPlanbtnsSelect(PlanId):
    cats = await db_manager.execute_query_all(f"SELECT * FROM  category ")
    btns = []
    for cat in cats :
        btns.append([InlineKeyboardButton(cat[1],callback_data=f"AddCatToPlan_{PlanId}_{cat[0]}")])    
    btns.append([InlineKeyboardButton("بازگشت",callback_data=f"EditCPlan_{PlanId}")])    
    
    return btns

async def AddCatToPlan(PlanId , CatId):

  try:  
    res =  await db_manager.execute_query_one(f"SELECT * FROM PlanCat WHERE CatId = {CatId} AND PlanId = {PlanId}")
    if res == None:
        await db_manager.Query("INSERT INTO PlanCat(PlanId,CatId) VALUES(?,?)",(PlanId,CatId))
        return True
    else: 
        return False
  except :
      return False
  

async def DeleteCatPlan(serverId):
    try:
        await db_manager.QueryWidthOutValue(f"DELETE FROM PlanCat WHERE Id = {serverId} ")
        return True
    except:
        return False       
      
async def GetCatsPlan(PlanId):
 Cats = await db_manager.execute_query_all(f"SELECT category.*,PlanCat.Id FROM PlanCat JOIN category ON category.Id = PlanCat.CatId WHERE PlanId = {PlanId}     ")
 btns = []
 if len(Cats) != 0:
     for cat in Cats:
         btns.append([InlineKeyboardButton("❌",callback_data=f"DeleteCatPlan_{cat[5]}"),InlineKeyboardButton(f"{cat[1]}",callback_data="ARS")])
 btns.append([InlineKeyboardButton("افزودن دسته بندی",callback_data=f"CatListToPlan_{PlanId}")])    
 btns.append([InlineKeyboardButton("بازگشت",callback_data=f"EditPlan_{PlanId}")])    
 return btns
async def GetEditPlansBtns(data):
    btns = []
    plan =await db_manager.execute_query_one(f"SELECT * FROM ServerPlans WHERE Id = {data}")       
    catName  =await  db_manager.execute_query_one(f"SELECT Title FROM category WHERE Id = {plan[6]}") 
    if plan != None:
     btns.append([InlineKeyboardButton(plan[1],callback_data=f"EditPName_{plan[0]}"),InlineKeyboardButton("نام",callback_data="ARS")])
     btns.append([InlineKeyboardButton(plan[2],callback_data=f"EditDPlane_{plan[0]}"),InlineKeyboardButton("توضیحات",callback_data="ARS")])
     btns.append([InlineKeyboardButton(plan[3],callback_data=f"EditMPlan_{plan[0]}"),InlineKeyboardButton("ماه",callback_data="ARS")])
     btns.append([InlineKeyboardButton(plan[4],callback_data=f"EditPricePlan_{plan[0]}"),InlineKeyboardButton("قیمت",callback_data="ARS")])
     btns.append([InlineKeyboardButton(plan[5],callback_data=f"EditVPlan_{plan[0]}"),InlineKeyboardButton("حجم",callback_data="ARS")])
     btns.append([InlineKeyboardButton(plan[7],callback_data=f"EditSPlan_{plan[0]}"),InlineKeyboardButton("تعداد فروش",callback_data="ARS")])
     btns.append([InlineKeyboardButton(plan[9],callback_data=f"EditUserPlan_{plan[0]}"),InlineKeyboardButton("محدودیت کاربر",callback_data="ARS")])
     btns.append([InlineKeyboardButton("مدیریت دسته بندی ها",callback_data=f"EditCPlan_{plan[0]}")])

    else:
      btns.append([InlineKeyboardButton("یافت نشد !",callback_data="ARS")])

    btns.append([InlineKeyboardButton("بازگشت",callback_data="managePlan")])
    return btns


async def addCat(data,typeCats):
    await db_manager.QueryWidthOutValue(f"INSERT INTO category(Title,TypeServices) VALUES('{data}','{typeCats}')")
    
    return True
async def GetCatType(data):
    res = await db_manager.execute_query_one(f"SELECT TypeServices FROM category WHERE Id ={data}")
    return res[0]

async def GetCatByName(data):
    res = await db_manager.execute_query_one(f"SELECT Id FROM category WHERE Title ='{data}'")
    
    return res

async def GetServerByName(data):
    res = await db_manager.execute_query_one(f"SELECT Id FROM Server WHERE Name ='{data}'")
    
    return res[0]
async def EditPlanName(Data,planId):
   try: 
      
       await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET PlanName = '{Data}' , DataServer = 'empty' WHERE Id = {planId}")
       return True
   except :
       return False
async  def EditPlanDescription(Data,planId):
     try: 
       await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET Description = '{Data}' WHERE Id = {planId}  ")
       return True
     except :
       return False 
async  def EditPlanMonth(Data,planId):
     try: 
       await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET MonthCount = {Data} WHERE Id = {planId}  ")
       return True
     except :
       return False      
async  def EditPlanPrice(Data,planId):
     try: 
       await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET Price = {Data} WHERE Id = {planId}  ")
       return True
     except :
       return False        
async def EditPlanVloume(data, planId):
     try: 
       await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET Volume = {data} WHERE Id = {planId}  ")
       return True
     except :
       return False     
async def updateCatPlan(data, planId):
     try: 
       await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET CatId = {data} WHERE Id = {planId}  ")
       return True
     except :
       return False 
async def EditPlanCountShel(data, planId):
     try: 
       await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET CountSell = {data} WHERE Id = {planId}  ")
       return True
     except :
       return False                   
async def EditPlanSpeed(data,planId):
     try: 
      
       await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET SpeedLimit = {data} , DataServer = 'empty' WHERE Id = {planId}")
       return True
     except :
       return False     
async def EditPlanUser(data,planId):
     try: 
       plan = await db_manager.execute_query_one(f"SELECT * FROM ServerPlans WHERE Id = {planId}")
       
    
       await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET UserLimit = {data} , DataServer = 'empty' WHERE Id = {planId}")
       return True
     except :
       return False          
async def IsShop():
    res = await db_manager.execute_query_one("SELECT Shop FROM Setting")

    if res[0] == 1:
        return True
    else:
         False
         
async def GetPlanCatShellSingle(data,ServerId):
    btns = [[InlineKeyboardButton("قیمت",callback_data="ARS"),InlineKeyboardButton("حجم",callback_data="ARS")]]
    plans = await db_manager.execute_query_all(f"SELECT ServerPlans.PlanName , ServerPlans.Id , ServerPlans.Price , ServerPlans.Volume , ServerPlans.MonthCount  FROM PlanCat JOIN ServerPlans ON PlanCat.PlanId = ServerPlans.Id  WHERE PlanCat.CatId  = {data} ORDER BY ServerPlans.Price ")
    if plans !=None:
        for plan in plans:
            btns.append([InlineKeyboardButton(f"تومان {plan[2]}",callback_data=f"OrderSingle_{plan[1]}_{ServerId}_{data}"),InlineKeyboardButton(f"گیگ {plan[3]}",callback_data=f"OrderSingle_{plan[1]}_{ServerId}_{data}")])
    else:
        btns.append([InlineKeyboardButton("♦️پلنی موجود نیست♦️",callback_data="ARS")])  
    btns.append([InlineKeyboardButton("بازگشت",callback_data="SingleShop")])      
    return btns
async def GetPlanCatShell(data):
    btns = [[InlineKeyboardButton("قیمت",callback_data="ARS"),InlineKeyboardButton("حجم",callback_data="ARS")]]
    plans = await db_manager.execute_query_all(f"SELECT ServerPlans.PlanName , ServerPlans.Id , ServerPlans.Price , ServerPlans.Volume , ServerPlans.MonthCount  FROM PlanCat JOIN ServerPlans ON PlanCat.PlanId = ServerPlans.Id  WHERE PlanCat.CatId = {data} ORDER BY ServerPlans.Price ")
    if plans !=None:
        for plan in plans:
            btns.append([InlineKeyboardButton(f"تومان {plan[2]}",callback_data=f"getOrder_{plan[1]}_{data}"),InlineKeyboardButton(f"گیگ {plan[3]}",callback_data=f"getOrder_{plan[1]}_{data}")])
    else:
        btns.append([InlineKeyboardButton("♦️پلنی موجود نیست♦️",callback_data="ARS")])    
    btns.append([InlineKeyboardButton("بازگشت",callback_data="MultiShop")])      
    return btns
async def UpdateCatState(catId , show):
    await db_manager.QueryWidthOutValue(f"UPDATE category SET Show = {show} WHERE Id = {catId}")
    

async def CreateOrderSingle(userId  , planId,state , price , type,monthCount,ServerId,catId):
    try :
        now = datetime.datetime.now()
        
        timestamp = int( datetime.datetime.timestamp(now) )
        
        res = await db_manager.Query(f"INSERT INTO OrdersList(DateTime, PlanId, UserId , Type, State,Price,EndTimePlan,ServerId,CatId) VALUES(?,?,?,?,?,?,?,?,?)",(timestamp, planId, userId, type,  state,price,monthCount,ServerId,catId))
        res.lastrowid 
        
        
         
        return [True,res.lastrowid]
    except:
        return [False  ,0  ]


async def CreateOrder(userId  , planId,state , price , type,monthCount,CatId):
    try :
        now = datetime.datetime.now()
        
        timestamp = int( datetime.datetime.timestamp(now) )
        
        res = await db_manager.Query(f"INSERT INTO OrdersList(DateTime, PlanId, UserId , Type, State,Price,EndTimePlan,CatId,ServerId) VALUES(?,?,?,?,?,?,?,?,?)",(timestamp, planId, userId, type,  state,price,monthCount,CatId,0))
        res.lastrowid 
        
        

        return [True,res.lastrowid]
    except:
        return [False  ,0  ]
async def GetPlanById(data):
    res =  await db_manager.execute_query_one(f"SELECT PlanName,Description,MonthCount,Price,Volume,CountSell , SpeedLimit, UserLimit,ContSold , CatId FROM ServerPlans WHERE Id = {data}")
    
    return res
async def GetBtnsShel(data,catId):

    res = await db_manager.execute_query_one("SELECT CardToCard,Wallet,OnlinePayment,CardToCardAutomatically,Discount,SubDomain,madpal,OnlineXG FROM Setting ")
    btns = []
    if res[0] != 0:
        btns.append([InlineKeyboardButton("💳 کارت به کارت",callback_data=f"CardToCard_{data}")])

    if res[1]!=0    :
        btns.append([InlineKeyboardButton("💰 کیف پول",callback_data=f"PayWallet_{data}")])

    if  res[2]!= 0 or  res[6]!= 0  :
          btns.append([InlineKeyboardButton("📡 پرداخت انلاین",callback_data=f"payOnline_{data}")])   

    if res[3] != 0:
        btns.append([InlineKeyboardButton("💳 کارت به کارت",callback_data=f"CardToAuto_{data}")])      

    if res[4] != 0:
        btns.append([InlineKeyboardButton("🎁 با کد تخفیف",callback_data=f"WithCodeDis_{data}")])      

    catType =  await db_manager.execute_query_one(f"SELECT TypeServices FROM category WHERE Id = {catId}")

    if catType != None :
        if catType[0] == 'sub':
            btns.append([InlineKeyboardButton("⬅️ پلن ها ",callback_data=f"planshop_{catId}")])
        else:
            btns.append([InlineKeyboardButton("⬅️ سرور ها ",callback_data=f"SingleShop")])
            
    return btns        
async def GetBtnsShellWallet(data):
    res = await db_manager.execute_query_one("SELECT CardToCard,OnlinePayment,CardToCardAutomatically,SubDomain,madpal,OnlineXG FROM Setting ")
    btns = []
    if res[0] != 0:
        btns.append([InlineKeyboardButton("💳 کارت به کارت",callback_data=f"CardToCard_{data}")])
    if  res[1]!= 0 or res[4]!= 0  :
                 btns.append([InlineKeyboardButton("📡 پرداخت انلاین",callback_data=f"payOnline_{data}")])

   
                       
    if res[2] != 0:
        btns.append([InlineKeyboardButton("💳 کارت به کارت",callback_data=f"CardToAuto_{data}")])      
 
        
    
    return btns

async def GetBtnsSheldIScOUNT(data,catId):
    res = await db_manager.execute_query_one("SELECT CardToCard,Wallet,OnlinePayment,CardToCardAutomatically,Discount,SubDomain,madpal,OnlineXG FROM Setting ")
    btns = []
    if res[0] != 0:
        btns.append([InlineKeyboardButton("💳 کارت به کارت",callback_data=f"CardToCard_{data}")])
    if res[1]!=0    :
        btns.append([InlineKeyboardButton("💰 کیف پول",callback_data=f"PayWallet_{data}")])
    if  res[2]!= 0 or  res[6] !=  0:
          btns.append([InlineKeyboardButton("📡 پرداخت انلاین",callback_data=f"payOnline_{data}")])
                
    if res[3] != 0:
        btns.append([InlineKeyboardButton("💳 کارت به کارت",callback_data=f"CardToAuto_{data}")])      
   
    catType =  await db_manager.execute_query_one(f"SELECT TypeServices FROM category WHERE Id = {catId}")

    if catType != None :
        if catType[0] == 'sub':
            btns.append([InlineKeyboardButton("⬅️ پلن ها ",callback_data=f"planshop_{catId}")])
        else:
            btns.append([InlineKeyboardButton("⬅️ سرور ها ",callback_data=f"SingleShop")]) 
    return btns         

async def EditCardNumber(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET CardAdminNumber = '{data}'")
    
async def GetTextAlertOnline():
    data = await  db_manager.execute_query_one("SELECT AlertOnline FROM Setting ")
    return data[0]


async def GetOnlinePayBtns(data):
    res = await  db_manager.execute_query_one("SELECT madpal,OnlinePayment,SubDomain,OnlineXG FROM Setting ")
    btns=[]
    if res[3] != 0:

          OrderAmount = await db_manager.execute_query_one(f"SELECT Price , PriceAfterDiscount FROM OrdersList WHERE Id = {data}")
          amount = OrderAmount[0]
          if OrderAmount[1] != None:
             amount = OrderAmount[1]
             
        #   btns.append([InlineKeyboardButton("📡 1 پرداخت انلاین",url=f"https://xenitgame.com/onlinepay/requestdo.php?token={data}&amount={amount}")])

    if  res[1]!= 0 :
          btns.append([InlineKeyboardButton("📡 پرداخت انلاین",url=f"{res[2]}/onlinepay?token={data}")])
    if  res[0]!= 0 :
          btns.append([InlineKeyboardButton("🌐 پرداخت آنلاین",url=f"{res[2]}/request.php?token={data}")])
    
                
    if len(btns) == 0:
           btns.append([InlineKeyboardButton("درگاهی یافت نشد",callback_data=f"ARS")])

    return btns
async def EditCardNamerName(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET CardAdminName = '{data}'")
    
async def ChangeCardAutoData(email,password,apikey,data):
 try:     
      dataSend = {
    "email": f"{email}",
    "password": f"{password}",
      }
      async with httpx.AsyncClient() as client:
    
      
      
         response = await client.post(f'https://sopall.solarteam.site/api/CheckAuth',json=dataSend)
         if response.status_code!= 200 :
             await db_manager.QueryWidthOutValue("UPDATE Setting SET CardToCardAutomatically = 0")
             return False
       
      await db_manager.QueryWidthOutValue(f"UPDATE AutoCard SET ApiKey = '{apikey}' , Password = '{password}' , Email = '{email}'")
      await db_manager.QueryWidthOutValue("UPDATE Setting SET CardToCardAutomatically = 1 , CardToCard = 0")
      
      return True
 except:
     return False
async def GetDataForCardToCard():
    res = await db_manager.execute_query_one("SELECT CardAdminName,CardAdminNumber,AlertCard FROM  Setting")
    
    
    return res
async def GetdataPriceOrder(data):
    res = await db_manager.execute_query_one(f"SELECT Price, DiscountId, PriceAfterDiscount,Type FROM OrdersList WHERE Id = {data} ")    
    
    return res

async def ShopANDGetSubscribe(orderId,userId):
    order = await db_manager.execute_query_one(f"SELECT Price FROM OrdersList WHERE Id = {orderId} ")
    user  = await db_manager.execute_query_one(f"SELECT Wallet FROM Users WHERE UserId = {userId}")
    if order[0] <= user[0]:
        res = user[0] - order[0] 
        await db_manager.QueryWidthOutValue(f"UPDATE Users SET Wallet = {res} WHERE UserId = {userId}")
        return True
    else:
        return False    



async def GetStateBot():
    data = await db_manager.execute_query_one("SELECT Status FROM Setting ")
    if data[0] == 1:
        return True
    else:
        return False

async def checkOrderCard(orderId):
    res = await db_manager.execute_query_one(f"SELECT State,Type FROM OrdersList WHERE Id = {orderId}")
    if res[0] != 0 :
        return [False,""]
    
    else:
        return [True,res[1]] 
    

async def SaveFileConfig(data):
 async with aiofiles.open('Config/Config.json', mode='w',encoding='utf-8') as f: 
      await f.write(json.dumps(data))

async def SaveFileMessage(data):
 async with aiofiles.open('Config/Messages.json', mode='w',encoding='utf-8') as f: 
      await f.write(json.dumps(data))
async def CreateSingle(order,app):
  catId = await db_manager.execute_query_one(f"SELECT CatId,Volume,UserLimit FROM ServerPlans WHERE Id = {order[2]}")

  server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {order[10]}  ")
  days = int(order[7]) * 30
  allow = False
 

  randomId  = random.randint(100, 9999)  
  random2Id =random.randint(100, 9999)  
  SingleName =await db_manager.execute_query_one("SELECT SingleName,LockChanel FROM Setting")
  EndTime = datetime.datetime.now() + datetime.timedelta(days=days)
  Volume = catId[1] * 1024 * 1024 * 1024
  email =f"{randomId}-{random2Id}"
  configUrl =get_random_string(12)
  uuid=uuid4()
  endTimeMikro =int(datetime.datetime.timestamp(EndTime) ) * 1000
  ServiceId = await db_manager.Query("INSERT INTO Service(UserId,Email,Password,CreateDate,EndDate,OrderId,PlanId,CatId,ServerIds,configUrl,TransformEnable,RandomId,TypeService,ServiceTest,UserLimit) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(order[3],email,str(uuid),int(datetime.datetime.timestamp(datetime.datetime.now())),endTimeMikro,order[0],order[2],order[11],f'[{server[0]}]',configUrl,Volume,randomId,"single","empty",catId[2]))

#   serversCount = []
  try:     
      data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ str(uuid) +'", "alterId": 0, "email": "'+ email +'", "totalGB": '+ str(int(Volume)) +', "expiryTime": '+str(endTimeMikro)+', "enable": true,  "limitIp":'+ str(catId[2]) + '   , "tgId": "", "subId": ""}]}'
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
      
         session = ""
      
         headers['Cookie']  = f"lang=en-US; {server[8]}"
         try:
          response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers)
         except:
          response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers)
          
       
         data = json.loads(response.text)
         
         if data['success'] == False:
              fileConfig =await ReadFileConfig()
              await app.send_message(fileConfig['ownerId'],f"درون سرور با نام {server[6]}  کانفیگ برای یوزر ساخت نشد ")
              await db_manager.QueryWidthOutValue(f"DELETE FROM Service WHERE Id = {ServiceId.lastrowid}")
              return [ False,"هنگام ساخت کانفیگ مشکلی پیش آمد"]
         

          
             
         else:
             await db_manager.Query("INSERT INTO Configs(ServiceId,Name,uuid,Upload,Download,TotalUsed,TansformEnable,ServerId,State,isDelete,EndDate,CreateDate) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(ServiceId.lastrowid,email,str(uuid),0,0,0,Volume,server[0],1,0,endTimeMikro,int(datetime.datetime.timestamp(datetime.datetime.now()))))
            
             inviteId = await db_manager.execute_query_one(f"SELECT InvitedFrom FROM Users WHERE UserId =  {order[3]} ")
             if inviteId != None:
                    if  inviteId[0] !=None:
                    
                      
                       userInviter = await db_manager.execute_query_one(f"Select Wallet FROM Users WHERE UserId = {inviteId[0]}")
                       if userInviter !=None:
                        rew = await db_manager.execute_query_one("SELECT RewardInvite FROM Setting ")
                        price = 0
                        if order[9] != None:
                          price = order[9]
                        else :
                         price = order[6]
                      
                        res = userInviter[0] + (price * rew[0] / 100)
                        await db_manager.QueryWidthOutValue(f"UPDATE Users SET Wallet = {res} WHERE UserId = {inviteId[0]}")
                        await app.send_message(inviteId[0],f"""🤩 • کاربر گرامی توجه
                                               
❤️‍🔥 • کاربری که دعوت کرده بودید سرویس خریده است                                                

☑️ • نامبر ایدی: <code>{order[3]}</code>

💶 • مبلغ: {int(price * rew[0] / 100)}

💰 • کیف پول شما: {int(res)}

⚪️ • /start
""")

           
             await db_manager.QueryWidthOutValue(f"UPDATE OrdersList SET State = 1 WHERE Id = {order[0]} ")   
             countShopUser =  await db_manager.execute_query_one(f"SELECT CountShopped FROM Users WHERE UserId = {order[3]}")
             if countShopUser == None:
                   fileConfig =await ReadFileConfig()
                   await app.send_message(fileConfig['ownerId'],f" هنگام افزودن تعداد خرید")
                
                #   await db_manager.QueryWidthOutValue(f"UPDATE Users SET CountShopped  = {countShopUser[0] + 1} WHERE UserId = {order[3]}") 
             else:
                   await db_manager.QueryWidthOutValue(f"UPDATE Users SET CountShopped  = {countShopUser[0] + 1} WHERE UserId = {order[3]}") 
             countShell = await db_manager.execute_query_one(f"SELECT CountSell,ContSold FROM ServerPlans WHERE Id = {order[2]} ")
           
             if countShell[0] - 1 < countShell[1] + 1:
                await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET CountSell = {countShell[0] - 1 }  , ContSold = {countShell[1] + 1 } WHERE Id = {order[2]} ") 
                 
             await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET CountSell = {countShell[0] - 1 }  , ContSold = {countShell[1] + 1 } WHERE Id = {order[2]} ") 
             return [True,"کانفیگ با موفقیت تایید شد",ServiceId.lastrowid,order[3]]
  except:
        fileConfig =await ReadFileConfig()
        await app.send_message(fileConfig['ownerId'],f"هنگام ساخت کانفیگ تکی از سرور {server[6]}")
        return [ False,"هنگام ساخت کانفیگ مشکلی پیش آمد"]










async def CreateSub(orderId,app,free=0):
 order =  await db_manager.execute_query_one(f"SELECT * FROM OrdersList WHERE Id = {orderId} ")
 if order[4] == "BuySingle":
     return await CreateSingle(order,app)
 catId = await db_manager.execute_query_one(f"SELECT CatId,Volume,UserLimit FROM ServerPlans WHERE Id = {order[2]}")
 
 servers = await db_manager.execute_query_all(f"SELECT Server.* FROM ServerCat JOIN Server ON Server.Id = ServerCat.ServerId AND Server.State = 1  WHERE ServerCat.CatId = {order[11]}  ")
 days = int(order[7]) * 30
 allow = False
 
 fileConfig =await ReadFileConfig()
 
 randomId  = random.randint(100, 9999)  
 random2Id =random.randint(100, 9999)  

 EndTime = datetime.datetime.now() + datetime.timedelta(days=days)
 Volume = catId[1] * 1024 * 1024 * 1024
 SubName = await db_manager.execute_query_one("SELECT SubName,LockChanel FROM Setting")
 email =f"{randomId}-{random2Id}"

 configUrl =get_random_string(12)
 uuid=uuid4()
 endTimeMikro =int(datetime.datetime.timestamp(EndTime) ) * 1000
 counter = 0
 serversCount = []
 ServceId = await db_manager.Query("INSERT INTO Service(UserId,Email,Password,CreateDate,EndDate,OrderId,PlanId,CatId,ServerIds,configUrl,TransformEnable,RandomId,TypeService,ServiceTest,UserLimit) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(order[3],email,str(uuid),int(datetime.datetime.timestamp(datetime.datetime.now())),endTimeMikro,order[0],order[2],order[11],f'{serversCount}',configUrl,Volume,randomId,"sub","empty",catId[2]))
 for server in servers :

  try:     
      data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ str(uuid) +'", "alterId": 0, "email": "'+ email +'", "totalGB": '+ str(int(Volume)) +', "expiryTime": '+str(endTimeMikro)+', "enable": true , "limitIp":'+ str(catId[2]) + '   , "tgId": "", "subId": ""}]}'
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
                 await app.send_message(fileConfig['ownerId'],f"""درون سرور با نام {server[6]}  کانفیگ برای یوزر ساخت نشد 
                                        
جزییات پاسخ سرور : {data['msg']}                                    
                                        
عملیات افزودن خودکار اعمال نخواهد شد 
                                        """)


          
             
         else:
             counter +=1
             serversCount.append(server[0])
             await db_manager.Query("INSERT INTO Configs(ServiceId,Name,uuid,Upload,Download,TotalUsed,TansformEnable,ServerId,State,isDelete,EndDate,CreateDate) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(ServceId.lastrowid,email,str(uuid),0,0,0,Volume,server[0],1,0,endTimeMikro,int(datetime.datetime.timestamp(datetime.datetime.now()))))
             
             
             
  except:

      await db_manager.Query("INSERT INTO imperfect(Type,DateCreateImperfect,ServiceId,ServerId) VALUES(?,?,?,?)",("insert",datetime.datetime.now().timestamp(),ServceId.lastrowid,server[0]))

 if counter != 0:
             
             await db_manager.QueryWidthOutValue(f"UPDATE Service SET ServerIds = '{str(serversCount)}' WHERE Id= {ServceId.lastrowid}")
            
             inviteId = await db_manager.execute_query_one(f"SELECT InvitedFrom FROM Users WHERE UserId =  {order[3]} ")
             if inviteId != None:
                    if  inviteId[0] !=None:
                   
                      
                       userInviter = await db_manager.execute_query_one(f"Select Wallet FROM Users WHERE UserId = {inviteId[0]}")
                       if userInviter !=None:
                        rew = await db_manager.execute_query_one("SELECT RewardInvite FROM Setting ")
                        price = 0
                        if order[9] != None:
                          price = order[9]
                        else :
                         price = order[6]
                      
                        res = userInviter[0] + (price * rew[0] / 100)
                        await db_manager.QueryWidthOutValue(f"UPDATE Users SET Wallet = {res} WHERE UserId = {inviteId[0]}")
                        await app.send_message(inviteId[0],f"""🤩 • کاربر گرامی توجه
                                               
❤️‍🔥 • کاربری که دعوت کرده بودید سرویس خریده است                                                

☑️ • نامبر ایدی: <code>{order[3]}</code>

💶 • مبلغ: {int(price * rew[0] / 100)}

💰 • کیف پول شما: {int(res)}

⚪️ • /start
""")

             if free==0 :
              await db_manager.QueryWidthOutValue(f"UPDATE OrdersList SET State = 1 WHERE Id = {order[0]} ")   
             countShopUser =  await db_manager.execute_query_one(f"SELECT CountShopped FROM Users WHERE UserId = {order[3]}")
             if countShopUser != None:
                                   await db_manager.QueryWidthOutValue(f"UPDATE Users SET CountShopped  = {countShopUser[0] + 1} WHERE UserId = {order[3]}") 

                
                #   await db_manager.QueryWidthOutValue(f"UPDATE Users SET CountShopped  = {countShopUser[0] + 1} WHERE UserId = {order[3]}") 
       
             countShell = await db_manager.execute_query_one(f"SELECT CountSell,ContSold FROM ServerPlans WHERE Id = {order[2]} ")
           
             if countShell[0] - 1 < countShell[1] + 1:
                await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET CountSell = {countShell[0] - 1 }  , ContSold = {countShell[1] + 1 } WHERE Id = {order[2]} ") 
                 
             await db_manager.QueryWidthOutValue(f"UPDATE ServerPlans SET CountSell = {countShell[0] - 1 }  , ContSold = {countShell[1] + 1 } WHERE Id = {order[2]} ") 
             return [True,"کانفیگ با موفقیت تایید شد",ServceId.lastrowid,order[3]]
 else:
     await db_manager.QueryWidthOutValue(f"DELETE FROM imperfect WHERE ServiceId = {ServceId.lastrowid}")
     await db_manager.QueryWidthOutValue(f"DELETE FROM Configs WHERE ServiceId = {ServceId.lastrowid}")
     await db_manager.QueryWidthOutValue(f"DELETE FROM Service WHERE Id = {ServceId.lastrowid}")
     return [ False,"هنگام ساخت کانفیگ هیچ سروری متصل نبود !"]
    







async def UpdateorderPrice(orderId,Price):
    await db_manager.QueryWidthOutValue(f"UPDATE OrdersList SET Price = {Price} WHERE Id = {orderId}")
def generate_password(length):
    characters = [random.choice(string.ascii_letters +string.ascii_lowercase + string.digits ) for _ in range(length)]
    random.shuffle(characters)
    return ''.join(characters)
 
async def SuccessWallet(orderId):
  try:  
    order = await db_manager.execute_query_one(f"SELECT * FROM OrdersList WHERE Id = {orderId}")
    walletUser = await db_manager.execute_query_one(f"SELECT Wallet FROM Users WHERE UserId = {order[3]}")
    wallet = walletUser[0] + order[6]
    await db_manager.QueryWidthOutValue(f"UPDATE Users SET wallet = {wallet} WHERE UserId = {order[3]} ")
    await db_manager.QueryWidthOutValue(f"UPDATE OrdersList SET State = 1 WHERE Id = {orderId} ")
    return [True,f"کاربر گرامی مبلغ {order[6]} ✅به حساب شما افزوده شد و توسط ادمین تایید شد ",order[3]]

  except:
      return [False,"هنگام تایید مشکلی پیش امد"]  
def get_random_string(length):
   
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def FindTrojanPass(conf: str):
    content = conf[9:]
    return content.split("@")[0]


async def SearchConfigUser(ConfigUser):
  try:

    subAddressBot =await db_manager.execute_query_one("SELECT SubDomain FROM Setting ")

    if ConfigUser.strip().startswith("vless://"):
           
           uuid = convert_link_vless(ConfigUser)
    elif ConfigUser.strip().startswith("vmess://"):
    
        uuid = convert_link_vmess(ConfigUser)
        if uuid=="configKosSher":
            
              return [False,0]
    
    elif ConfigUser.strip().startswith("trojan://"):
       
        uuid = FindTrojanPass(ConfigUser)
        trojan = True
    elif "vnext" in ConfigUser:
       
        details = json.loads(ConfigUser)
    
        if details["outbounds"][0]["protocol"] == "trojan":
         trojan = True
         uuid = details["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"]
    elif ConfigUser.strip().startswith("wings://"):
      
      data = wings(ConfigUser)
    
      if data["outbound"]["protocol"] == "trojan":
        trojan = True
        uuid = data["outbound"]["uuid"]
    
    
    elif subAddressBot[0] in ConfigUser :
        tokenConfig =  ConfigUser.split("?token=")[1]
        Servcice = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE ConfigURL = '{tokenConfig}' ")
        if Servcice != None:
           return [True , Servcice]
        else:
          return [False,0]
            


    else:
        uuid = ConfigUser
    Servcice = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE Password = '{uuid}' OR ConfigURL = '{uuid}' OR Email = '{uuid}' ")    
    if Servcice != None:
           return [True , Servcice]
    else:
          return [False,0]
  except:
         return [False,0]
async def GetConfigInfo(ConfigUser):
  try:

    counterDisable = 0
    email = ""
    uuid  = ""
    allow = False
    trojan = False
    startUse = ""
    addToDate = ""
    jalili_date = ""
    subAddressBot = await db_manager.execute_query_one("SELECT SubDomain FROM Setting ")

    if ConfigUser.strip().startswith("vless://"):
           
           uuid = convert_link_vless(ConfigUser)
    elif ConfigUser.strip().startswith("vmess://"):
    
        uuid = convert_link_vmess(ConfigUser)
        if uuid=="configKosSher":
            
            return [False,"لطفا کانفیگ خود را به درستی وارد کنید"]
    
    elif ConfigUser.strip().startswith("trojan://"):
       
        uuid = FindTrojanPass(ConfigUser)
        trojan = True
    elif "vnext" in ConfigUser:
       
        details = json.loads(ConfigUser)
    
        if details["outbounds"][0]["protocol"] == "trojan":
         trojan = True
         uuid = details["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"]
    elif ConfigUser.strip().startswith("wings://"):
      
      data = wings(ConfigUser)
    
      if data["outbound"]["protocol"] == "trojan":
        trojan = True
        uuid = data["outbound"]["uuid"]
    
    
    elif subAddressBot[0] in ConfigUser:
        tokenConfig =  ConfigUser.split("?token=")[1]
        ServiceId = await db_manager.execute_query_one(f"SELECT Id FROM Service WHERE ConfigURL = '{tokenConfig}' ")
        if ServiceId != None:
            return await GetCofigUser(ServiceId[0])
        else:
          return [ False,"سرویس یافت نشد"]
            


    else:
        uuid = ConfigUser
    ServiceId = await db_manager.execute_query_one(f"SELECT Id FROM Service WHERE Password = '{uuid}' AND TypeService = 'sub' ")
    if ServiceId != None:
            return await GetCofigUser(ServiceId[0])
           
    data = {
         "expired_at": 0,
         "transfer_enable":0,
         "d":0,
         "u":0,
         "subscribe_url":'',
         "state":1,
         "subsingle" : ""
     }
    servers = await db_manager.execute_query_all("SELECT * FROM Server  ")
    
    for server in servers :
     try:    
         if email != "":
            break
           
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

         async with httpx.AsyncClient() as clienthttp:
          response = None
          try:

             headers['Cookie']  = f"lang=en-US; {server[8]}"
             response = await  clienthttp.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list",headers= headers, timeout=6)
          except:
           response = await  clienthttp.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list",headers= headers, timeout=6)
         info_json = json.loads(response.text)
          
          
      
         inbounds = info_json["obj"]
         
         for inbound in inbounds:
            if email != "":
                break
            settings = json.loads(inbound['settings'])
            for client in settings['clients']:
                if inbound["protocol"] == "trojan":
                    if trojan == True:
                        if uuid == client['password']:
                            email = client['email']
                            break

                else:
                    if uuid == client['id']:
                        email = client['email']
                        break

            if email != "":
             
                states = inbound['clientStats']
              
                for state in states:
                    if state["email"] == email:
                                data['expired_at'] = state['expiryTime']
                                data['transfer_enable'] = state['total']
                                data['d'] = state['down']
                                data['u'] = state['up']
                                data['subscribe_url'] = GetConfig(inbound["streamSettings"], uuid, email, inbound["port"],
                                           inbound["protocol"], server[5])
                                 
                                if state['expiryTime'] != 0 and int(datetime.datetime.timestamp(datetime.datetime.now())) >= (state['expiryTime']/1000):
                                 data['state'] = 0
                                if state['total'] != 0 and (data['d'] + data['u']) >= state['total']:
                                     data['state'] = 0
                                return [True,"کانفیگ با موفقیت دریافت شد...",data,f"{email}" ]
    
     except:
         pass 
    return [ False,"سرویس یافت نشد"]

  except :
         return [ False,"هنگام دریافت سرویس مشکلی پیش آمد !"] 
async def GetConfigSingleUser(pay):
    serverIds = ast.literal_eval(pay[17]) 
    try:
      counterDisable = 0
      data = {
         "expired_at": pay[7],
         "transfer_enable": pay[18],
         "d":0,
         "u":0,
         "subscribe_url":'',
         "state":pay[16],
         "subsingle" : ""
     }
    
      try:
       chanel = await db_manager.execute_query_one("SELECT LockChanel FROM Setting")     
       nameConfog = pay[3] + f' - @{chanel[0]}' 
       server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {serverIds[0]}")
       origin= server[3].split("/")
       async with httpx.AsyncClient() as client:
         response = None
         
       

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
         
         
         try:
              response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers = headers, timeout=6)
         except:
              response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers=headers, timeout=6)  
       
         info_json = json.loads(response.text)
         inbounds = info_json["obj"]
       
         for inbound in inbounds:
           if inbound['id']  == server[10]:
               states = inbound['clientStats']
               for state in states:
                    if state["email"] == pay[3]:
                                print(state)
                                data['expired_at'] = state['expiryTime']
                                data['transfer_enable'] = state['total']
                                data['d'] = state['down']
                                data['u'] = state['up']
                                data['subscribe_url'] = GetConfig(inbound["streamSettings"], pay[4], nameConfog, inbound["port"],
                                           inbound["protocol"], server[5])
                                 
                                if state['expiryTime'] != 0 and int(datetime.datetime.timestamp(datetime.datetime.now())) >= (state['expiryTime']/1000):
                                 data['state'] = 0
                                if state['total'] != 0 and (data['d'] + data['u']) >= state['total']:
                                     data['state'] = 0
                                subdomain = await db_manager.execute_query_one("SELECT SubDomain , SubSingle FROM Setting ")
                                if subdomain[1] == 1 :

                                    data['subsingle'] = f"{subdomain[0]}/kaiser?token={pay[2]}"     
                                return [True,"کانفیگ با موفقیت دریافت شد...",data,f"{pay[3]}" ]

                            
                        
                        
      except:
          return [ False,"هنگام دریافت سرویس مشکلی پیش آمد !"]
     
      
    
    except:
       return [ False,"هنگام دریافت سرویس مشکلی پیش آمد !"]

async def GetCofigUser(data):
    
    pay = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE Id = {data} AND isDelete = 0")
    if pay == None:
        return [ False,"سرویس شما از سرور پاک شده "]
    if pay[24] =="single":
        return await GetConfigSingleUser(pay)
    serverIds = ast.literal_eval(pay[17]) 
    try:
     counterDisable = 0
     data = {
         "expired_at": pay[7],
         "transfer_enable": pay[18],
         "d":0,
         "u":0,
         "subscribe_url":'',
         "state":pay[16],
         "subsingle" : ""
     }
     for serverId in serverIds:
      try:

       server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {serverId}")
       origin= server[3].split("/")
       async with httpx.AsyncClient() as client:
         response = None
         

     
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

         try:
              response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers = headers, timeout=6)
         except:
              response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers=headers, timeout=6)  
       
         info_json = json.loads(response.text)
         inbounds = info_json["obj"]
       
         for inbound in inbounds:
           if inbound['id']  == server[10]:
               states = inbound['clientStats']
               for state in states:
                    if state["email"] == pay[3]:
                        data['d']+= state['down']
                        data['u']+= state['up']
                        break

                            
                        
                        
      except:
          pass
     
      
     
     subdomain = await db_manager.execute_query_one("SELECT SubDomain FROM Setting ")
     data['subscribe_url'] = f"{subdomain[0]}/kaiser?token={pay[2]}"
     return [True,"سرویس با موفقیت دریافت شد...",data,f"{pay[3]}" ]
    except:
       return [ False,"هنگام دریافت سرویس مشکلی پیش آمد !"]

                           
async def CheckUserService(app):
   servers = await db_manager.execute_query_all("SELECT * FROM Server")


   async def UpdateData(server, semaphore):
         async with semaphore:
          origin = server[3].split("/")
          try:
            limits = httpx.Limits(max_connections=4)  
            async with httpx.AsyncClient(limits=limits) as client:

                print(server[6])
                response =None
        
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Origin': f'{origin[0]}://{origin[2]}',
                    'Connection': 'keep-alive',
                    'Referer': f'{server[3]}/{"panel"if server[4]== "sanaei" else "xui"}/inbounds',
                    'Cookie': f'lang=en-US; {server[8]}'
                }

                try:
                    response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers=headers, timeout=6)
                except:
                    response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers=headers, timeout=6)

                info_json = json.loads(response.text)
                inbounds = info_json["obj"]

                for inbound in inbounds:
                    if inbound['id'] == server[10]:
                        for servicedata in inbound['clientStats']:
                           config = await db_manager.QueryWidthOutValue(f"UPDATE Configs SET  Upload = {servicedata['up']} , Download = {servicedata['down']} ,TotalUsed = {servicedata['up'] + servicedata['down']} WHERE Name == '{servicedata['email']}' AND ServerId = {server[0]}  ")
                        await ServerManager.QueryWidthOutValue(f"UPDATE ServerData SET Data = '{json.dumps( inbound['clientStats'])}' WHERE ServerId = {server[0]} ")
                        break
          except:
            pass
              
   semaphore = asyncio.Semaphore(1)  
   await asyncio.gather(*[UpdateData(server, semaphore) for server in servers])
   
   configData =  await ReadFileConfig()
   print(configData['offset'])
   Services = await db_manager.execute_query_all(f"SELECT * FROM Service WHERE isDelete = 0 LIMIT 500 OFFSET {configData['offset']}")
   
   AlertVolume = await db_manager.execute_query_one("SELECT SendAlertVolumeFirst,SendAlertVolumeTwo FROM Setting") 
   if Services == None or Services == []: 
        configData['offset'] = 0
        await SaveFileConfig(configData)
        return
   async def check_service(service,semaphore):
     async with semaphore:  
       async def disableConfig(server_id,semaphore):

        async with semaphore:
     
         try:

          server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {server_id}")
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
    "settings": '{"clients": [{"id": "'+ service[4] +'", "alterId": 0, "email": "'+ service[3] +'", "totalGB": '+ str(int(service[18])) +', "expiryTime": '+str(service[7])+', "enable": false , "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
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
               await db_manager.QueryWidthOutValue(f"UPDATE Configs SET State = 0 WHERE ServiceId = {service[0]} AND ServerId = {server[0]}")


             
         except:

              config = await db_manager.execute_query_one(f"SELECT * FROM Configs WHERE ServerId = {server[0]} AND ServiceId = {service[0]}")
              await db_manager.Query("INSERT INTO imperfect(Type,ConfigId,UserId,DateCreateImperfect) VALUES(?,?,?,?)",("disable",config[0],service[1],datetime.datetime.now().timestamp()))   
             
           
        
       serverIds  = ast.literal_eval(service[17])
    #    upload  = 0
    #    download = 0
    #    total_usage = 0 
    #    for serverId in serverIds:
    #       try:  
    #           serverDataCatch = await ServerManager.execute_query_one(f"SELECT Data FROM ServerData WHERE ServerId  = {serverId}")
    #           serverData = ""
    #           try:
    #            serverData = json.loads(serverDataCatch[0])
    #           except:
    #             serverDataCatch = await ServerManager.execute_query_one(f"SELECT Data FROM ServerData WHERE ServerId  = {serverId}")
    #             serverData = json.loads(serverDataCatch[0])
    #           for data in serverData:
    #               if data['email'] == service[3]:
    #                   upload+= data['up']
    #                   download += data['down']
                      
    #                   break
    #       except:
    #           pass     
    # 
    # 
    #        
       
       download = await db_manager.execute_query_one(f"SELECT SUM(Download) FROM Configs WHERE ServiceId = {service[0]}")
       upload = await db_manager.execute_query_one(f"SELECT SUM(Upload) FROM Configs WHERE ServiceId = {service[0]}")
       print(service[3])
       try:
        total_usage = download[0] + upload[0]
        if AlertVolume[0] != 0:                   
         if service[21] == 0:
           
          if (service[18] - total_usage) <= (AlertVolume[0] * 1024 * 1024 * 1024):
               await db_manager.QueryWidthOutValue(f"UPDATE Service SET AlertVolumeFirst = 1  WHERE Id = {service[0]} ") 
             
        if AlertVolume[1] != 0 :
         if service[22] == 0 :
            if (service[18] - total_usage) <= (AlertVolume[1] * 1024 * 1024 * 1024):
                        await db_manager.QueryWidthOutValue(f"UPDATE Service SET AlertVolumeTwo = 1  WHERE Id = {service[0]} ") 
                        
           
                
        if total_usage >= service[18]:
            semaphore = asyncio.Semaphore(6)  
            try:
             await asyncio.gather(*[disableConfig(serverId, semaphore) for serverId in serverIds])
             configsDisabled = await db_manager.execute_query_one(f"SELECT * FROM Configs WHERE State = 1 AND ServiceId = {service[0]}")
             if configsDisabled == None:
                 
                 await db_manager.QueryWidthOutValue(f"UPDATE Service SET State = 0 , Upload = {upload[0]} , Download = {download[0]} , TotalUsed = {total_usage} WHERE Id = {service[0]} ") 
           

            except : 
                 await db_manager.QueryWidthOutValue(f"UPDATE Service SET Upload = {upload[0]} , Download = {download[0]} , TotalUsed = {total_usage} WHERE Id = {service[0]} ") 

          
        else:
            await db_manager.QueryWidthOutValue(f"UPDATE Service SET Upload = {upload[0]} , Download = {download[0]} , TotalUsed = {total_usage} WHERE Id = {service[0]} ") 
       
       except:
           ...
  
   
   semaphore = asyncio.Semaphore(1)  
   await asyncio.gather(*[check_service(service, semaphore) for service in Services])
   configData['offset'] += 500 
   print(configData['offset'])
   await SaveFileConfig(configData)
   return

  

  
                           
async def CheckUserServiceEnd(app):
   servers = await db_manager.execute_query_all("SELECT * FROM Server")

   async def UpdateData(server, semaphore):
         async with semaphore:   
          origin = server[3].split("/")
          try:  
            limits = httpx.Limits(max_connections=4)  
            async with httpx.AsyncClient(limits=limits) as client:

                print(server[6])
                response = None
            
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Origin': f'{origin[0]}://{origin[2]}',
                    'Connection': 'keep-alive',
                    'Referer': f'{server[3]}/{"panel"if server[4]== "sanaei" else "xui"}/inbounds',
                    'Cookie': f'lang=en-US; {server[8]}'
                }

                try:
                    response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers=headers, timeout=6)
                except:
                    response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers=headers, timeout=6)

                info_json = json.loads(response.text)
                inbounds = info_json["obj"]

                for inbound in inbounds:
                    if inbound['id'] == server[10]:
                   
                        await ServerManager.QueryWidthOutValue(f"UPDATE ServerData SET Data = '{json.dumps( inbound['clientStats'])}' WHERE ServerId = {server[0]} ")
                        break
          except:
                  data = await ReadFileConfig()
                  await app.send_message(data['ownerId'],f"سرور {server[6]}")              
   semaphore = asyncio.Semaphore(1)  
   await asyncio.gather(*[UpdateData(server, semaphore) for server in servers])
   

   Services = await db_manager.execute_query_all("SELECT * FROM Service ")
   AlertVolume = await db_manager.execute_query_one("SELECT SendAlertVolumeFirst,SendAlertVolumeTwo FROM Setting") 
   if Services == None : 
        return

   async def check_service(service,semaphore):
     async with semaphore:  
       async def disableConfig(server_id,semaphore):
         async with semaphore:
       

          server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {server_id}")
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
    "settings": '{"clients": [{"id": "'+ service[4] +'", "alterId": 0, "email": "'+ service[3] +'", "totalGB": '+ str(int(service[18])) +', "expiryTime": '+str(service[7])+', "enable": false,  "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
}
          limits = httpx.Limits(max_connections=3)
          async with httpx.AsyncClient(limits=limits) as client:
           response =None



           headers['Cookie'] = f"lang=en-US; {server[8]}"
           response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{service[4]}',data=data,headers=headers)
           data = json.loads(response.text)
         
           if data['success'] == False or response.status_code!=200:
              data = await ReadFileConfig()
              await app.send_message(data['ownerId'],f"""🔔 توجه ادمین گرامی 

سرور با نام {server[6]} هنگام غیر فعال کردن سرویس {service[3]} با uuid {service[4]}
مشکلی پیش آمد
و سرویس غیر فعال شد لطفا به صورت دستی ان را از پنل غیر فعال کنید

با تشکر ❤️
""")
             
              
        
           
        
       serverIds  = ast.literal_eval(service[17])
       upload  = 0
       download = 0
       total_usage = 0 
       for serverId in serverIds:
          try:  
              serverDataCatch = await ServerManager.execute_query_one(f"SELECT Data FROM ServerData WHERE ServerId  = {serverId}")
              serverData = ""
              try:
               serverData = json.loads(serverDataCatch[0])
              except:
                serverDataCatch = await ServerManager.execute_query_one(f"SELECT Data FROM ServerData WHERE ServerId  = {serverId}")
                serverData = json.loads(serverDataCatch[0])
              for data in serverData:
                  if data['email'] == service[3]:
                      upload+= data['up']
                      download += data['down']
                      
                      break
          except:
              pass            
       total_usage = download + upload
       if AlertVolume[0] != 0:                   
        if service[21] == 0:
           
          if   (service[18] - total_usage) <= (AlertVolume[0] * 1024 * 1024 * 1024):
               await db_manager.QueryWidthOutValue(f"UPDATE Service SET AlertVolumeFirst = 1  WHERE Id = {service[0]} ") 
             
       if AlertVolume[1] != 0 :
        if service[22] == 0 :
            if (service[18] - total_usage) <= (AlertVolume[1] * 1024 * 1024 * 1024):
                        await db_manager.QueryWidthOutValue(f"UPDATE Service SET AlertVolumeTwo = 1  WHERE Id = {service[0]} ") 
                        
           
                
       if total_usage >= service[18]:
            semaphore = asyncio.Semaphore(6)  
            try:
             await asyncio.gather(*[disableConfig(serverId, semaphore) for serverId in serverIds])
             await db_manager.QueryWidthOutValue(f"UPDATE Service SET State = 0 , Upload = {upload} , Download = {download} , TotalUsed = {total_usage} WHERE Id = {service[0]} ") 
             print('Disabled User')
            except : 
             data = await ReadFileConfig()
             await app.send_message(data['ownerId'],f" {service[3]}هنگام غیر فعال سازی مشکلی پیش آومده")
          
       else:
            await db_manager.QueryWidthOutValue(f"UPDATE Service SET Upload = {upload} , Download = {download} , TotalUsed = {total_usage} WHERE Id = {service[0]} ") 
       

  
   semaphore = asyncio.Semaphore(1)  
   await asyncio.gather(*[check_service(service, semaphore) for service in Services])
   return


async def GetCofigUserANDChange(data,app):
    try:
        service = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE Id = {data} AND isDelete = 0")

        configUrl =get_random_string(12)
        uuid=uuid4()
        serverIdes =  serverIds  = ast.literal_eval(service[17])
        for serverId in serverIds:
         try: 
          server = await db_manager.execute_query_one(f"SELECT * FROM server WHERE Id = {serverId}")
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
    "settings": '{"clients": [{"id": "'+ str(uuid) +'", "alterId": 0, "email": "'+ service[3] +'", "totalGB": '+ str(int(service[18])) +', "expiryTime": '+str(service[7])+', "enable": true,  "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
}
        
          async with httpx.AsyncClient() as client:
           response = None

         
           headers['Cookie'] = f"lang=en-US; {server[8]}"

           try:
            response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{service[4]}',data=data,headers=headers)
           except:
            response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{service[4]}',data=data,headers=headers)
               
           data = json.loads(response.text)
           
           if data['success'] ==True  :
               await db_manager.QueryWidthOutValue(f"UPDATE Configs SET uuid = '{str(uuid)}' WHERE ServerId = {serverId} AND ServiceId = {service[0]} ")
           else:
              config = await db_manager.execute_query_one(f"SELECT * FROM Configs WHERE ServerId = {serverId} AND ServiceId = {service[0]}")
              await db_manager.Query("INSERT INTO imperfect(Type , ConfigId,uuid,UserId,DateCreateImperfect) VALUES(?,?,?,?,?)",("change",config[0],str(uuid),service[1],datetime.datetime.now().timestamp()))
                   
         except:
              config = await db_manager.execute_query_one(f"SELECT * FROM Configs WHERE ServerId = {serverId} AND ServiceId = {service[0]}")
              await db_manager.Query("INSERT INTO imperfect(Type , ConfigId,uuid,UserId,DateCreateImperfect) VALUES(?,?,?,?,?)",("change",config[0],str(uuid),service[1],datetime.datetime.now().timestamp()))
        await db_manager.QueryWidthOutValue(f"UPDATE Service SET ConfigURL = '{configUrl}'  , Password = '{str(uuid)}' WHERE Id = {service[0]}")
        return await GetCofigUser(service[0])

    except:
      return [False,"هنگام تغییر مشکلی پیش آمد"]            
    
async def GetCofigUserTest(userId):
 test = await db_manager.execute_query_one("SELECT * FROM TestFree")
 servers = None
 if test[4] == 0:
     servers = await db_manager.execute_query_all(f"SELECT Server.* FROM ServerCat JOIN Server ON Server.Id = ServerCat.ServerId AND Server.State = 1  WHERE ServerCat.CatId = {test[5]}  ")
     
     allow = False
     fileConfig =await ReadFileConfig()
     
     randomId  = random.randint(100, 9999)  
     random2Id =random.randint(100, 9999)  
     TestName = await db_manager.execute_query_one("SELECT TestName,LockChanel FROM Setting")
     EndTime = datetime.datetime.now() + datetime.timedelta(days=int(test[2]))
     Volume = test[1] * 1024 * 1024 * 1024
     email =f"{randomId}-{random2Id}"
     configUrl =get_random_string(12)
     uuid=uuid4()
     endTimeMikro =int(datetime.datetime.timestamp(EndTime) ) * 1000
     counter = 0
     serversCount = []
     ServiceId = await db_manager.Query("INSERT INTO Service(UserId,Email,Password,CreateDate,EndDate,OrderId,PlanId,CatId,ServerIds,configUrl,TransformEnable,RandomId,TypeService,ServiceTest) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(userId,email,str(uuid),int(datetime.datetime.timestamp(datetime.datetime.now())),endTimeMikro,0,0,test[5],f'{serversCount}',configUrl,Volume,randomId,"sub","ok"))
 
     for server in servers :
 
      try:     
       data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ str(uuid) +'", "alterId": 0, "email": "'+ email +'", "totalGB": '+ str(int(Volume)) +', "expiryTime": '+str(endTimeMikro)+', "enable": true, "tgId": "", "subId": ""}]}'
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
  'Referer': f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbounds',
  'Cookie': ''
}

       async with httpx.AsyncClient() as client:
   
         
         headers['Cookie']  = f"lang=en-US; {server[8]}"
         try:
          response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers)
         except:
          response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers)
         data = json.loads(response.text)
         
         if data['success'] == False:
             pass
             
         else:
             counter +=1
             serversCount.append(server[0])
             await db_manager.Query("INSERT INTO Configs(ServiceId,Name,uuid,Upload,Download,TotalUsed,TansformEnable,ServerId,State,isDelete,EndDate,CreateDate) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(ServiceId.lastrowid,email,str(uuid),0,0,0,Volume,server[0],1,0,endTimeMikro,int(datetime.datetime.timestamp(datetime.datetime.now()))))


             
             
      except:
       pass
     if counter != 0:
             await db_manager.QueryWidthOutValue(f"UPDATE Service SET ServerIds = '{serversCount}' WHERE Id= {ServiceId.lastrowid}")
           
             await db_manager.QueryWidthOutValue(f"UPDATE Users SET UseFreeTrial = 1 WHERE UserId = {userId}")
             await db_manager.QueryWidthOutValue(f"UPDATE TestFree SET Geted = {test[6]+1} ")
             return [True,"کانفیگ با موفقیت تایید شد",ServiceId.lastrowid,email]
     else:
         await db_manager.QueryWidthOutValue(f"DELETE FROM Service WHERE Id = {ServiceId.lastrowid}")
         return [ False,"هنگام ساخت کانفیگ هیچ سروری متصل نبود !"]


 else:   
     server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {test[4]}  ")
      
     allow = False
     randomId  = random.randint(100, 9999)  
     random2Id =random.randint(100, 9999)  
     TestName = await db_manager.execute_query_one("SELECT TestName,LockChanel FROM Setting")
     EndTime = datetime.datetime.now() + datetime.timedelta(days=int(test[2]))
     Volume = test[1] * 1024 * 1024 * 1024
     email =f"{randomId}-{random2Id}"
     configUrl =get_random_string(12)
     uuid=uuid4()
     endTimeMikro =int(datetime.datetime.timestamp(EndTime) ) * 1000
     counter = 0
     serversCount = []
 
     ServiceId = await db_manager.Query("INSERT INTO Service(UserId,Email,Password,CreateDate,EndDate,OrderId,PlanId,CatId,ServerIds,configUrl,TransformEnable,RandomId,TypeService,ServiceTest) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(userId,email,str(uuid),int(datetime.datetime.timestamp(datetime.datetime.now())),endTimeMikro,0,0,test[5],f'[{server[0]}]',configUrl,Volume,randomId,"single","ok"))
    
 
    #  try:     
     data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ str(uuid) +'", "alterId": 0, "email": "'+ email +'", "totalGB": '+ str(int(Volume)) +', "expiryTime": '+str(endTimeMikro)+', "enable": true, "tgId": "", "subId": ""}]}'
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
  'Referer': f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbounds',
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
             await db_manager.QueryWidthOutValue(f"DELETE FROM Service WHERE Id = {ServiceId.lastrowid}")
             return [False , "هنگام افزودن یه مشکل خوردیم"]
             
         else:
             
             await db_manager.QueryWidthOutValue(f"UPDATE Users SET UseFreeTrial = 1 WHERE UserId = {userId}")
             await db_manager.QueryWidthOutValue(f"UPDATE TestFree SET Geted = {test[6]+1} ")
             return [True,"کانفیگ با موفقیت تایید شد",ServiceId.lastrowid,email]

             
             
    #  except:
    #    return [False , "هنگام افزودن یه مشکل خوردیم"]
    
async def EditVolumeConfig(serviceId,c,volume)    :
    try:
      service = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE Id = {serviceId}")
      serverIds  = ast.literal_eval(service[17])
      newvolume = int(volume) * 1024 * 1024 * 1024
      for serverId in serverIds:
          
        server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {serverId}")
        try:
          if server == None :
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
    "settings": '{"clients": [{"id": "'+ service[4] +'", "alterId": 0, "email": "'+ service[3] +'", "totalGB": '+ str(newvolume) +', "expiryTime": '+str(service[7])+', "enable": true, "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
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
         
           if data['success'] == False or response.status_code!=200:
              data = await ReadFileConfig()
              await c.send_message(data['ownerId'],f"""🔔 توجه ادمین گرامی 

سرور با نام {server[6]} هنگام غیر فعال کردن یا فعال کردن سرویس {service[3]} با uuid {service[4]}
مشکلی پیش آمد
و سرویس غیر فعال شد لطفا به صورت دستی ان را از پنل غیر فعال کنید

با تشکر ❤️
""")
        except:
              
              await c.send_message(data['ownerId'],f"""🔔 توجه ادمین گرامی 

سرور با نام {server[6]} هنگام غیر فعال کردن یا فعال سرویس {service[3]} با uuid {service[4]}
مشکلی پیش آمد

لطفا هر چه سریع تر اتصال را بررسی و مجدد امتحان کنید

با تشکر ❤️
""")
              return False
     
      await db_manager.QueryWidthOutValue(f"UPDATE Service SET TransformEnable = {newvolume} WHERE Id = {serviceId}")        
           
      return True 
    except:
        return False              

async def EditDateConfig(serviceId,c,days,typedate)    :
    try:
      service = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE Id = {serviceId}")
      serverIds  = ast.literal_eval(service[17])
      date = 0
      if typedate == True :
          
       date = datetime.datetime.fromtimestamp(service[7]/1000) + datetime.timedelta(days=days)
      else:
       date = datetime.datetime.fromtimestamp(service[7]/1000) - datetime.timedelta(days=days)
           
      newdate = datetime.datetime.timestamp(date) * 1000

      for serverId in serverIds:
          
        server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {serverId}")
        try:
          if server == None :
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
    "settings": '{"clients": [{"id": "'+ service[4] +'", "alterId": 0, "email": "'+ service[3] +'", "totalGB": '+ str(service[18]) +', "expiryTime": '+str(int(newdate))+', "enable": true, "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
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
         
           if data['success'] == False or response.status_code!=200:
              data = await ReadFileConfig()
              await c.send_message(data['ownerId'],f"""🔔 توجه ادمین گرامی 

سرور با نام {server[6]} هنگام تغییر زمان سرویس {service[3]} با uuid {service[4]}
مشکلی پیش آمد
و سرویس غیر فعال شد لطفا به صورت دستی ان را از پنل غیر فعال کنید

با تشکر ❤️
""")
        except:
              
              await c.send_message(data['ownerId'],f"""🔔 توجه ادمین گرامی 

سرور با نام {server[6]} هنگام تغییر زمان {service[3]} با uuid {service[4]}
مشکلی پیش آمد

لطفا هر چه سریع تر اتصال را بررسی و مجدد امتحان کنید

با تشکر ❤️
""")
              return False
     
      await db_manager.QueryWidthOutValue(f"UPDATE Service SET EndDate = {newdate} WHERE Id = {serviceId}")        
           
      return True 
    except:
        return False                      
async def DisableOrEnableConfig(serviceId,c,typeUpdate):
    try:
      service = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE Id = {serviceId}")
      serverIds  = ast.literal_eval(service[17])
      for serverId in serverIds:
          
        server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {serverId}")
        try:
          if server == None :
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
    "settings": '{"clients": [{"id": "'+ service[4] +'", "alterId": 0, "email": "'+ service[3] +'", "totalGB": '+ str(int(service[18])) +', "expiryTime": '+str(service[7])+', "enable": '+ typeUpdate+', "limitIp":'+ str(service[28]) + ', "tgId": "", "subId": ""}]}'
}
          limits = httpx.Limits(max_connections=1)
          async with httpx.AsyncClient(limits=limits) as client:
           response = None
         
           headers['Cookie'] = f"lang=en-US; {server[8]}"
           try:
               
             response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{service[4]}',data=data,headers=headers)
           except:
             response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{service[4]}',data=data,headers=headers)

           data = json.loads(response.text)
         
           if data['success'] == False or response.status_code!=200:
              data = await ReadFileConfig()
              await c.send_message(data['ownerId'],f"""🔔 توجه ادمین گرامی 

سرور با نام {server[6]} هنگام تغییر حجم سرویس {service[3]} با uuid {service[4]}
مشکلی پیش آمد
و سرویس غیر فعال شد لطفا به صورت دستی ان را از پنل غیر فعال کنید

با تشکر ❤️
""")
        except:
              
              await c.send_message(data['ownerId'],f"""🔔 توجه ادمین گرامی 

سرور با نام {server[6]} هنگام تغییر زمان سرویس {service[3]} با uuid {service[4]}
مشکلی پیش آمد

لطفا هر چه سریع تر اتصال را بررسی و مجدد امتحان کنید

با تشکر ❤️
""")
              return False
      await db_manager.QueryWidthOutValue(f"UPDATE Service SET State = {'0' if typeUpdate == 'false' else '1'} WHERE Id = {serviceId}")        
      return True 
    except:
        return False                  
async def mainManageService(serviceId,call):
               Service = await GetServiceById(serviceId)
               
               date =  datetime.datetime.fromtimestamp(Service[1][7]/1000)
               shamsi = jdatetime.datetime.fromgregorian(date =date)
               username = await GetUserNameByUserId(Service[1][1])
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
                                                                               [InlineKeyboardButton(" فعال کردن 🟢" ,callback_data=f"EnableConfigUser_{Service[1][0]}"),InlineKeyboardButton(" غیرفعال کردن 🔴" ,callback_data=f"DisableConfigUser_{Service[1][0]}")],
                                                                               [InlineKeyboardButton("حذف ❌" ,callback_data=f"DeleteConfigUser_{Service[1][0]}")]
                                                                               
                                                                               ]) )         
     
     
async def DeleteConfig(serviceId,app):
  try:  
    service = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE Id = {serviceId}")   
    serverIds  = ast.literal_eval(service[17])
    for serverId in serverIds:
          server = await db_manager.execute_query_one(f"SELECT * FROM server WHERE Id = {serverId}")
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
          
           headers['Cookie'] = f"lang=en-US; {server[8]}"
           
           try:        
             response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/{server[10]}/delClient/{service[4]}',headers=headers)
           except:
             response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/{server[10]}/delClient/{service[4]}',headers=headers)
                 
           data = json.loads(response.text)
           if data['success'] == False or response.status_code != 200:
                rec = await ReadFileConfig()
                await app.send_message(chat_id=rec['ownerId'],text=f"""هنگام حذف کانفیگ از این سرور مشکلی پیش آمد 🔔
                                       
Server : <code>{server[6]}</code>
        
uuid : <code>{service[4]}</code>

""")
  
    await db_manager.QueryWidthOutValue(f"DELETE FROM Service WHERE Id = {service[0]}")
    return [True , ""]
  except:
      return [False , "هنگام حذف مشکلی پیش آمد"]     

async def checkServiceBtn(data):

    res = await db_manager.execute_query_one("SELECT BtnBot,Test FROM Setting ")
    result = json.loads(res[0])
    if result[data] =='on' and res[1] == 1:
        return True
    else:
        return False

async def checkTestState():
   res = await db_manager.execute_query_one("SELECT Geted,CountGet FROM TestFree")        
   if res == None : 
         return False
   elif res[0]>= res[1]:
        return False
   else:
       return True
       
async def GetServiceList(data):
    res = await db_manager.execute_query_all(f"SELECT Email,Id FROM Service WHERE UserId = {data} AND isDelete = 0")
    btns=[]
    if len(res) != 0:
        for r in res:
            btns.append([InlineKeyboardButton( f"{r[0]}",callback_data=f"GETConfig_{r[1]}")])
    else:
        btns.append([InlineKeyboardButton("شما خرید نداشتید",callback_data="ARS")]) 
    return btns           

 
async def GetServiceListForAdmin(data):
    res = await db_manager.execute_query_all(f"SELECT Email,Id FROM Service WHERE UserId = {data}")
    btns=[]
    if len(res) != 0:
        for r in res:
            btns.append([InlineKeyboardButton( f"{r[0]}",callback_data=f"GETConfig_{r[1]}"),InlineKeyboardButton( f"❌",callback_data=f"DeleteConfig_{r[1]}")])
    else:
        btns.append([InlineKeyboardButton("این کاربر خرید نداشته",callback_data="ARS")]) 
    return btns           

async def GetManageTestBtn():
    res= await db_manager.execute_query_one("SELECT * FROM TestFree")
    
    btns =[]
    if res ==None:
        btns =[[InlineKeyboardButton("تست اضافه نشده",callback_data="ARS")],
      [InlineKeyboardButton("افزودن",callback_data="AddTest")]]
    else:
       groupname = await db_manager.execute_query_one(f"SELECT Title FROM category WHERE Id = {res[5]}")
       if  groupname != None:
         
         btns =[
             [InlineKeyboardButton(res[1],callback_data=f"EditVolumetest_{res[0]}"),InlineKeyboardButton("حجم ♦️",callback_data="ARS")],
        [InlineKeyboardButton(res[2],callback_data=f"EditTimetest_{res[0]}"),InlineKeyboardButton("زمان 🕐",callback_data="ARS")],
        [InlineKeyboardButton(res[6],callback_data=f"EditSended_{res[0]}"),InlineKeyboardButton("ارسال شده",callback_data="ARS")],
        [InlineKeyboardButton(res[3],callback_data=f"ARS"),InlineKeyboardButton("ظرفیت ارسال",callback_data="ARS")],
        [InlineKeyboardButton(groupname[0],callback_data=f"ARS"),InlineKeyboardButton("دسته بندی",callback_data="ARS")],
        [InlineKeyboardButton("❌ حذف",callback_data=f"DeleteTest_{res[0]}")]
        ]
       else:
          btns =[
             [InlineKeyboardButton(res[1],callback_data=f"EditVolumetest_{res[0]}"),InlineKeyboardButton("حجم ♦️",callback_data="ARS")],
        [InlineKeyboardButton(res[2],callback_data=f"EditTimetest_{res[0]}"),InlineKeyboardButton("زمان 🕐",callback_data="ARS")],
        [InlineKeyboardButton(res[6],callback_data=f"EditSended_{res[0]}"),InlineKeyboardButton("ارسال شده",callback_data="ARS")],
        [InlineKeyboardButton(res[3],callback_data=f"ARS"),InlineKeyboardButton("ظرفیت ارسال",caسllback_data="ARS")],
     
        [InlineKeyboardButton("دسته بندی یافت نشد",callback_data=f"ARS"),InlineKeyboardButton("دسته بندی",callback_data="ARS")],
        [InlineKeyboardButton("❌ حذف",callback_data=f"DeleteTest_{res[0]}")]
        ]
    btns.append([InlineKeyboardButton("بازگشت به منو ادمین🔙",callback_data="mainAdmin")])    
    return btns


async def AddTest(days , volume,countGet,ServerId,catId):
  try:
         
         await db_manager.Query("INSERT INTO TestFree(Days,Volume,CountGet,ServerId,GroupId) VALUES(?,?,?,?,?)",(days,int(volume),countGet,ServerId,catId))
         return True
  except:
      return False       
         
async def DeleteTestFree(data):
  try:   
    
     await db_manager.QueryWidthOutValue(f"DELETE FROM TestFree WHERE Id = {data}")
     return True
     
  except:
      return False      


async def GetmesChanell():
   res =  await db_manager.execute_query_all("SELECT * FROM MessageChanell")
   btns = []
   if res !=None:
    for r in res:
       btns.append([InlineKeyboardButton(r[1] ,callback_data=f"GetMesCahnell_{r[0]}"),InlineKeyboardButton("👁",callback_data=f"GetmessageShow_{r[0]}")])
   btns.append([InlineKeyboardButton("افزودن",callback_data="AddMesChanel")]) 
   btns.append([InlineKeyboardButton("بازگشت",callback_data="businnes")])
   return btns    
async def addMessageChanell(mesId,userId):
  try:  
    MesChanellId = await db_manager.Query("INSERT INTO MessageChanell(MessageId,UserId) VALUES(?, ?)",(mesId,userId))
    
    return [True, MesChanellId.lastrowid]
  except:
    return [True, 0]
   
async def GetMessageSettingBtns(mesId):
    data= await db_manager.execute_query_one(f"SELECT * FROM MessageChanell WHERE Id = {mesId} ")
    btns = [
        [InlineKeyboardButton("ویرایش",callback_data=f"EditMesChanell_{data[0]}")],
        [InlineKeyboardButton("دریافت",callback_data=f"GetmessageShow_{data[0]}")],
        [InlineKeyboardButton(f"روز {data[3]}",callback_data=f"ChangetimeSendMes_{data[0]}"),InlineKeyboardButton("زمانبندی ارسال",callback_data=f"ARS")],
        [InlineKeyboardButton('🟢' if data[4] == 1 else '🔴',callback_data=f"ChangeStatMes_{data[0]}_{data[4]}"),InlineKeyboardButton("وضعیت",callback_data=f"ARS")],
        [InlineKeyboardButton("🔙 بازگشت",callback_data="sendChanellMes")]
    ]
    return btns
  
async def GetMessageSettingBtnsEditStat(mesId,stat):
    data= await db_manager.execute_query_one(f"SELECT * FROM MessageChanell WHERE Id = {mesId} ")
    btns = [
        [InlineKeyboardButton("ویرایش",callback_data=f"EditMesChanell_{data[0]}")],
        [InlineKeyboardButton("دریافت",callback_data=f"GetmessageShow_{data[0]}")],
        [InlineKeyboardButton(f"روز {data[3]}",callback_data=f"ChangetimeSendMes_{data[0]}"),InlineKeyboardButton("زمانبندی ارسال",callback_data=f"ARS")],
        [InlineKeyboardButton('🟢' if stat == 1 else '🔴',callback_data=f"ChangeStatMes_{data[0]}_{stat}"),InlineKeyboardButton("وضعیت",callback_data=f"ARS")],
        [InlineKeyboardButton("🔙 بازگشت",callback_data="sendChanellMes")]
    ]
    return btns
async def ChangeStatMessage(data,stat):
    await db_manager.QueryWidthOutValue(f"UPDATE MessageChanell SET CanSend = {stat} WHERE Id = {data}")
    
    
async def EditMessageDays(dyas,MesID):

    await db_manager.QueryWidthOutValue(f"UPDATE MessageChanell SET TimeSend= {dyas} WHERE Id = {MesID}")
    

async def EditMessageChanell(mesId,userId,data):
    await db_manager.QueryWidthOutValue(f"UPDATE MessageChanell SET MessageId= {mesId} , UserId = {userId} WHERE Id = {data}")
    

async def GetMessageDetails(data):
    return await db_manager.execute_query_one(f"SELECT * FROM MessageChanell WHERE Id = {data} ")

async def LotteryManage():
    return await db_manager.execute_query_one("SELECT LotteryTime, LotteryState, LotteryTimeAfter,UserNumberLottery, LotteryPlan FROM Setting  ")

async def LotteryManageBtns():
    data = await LotteryManage()
    planName = await db_manager.execute_query_one(f"SELECT PlanName FROM ServerPlans WHERE Id = {data[4]}")
    if planName != None :
     btns = [
        [InlineKeyboardButton(f"{data[0]}",callback_data=f"LotteryTimeEdit"),InlineKeyboardButton("زمان تکرار قرعه کشی",callback_data="ARS")],
        [InlineKeyboardButton('🟢' if data[1] == 1 else '🔴',callback_data=f"LotteryStateEdit_{data[1]}")],
        [InlineKeyboardButton(f"{data[2]} ",callback_data=f"ARS"),InlineKeyboardButton("گذشته روز",callback_data="ARS")],
        [InlineKeyboardButton(f"{data[3]} نفر",callback_data=f"UserNumberLottery"),InlineKeyboardButton("هدیه به کاربران",callback_data="ARS")],
        [InlineKeyboardButton(f"{planName[0]} ",callback_data=f"AddPlanLottery"),InlineKeyboardButton("پلن",callback_data="ARS")] 
     ]
    else:
          btns = [
        [InlineKeyboardButton(f"{data[0]}",callback_data=f"LotteryTimeEdit"),InlineKeyboardButton("زمان تکرار قرعه کشی",callback_data="ARS")],
        [InlineKeyboardButton('🟢' if data[1] == 1 else '🔴',callback_data=f"LotteryStateEdit_{data[1]}")],
        [InlineKeyboardButton(f"{data[2]} ",callback_data=f"ARS"),InlineKeyboardButton("گذشته روز",callback_data="ARS")],
        [InlineKeyboardButton(f"{data[3]} نفر",callback_data=f"UserNumberLottery"),InlineKeyboardButton("هدیه به کاربران",callback_data="ARS")],
[InlineKeyboardButton("اضافه کنید پلنی موجود نیست ",callback_data="AddPlanLottery")]
     ]

    return btns
    
async def UpdateDaysLottery(days):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET LotteryTime = {days} ")
    
async def UpdateLotteryState(state):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET LotteryState = {state} ")
    

async def UpdateLotteryUserNumber(number):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET UserNumberLottery = {number} ")
    

async def GetAllPlanName():
    plans = await db_manager.execute_query_all("SELECT PlanName,Id FROM ServerPlans")    
    
    return plans


async def UpdatePlanIdLottery(data):
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET LotteryPlan  = {data}")
    

async def GetAllDiscount():
    res =await db_manager.execute_query_all(f"SELECT * FROM Discounts")
    
    return res

async def GetAllDiscountBtn():
    data = await GetAllDiscount()
    btns = []
    if data != None:
        for d in data :
           btns.append([InlineKeyboardButton(d[2],callback_data=f"EditDis_{d[0]}")])
    else:
        btns.append([InlineKeyboardButton("🔺 کد تخفیف نداریم",callback_data="ARS")])    
    btns.append([InlineKeyboardButton("➕ افزودن",callback_data="AddDis"),InlineKeyboardButton("🔙 بازگشت",callback_data="mainAdmin")])    
    return btns

async def AddDisCount(percent ,count,Canuse,days):
  try:
    dateEnd =int(datetime.datetime.timestamp( datetime.datetime.now() + datetime.timedelta(days=days)))
    TimeStart = int(datetime.datetime.timestamp( datetime.datetime.now()))
    randomId = get_random_string(8)
    res =await db_manager.Query("INSERT INTO Discounts(Percent, DiscountCode, Count, DateEnd, DateStart, CanUse) VALUES(?,?,?,?,?,?)",(percent,randomId,count,dateEnd,TimeStart,Canuse))
    
    return [True,res.lastrowid,randomId]
  except:
      return [False,0]

async def GetDisBtns(disId):
    dis = await  db_manager.execute_query_one(f"SELECT * FROM Discounts WHERE Id = {disId}")
    
    Convert = datetime.datetime.fromtimestamp(dis[4])
    disDate = Convert - datetime.datetime.now() 
    btns = [
        [InlineKeyboardButton(dis[2],callback_data=f"EditCode_{dis[0]}"),InlineKeyboardButton("ویرایش خودکار",callback_data="ARS")],
        [InlineKeyboardButton(dis[2],callback_data=f"EditCodeManual_{dis[0]}"),InlineKeyboardButton("ویرایش دستی",callback_data="ARS")],
        [InlineKeyboardButton(dis[3],callback_data=f"EditCountDis_{dis[0]}"),InlineKeyboardButton("تعداد باقی مانده",callback_data="ARS")],
        [InlineKeyboardButton(dis[6],callback_data=f"EditCanUserDis_{dis[0]}"),InlineKeyboardButton("تعداد استفاده هر کاربر",callback_data="ARS")],
        [InlineKeyboardButton(disDate.days if disDate.days > 0 else "پایان رسیده",callback_data=f"EditDateDis_{dis[0]}"),InlineKeyboardButton("روز باقی مانده",callback_data="ARS")],
        [InlineKeyboardButton(dis[1],callback_data=f"EditPercentDis_{dis[0]}"),InlineKeyboardButton("تخفیف درصد",callback_data="ARS")],
        [InlineKeyboardButton('🟢' if dis[7] ==1 else '🔴',callback_data=f"EditStateDis_{dis[0]}_{dis[7]}"),InlineKeyboardButton("وضعیت",callback_data="ARS")],
[InlineKeyboardButton(' بازگشت به لیست ',callback_data="manageOffer")]

    ]
    return btns
async def UpdateCodeDiscountManual(discountId,DiscountCode):
    await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET DiscountCode = '{DiscountCode}' WHERE Id = {discountId} ")
async def  UpdateDisCode(disId):
    randomId = get_random_string(8)
    
    await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET DiscountCode = '{randomId}' WHERE Id = {disId}")
    return randomId
async def EditCountDsicount(disId,count):
    if count <=0 :
      await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET Count = {count} , Status = 0 WHERE Id = {disId}")
      return

    await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET Count = {count} WHERE Id = {disId}")
async def EditCountUserDsicount(disId , countUser):
    await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET CanUse = {countUser} WHERE Id = {disId}")
    
async def EditDaysDsicount(disId,dateNew):
        startDate = await db_manager.execute_query_one(f"SELECT DateStart FROM Discounts WHERE Id = {disId}")
        dateEnd =int(datetime.datetime.timestamp( datetime.datetime.fromtimestamp(startDate[0]) + datetime.timedelta(days=dateNew)))
        Convert = datetime.datetime.fromtimestamp(dateEnd)
        disDate = Convert - datetime.datetime.now() 
        if disDate.days <= 0:
             await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET DateEnd = {dateEnd} , Status = 0 WHERE Id = {disId}")
             return
        await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET DateEnd = {dateEnd} WHERE Id = {disId}")
async def EditPercentDsicount(disId , Percent):
    await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET Percent = '{Percent}' WHERE Id = {disId}")
async def GetDiscountCode(disId):
    res =await db_manager.execute_query_one(f"SELECT DiscountCode FROM Discounts WHERE Id = {disId}")
    return res[0]

async def EditStatusDiscount(disId , state):
        await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET Status = {state} WHERE Id = {disId}")


async def GetdisCountWithCode(code,orderId,userId):
  try : 
    res = await db_manager.execute_query_one(f"SELECT Id,Count,CanUse,Percent FROM Discounts WHERE DiscountCode = '{code}' AND Status = 1 ")
    if res !=None:
        disId =  res[0]
        if res[1]==0:
           return  [False,'ظرفیت این کد تخفیف به پایان رسیده',0]    
        UserUsed = await db_manager.execute_query_all(f"SELECT * FROM DiscountUser WHERE UserId = {userId} AND DiscountId  = {disId}")
        if UserUsed != None:
                if len(UserUsed) == res[2]:
                     return [False,'تعداد دفعات استفاده شما از حد مجاز گذشته',0]    
                
        price = await db_manager.execute_query_one(f"SELECT Price FROM OrdersList WHERE Id = {orderId} ")  
        priceoffer = price[0] - ( price[0] * res[3]  / 100  )

        await db_manager.QueryWidthOutValue(f"UPDATE Discounts SET Count = {res[1] - 1} ")
        await db_manager.Query("INSERT INTO DiscountUser(UserId , DiscountId) VALUES(?, ?)",(userId,res[0]))
        await db_manager.QueryWidthOutValue(f"UPDATE OrdersList SET DiscountId = {disId} , PriceAfterDiscount = {priceoffer} WHERE Id = {orderId}") 
        return [True,0,int(priceoffer)]
        
    else:
        return [False,'این کد یافت نشد',0]    
  except:
        return [False,'هنگام دریافت اطلاعات مشکلی پیش آمد',0]    
        
async def PlanidGetDiscountOrderDetails(orderId):
 res = await db_manager.execute_query_one(f"SELECT PlanId FROM OrdersList WHERE Id = {orderId}")
 return res[0]





async def GetAccount(data):
    res = await db_manager.execute_query_one("SELECT BtnBot FROM Setting ")
    result = json.loads(res[0])
    if result[data] =='on':
        return True
    else:
        return False
async def GetDetailsUserAcc(userId):
    user = await db_manager.execute_query_one(f"SELECT * FROM Users WHERE UserId = {userId}")
    count =await db_manager.execute_query_all(f"SELECT COUNT() FROM  Service WHERE UserId = {userId}")
    
    return [user,count]


async def CreateOrderWallet(price):
    await db_manager.QueryWidthOutValue("INSERT INTO OrdersList()")


async def CheckUserFreeUsed(userId):
    data = await db_manager.execute_query_one(f"SELECT UseFreeTrial,IsAdmin FROM Users WHERE UserId  = {userId}")
    
    
    if data[1] == 1:
         return True
    else : 
        adminId = await ReadFileConfig()
        if adminId['ownerId'] ==userId :
            return True
    if data[0] == 0:
        return True
    else: 
        return False

async def TranformData(data,userId,userUserId):
 try: 
  walletUser = await db_manager.execute_query_one(f"SELECT Wallet FROM Users WHERE UserId = {userUserId}")
  if walletUser[0]  < int(data):
      return [False,"مبلغ ارسالی از مقدار کیف پول شما بیشتر است"]
  walletUserTransform = await db_manager.execute_query_one(f"SELECT Wallet FROM Users WHERE UserId = {userId}")
  trans =  walletUserTransform[0]  + int(data)
  ter = walletUser[0] - int(data)
  await db_manager.QueryWidthOutValue(f"UPDATE Users SET Wallet = {ter} WHERE UserId = {userUserId}")
  await db_manager.QueryWidthOutValue(f"UPDATE Users SET Wallet = {trans} WHERE UserId = {userId}")
  return [True, "✅ مبلغ با موفقیت انتقال پیدا کرد"]

 except:   
      return [False,"هنگام انتقال مشکلی پیش آمده است"]


async def GetBtnsAmar():
    serviceShop = await db_manager.execute_query_one("SELECT SUM(Price) FROM OrdersList WHERE State = 1 AND DiscountId = 0 AND Type = 'BuySub' OR Type= 'BuySingle' ")
    
    if serviceShop[0] == None:
        serviceShop = (0,)
   

    serviceShopWallet = await db_manager.execute_query_one("SELECT SUM(Price) FROM OrdersList WHERE State = 1 AND DiscountId = 0 AND Type = 'AddWallet' ")
   
    if serviceShopWallet[0] == None :
        serviceShopWallet = (0,)
   
    servicediscount = await db_manager.execute_query_one("SELECT SUM(PriceAfterDiscount) FROM OrdersList WHERE State = 1 AND DiscountId != 0 ")
    if servicediscount[0] == None:
       servicediscount = (0,)

    
    finalShoped = serviceShop[0] + servicediscount[0] + serviceShopWallet[0]
    catCount = await db_manager.execute_query_one("SELECT COUNT() FROM category")
    PlanCount = await db_manager.execute_query_one("SELECT COUNT() FROM ServerPlans")
    UserCount = await db_manager.execute_query_one("SELECT COUNT() FROM Users")
    pubmicMesState = await db_manager.execute_query_one("SELECT COUNT() FROM PublicMessage WHERE IsSended = 0 AND IsDelete = 0")
    ServiceActive= await db_manager.execute_query_one("SELECT COUNT() FROM Service WHERE State = 1 AND isDelete = 0 ")
    btns = [
            [InlineKeyboardButton(" = اطلاعات = ",callback_data="ARS"),InlineKeyboardButton("= درباره =",callback_data="ARS")],
            [InlineKeyboardButton(f"  {UserCount[0]}  ",callback_data="ARS"),InlineKeyboardButton(" کاربران ",callback_data="ARS")],
            [InlineKeyboardButton(f"  {catCount[0]}  ",callback_data="ARS"),InlineKeyboardButton(" دسته بندی ",callback_data="ARS")],
            [InlineKeyboardButton(f"  {PlanCount[0]}  ",callback_data="ARS"),InlineKeyboardButton(" پلن ها ",callback_data="ARS")],
            [InlineKeyboardButton(f"  {ServiceActive[0]}  ",callback_data="ARS"),InlineKeyboardButton("سرویس های فعال",callback_data="ARS")],
            [InlineKeyboardButton(f" {'در حال ارسال' if  pubmicMesState[0] != 0 else 'در صف نیست' }  ",callback_data="ARS"),InlineKeyboardButton(" پیام همگانی ",callback_data="ARS")],
            [InlineKeyboardButton(f"  {finalShoped:,} تومان  ",callback_data="ARS"),InlineKeyboardButton(" درآمد کلی ",callback_data="ARS")],
            [InlineKeyboardButton(f" 🔙 بازگشت 🔙 ",callback_data="mainAdmin")]

    ]
    return btns
async def GetBtnsSetting():
    res = await db_manager.execute_query_one("SELECT BtnBot FROM Setting")
    btnsData =  json.loads(res[0])
    btns = [
        [InlineKeyboardButton("وضعیت",callback_data="ARS"),InlineKeyboardButton("نام",callback_data="ARS")],
        [InlineKeyboardButton("🟢" if btnsData['btnshop'] == 'on' else "🔴" ,callback_data=f"BtnShop_{btnsData['btnshop']}"),InlineKeyboardButton("دکمه خرید",callback_data="ARS")],
        [InlineKeyboardButton("🟢" if btnsData['freetest'] == 'on' else "🔴" ,callback_data=f"BtnTest_{btnsData['freetest']}"),InlineKeyboardButton("دکمه تست",callback_data="ARS")],
        [InlineKeyboardButton("🟢" if btnsData['myacc'] == 'on' else "🔴" ,callback_data=f"BtnAccount_{btnsData['myacc']}"),InlineKeyboardButton("دکمه اکانت من",callback_data="ARS")],
        [InlineKeyboardButton("🟢" if btnsData['mysub'] == 'on' else "🔴" ,callback_data=f"BtnSub_{btnsData['mysub']}"),InlineKeyboardButton("دکمه اشتراک های من",callback_data="ARS")],
        [InlineKeyboardButton("🟢" if btnsData['hamkarbtn'] == 'on' else "🔴" ,callback_data=f"Hamkarbtn_{btnsData['hamkarbtn']}"),InlineKeyboardButton("دکمه همکاری",callback_data="ARS")],
        [InlineKeyboardButton("🟢" if btnsData['tamdidbtn'] == 'on' else "🔴" ,callback_data=f"Tamdidbtn_{btnsData['tamdidbtn']}"),InlineKeyboardButton("دکمه تمدید",callback_data="ARS")],
        [InlineKeyboardButton("🟢" if btnsData['configdata'] == 'on' else "🔴" ,callback_data=f"GetConfigData_{btnsData['configdata']}"),InlineKeyboardButton("دکمه مشخصات اشتراک",callback_data="ARS")],
        # [InlineKeyboardButton("🟢" if btnsData['buyagain'] == 'on' else "🔴" ,callback_data=f"buyagainservice_{btnsData['buyagain']}"),InlineKeyboardButton("دکمه  خرید مجدد",callback_data="ARS")],
        [InlineKeyboardButton(f" 🔙 بازگشت 🔙 ",callback_data="mainAdmin")]


    ]
    return btns
async def UpdateBtns(btn , state):
    res = await db_manager.execute_query_one("SELECT BtnBot FROM Setting")
    btnsData =  json.loads(res[0])
    btnsData[f'{btn}'] = state
    await db_manager.QueryWidthOutValue(f"UPDATE Setting SET BtnBot = '{json.dumps(btnsData)}'")

async def getbtnsCountShpped():
   datas =   await db_manager.execute_query_all("SELECT Name,CountShopped FROM Users  ORDER BY CountShopped DESC LIMIT 5")
   btns = [[InlineKeyboardButton("تعداد",callback_data="ARS"),InlineKeyboardButton("نام",callback_data="ARS"),InlineKeyboardButton("🔻",callback_data="ARS")]]
   counter = 0
   for data in datas:
       counter += 1
       btns.append([InlineKeyboardButton(data[1],callback_data="ARS"),InlineKeyboardButton(data[0],callback_data="ARS"),InlineKeyboardButton(counter,callback_data="ARS")])
   btns.append([InlineKeyboardButton("بازگشت 🔙",callback_data="MainDays")])   
   return btns 
async def getbtnsCountInvitedBest():
   datas =   await db_manager.execute_query_all("SELECT Name,Invited FROM Users  ORDER BY Invited DESC LIMIT 5")
   btns = [[InlineKeyboardButton("تعداد",callback_data="ARS"),InlineKeyboardButton("نام",callback_data="ARS"),InlineKeyboardButton("🔻",callback_data="ARS")]]
   counter = 0
   for data in datas:
       counter += 1
       btns.append([InlineKeyboardButton(data[1],callback_data="ARS"),InlineKeyboardButton(data[0],callback_data="ARS"),InlineKeyboardButton(counter,callback_data="ARS")])
   btns.append([InlineKeyboardButton("بازگشت 🔙",callback_data="MainDays")])   
   return btns 
async def GetTopShopped():
    datas = await  db_manager.execute_query_all("SELECT UserId, SUM(Price) AS SUmer FROM OrdersList  GROUP BY UserId ORDER BY SUmer DESC LIMIT 5")
    btns = [[InlineKeyboardButton("مقدار",callback_data="ARS"),InlineKeyboardButton("نام",callback_data="ARS"),InlineKeyboardButton("🔻",callback_data="ARS")]]
    counter = 0
    for data in datas:
      counter += 1
      
      Name = await db_manager.execute_query_one(f"SELECT Name FROM Users WHERE UserId = {data[0]}")
      btns.append([InlineKeyboardButton(data[1],callback_data="ARS"),InlineKeyboardButton(Name[0],callback_data="ARS"),InlineKeyboardButton(counter,callback_data="ARS")])
    btns.append([InlineKeyboardButton("بازگشت 🔙",callback_data="MainDays")])   

    return btns 

async def GetTopUseUsers():
    datas = await  db_manager.execute_query_all("SELECT UserId, SUM(TotalUsed) AS Used FROM Service GROUP BY UserId ORDER BY Used DESC")
    btns = [[InlineKeyboardButton("مقدار",callback_data="ARS"),InlineKeyboardButton("نام",callback_data="ARS"),InlineKeyboardButton("🔻",callback_data="ARS")]]
    counter = 0
    for data in datas:
      counter += 1
      
      Name = await db_manager.execute_query_one(f"SELECT Name FROM Users WHERE UserId = {data[0]}")
      btns.append([InlineKeyboardButton(round (data[1] / 1024 /1024 /1024,2),callback_data="ARS"),InlineKeyboardButton(Name[0],callback_data="ARS"),InlineKeyboardButton(counter,callback_data="ARS")])
    btns.append([InlineKeyboardButton("بازگشت 🔙",callback_data="MainDays")])   

    return btns 
async def GetAllPlanExtension():
    plans =  await db_manager.execute_query_all("SELECT * FROM PlanExtension")
    btns = []
    if plans != None or len(plans) != 0:
     for plan in plans : 
        btns.append([InlineKeyboardButton(plan[1],callback_data=f"EditPlanExt_{plan[0]}")])
    else:
        btns.append([InlineKeyboardButton("پلنی موجود نیست !",callback_data="addplanExtension")])

    btns.append([InlineKeyboardButton("➕ افزودن ➕",callback_data="addplanExtension")])
    btns.append([InlineKeyboardButton("بازگشت 🔙",callback_data="mainAdmin")])
    return    btns  

async def GetServiceForExtension(userId):
    services = await db_manager.execute_query_all(f"SELECT * FROM Service WHERE UserId = {userId} AND isDelete = 0")
    btns  = [[InlineKeyboardButton("تمدید",callback_data="ARS"),InlineKeyboardButton("نام",callback_data="ARS")]]
    if services != None or len(services) != 0:
     for ser in services:
     
        btns.append([InlineKeyboardButton("🔁" ,callback_data=f"extension_{ser[0]}"),InlineKeyboardButton(f"{ser[3]} 🔺",callback_data="ARS")])
    else:
        btns.append([InlineKeyboardButton("هنوز سرویسی تهیه نکردید",callback_data="ARS")])
    return btns     


async def AddExtension(Name,Price,Volume,Month):
    await db_manager.Query("INSERT INTO PlanExtension(Name,Price,Volume,MonthCount) VALUES(?,?,?,?)",(Name,Price,Volume,Month))
    
async def GetBtnEXT(planId):
    data = await db_manager.execute_query_one(f"SELECT * FROM PlanExtension WHERE Id= {planId}")
    btns = [

        [InlineKeyboardButton(data[1],callback_data=f"EditNamePlanExt_{data[0]}"),InlineKeyboardButton("نام",callback_data="ARS")],
        [InlineKeyboardButton(data[2],callback_data=f"EditPricePlanExt_{data[0]}"),InlineKeyboardButton("قیمت",callback_data="ARS")],
        [InlineKeyboardButton(data[3],callback_data=f"EditVolumePlanExt_{data[0]}"),InlineKeyboardButton("حجم",callback_data="ARS")],
        [InlineKeyboardButton(data[4],callback_data=f"EditMonthCountPlanExt_{data[0]}"),InlineKeyboardButton("تعداد ماه",callback_data="ARS")],
        [InlineKeyboardButton(" حذف 🔴",callback_data=f"DeletePlanExt_{data[0]}")],
        [InlineKeyboardButton(" بازگشت 🔙",callback_data=f"PlanExtension")],
    ]
    return btns
async def UpdateNameExtPlan(planId , Name):
    await db_manager.QueryWidthOutValue(f"UPDATE PlanExtension SET Name = '{Name}' WHERE Id = {planId}")


async def UpdatePiceExtPlan(planId , Price):
    await db_manager.QueryWidthOutValue(f"UPDATE PlanExtension SET Price = {Price} WHERE Id = {planId}")



async def UpdateVolumeExtPlan(planId , Volume):
    await db_manager.QueryWidthOutValue(f"UPDATE PlanExtension SET Volume = {Volume} WHERE Id = {planId}")


async def UpdateMonthExtPlan(planId , Month):
    await db_manager.QueryWidthOutValue(f"UPDATE PlanExtension SET MonthCount = {Month} WHERE Id = {planId}")    

async def DeleteExtPlan(PlanId):
    await db_manager.QueryWidthOutValue(f"DELETE FROM PlanExtension WHERE Id = {PlanId}")


async def GetPlanExtForExt(serviceId):
    plans =  await db_manager.execute_query_all("SELECT * FROM PlanExtension")
    btns = [[InlineKeyboardButton("قیمت",callback_data="ARS"),InlineKeyboardButton("حجم",callback_data="ARS")]]
    if plans != None or len(plans) != 0:
     for plan in plans : 
        btns.append([InlineKeyboardButton(f"💰 تومان {plan[2]}",callback_data=f"ExtensionFinall_{plan[0]}_{serviceId}"),InlineKeyboardButton(f"{plan[3]} GB",callback_data=f"ExtensionFinall_{plan[0]}_{serviceId}")])
     
    else:
        btns.append([InlineKeyboardButton("پلنی موجود نیست !",callback_data="addplanExtension")])
    btns.append([InlineKeyboardButton("بازگشت 🔙",callback_data="extensionList")])
    return btns
async def CheckWalletForExtension(planId , UserId):
    Price = await db_manager.execute_query_one(f"SELECT Price FROM PlanExtension WHERE Id = {planId}")
    WalletUser = await db_manager.execute_query_one(f"SELECT Wallet FROM Users WHERE UserId = {UserId}")
    if Price[0] <= WalletUser[0] :
        return True
    else:
        return False
async def ExtensionFinall(planId , userId , serviceId):
 plan = await db_manager.execute_query_one(f"SELECT * FROM PlanExtension WHERE Id = {planId}")

 pay = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE Id = {serviceId} AND isDelete != 1")

 endTimeMikro = datetime.datetime.now() + datetime.timedelta(days=plan[4] * 31)
 Volume = pay[18]  + (plan[3] * 1024 * 1024 * 1024)
 
 
 counter = 0
 serversCount = []
 serverIds = ast.literal_eval(pay[17]) 
 try:

    
   for serverId in serverIds:
    try:

       server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {serverId} ")
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
    "settings": '{"clients": [{"id": "'+ pay[4] +'", "alterId": 0, "email": "'+ pay[3] +'", "totalGB": '+ str(int(Volume)) +', "expiryTime": '+str(int(endTimeMikro.timestamp())* 1000)+', "enable": true, "limitIp":'+ str(pay[28]) + ', "tgId": "", "subId": ""}]}'
}
       async with httpx.AsyncClient() as client:
         response = None
         headers['Cookie'] = f"lang=en-US; {server[8]}"
         try:
           response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{pay[4]}',data=data,headers=headers)
         except:
           response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/updateClient/{pay[4]}',data=data,headers=headers)
               
         data = json.loads(response.text)
         
         if data['success'] != False:
            counter +=1
            serversCount.append(server[0])
            await db_manager.QueryWidthOutValue(f"UPDATE Configs SET TansformEnable = {Volume} , State = 1 , EndDate = {int(endTimeMikro.timestamp())* 1000} WHERE ServerId = {serverId } AND ServiceId = {pay[0]} ")

        
            
             
             
    except:
       config =  await db_manager.execute_query_one(f"SELECT * FROM Configs WHERE ServerId = {serverId } AND ServiceId = {pay[0]}" )
       await db_manager.Query("INSERT INTO imperfect(Type,ConfigId,Volume,EndDate,CreateDate,UserId,DateCreateImperfect) VALUES(?,?,?,?,?,?,?)",("extension",config[0],Volume,int(endTimeMikro.timestamp() * 1000),int(datetime.datetime.now().timestamp()),userId,int(datetime.datetime.now().timestamp())))
       
                 
                  
 except:
       return [ False,"هنگام دریافت سرویس مشکلی پیش آمد !"]
 if counter != 0:
               await db_manager.QueryWidthOutValue(f"UPDATE Service SET CreateDate= {int(datetime.datetime.now().timestamp())}, EndDate = {int(endTimeMikro.timestamp()) * 1000} , State = 1,TransformEnable = {Volume} , AlertVolumeTwo = 0, AlertVolumeFirst = 0, AlertTimeFirst = 0,AlertTimeTwo = 0 WHERE  Id = {serviceId}")
               WalletUser = await db_manager.execute_query_one(f"SELECT Wallet FROM Users WHERE UserId = {userId}")
               if plan[2] <= WalletUser[0] :
                   await db_manager.QueryWidthOutValue(f"UPDATE Users SET Wallet = {WalletUser[0] - plan[2]} WHERE UserId = {userId}")

                  
               return [True,f"""   سرویس با موفقیت تمدید شد  ...
                       
مبلغ {plan[2]:,} ✅از حساب شما کم شد و سرویس شما تمدید شد 

{

    f"❤️ کاربر گرامی تمدید چندین سرور در سرویس شما موفقیت آمیز نبود در صورت اتصال سرور ها تمدید شما به صورت اتوماتیک صورت خواهد گرفت " if counter != len(serverIds) else ""
}
                       """]
          
 else:
       return [ False,"هنگام تمدید سرویس مشکلی پیش آمد !"]
     
async def GetbtnsCollection(userId):
   user = await db_manager.execute_query_one(f"SELECT Invited FROM Users WHERE UserId = {userId}")
   countShell = await db_manager.execute_query_one(f"SELECT SUM(CountShopped) FROM Users WHERE InvitedFrom = {userId}") 
   btns = [
       [InlineKeyboardButton(user[0],callback_data="ARS"),InlineKeyboardButton("🫴🏻 تعداد دعوت شده ها",callback_data="ARS")],
       [InlineKeyboardButton(countShell[0] if countShell[0]!= None else "خریدی نداشته اند",callback_data="ARS"),InlineKeyboardButton("💰 مقدار خرید دعوت شده ها",callback_data="ARS")],
       [InlineKeyboardButton("📥 دریافت لینک دعوت شما",callback_data="GetInviteLink")],
       [InlineKeyboardButton("🔙 بازگشت ",callback_data="mainCooperation")],

   ]
   return btns
async def UpdateInviteLink(link,userId):
    await db_manager.QueryWidthOutValue(f"UPDATE Users SET InviteCode = '{link}' WHERE UserId = {userId}")
async def AddTiket(text , userId):
    try: 
        res = await db_manager.Query("INSERT INTO Tikets(Description , UserId ) VALUES(?,?)",(text,userId))
        return [ True , res.lastrowid]
    except:    
        return [ False , 0]
async def GetTiketById(tiketId):
    res = await db_manager.execute_query_one(f"SELECT * FROM Tikets WHERE Id = {tiketId}")
    return res
async def UpdateTiket(tiketId):
    await db_manager.QueryWidthOutValue(f"UPDATE Tikets SET Answer = 1 WHERE Id = {tiketId}")
async def CheckTiket(tiketId):
     res = await db_manager.execute_query_one(f"SELECT Answer FROM Tikets WHERE Id = {tiketId}")
     if res[0] == 1:
         return False
     else: 
         return True
async def GetAllBtnsCooperation(userId):
    userDis =  await db_manager.execute_query_one(f"SELECT * FROM Users WHERE UserId = {userId}")
    btns = []
    if userDis[14] != 0:
      userDisPercent = await db_manager.execute_query_one(f"SELECT Percent FROM CooperationDiscount  WHERE Id = {userDis[14]}")
      btns.append([InlineKeyboardButton("درصد تخفیف حال",callback_data="ARS")])
      btns.append([InlineKeyboardButton(f"{userDisPercent[0]} %"  ,callback_data="ARS")])

    discounts =  await db_manager.execute_query_all("SELECT * FROM CooperationDiscount ORDER BY Percent DESC")   
    if len(discounts) != 0:
        for dis in discounts:
             if dis[2] <=userDis[10] : 
                   if userDis[14] == dis[0] :
                      btns.append([InlineKeyboardButton("🟢 فعال " ,callback_data=f"ARS"),InlineKeyboardButton(f"سرویس  {dis[2]}",callback_data="ARS"),InlineKeyboardButton(f"   {dis[1]}%",callback_data="ARS")])
                   else:    
                       btns.append([InlineKeyboardButton("✅ درخواست " ,callback_data=f"ReqCooperation_{dis[0]}"),InlineKeyboardButton(f"سرویس  {dis[2]}",callback_data="ARS"),InlineKeyboardButton(f"   {dis[1]}%",callback_data="ARS")])
             else:
                   btns.append([InlineKeyboardButton("❌ فعال نیست",callback_data="ARS"),InlineKeyboardButton(f"سرویس  {dis[2]}",callback_data="ARS"),InlineKeyboardButton(f" {dis[1]}%",callback_data="ARS")])
                       
    else: 
      btns.append([InlineKeyboardButton(f"درصدی موجود نیست !" , callback_data="ARS" )])
    btns.append([InlineKeyboardButton(f"🔙 بازگشت " , callback_data="mainCooperation" )])
    return btns


async def GetBtnsPercent():
    discounts = await db_manager.execute_query_all("SELECT * FROM CooperationDiscount")
    btns = []
    if len(discounts) != 0:
      for dis in discounts:
          btns.append([InlineKeyboardButton(f" {dis[2]} تعداد -  {dis[1]} درصد",callback_data=f"DisCountper_{dis[0]}")])
    else:
     btns.append([InlineKeyboardButton("! موجود نیست",callback_data="ARS")])
    btns.append([InlineKeyboardButton("➕ افزودن",callback_data="AddPersentDis"),InlineKeyboardButton("🔙 بازگشت ",callback_data="mainAdmin")]) 
    return btns
async def AddNewPercentDis(percent , count):
    await db_manager.Query("INSERT INTO CooperationDiscount(Percent , Count) VALUES (?,?)",(percent,count))
    
async def GetCooperationDiscount(discountId):
   
    res = await db_manager.execute_query_one(f"SELECT * FROM CooperationDiscount WHERE Id = {discountId}")
    btns = [
        [ InlineKeyboardButton(res[1],callback_data=f"EditPerDisCo_{res[0]}"),InlineKeyboardButton("درصد تخفیف",callback_data="ARS")],
        [ InlineKeyboardButton(res[2],callback_data=f"EditCountDisCo_{res[0]}"),InlineKeyboardButton("تعداد لازم تخفیف",callback_data="ARS")],
        [ InlineKeyboardButton("❌ حذف ",callback_data=f"DeleteDisCo_{res[0]}"),InlineKeyboardButton("🔙 بازگشت ",callback_data="ManagePercent")],
    ]
    return btns

async def UpdatePerDisCo(disId , Percent):
    await db_manager.QueryWidthOutValue(f"UPDATE CooperationDiscount SET Percent = {Percent} WHERE Id = {disId} ")

async def UpdateCountDisCo(disId , Count):
    await db_manager.QueryWidthOutValue(f"UPDATE CooperationDiscount SET Count = {Count} WHERE Id = {disId} ")    
async def DeleteDisCo(disId):
    await db_manager.QueryWidthOutValue(f"DELETE FROM CooperationDiscount WHERE Id = {disId}")

async def GetPercentById(PerId):
    res = await db_manager.execute_query_one(f"SELECT * FROM CooperationDiscount WHERE Id = {PerId}")
    return res
async def UpdatePerUser(userIdd , perId):
    userId = await db_manager.execute_query_one(f"SELECT UserId FROM Users WHERE Id = {userIdd}")
    await db_manager.QueryWidthOutValue(f"UPDATE Users SET CooperationId = {perId} WHERE Id ={userIdd}")
    return userId[0]

async def GetUserPerId(userId):
    res = await db_manager.execute_query_one(f"SELECT CooperationId FROM Users WHERE UserId = {userId}")
    if res == None:
        return 0
    return res[0]
async def UpdayeOrderReject(orderId):
    await db_manager.QueryWidthOutValue(f"UPDATE OrdersList SET State = 2 WHERE Id ={orderId}")

async def GetUserIdByOrderId(orderId):
    userId = await db_manager.execute_query_one(f"SELECT UserId FROM OrdersList WHERE Id ={orderId}")
    return userId[0]
async def GetCountShopUser(userId):
    userId = await db_manager.execute_query_one(f"SELECT CountShopped FROM Users WHERE UserId ={userId}")
    return userId[0]
async def DeleteServer(serverId) :
    try:
        await db_manager.QueryWidthOutValue(f"DELETE FROM  ServerCat WHERE ServerId = {serverId}")
        await ServerManager.QueryWidthOutValue(f"DELETE FROM ServerData WHERE ServerId = {serverId}")
        await db_manager.QueryWidthOutValue(f"DELETE FROM Server WHERE Id = {serverId}")
        return True
    except:
        return False

async def GetAllServersBtns():

 server  = await db_manager.execute_query_all("SELECT * FROM Server")
 btns =[]
 if server !=None or len(server) !=0 :
    for s in server :
        btns.append([InlineKeyboardButton("❌",callback_data = f"DeleteServer_{s[0]}"),InlineKeyboardButton(s[6],callback_data=f"EditServer_{s[0]}")])
 else:
     btns.append([InlineKeyboardButton("سروری موجود نیست !",callback_data="ARS")])
 btns.append([InlineKeyboardButton("افزودن سرور ",callback_data="AddNewServer")])    
 btns.append([InlineKeyboardButton("بازگشت",callback_data="mainAdmin")])
 return btns

async def GetServerCatForShop(catId):
    btns = []
    servers =await db_manager.execute_query_all(f"SELECT Server.*  FROM  ServerCat JOIN Server ON Server.Id =ServerCat.ServerId AND Server.State = 1   WHERE ServerCat.CatId = {catId} ")
    for server in servers :
        btns.append([InlineKeyboardButton(server[6],callback_data=f"GetPlanCat_{catId}_{server[0]}")])

   
    btns.append([InlineKeyboardButton("بازگشت",callback_data=f"SingleShop")])
    return btns
async def RefreshAllTest():
  try :  
    await db_manager.QueryWidthOutValue("UPDATE Users SET UseFreeTrial = 0")
    return True
  except:
    return False
async def GetServerCatForTest(catId):
    btns = []
    servers =await db_manager.execute_query_all(f"SELECT Server.*  FROM  ServerCat JOIN Server ON Server.Id =ServerCat.ServerId WHERE ServerCat.CatId = {catId} ")
    for server in servers :
        btns.append([server[6]])

   
    btns.append(["انصراف"])
    return btns

async def DeleteCatServer(serverId):
    try:
        await db_manager.QueryWidthOutValue(f"DELETE FROM ServerCat WHERE Id = {serverId} ")
        return True
    except:
        return False    

 
async def GetServerCatFortManage(serverId):
    btns = []
    cats =await db_manager.execute_query_all(f"SELECT category.* , ServerCat.Id FROM  ServerCat JOIN category ON category.Id =ServerCat.CatId WHERE ServerCat.ServerId = {serverId} ")
    for cat in cats :
        btns.append([InlineKeyboardButton("❌",callback_data=f"deletecatServer_{cat[5]}"),InlineKeyboardButton(cat[1],callback_data="ARS")])

    btns.append([InlineKeyboardButton("افزودن دسته بندی",callback_data=f"catListserver_{serverId}")])    
    btns.append([InlineKeyboardButton("بازگشت",callback_data=f"EditServer_{serverId}")])
    return btns
async def AddCatToServer(serverId ,Catid):
  try:  
    CatServer = await db_manager.execute_query_one(f"SELECT * FROM ServerCat WHERE ServerId = {serverId} AND CatId = {Catid}")
    if CatServer == None :
        await db_manager.Query("INSERT INTO ServerCat(ServerId,CatId) VALUES(?,?)",(serverId,Catid))
        return True
    else:
        return False    
  except:
    return False
async def GetCatforSelectServer(serverId):
    cats =  await  db_manager.execute_query_all("SELECT * FROM category ")
    btns = []
    for cat in cats:
        btns.append([InlineKeyboardButton(cat[1],callback_data=f"AddCatToServer_{serverId}_{cat[0]}")])

    btns.append([InlineKeyboardButton("بازگشت",callback_data=f"CatServerManage_{serverId}")])
    return btns
async def GetServerById(serverId):
    server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {serverId}")
    serverCatName = await db_manager.execute_query_one(f"SELECT Title FROM category WHERE Id = {server[9]}")
    btns = [
        [ InlineKeyboardButton("اطلاعات",callback_data=f"ARS"),InlineKeyboardButton("درباره",callback_data="ARS")],
        
        [InlineKeyboardButton("🟢" if server[7] == 1 else "🔴",callback_data=f"EditStateSr_{server[0]}_{server[7]}"),InlineKeyboardButton("وضعیت",callback_data="ARS")],
        [InlineKeyboardButton(server[6],callback_data=f"ServerName_{server[0]}"),InlineKeyboardButton("نام",callback_data="ARS")],
        [InlineKeyboardButton(server[5],callback_data=f"DomainServer_{server[0]}"),InlineKeyboardButton("دامنه",callback_data="ARS")],
        [InlineKeyboardButton(server[3],callback_data=f"ARS"),InlineKeyboardButton("ادرس",callback_data="ARS")],
        [InlineKeyboardButton(server[1],callback_data=f"ARS"),InlineKeyboardButton("نام کاربری",callback_data="ARS")],
        [InlineKeyboardButton(server[2],callback_data=f"ARS"),InlineKeyboardButton("پسورد",callback_data="ARS")],
        [InlineKeyboardButton(server[4],callback_data=f"ARS"),InlineKeyboardButton("نوع",callback_data="ARS")],     
        [InlineKeyboardButton("دسته بندی ها",callback_data=f"CatServerManage_{server[0]}")],
        [InlineKeyboardButton("ℹ️ بررسی سرور ",callback_data=f"GetInfoServer_{server[0]}")],
        [InlineKeyboardButton("ویرایش اطلاعات ورود",callback_data=f"ServerEdit_{server[0]}")],
        [InlineKeyboardButton("بازگشت 🔙",callback_data=f"manageServers")]
        ]
    return btns
async def GetBtnsServerData(data,serverId):
    btns = [
        [InlineKeyboardButton("اطلاعات",callback_data="ARS"),InlineKeyboardButton("نام",callback_data="ARS")],
        [InlineKeyboardButton(f"{round(float(data['cpu']),2)} %",callback_data="ARS"),InlineKeyboardButton("CPU",callback_data="ARS")],
        
      
        [InlineKeyboardButton(f"{data['cpuSpeedMhz']}",callback_data="ARS"),InlineKeyboardButton("cpuSpeedMhz",callback_data="ARS")],
        [InlineKeyboardButton(f"{round(data['mem']['current']/1024/1024/1024,2)} GB",callback_data="ARS"),InlineKeyboardButton("RAM Used",callback_data="ARS")],
        [InlineKeyboardButton(f"{round(data['mem']['total']/1024/1024/1024,2)} GB",callback_data="ARS"),InlineKeyboardButton("RAM Total",callback_data="ARS")],
        [InlineKeyboardButton(f"{data['xray']['state']}",callback_data="ARS"),InlineKeyboardButton("xray",callback_data="ARS")],
        [InlineKeyboardButton(f"{data['xray']['version']}",callback_data="ARS"),InlineKeyboardButton("version",callback_data="ARS")],
        [InlineKeyboardButton(f"{data['publicIP']['ipv4']}",callback_data="ARS"),InlineKeyboardButton("IPV4",callback_data="ARS")],
        [InlineKeyboardButton(f"{data['publicIP']['ipv6']}",callback_data="ARS"),InlineKeyboardButton("ipv6",callback_data="ARS")],
        [InlineKeyboardButton(f"بازگشتی 🔙",callback_data=f"EditServer_{serverId}")],


    ]
    return btns
async def GetServerData(serverId):
    server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE ID = {serverId}")
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

    async with httpx.AsyncClient() as client :
        try: 
         response = None

         session = server[8]
         headers['Cookie'] = f"lang=en-US; {server[8]}"
         response = await client.post(f"{server[3]}/server/status",headers=headers)
         data = json.loads(response.text)
         if data['success'] == True:
             return [True , data['obj']]
         else:
             return [False,0]   
        except: 
                  return [False,0]   
async def UpdateServerName(name , serverId):
    await db_manager.QueryWidthOutValue(f"UPDATE Server SET Name = '{name}' WHERE Id = {serverId}")

async def UpdateServerDomainName(domain , serverId):
    await db_manager.QueryWidthOutValue(f"UPDATE Server SET Domain = '{domain}' WHERE Id = {serverId}")


async def EditServerState( serverId , state):
    await db_manager.QueryWidthOutValue(f"UPDATE Server SET State = {state} WHERE Id = {serverId} ")

async def EditServerSafe( serverId , state):
    await db_manager.QueryWidthOutValue(f"UPDATE Server SET SafeServer = {state} WHERE Id = {serverId} ")
async def GetCatEditBtns(catId):
       res = await db_manager.execute_query_all(f"SELECT Server.Name,Server.Id FROM Server JOIN ServerCat ON Server.Id = ServerCat.ServerId WHERE ServerCat.CatId = {catId}")
       btns = []
       if res !=None or len(res) != 0:
           for r in res :
               btns.append([InlineKeyboardButton(r[0],callback_data ="ARS")])
       else:
               btns.append([InlineKeyboardButton("سروری موجود نیست!",callback_data ="ARS")])
       btns.append([InlineKeyboardButton("🔙 بازگشت",callback_data="managecategury")])
       return btns       
           
async def GetCatBtnsSelect():
    res = await db_manager.execute_query_all("SELECT Id,Title FROM category ")
    btns = []
    for r in res:
        btns.append([r[1]])
      
    btns.append(['انصراف'])
    return btns
    
async def GetServerBtnsSelect():
    res = await db_manager.execute_query_all("SELECT Id,Name FROM Server ")
    btns = []
    for r in res:
        btns.append([r[1]])
      
    btns.append(['انصراف'])
    return btns

async def GetAllCatBtnsInline(serverId):
    res = await db_manager.execute_query_all("SELECT Id,Title FROM category ")
    btns = []
    for r in res:
        btns.append([InlineKeyboardButton(r[1],callback_data=f"EditCatSR_{r[0]}_{serverId}")])
    btns.append([InlineKeyboardButton("🔙 بازگشت",callback_data=f"EditServer_{serverId}")])    
    return btns    

async def UpdateCatServer(serverId, catId):
     await db_manager.QueryWidthOutValue(f"UPDATE Server SET CatId = {catId} WHERE Id = {serverId}")

async def CheckServiceTime(app):
    services = await db_manager.execute_query_all("SELECT AlertTimeFirst,AlertTimeTwo,Email,EndDate,UserId,Id,PlanId,CatId,TypeService,ServiceTest,ServerIds FROM Service WHERE State = 1")
    AlertTime = await db_manager.execute_query_one("SELECT SendAlertTimeFirst,SendAlertTimeTwo FROM Setting") 

    for service in services:
       if service[9] == "empty": 
        getSetting =  await db_manager.execute_query_one("SELECT buyagain FROM Setting")   
        if AlertTime[0] != 0:
            if service[0] == 0 :
                date = datetime.datetime.fromtimestamp(service[3]/1000) - datetime.datetime.now()
                if date.days > 0:
                
                    if date.days <= AlertTime[0]: 
                         await db_manager.QueryWidthOutValue(f"UPDATE Service SET AlertTimeFirst = 1  WHERE Id = {service[5]} ") 
                         if service[6] != 0:
                          if getSetting[0] == 1 :
                             if service[24] == "sub":
                                 
                                await app.send_message(service[4],f"""🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[0] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")],[InlineKeyboardButton("📥 خرید مجدد",callback_data=f"getOrder_{service[10]}_{service[15]}")]]))
                             else:
                                 serverIdService = ast.literal_eval(17)
                                 await app.send_message(service[4],f"""🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[0] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")],[InlineKeyboardButton("📥 خرید مجدد",callback_data=f"OrderSingle_{service[10]}_{serverIdService[0]}_{service[15]}")]]))
                         
                          else:
                               await app.send_message(service[4],f""" 🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[0] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")]]))
                         else:
                              await app.send_message(service[4],f""" 🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[0] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")]]))
                elif  date.days == 0 and date.seconds > 0:
                         await db_manager.QueryWidthOutValue(f"UPDATE Service SET AlertTimeFirst = 1  WHERE Id = {service[5]} ") 
                         if service[6] != 0:
                          if getSetting[0] == 1 :
                             if service[8] == "sub":
                                 
                                await app.send_message(service[4],f"""🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[0] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")],[InlineKeyboardButton("📥 خرید مجدد",callback_data=f"getOrder_{service[6]}_{service[7]}")]]))
                             else:
                                 serverIdService = ast.literal_eval(service[10])
                                 await app.send_message(service[4],f"""🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[0] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")],[InlineKeyboardButton("📥 خرید مجدد",callback_data=f"OrderSingle_{service[6]}_{serverIdService[0]}_{service[7]}")]]))
                         
                          else:
                               await app.send_message(service[4],f""" 🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[0] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")]]))
                         else:
                              await app.send_message(service[4],f""" 🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[0] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")]]))
        if AlertTime[1] != 0:
            if service[1] == 0 :
               date = datetime.datetime.fromtimestamp(service[3]/1000) - datetime.datetime.now()
               if date.days > 0:
                
                    if date.days <= AlertTime[1]: 
                         await db_manager.QueryWidthOutValue(f"UPDATE Service SET AlertTimeTwo = 1  WHERE Id = {service[5]} ") 
                         if service[6] != 0:
                          if getSetting[0] == 1 :
                             if service[24] == "sub":
                                 
                                await app.send_message(service[4],f"""🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[1] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")],[InlineKeyboardButton("📥 خرید مجدد",callback_data=f"getOrder_{service[10]}_{service[15]}")]]))
                             else:
                                 serverIdService = ast.literal_eval(17)
                                 await app.send_message(service[4],f"""🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[1] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")],[InlineKeyboardButton("📥 خرید مجدد",callback_data=f"OrderSingle_{service[10]}_{serverIdService[0]}_{service[15]}")]]))
                         
                          else:
                               await app.send_message(service[4],f""" 🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[1] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")]]))
                         else:
                              await app.send_message(service[4],f""" 🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[1] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")]]))
               elif  date.days == 0 and date.seconds > 0:
                         await db_manager.QueryWidthOutValue(f"UPDATE Service SET AlertTimeTwo = 1  WHERE Id = {service[5]} ") 
                         if service[6] != 0:
                          if getSetting[0] == 1 :
                             if service[8] == "sub":
                                 
                                await app.send_message(service[4],f"""🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[1] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")],[InlineKeyboardButton("📥 خرید مجدد",callback_data=f"getOrder_{service[6]}_{service[7]}")]]))
                             else:
                                 serverIdService = ast.literal_eval(service[10])
                                 await app.send_message(service[4],f"""🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[1] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")],[InlineKeyboardButton("📥 خرید مجدد",callback_data=f"OrderSingle_{service[6]}_{serverIdService[0]}_{service[7]}")]]))
                         
                          else:
                               await app.send_message(service[4],f""" 🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[1] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")]]))
                         else:
                              await app.send_message(service[4],f""" 🔔 | اطلاعیه زمان باقی مانده

👤 | کاربر گرامی با اشتراک {service[2]} 

⏰ | از اشتراک شما کمتر از {AlertTime[1] } روز باقی مانده است لطفا برای تمدید یا خرید مجدد اقدام نمایید

♻️ /start
""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 🔁 تمدید",callback_data=f"extension_{service[5]}")]]))


async def GePhotoStart():
    res = await db_manager.execute_query_one("SELECT SendPhotoWithStartBot,PhotoStart FROM Setting")
    return res    


async def AddConfigUserManual(nmuberStart,endTimeMikro,configName,Volume,numberOfConf,catId,mes,userId,serverId):
                  servers = None
                  if serverId != 0:
                      servers = await db_manager.execute_query_all(f"SELECT * FROM Server WHERE Id = {serverId} ")
                  else:    
                   servers = await db_manager.execute_query_all(f"SELECT * FROM Server JOIN ServerCat ON Server.Id = ServerCat.ServerId WHERE ServerCat.CatId = {catId} ")
                  catType = await db_manager.execute_query_one(f"SELECT * FROM category WHERE Id = {catId}")
                  NameConfigs = await db_manager.execute_query_one("SELECT SubName , SingleName FROM Setting ")
                  i =1    
                  uuid = []
                  print(servers)
                  await mes.reply("ارسال شروع شد")
                  while i <= numberOfConf:
                    uuid=uuid4()
                    email = configName + f'{nmuberStart}'
                    nmuberStart += 1
                    randomId = random.randint(100000,999999)
                    serversCount = []
                    configUrl =get_random_string(12)
                    lastrowId = await db_manager.Query("INSERT INTO Service(UserId,Email,Password,CreateDate,EndDate,OrderId,PlanId,CatId,ServerIds,configUrl,TransformEnable,RandomId,TypeService) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(userId,email,str(uuid),int(datetime.datetime.timestamp(datetime.datetime.now())),endTimeMikro,0,0,catId,f'{serversCount}',configUrl,Volume,randomId,"sub" if catType == "sub" else "single"))

                    counter = 0
                    for server in servers:

                             try:     
                               data = {
    "id": f"{server[10]}",
    "settings": '{"clients": [{"id": "'+ str(uuid) +'", "alterId": 0, "email": "'+ email +'", "totalGB": '+ str(int(Volume)) +', "expiryTime": '+str(endTimeMikro)+', "enable": true, "tgId": "", "subId": ""}]}'
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
                                          response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers)
                                          data = json.loads(response.text)
         
                                          if data['success'] == False:
                                                          pass

          
             
                                          else:
                                                   await db_manager.Query("INSERT INTO Configs(ServiceId,Name,uuid,Upload,Download,TotalUsed,TansformEnable,ServerId,State,isDelete,EndDate,CreateDate) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(lastrowId.lastrowid,email,str(uuid),0,0,0,Volume,server[0],1,0,endTimeMikro,int(datetime.datetime.timestamp(datetime.datetime.now()))))
                                                   counter +=1
                                                   serversCount.append(server[0])

             
             
                             except:
                                         ...
                    if counter != 0:
                       try: 
                         await db_manager.QueryWidthOutValue(f"UPDATE Service SET ServerIds = '{str(serversCount)}' WHERE Id= {lastrowId.lastrowid}")
                         subdomain = await db_manager.execute_query_one("SELECT SubDomain FROM Setting ")
                         text = ""
                 
                         if catType[4] == "sub":
                             text =f" <code>{subdomain[0]}/kaiser?token={configUrl}</code>"
                         else:
                            response = None
                            async with httpx.AsyncClient() as client:
                             
         

     
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
                             try:
                              try:
                                   response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers = headers, timeout=6)
                              except:
                               response = await client.post(server[3] + f"/{'panel' if server[4]=='sanaei' else 'xui'}/inbound/list", headers=headers, timeout=6)  
                             except :
                                ...
                            info_json = json.loads(response.text)
                        
                            text = GetConfig(info_json['streamSettings'],str(uuid),email,info_json['port'],
                                             info_json['protocol'],server[5])    
                         qr_stream = BytesIO()
                      
                         qr = qrcode.make(text)
                         qr.save(qr_stream)
                         qr_stream.seek(0)
                         dateConverted = datetime.datetime.fromtimestamp(endTimeMikro/ 1000) 
                         endDate = dateConverted - datetime.datetime.now()
                         mess =f"""
✅ | اشتراک با موفقیت ایجاد کرد
👤 | نام اشتراک : { email}
📊 | مقدار حجم : {round(Volume /1024 / 1024 /1024,2)} GB
⏰ | مقدار زمان : {endDate.days + 1} روز

🔗 | کانفیگ شما :

<code>{text}</code>

⚠️ | آموزش اتصال در ربات می‌باشد
"""
                         
                         await mes.reply_photo(photo=qr_stream,caption=mess )  
                       except:
                           print("Error")
                    
                    else:
                        await mes.reply("هنگام ساخت سرویس مشکلی پیش آمد")
                        await db_manager.QueryWidthOutValue(f"DELETE FROM Service WHERE Id = {lastrowId.lastrowid}")
                    i+=1      
                  await mes.reply("✅",reply_markup=ReplyKeyboardMarkup(await GetMainKeys(userId),resize_keyboard=True))   

async def ChangeStep(userId, STEP):

    await db_manager.QueryWidthOutValue(f"UPDATE Users SET STEP = '{STEP}' WHERE UserId = {userId}")

async def GetUserSTEP(userId):
  try:  
    res =  await db_manager.execute_query_one(f"SELECT STEP FROM Users WHERE UserId = {userId} ")
    return res[0]             
  except:
      return "problem"
 
async def GetServiceById(ServiceId):
    Service = await db_manager.execute_query_one(f"SELECT * FROM Service WHERE Id = {ServiceId}")
    if Service == None :
        return [False,0]
    else:
     return [True,Service]     
 
async def GetServiceByUuid(uudiUser):
    serviceId = await db_manager.execute_query_one(f"SELECT Id FROM Service WHERE Password = '{uudiUser}'")
    if serviceId == None :
        return False
    else:
     return serviceId[0]     



async def IsChannelLock():
 data = await db_manager.execute_query_one("SELECT chanelLock FROM Setting ")
 if data[0] == 0:
     return False
 return True



#        [InlineKeyboardButton( {'🟢' if res[0] == 1 else '🔴'} ,callback_data=f"TarefeSate_{res[0]}"),InlineKeyboardButton("وضعیت",callback_data="ARS")],
#        [InlineKeyboardButton( "افزودن فیلم" ,callback_data=f"TarefeSate"),InlineKeyboardButton("وضعیت",callback_data="ARS")],
#        [InlineKeyboardButton( "افزودن عکس"  ,callback_data=f"AddMovieTarrefe"),InlineKeyboardButton("وضعیت",callback_data="ARS")],
#        [InlineKeyboardButton( "نمایش نمونه" ,callback_data=f"ShowTarefeTest"),InlineKeyboardButton("بازگشت ",callback_data="businnes")]
#    ]



   
#  settings = json.loads(inbound['settings'])
#             for client in settings['clients']:
#                 if inbound["protocol"] == "trojan":
#                     if trojan == True:
#                         if pay[2] == client['password']:
#                             email = client['email']
#                             break

#                 else:
#                     if pay[2] == client['id']:
#                         email = client['email']
#                         break

#             if email != "":
               