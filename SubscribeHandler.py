from flask import Flask, request, render_template
import time
from db import Context
import asyncio
import ast
import httpx
import json
import base64
from uuid import uuid4
from service import orm
import urllib.request
from flask_cors import CORS
import string
import requests
import datetime
import jdatetime
import aiofiles
from ippanel import Client
import random

import __main__

app = Flask(__name__, template_folder="templates")
CORS(app)

db_manager = Context.DatabaseManager()
async def SaveFileConfig(data):
    async with aiofiles.open("Config/Config.json", mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(data))


async def ReadFileConfig():
    async with aiofiles.open("Config/Config.json", mode="r", encoding="utf-8") as f:
        res = json.loads(await f.read())
    return res


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def DictDatas(data):

    returnData = []
    for d in data:
        apendData = []
        apendData = [de for de in d]
        returnData.append(apendData)
    return returnData

   
async def GetCofigUserTest(phoneNumber):
 test = await db_manager.execute_query_one("SELECT * FROM TestFree")
 servers = None
 if test[4] == 0:
     servers = await db_manager.execute_query_all(f"SELECT Server.* FROM ServerCat JOIN Server ON Server.Id = ServerCat.ServerId AND Server.State = 1  WHERE ServerCat.CatId = {test[5]}  ")
     
     allow = False
     fileConfig =await ReadFileConfig()
     fileConfig['NumberConfig']+=1 
     randomId  = fileConfig['NumberConfig']
     await SaveFileConfig(fileConfig)
     TestName = await db_manager.execute_query_one("SELECT TestName,LockChanel FROM Setting")
     EndTime = datetime.datetime.now() + datetime.timedelta(days=int(test[2]))
     Volume = test[1] * 1024 * 1024 * 1024
     email =f"{TestName[0]}{randomId}"
     configUrl =get_random_string(12)
     uuid=uuid4()
     endTimeMikro =int(datetime.datetime.timestamp(EndTime) ) * 1000
     counter = 0
     serversCount = []
 
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
         
         response =  await client.post(url=f"{server[3]}/login",data={"username":f"{server[1]}","password":f"{server[2]}"})
         session = response.headers.get("Set-Cookie").split("; ")[0]   
         headers['Cookie']  = f"lang=en-US; {session}"
         response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers)
         data = json.loads(response.text)
         
         if data['success'] == False:
             pass
             
         else:
             counter +=1
             serversCount.append(server[0])

             
             
      except:
       pass
     if counter != 0:
           
             lastrowId = await db_manager.Query("INSERT INTO Service(UserId,Email,Password,CreateDate,EndDate,OrderId,PlanId,CatId,ServerIds,configUrl,TransformEnable,RandomId,TypeService,ServiceTest,PhoneNumber) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(0,email,str(uuid),int(datetime.datetime.timestamp(datetime.datetime.now())),endTimeMikro,0,0,test[5],f'{serversCount}',configUrl,Volume,randomId,"sub","ok",phoneNumber))
             await db_manager.QueryWidthOutValue(f"UPDATE Users SET UseFreeTrial = 1 WHERE PhoneNumber = {phoneNumber}")
             await db_manager.QueryWidthOutValue(f"UPDATE TestFree SET Geted = {test[6]+1} ")
             return { "success":True,"message":"کانفیگ با موفقیت تایید شد","serviceId":lastrowId.lastrowid}
     else:
         return {"success": False,"message":"هنگام ساخت کانفیگ هیچ سروری متصل نبود !"}


 else:   
     server = await db_manager.execute_query_one(f"SELECT * FROM Server WHERE Id = {test[4]}  ")
      
     allow = False
     
     randomId  = random.randint(1000, 99999)  
     random2Id =random.randint(1000, 99999)  
     TestName = await db_manager.execute_query_one("SELECT TestName,LockChanel FROM Setting")
     EndTime = datetime.datetime.now() + datetime.timedelta(days=int(test[2]))
     Volume = test[1] * 1024 * 1024 * 1024
     email =f"{TestName[0]}{randomId}-{random2Id} "
     configUrl =get_random_string(12)
     uuid=uuid4()
     endTimeMikro =int(datetime.datetime.timestamp(EndTime) ) * 1000
     counter = 0
     serversCount = []
 
    
 
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
         response = ""
         try:
             
            response =  await client.post(url=f"{server[3]}/login",data={"username":f"{server[1]}","password":f"{server[2]}"},timeout=15)
         except:
            response =  await client.post(url=f"{server[3]}/login",data={"username":f"{server[1]}","password":f"{server[2]}"},timeout=15)
                
         session = response.headers.get("Set-Cookie").split("; ")[0]   
         headers['Cookie']  = f"lang=en-US; {session}"
         try:
             
            response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers,timeout=15)
         except:
             response = await client.post(f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',data=data,headers=headers,timeout=15)
         print(response.text)
         data = json.loads(response.text)
         
         if data['success'] == False:
             return {"success": False,"message":"هنگام ساخت کانفیگ هیچ سروری متصل نبود !"}
             
         else:
             lastrowId = await db_manager.Query("INSERT INTO Service(UserId,Email,Password,CreateDate,EndDate,OrderId,PlanId,CatId,ServerIds,configUrl,TransformEnable,RandomId,TypeService,ServiceTest,PhoneNumber) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(0,email,str(uuid),int(datetime.datetime.timestamp(datetime.datetime.now())),endTimeMikro,0,0,test[5],f'[{server[0]}]',configUrl,Volume,randomId,"single","ok",phoneNumber))
             await db_manager.QueryWidthOutValue(f"UPDATE Users SET UseFreeTrial = 1 WHERE PhoneNumber = {phoneNumber}")
             await db_manager.QueryWidthOutValue(f"UPDATE TestFree SET Geted = {test[6]+1} ")
             return { "success":True,"message":"کانفیگ با موفقیت تایید شد","serviceId":lastrowId.lastrowid}

             
             
    #  except:
    #    return [False , "هنگام افزودن یه مشکل خوردیم"]


@app.route("/editServer", methods=["POST"])
async def UpdateServer():
  try:
  
    data = request.get_json()
    print(str(data))
    await db_manager.QueryWidthOutValue(f"UPDATE Server SET Url = '{data['url']}', User = '{data['user']}' , Password = '{data['password']}', PanelType = '{data['type']}' , Session  = '{data['session']}' , InboundId = {data['inbound']} WHERE Id = {data['serverId']} ")
    return {"success":True}
  except:
          return {"success":False}

@app.route('/getUserService',methods=["GET"])

async def GetUserService():
    data = request.args.get('token','ars')
    time.sleep(1)
    if data !='ars':
        userService = await db_manager.execute_query_all(f"SELECT Id,Email  FROM Service WHERE PhoneNumber = {data} AND isDelete = 0")
        if userService == None or userService == []:
             
             return {'success':False,"message":"سرویسی یافت نشد!"}    
        print(userService[0][0])
        data =DictDatas(userService)
        return {"success": True, "data": data}
    else:
         return {'success':False,"message":"مقادیر ارسالی دارای مشکل میباشند"}    

@app.route('/getTest',methods=["GET"])

async def GetTest():
    data = request.args.get('token','ars')
    time.sleep(2)
    if data !='ars':
        user = await db_manager.execute_query_one(f"SELECT * FROM Users WHERE PhoneNumber = {data}")
        if user[8] == 0 or user[3] == 1:
            testActive = await db_manager.execute_query_one("SELECT Test FROM Setting ")
            if testActive[0] == 1:
                  print('testttttt')
                  return await GetCofigUserTest(int(data))
            else:
                 return {'success':False,"message":'درحال حاضر تست فعال نمیباشد'}    
        else:
            return {'success':False,"message":"شما قبلا تست خود را دریافت کرده اید"}    

    else:
         return {'success':False,"message":"مقادیر ارسالی دارای مشکل میباشند"}    

@app.route("/createOrder", methods=["POST"])
async def CreateOrder():
    data = request.get_json()
    try:

        if (
            data["phonenumber"] == 0
            or data["serverId"] != None
            or data["catId"] != None
            or data["planId"] != None
        ):
            ...
    except:
        return {"success": False, "message": "مقادیر ارسالی داری مشکل هستند"}

    now = datetime.datetime.now()

    timestamp = int(datetime.datetime.timestamp(now))
    plan = await db_manager.execute_query_one(
        f"SELECT * FROM ServerPlans WHERE Id = {data['planId']}"
    )
    if plan == None:
        return {"success": False, "message": "مقادیر ارسالی دارای مشکل هستند"}
    res = await db_manager.Query(
        f"INSERT INTO OrdersList(DateTime, PlanId, PhoneNumber , Type, State,Price,EndTimePlan,ServerId,CatId) VALUES(?,?,?,?,?,?,?,?,?)",
        (
            timestamp,
            data["planId"],
            data["phonenumber"],
            "single",
            0,
            plan[4],
            plan[3],
            data["serverId"],
            data["catId"],
        ),
    )
    return {"success": True, "orderId": res.lastrowid, "price": plan[4]}


@app.route("/setCode", methods=["POST"])
async def SetCode():
    data = request.get_json()
    try:

        if data["phonenumber"] == 0 or data["userId"] != None:
            ...
    except:
        return {"success": False, "message": "مقادیر ارسالی داری مشکل هستند"}
    user = await db_manager.execute_query_one(
        f"SELECT * FROM Users WHERE PhoneNumber = {data['phonenumber']} AND ActiveCode = {data['code']}"
    )
    if user != None:
        await db_manager.QueryWidthOutValue(
            f"UPDATE Users SET IsActivePhone = 1 WHERE PhoneNumber = {data['phonenumber']}"
        )
        return {"success": True}
    else:
        return {"success": False, "message": "لطفا کد تایید را به درستی وارد کنید"}


@app.route("/sendCode", methods=["POST"])
async def SendCode():
    num = random.randint(100000, 999999)
    data = request.get_json()
    try:

        if data["phonenumber"] == 0 or data["userId"] != None:
            ...
    except:
        return {"success": False, "message": "مقادیر ارسالی داری مشکل هستند"}

    headers = {
      'Content-Type': 'application/json',
      'apikey': '6qbJ8aXJCypnHGEYL5ErOQYonRDMB-UCD9lquHUmh8c='
    }
    num = random.randint(100000, 999999)
    data = request.get_json()
    api_key = "6qbJ8aXJCypnHGEYL5ErOQYonRDMB-UCD9lquHUmh8c="
    sms = Client(api_key)
    try:

        if data["phonenumber"] == 0 or data["userId"] != None:
            ...
    except:
        return {"success": False, "message": "مقادیر ارسالی داری مشکل هستند"}
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"
    payload = json.dumps({
  "code": "i5dpx4vtkt7kx6e",
  "sender": "+983000505",
  "recipient": f"0{data['phonenumber']}",
  "variable": {
    "num": num
  }
})

    if data["userId"] != None:
        user = await db_manager.execute_query_one(
            f"SELECT * FROM Users WHERE PhoneNumber = {data['phonenumber']} AND UserId = {data['userId']} "
        )
        if user == None:
            user = await db_manager.execute_query_one(
                f"SELECT * FROM Users WHERE UserId = {data['userId']} AND PhoneNumber = 0"
            )
            if user == None:
                user = await db_manager.execute_query_one(
                    f"SELECT * FROM Users WHERE PhoneNumber = {data['phonenumber'] } "
                )
                if user != None:
                    response = requests.request("POST", url, headers=headers, data=payload)

                    if response.status_code ==200:

                        await db_manager.QueryWidthOutValue(
                            f"UPDATE Users SET  ActiveCode = {num} WHERE PhoneNumber = {data['phonenumber'] } "
                        )
                        return {"success": True}
                    else:
                        return {
                            "success": False,
                            "message": "هنگام ارسال پیامک مشکلی پیش امده",
                        }
            else:

                response = requests.request("POST", url, headers=headers, data=payload)

                if response.status_code ==200:

                    await db_manager.QueryWidthOutValue(
                        f"UPDATE Users SET PhoneNumber = {data['phonenumber']} , IsActivePhone = 0 , ActiveCode = {num} WHERE UserId= {data['userId']} "
                    )
                    return {"success": True}
                else:
                    return {
                        "success": False,
                        "message": "هنگام ارسال پیامک مشکلی پیش امده",
                    }

        else:
                response = requests.request("POST", url, headers=headers, data=payload)

                if response.status_code ==200:
                 await db_manager.QueryWidthOutValue(
                    f"UPDATE Users SET PhoneNumber = {data['phonenumber']} , IsActivePhone = 0 , ActiveCode = {num} WHERE UserId= {data['userId']} "
                )
                 return {"success": True}
                else:
                     return {"success": False, "message": "هنگام ارسال پیامک مشکلی پیش امده"}

    user = await db_manager.execute_query_one(
        f"SELECT * FROM Users WHERE PhoneNumber = {data['phonenumber'] } "
    )
    if user != None:
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code ==200:

            
            await db_manager.QueryWidthOutValue(
                f"UPDATE Users SET  ActiveCode = {num} WHERE PhoneNumber = {data['phonenumber'] }"
            )
            return {"success": True}
        else:
            return {"success": False, "message": "هنگام ارسال پیامک مشکلی پیش امده"}
    else:
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code ==200:


            
            timeJoin = datetime.datetime.timestamp(datetime.datetime.now())
            await db_manager.Query(
                "INSERT INTO Users(UserId,UserName,Name,TimeJoin,IsAdmin,CountShopped,Invited,CooperationId,UseFreeTrial,Wallet,STEP,ActiveCode,PhoneNumber,IsActivePhone) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    0,
                    "",
                    "",
                    timeJoin,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    "home",
                    num,
                    data["phonenumber"],
                    0,
                ),
            )
            return {"success": True}
        else:
            return {"success": False, "message": "هنگام ارسال پیامک مشکلی پیش امده"}


@app.route("/getCategory", methods=["GET"])
async def GetAllCategory():

    data = await db_manager.execute_query_all(
        "SELECT Id,Title FROM category WHERE SHOW  = 1"
    )

    return {"success": True, "data": DictDatas(data)}


@app.route("/getServerCat", methods=["GET"])
async def ServeCat():
    time.sleep(1)
    CatId = request.args.get("CatId", "ars")
    if CatId == "ars":
        return {"success": False, "message": "مقادیر ارسالی درست نمیباشد"}

    cat = await db_manager.execute_query_one(
        f"SELECT * FROM category WHERE SHOW  = 1 AND Id = {CatId}"
    )
    if cat == None:

        return {"success": False, "message": "!دسته بندی یافت نشد"}

    servers = await db_manager.execute_query_all(
        f"SELECT Server.Id,Server.Name  FROM  ServerCat JOIN Server ON Server.Id = ServerCat.ServerId AND Server.State = 1   WHERE ServerCat.CatId = {CatId} "
    )
    if servers != []:

        return {"success": True, "data": DictDatas(servers), "catId": CatId}

    else:
        return "NotFound"


@app.route("/getserverPlan", methods=["GET"])
async def PlanCart():

    CatId = request.args.get("CatId", "cat")
    ServerId = request.args.get("ServerId", "server")
    if ServerId != "server" and CatId != "cat":
        plans = await db_manager.execute_query_all(
            f"SELECT ServerPlans.Id  , ServerPlans.PlanName  , ServerPlans.Price , ServerPlans.Volume , ServerPlans.MonthCount  FROM PlanCat JOIN ServerPlans ON PlanCat.PlanId = ServerPlans.Id  WHERE PlanCat.CatId  = {CatId} ORDER BY ServerPlans.Price "
        )
        if plans != None or plans != []:
            return {
                "success": True,
                "data": DictDatas(plans),
                "serverId": ServerId,
                "catId": CatId,
            }
        else:
            return {"success": False, "message": "پلن یافت نشد"}
    else:
        return "NotFound"


@app.route("/kaiser", methods=["GET"])
async def handle_request():
    resualt = ""
    token = request.args.get("token", "ARS")
    if token == "ARS":

        return "Invalid Data"
    res = None
    try:
        tokenConvert = int(token)
        res = await db_manager.execute_query_one(
            f"SELECT Password,ServerIds,Email,TransformEnable,RandomId,EndDate,State,CreateDate,CatId,Id FROM Service WHERE ConfigURL = '{token}' OR Id = {tokenConvert} AND isDelete = 0 "
        )
    except:

        res = await db_manager.execute_query_one(
            f"SELECT Password,ServerIds,Email,TransformEnable,RandomId,EndDate,State,CreateDate,CatId,Id FROM Service WHERE ConfigURL = '{token}' AND isDelete = 0 "
        )
    if res != None:
        serverIds = ast.literal_eval(res[1])

        async def GetData(serverid, semaphore):
            async with semaphore:
                try:
                    nonlocal upload
                    nonlocal download
                    nonlocal resualt
                    server = await db_manager.execute_query_one(
                        f"SELECT * FROM Server WHERE Id = {serverid}"
                    )
                    origin = server[3].split("/")
                    config = await db_manager.execute_query_one(f"SELECT * FROM Configs WHERE ServiceId = {res[9]} AND ServerId = {server[0]}")
                    limits = httpx.Limits(max_connections=2)
                    async with httpx.AsyncClient(limits=limits) as client:
                   

                        session = server[8]
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
                            "Accept": "application/json, text/plain, */*",
                            "Accept-Language": "en-US,en;q=0.5",
                            "Accept-Encoding": "gzip, deflate",
                            "X-Requested-With": "XMLHttpRequest",
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Origin": f"{origin[0]}://{origin[2]}",
                            "Connection": "keep-alive",
                            "Referer": f"{server[3]}/panel/inbounds",
                            "Cookie": "",
                        }

                        headers["Cookie"] = f"lang=en-US; {session}"
                        try:
                            response = await client.post(
                                server[3] + "/panel/inbound/list",
                                headers=headers,
                                timeout=6,
                            )
                        except:
                            response = await client.post(
                                server[3] + "/panel/inbound/list",
                                headers=headers,
                                timeout=6,
                            )

                        info_json = json.loads(response.text)
                        inbounds = info_json["obj"]

                        for inbound in inbounds:
                            if inbound["id"] == server[10]:
                                states = inbound["clientStats"]
                                for state in states:
                                    if state["email"] == res[2]:
                                        upload += state["up"]
                                        download += state["down"]
                                        resualt += (
                                            GetConfig(
                                                inbound["streamSettings"],
                                                config[3],
                                                server[6],
                                                inbound["port"],
                                                inbound["protocol"],
                                                server[5]
                                              
                                            )
                                            + "\n"
                                        )
                                        return
                except:
                    pass

        upload = 0
        download = 0
        semaphore = asyncio.Semaphore(3)
        await asyncio.gather(*[GetData(serverid, semaphore) for serverid in serverIds])
        safeConfig =await db_manager.execute_query_one("SELECT SafeMode,SafeModCat FROM Setting")
        configSafe =""
        if safeConfig[1] == res[8]:
            configSafe = safeConfig[0]
          
        totalConf = getTotal(download, upload, res[3])
        nameConf = await getName(res[2],res[6])
        dateConf = getDate(res[5])
        
        # state 6
        #    date 5
        if (
            str(request.accept_mimetypes.best) == "text/html"
            or str(request.accept_mimetypes.best) == "application/signed-exchange; v=b3"
        ):
            PercentUsages = (download + upload) * 100 / res[3]

            usageGB = round((download + upload) / 1024 / 1024 / 1024, 2)
            Total = round(res[3] / 1024 / 1024 / 1024, 2)
            rest = round((res[3] - (download + upload)) / 1024 / 1024 / 1024, 2)
            #    date = datetime.datetime.fromtimestamp(res[5] /1000) - datetime.datetime.now()
            #    dateTotal = datetime.datetime.fromtimestamp(res[5] /1000) - datetime.datetime.fromtimestamp(res[7] )
            #    daterest = int( 100 - ( date.days * 100 / dateTotal.days) )
            date = jdatetime.datetime.fromtimestamp(res[5] / 1000)

            print(PercentUsages)
            state = ""
            if res[6] == 1:
                state = "فعال"
            else:
                state = "غیر فعال"
            resualt = resualt +"\n" + configSafe
            return render_template(
                 "state1.html",
                usageGB=usageGB,
                rest=rest,
                TotalUsage=Total,
                date=str(date.date()),
                usage=PercentUsages,
                name=f"👑 | K {res[2]}",
                state=state,
                result=resualt,
            )

        resualt =nameConf +"\n" +  resualt +(f"\n{configSafe}" if configSafe !="" else ""  ) +"\n"+  totalConf  +"\n" + dateConf    
        sample_string_bytes = resualt.encode("utf-8")

        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return f"{base64_string}"

    else:
        return "<h1>Not Found Service</h1></br><p>Please Send Invalid Data</p>"


def get_random_string(length):

    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


async def CreateSingle(order):
    catId = await db_manager.execute_query_one(
        f"SELECT CatId,Volume FROM ServerPlans WHERE Id = {order[2]}"
    )

    server = await db_manager.execute_query_one(
        f"SELECT * FROM Server WHERE Id = {order[10]}  "
    )
    days = int(order[7]) * 30
    allow = False
    randomId  = random.randint(1000, 99999)  
    random2Id =random.randint(1000, 99999)  
    SingleName = await db_manager.execute_query_one(
        "SELECT SingleName,LockChanel FROM Setting"
    )
    EndTime = datetime.datetime.now() + datetime.timedelta(days=days)
    Volume = catId[1] * 1024 * 1024 * 1024
    email = f"{SingleName[0]}{randomId}-{random2Id}"
    configUrl = get_random_string(12)
    uuid = uuid4()
    endTimeMikro = int(datetime.datetime.timestamp(EndTime)) * 1000

    #   serversCount = []
    print("ARSSSSSSSSSSSSSSSSSSSS")
    try:
        data = {
            "id": f"{server[10]}",
            "settings": '{"clients": [{"id": "'
            + str(uuid)
            + '", "alterId": 0, "email": "'
            + email
            + '", "totalGB": '
            + str(int(Volume))
            + ', "expiryTime": '
            + str(endTimeMikro)
            + ', "enable": true, "tgId": "", "subId": ""}]}',
        }
        origin = server[3].split("/")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": f"{origin[0]}://{origin[2]}",
            "Connection": "keep-alive",
            "Referer": f'{server[3]}/{"panel"if server[4] == "sanaei" else "xui" }/inbounds',
            "Cookie": "",
        }

        async with httpx.AsyncClient() as client:
            print("ARSSSSSSSSSSSSSSSSSSSS")
            response = ""
            try:
                response = await client.post(
                    url=f"{server[3]}/login",
                    data={"username": f"{server[1]}", "password": f"{server[2]}"},
                    timeout=15,
                )
            except:
                response = await client.post(
                    url=f"{server[3]}/login",
                    data={"username": f"{server[1]}", "password": f"{server[2]}"},
                    timeout=15,
                )

            session = response.headers.get("Set-Cookie").split("; ")[0]
            headers["Cookie"] = f"lang=en-US; {session}"
            try:
                response = await client.post(
                    f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',
                    data=data,
                    headers=headers,
                    timeout=15,
                )
            except:
                response = await client.post(
                    f'{server[3]}/{"panel"if server[4]=="sanaei" else "xui" }/inbound/addClient',
                    data=data,
                    headers=headers,
                    timeout=15,
                )

            data = json.loads(response.text)

            if data["success"] == False:

                return {"success": "false", "message": "هنگام ساخت کانفیگ مشکلی پیش آمد"}

            else:
                lastrowId = await db_manager.Query(
                    "INSERT INTO Service(UserId,Email,Password,CreateDate,EndDate,OrderId,PlanId,CatId,ServerIds,configUrl,TransformEnable,RandomId,TypeService,ServiceTest,PhoneNumber) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        0,
                        email,
                        str(uuid),
                        int(datetime.datetime.timestamp(datetime.datetime.now())),
                        endTimeMikro,
                        order[0],
                        order[2],
                        order[11],
                        f"[{server[0]}]",
                        configUrl,
                        Volume,
                        randomId,
                        "single",
                        "empty",
                        order[12],
                    ),
                )

                await db_manager.QueryWidthOutValue(
                    f"UPDATE OrdersList SET State = 1 WHERE Id = {order[0]} "
                )
                countShopUser = await db_manager.execute_query_one(
                    f"SELECT CountShopped FROM Users WHERE PhoneNumber = {order[12]}"
                )

                await db_manager.QueryWidthOutValue(
                    f"UPDATE Users SET CountShopped  = {countShopUser[0] + 1} WHERE PhoneNumber = {order[12]}"
                )
                countShell = await db_manager.execute_query_one(
                    f"SELECT CountSell,ContSold FROM ServerPlans WHERE Id = {order[2]} "
                )

                if countShell[0] - 1 < countShell[1] + 1:
                    await db_manager.QueryWidthOutValue(
                        f"UPDATE ServerPlans SET CountSell = {countShell[0] - 1 }  , ContSold = {countShell[1] + 1 } WHERE Id = {order[2]} "
                    )

                await db_manager.QueryWidthOutValue(
                    f"UPDATE ServerPlans SET CountSell = {countShell[0] - 1 }  , ContSold = {countShell[1] + 1 } WHERE Id = {order[2]} "
                )
                return {"success": "true", "serviceId": lastrowId.lastrowid}
    except:

        return {"success": "false", "message": "هنگام ساخت کانفیگ مشکلی پیش آمد"}


@app.route("/createconfig", methods=["POST"])
async def createconfig():
        print(request.get_json())

        try:
            orderId = request.get_json()
            print('testtttt')
            orderCheck = await db_manager.execute_query_one(
                f"SELECT * FROM OrdersList WHERE Id = {orderId['token']} AND State = 0 "
            )
            if orderCheck != None:
                print('testtttt')
                return await CreateSingle(orderCheck)

            else:
                return {"success": "false", "message": "سفارش پیدا نشد"}

        except:
            return {"success": "false", "message": "سفارش پیدا نشد"}


@app.route("/successpay", methods=["POST"])
async def successpay():

        print(request.get_json())

    
        try:
            orderId = request.get_json()

            orderCheck = await db_manager.execute_query_one(
                f"SELECT * FROM OrdersList WHERE Id = {orderId['token']} AND State = 0 "
            )
            if orderCheck != None:
                print(f"ORDER ID  {orderCheck[0]}")
                await db_manager.Query(
                    "INSERT INTO SendConfOnline(OrderId,Type,UserId) VALUES(?,?,?)",
                    (orderCheck[0], "XG", orderCheck[3]),
                )
                return {"success": "true", "message": "پرداخت تایید شد !"}

            else:
                return {"success": "false", "message": "سفارش پیدا نشد"}

        except:
            return {"success": "false", "message": "سفارش پیدا نشد"}


@app.route("/successpay", methods=["GET"])
async def successpayGet():

    success = request.args.get("success", "ARS")
    if success != "ARS":
        if success == "true":
            return render_template("success.html")
        else:
            return render_template("error.html")

    else:
        return "NOT FOUND"


@app.route("/onlinepay", methods=["GET"])
async def OnlinePayment():
    try:
        token = request.args.get("token", "ARS")
        if token == "ARS":
            return render_template("index.html")

        order = await db_manager.execute_query_one(
            f"SELECT * FROM OrdersList WHERE Id = {token} AND State = 0"
        )

        if order == None:
            return render_template("index.html")
        else:
            # TODO ADD To DataNeed   merchant
            DataNeed = await db_manager.execute_query_one(
                "SELECT SubDomain,PaymentGateway FROM Setting "
            )

            data = json.dumps(
                {
                    "merchant": f"{DataNeed[1]}",
                    "amount": order[6] * 10,
                    "callbackUrl": f"{DataNeed[0]}/CallBackDataZipal",
                    "orderId": f"{order[0]}",
                }
            )
            if order[9] != None:
                data["amount"] = order[9] * 10
            headers = {"Content-Type": "application/json"}
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url="https://gateway.zibal.ir/v1/request",
                    data=data,
                    headers=headers,
                )

                print(response.text)
                dataRes = json.loads(response.text)
                if dataRes["message"] == "success" and dataRes["result"] == 100:

                    return app.redirect(
                        f"https://gateway.zibal.ir/start/{dataRes['trackId']}"
                    )
                else:
                    return render_template("index.html")
    except:

        return render_template("index.html")


@app.route("/pay", methods=["GET"])
async def OnlinePaymentMad():
    try:
        token = request.args.get("token", "ARS")
        if token == "ARS":
            return render_template("index.html")

        order = await db_manager.execute_query_one(
            f"SELECT * FROM OrdersList WHERE Id = {token} AND State = 0"
        )

        if order == None:
            return render_template("index.html")
        else:
            # TODO ADD To DataNeed   merchant
            DataNeed = await db_manager.execute_query_one(
                "SELECT SubDomain,TokenMadPal FROM Setting "
            )
            data = json.dumps(
                {
                    "MerchantID": f"{DataNeed[1]}",
                    "Amount": order[6],
                    "Description": "خرید سرویس",
                    "CallbackURL": f"{DataNeed[0]}/CallBackDataZipal",
                    "InvoiceNumber": f"{order[0]}",
                }
            )
            # "MerchantID=ea02fe3a76151071778ecfd266242466&Amount=12000&Description=dfksdkdjf&InvoiceNumber=12&CardNumber=&CallbackURL=https://alireza.top"
            headers = {"Content-Type": "application/json"}
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url="https://madpal.ir/webservice/paymentRequest.php",
                    data=data,
                    headers=headers,
                )

                print(response.text)
                dataRes = json.loads(response.text)
                if dataRes["message"] == "success" and dataRes["result"] == 100:

                    return app.redirect(
                        f"https://gateway.zibal.ir/start/{dataRes['trackId']}"
                    )
                else:
                    return render_template("index.html")
    except:
        return render_template("index.html")


@app.route("/CallBackDataZipal", methods=["GET"])
async def CallBackDataZipal():
    try:

        success = request.args.get("success", "ARS")
        trackId = request.args.get("trackId", "ARS")
        orderId = request.args.get("orderId", "ARS")
        status = request.args.get("status", "ARS")
        if status == "ARS" or orderId == "ARS" or trackId == "ARS" or success == "ARS":
            return render_template("index.html")
        if status == "2":
            data = json.dumps({"merchant": "zibal", "trackId": trackId})

            headers = {"Content-Type": "application/json"}
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url="https://gateway.zibal.ir/v1/verify", data=data, headers=headers
                )
                print(response.text)
                dataRes = json.loads(response.text)
                if dataRes["message"] == "success" or dataRes["status"] == 1:
                    orderCheck = await db_manager.execute_query_one(
                        f"SELECT * FROM OrdersList WHERE Id = {orderId} AND State = 0 "
                    )
                    if orderCheck != None:
                        await db_manager.Query(
                            "INSERT INTO SendConfOnline(OrderId,Type,UserId) VALUES(?,?,?)",
                            (orderCheck[0], "zibal", orderCheck[3]),
                        )
                        return render_template("success.html")
                    else:
                        return render_template("index.html")
        elif status == "1":
            orderCheck = await db_manager.execute_query_one(
                f"SELECT * FROM SendConfOnline WHERE OrderId = {orderId}  "
            )
            if orderCheck != None:
                return render_template("index.html")
            else:
                orderCheck = await db_manager.execute_query_one(
                    f"SELECT * FROM OrdersList WHERE Id = {orderId} AND State = 0 "
                )
                if orderCheck != None:

                    await db_manager.Query(
                        "INSERT INTO SendConfOnline(OrderId,Type,UserId) VALUES(?,?,?)",
                        (orderCheck[0], "zibal", orderCheck[3]),
                    )
                    return render_template("success.html")
                else:
                    return render_template("index.html")

    except:
        return render_template("index.html")


async def getName(randId,stae):
    chanel = await db_manager.execute_query_one("SELECT LockChanel FROM Setting ")
    vmessConf = {
        "v": "2",
        "ps": f"👑 | K{randId} - @{chanel[0]} • State : {'🟢' if stae == 1 else '🔴'}",
        "add": "127.0.0.1",
        "port": 8321,
        "id": "empty",
        "aid": 0,
        "net": "ws",
        "type": "none",
        "tls": "none",
        "path": "",
        "host": "",
    }
    res = json.dumps(vmessConf)
    res = res[1:]

    res = "{\n" + res.replace("}", "\n}")
    res = res.replace(",", ",\n ")
    sample_string_bytes = res.encode("utf-8")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    newConfig = f"vmess://{base64_string}"
    return newConfig

def getDate(dateStamp):
    dateEnd = datetime.datetime.fromtimestamp(int(dateStamp) / 1000)
    dateCal = dateEnd - datetime.datetime.now()
    vmessConf = {
        "v": "2",
        "ps": f"📅 | {dateCal.days} Days ",
        "add": "127.0.0.1",
        "port": 8321,
        "id": "empty",
        "aid": 0,
        "net": "ws",
        "type": "none",
        "tls": "none",
        "path": "",
        "host": "",
    }
    res = json.dumps(vmessConf)
    res = res[1:]

    res = "{\n" + res.replace("}", "\n}")
    res = res.replace(",", ",\n ")
    sample_string_bytes = res.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    newConfig = f"vmess://{base64_string}"
    return newConfig    

def getTotal(down, up, total):
    usage = (down + up) / 1024 / 1024 / 1024
    vmessConf = {
        "v": "2",
        "ps": f"📊 | {round(usage,2)} GB - {round(total/1024/1024/1024,2)} GB  ",
        "add": "127.0.0.1",
        "port": 8321,
        "id": "empty",
        "aid": 0,
        "net": "ws",
        "type": "none",
        "tls": "none",
        "path": "",
        "host": "",
    }
    res = json.dumps(vmessConf)
    res = res[1:]

    res = "{\n" + res.replace("}", "\n}")
    res = res.replace(",", ",\n ")
    sample_string_bytes = res.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    newConfig = f"vmess://{base64_string}"
    return newConfig





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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run(host="0.0.0.0", port=8383))
