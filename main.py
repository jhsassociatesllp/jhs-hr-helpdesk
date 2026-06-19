

# # # from fastapi import FastAPI, HTTPException, BackgroundTasks
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from pydantic import BaseModel
# # # from pymongo import MongoClient
# # # from datetime import datetime
# # # import smtplib
# # # from email.mime.text import MIMEText
# # # from email.mime.multipart import MIMEMultipart
# # # import logging
# # # from typing import Optional, Dict, Any, List
# # # from fastapi.responses import HTMLResponse
# # # from fastapi.staticfiles import StaticFiles
# # # from dotenv import load_dotenv
# # # import os
# # # from fastapi.responses import FileResponse
# # # from jose import JWTError, jwt
# # # from fastapi import Depends, Header
# # # from datetime import timedelta

# # # load_dotenv()

# # # app = FastAPI(title="JHS HR Helpdesk API")
# # # print("🚀 UPDATED CODE FROM GITHUB RUNNING")

# # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # frontend_path = os.path.join(os.path.dirname(__file__), "static")
# # # @app.get("/favicon.ico", include_in_schema=False)
# # # async def favicon():
# # #     return FileResponse(os.path.join("static", "favicon.ico"))

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )


# # # SECRET_KEY = os.getenv("JWT_SECRET")
# # # ALGORITHM = "HS256"
# # # ACCESS_TOKEN_EXPIRE_MINUTES = 60

# # # client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
# # # print(os.getenv("MONGO_CONNECTION_STRING"))
# # # print("Secret Key: ",SECRET_KEY)
# # # db = client["HR_Helpdesk"]
# # # ticketscol = db["Tickets"]
# # # admins = db["Admins"]

# # # logging.basicConfig(level=logging.INFO)
# # # logger = logging.getLogger(__name__)

# # # SMTP_SERVER = "smtp.gmail.com"
# # # SMTP_PORT = 587
# # # SMTP_USER = os.getenv("SMTP_USER")
# # # SMTP_PASS = os.getenv("SMTP_PASS")
# # # print(f"Email: {SMTP_USER}, Pass: {SMTP_PASS}")
# # # logger.info(f"Email: {SMTP_USER}, Pass: {SMTP_PASS}")

# # # # HR_EMAILS = {
# # # #     'Janhavi Gamare': 'janhavi.gamare@jhsassociatesllp.in', 
# # # #     'Darshan Shah': 'darshan.shah@jhsassociates.in', 
# # # #     'Krutika Shivshivkar': 'krutika.shivshivkar@jhsassociates.in', 
# # # #     'Fiza Kudalkar': 'fiza.kudalkar@jhsassociates.in'
# # # #     # 'Janhavi Gamare': 'vasugadde1100@gmaul.com', 
# # # #     # 'Darshan Shah': 'vasugadde0203@gmail.com', 
# # # #     # 'Krutika Shivshivkar': 'vasugadde1234@gmail.com', 
# # # #     # 'Fiza Kudalkar': 'vasugadde1100@gmail.com'
# # # # }

# # # HR_EMAILS = {
# # #     "PAYSLIP": {
# # #         "name": "Janhavi Gamare",
# # #         "email": "janhavi.gamare@jhsassociatesllp.in"
# # #     },
# # #     "HRMS QUERY": {
# # #         "name": "Janhavi Gamare",
# # #         "email": "janhavi.gamare@jhsassociatesllp.in"
# # #     },
# # #     "ATTENDANCE": {
# # #         "name": "Janhavi Gamare",
# # #         "email": "janhavi.gamare@jhsassociatesllp.in"
# # #     },
# # #     "SALARY QUERY": {
# # #         "name": "Janhavi Gamare",
# # #         "email": "janhavi.gamare@jhsassociatesllp.in"
# # #     },
# # #     "BUDDY REFERRAL": {
# # #         "name": "Krutika Shivshivkar",
# # #         "email": "krutika.shivshivkar@jhsassociates.in"
# # #     },
# # #     "OTHER": {
# # #         "name": "Krutika Shivshivkar",
# # #         "email": "krutika.shivshivkar@jhsassociates.in"
# # #     }
# # # }

# # # class TicketCreate(BaseModel):
# # #     name: str
# # #     email: str
# # #     phone: Optional[str] = None
# # #     empCode: Optional[str] = None
# # #     category: str
# # #     issue: str
    

# # # class TicketUpdate(BaseModel):
# # #     assigned: Optional[str] = None
# # #     status: Optional[str] = None
# # #     hrEmail: Optional[str] = None
# # #     remark: Optional[str] = None  

# # # def get_current_admin(authorization: str = Header(None)):
# # #     if not authorization or not authorization.startswith("Bearer "):
# # #         raise HTTPException(status_code=401, detail="Missing token")

# # #     token = authorization.split(" ")[1]

# # #     try:
# # #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# # #         if payload.get("role") != "admin":
# # #             raise HTTPException(status_code=403, detail="Not authorized")
# # #         return payload
# # #     except JWTError:
# # #         raise HTTPException(status_code=401, detail="Invalid or expired token")


# # # def create_access_token(data: dict):
# # #     print("Creating access token")
# # #     to_encode = data.copy()
# # #     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# # #     to_encode.update({"exp": expire})
# # #     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# # # # ✅ FIXED: Corrected sendemail function
# # # def sendemail(recipients: List[str], subject: str, body: str):
# # #     logger.info(f"🔄 EMAIL ATTEMPT → Recipients: {recipients}, Subject: {subject}")
# # #     try:
# # #         msg = MIMEMultipart()
# # #         msg['From'] = SMTP_USER
# # #         msg['Subject'] = subject
# # #         msg.attach(MIMEText(body, 'plain'))
        
# # #         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
# # #         server.starttls()
# # #         server.login(SMTP_USER, SMTP_PASS)
        
# # #         valid_recipients = [r for r in recipients if r and r.strip()]
# # #         logger.info(f"📧 Valid recipients: {valid_recipients}")
        
# # #         if valid_recipients:
# # #             server.sendmail(SMTP_USER, valid_recipients, msg.as_string())
# # #             logger.info(f"✅ EMAILS SENT → {valid_recipients}")
# # #         else:
# # #             logger.warning("⚠️ No valid recipients")
# # #         server.quit()
# # #     except Exception as e:
# # #         logger.error(f"❌ EMAIL FAILED → {str(e)}")

# # # # @app.post("/api/admin/login")
# # # # async def admin_login(body: Dict[str, Any]):
# # # #     empCode = body.get("empCode")
# # # #     password = body.get("password")
# # # #     if not empCode or not password:
# # # #         raise HTTPException(status_code=400, detail="empCode and password required")
# # # #     admin = admins.find_one({"empCode": empCode.upper()})
# # # #     if not admin or admin.get("password") != password:
# # # #         raise HTTPException(status_code=401, detail="Invalid credentials")
# # # #     return {"message": "Login successful", "empCode": empCode.upper()}

# # # # @app.post("/api/admin/login")
# # # # async def admin_login(body: Dict[str, Any]):
# # # #     empCode = body.get("empCode")
# # # #     password = body.get("password")

# # # #     if not empCode or not password:
# # # #         raise HTTPException(status_code=400, detail="empCode and password required")

# # # #     empCode = empCode.upper().strip()

# # # #     admin = admins.find_one({
# # # #         "empCodes": empCode,      # 🔑 array match
# # # #         "password": password
# # # #     })
# # # #     print(admin)
# # # #     if not admin:
# # # #         raise HTTPException(status_code=401, detail="Invalid credentials")

# # # #     return {
# # # #         "message": "Login successful",
# # # #         "empCode": empCode,
# # # #         "name": admin.get("name")
# # # #     }

# # # from datetime import timedelta

# # # @app.post("/api/admin/login")
# # # async def admin_login(body: Dict[str, Any]):
# # #     empCode = body.get("empCode", "").upper().strip()
# # #     password = body.get("password")

# # #     if not empCode or not password:
# # #         raise HTTPException(status_code=400, detail="empCode and password required")

# # #     admin = admins.find_one({
# # #         "empCodes": empCode,
# # #         "password": password
# # #     })

# # #     if not admin:
# # #         raise HTTPException(status_code=401, detail="Invalid credentials")

# # #     token = create_access_token({
# # #         "sub": empCode,
# # #         "role": "admin",
# # #         "name": admin.get("name")
# # #     })
# # #     print(f"Token: {token}")

# # #     return {
# # #         "access_token": token,
# # #         "token_type": "bearer",
# # #         "name": admin.get("name")
# # #     }

# # # @app.post("/api/admin/register")
# # # async def admin_register(body: Dict[str, Any], admin=Depends(get_current_admin)):
# # #     name = body.get("name")
# # #     empCode = body.get("empCode")
# # #     password = body.get("password")
# # #     if not all([name, empCode, password]):
# # #         raise HTTPException(status_code=400, detail="Name, empCode, and password required")
# # #     if admins.find_one({"empCode": empCode.upper()}):
# # #         raise HTTPException(status_code=400, detail="Admin already exists")
# # #     admins.insert_one({
# # #         "empCode": empCode.upper(),
# # #         "password": password,
# # #         "name": name,
# # #         "createdAt": datetime.utcnow()
# # #     })
# # #     return {"message": f"Admin {empCode} registered successfully"}

# # # @app.get("/api/tickets")
# # # async def get_tickets(admin=Depends(get_current_admin)):
# # #     return list(ticketscol.find({}, {"_id": 0}).sort("createdAt", -1))

# # # # @app.post("/api/tickets")
# # # # async def create_ticket(ticket: TicketCreate, background_tasks: BackgroundTasks):
# # # #     count = ticketscol.count_documents({})
# # # #     ticket_id = f"TICKJHSHR{str(count + 1).zfill(2)}"
    
# # # #     ticket_data = {
# # # #         "id": ticket_id, "name": ticket.name, "email": ticket.email,
# # # #         "phone": ticket.phone, "empCode": ticket.empCode,
# # # #         "category": ticket.category, "issue": ticket.issue,
# # # #         "status": "Open", "assigned": "Unassigned", "hrEmail": None,
# # # #         "createdAt": datetime.utcnow(),
# # # #         "remark": ""  # optional but clean

# # # #     }
    
# # # #     ticketscol.insert_one(ticket_data)
    
# # # #     user_subject = f"JHS HR - Ticket {ticket_id} Created"
# # # #     user_body = f"Dear {ticket.name},\n\nTicket {ticket_id} created successfully.\nCategory: {ticket.category}\nIssue: {ticket.issue}\n\nHR will contact you soon.\n\nJHS HR Team"
    
# # # #     hr_subject = f"New HR Ticket: {ticket_id}"
# # # #     hr_body = f"New ticket {ticket_id}\nUser: {ticket.name} ({ticket.email})\nIssue: {ticket.issue}"
    
# # # #     background_tasks.add_task(sendemail, [ticket.email], user_subject, user_body)
# # # #     background_tasks.add_task(sendemail, list(HR_EMAILS.values()), hr_subject, hr_body)
    
# # # #     return {"message": f"Ticket {ticket_id} created", "ticketId": ticket_id}

# # # @app.post("/api/tickets")
# # # async def create_ticket(ticket: TicketCreate, background_tasks: BackgroundTasks):

# # #     count = ticketscol.count_documents({})
# # #     ticket_id = f"TICKJHSHR{str(count + 1).zfill(2)}"

# # #     category = ticket.category.upper().strip()

# # #     hr_data = HR_EMAILS.get(category)

# # #     assigned_name = hr_data["name"] if hr_data else "Unassigned"
# # #     assigned_email = hr_data["email"] if hr_data else None

# # #     ticket_data = {
# # #         "id": ticket_id,
# # #         "name": ticket.name,
# # #         "email": ticket.email,
# # #         "phone": ticket.phone,
# # #         "empCode": ticket.empCode,
# # #         "category": ticket.category,
# # #         "issue": ticket.issue,
# # #         "status": "Open",
# # #         "assigned": assigned_name,
# # #         "hrEmail": assigned_email,
# # #         "assignedAt": datetime.utcnow() if hr_data else None,
# # #         "createdAt": datetime.utcnow(),
# # #         "remark": ""
# # #     }

# # #     ticketscol.insert_one(ticket_data)

# # #     # 📧 User Email
# # #     background_tasks.add_task(
# # #         sendemail,
# # #         [ticket.email],
# # #         f"JHS HR - Ticket {ticket_id} Created",
# # #         f"""Dear {ticket.name},

# # # Your ticket {ticket_id} has been created successfully.

# # # Category: {ticket.category}
# # # Assigned HR: {assigned_name}

# # # JHS HR Team"""
# # #     )

# # #     # 📧 HR Email (ONLY assigned HR)
# # #     if assigned_email:
# # #         background_tasks.add_task(
# # #             sendemail,
# # #             [assigned_email],
# # #             f"New Ticket Assigned: {ticket_id}",
# # #             f"""Dear {assigned_name},

# # # A new ticket has been assigned to you.

# # # Ticket ID: {ticket_id}
# # # Employee: {ticket.name}
# # # Issue: {ticket.issue}"""
# # #         )

# # #     return {
# # #         "message": "Ticket created & auto-assigned",
# # #         "ticketId": ticket_id,
# # #         "assignedTo": assigned_name
# # #     }


# # # # @app.put("/api/tickets/{ticketid}")
# # # # async def update_ticket(ticketid: str, body: TicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# # # #     ticket = ticketscol.find_one({"id": ticketid})
# # # #     if not ticket: 
# # # #         raise HTTPException(404, "Ticket not found")
    
# # # #     logger.info(f"🔄 UPDATE → Ticket: {ticketid}, Body: {body}")
    
# # # #     update_data = {}
# # # #     old_assigned = ticket.get("assigned")
# # # #     if body.assigned and body.assigned != old_assigned:
# # # #         update_data["assigned"] = body.assigned
# # # #         update_data["assignedAt"] = datetime.utcnow()
# # # #         if body.hrEmail: 
# # # #             update_data["hrEmail"] = body.hrEmail
    
# # # #     if body.status and body.status.lower() == "closed" and ticket.get("status", "").lower() != "closed":
# # # #         update_data["status"] = "Closed"
# # # #         update_data["closedAt"] = datetime.utcnow()
# # # #         update_data["remark"] = body.remark   # ✅ ADD THIS
    
# # # #     if update_data:
# # # #         ticketscol.update_one({"id": ticketid}, {"$set": update_data})
    
# # # #     user_email = ticket.get("email")
# # # #     user_name = ticket.get("name")
# # # #     assigned_hr_name = body.assigned or ticket.get("assigned", "Unassigned")
# # # #     assigned_hr_email = HR_EMAILS.get(assigned_hr_name) if assigned_hr_name != "Unassigned" else None
    
# # # #     # Assignment emails
# # # #     if body.assigned and body.assigned != old_assigned and assigned_hr_email:
# # # #         background_tasks.add_task(sendemail, [user_email], 
# # # #             f"JHS Ticket {ticketid} Assigned to {assigned_hr_name}",
# # # #             f"Dear {user_name},\n\nTicket {ticketid} assigned to {assigned_hr_name}.")
# # # #         background_tasks.add_task(sendemail, [assigned_hr_email], 
# # # #             f"New Assignment: Ticket {ticketid}",
# # # #             f"Dear {assigned_hr_name},\n\nTicket {ticketid} assigned to you.\nUser: {user_name}")
    
# # # #     # Close emails
# # # #     if body.status and body.status.lower() == "closed":
# # # #         if assigned_hr_email:
# # # #             background_tasks.add_task(sendemail, [user_email], 
# # # #                 f"JHS Ticket {ticketid} - CLOSED",
# # # #                 f"Dear {user_name},\n\nTicket {ticketid} closed.")
# # # #             background_tasks.add_task(sendemail, [assigned_hr_email], 
# # # #                 f"Ticket {ticketid} - CLOSED",
# # # #                 f"Dear {assigned_hr_name},\n\nTicket {ticketid} marked CLOSED.")
# # # #         else:
# # # #             background_tasks.add_task(sendemail, [user_email], 
# # # #                 f"JHS Ticket {ticketid} - CLOSED",
# # # #                 f"Dear {user_name},\n\nTicket {ticketid} closed.")
    
# # # #     return {"message": "Updated", "ticketId": ticketid}

# # # @app.put("/api/tickets/{ticketid}")
# # # async def update_ticket(
# # #     ticketid: str, 
# # #     body: TicketUpdate, 
# # #     background_tasks: BackgroundTasks, 
# # #     admin=Depends(get_current_admin)
# # # ):
# # #     ticket = ticketscol.find_one({"id": ticketid})
# # #     if not ticket: 
# # #         raise HTTPException(404, "Ticket not found")
    
# # #     logger.info(f"🔄 UPDATE → Ticket: {ticketid}, Body: {body}")
    
# # #     update_data = {}
# # #     old_assigned = ticket.get("assigned")

# # #     # ✅ Handle assignment changes
# # #     if body.assigned and body.assigned != old_assigned:
# # #         update_data["assigned"] = body.assigned
# # #         update_data["assignedAt"] = datetime.utcnow()
# # #         if body.hrEmail: 
# # #             update_data["hrEmail"] = body.hrEmail
    
# # #     # ✅ Handle status change to CLOSED
# # #     if body.status and body.status.lower() == "closed" and ticket.get("status", "").lower() != "closed":
# # #         update_data["status"] = "Closed"
# # #         update_data["closedAt"] = datetime.utcnow()
# # #         update_data["remark"] = body.remark   # ✅ Add remark
    
# # #     if update_data:
# # #         ticketscol.update_one({"id": ticketid}, {"$set": update_data})
    
# # #     # ✅ Emails setup
# # #     user_email = ticket.get("email")
# # #     user_name = ticket.get("name")
# # #     assigned_hr_name = body.assigned or ticket.get("assigned", "Unassigned")
    
# # #     # 🔹 Lookup HR email by name
# # #     assigned_hr_email = None
# # #     for data in HR_EMAILS.values():
# # #         if data["name"] == assigned_hr_name:
# # #             assigned_hr_email = data["email"]
# # #             break
    
# # #     # ✅ Assignment emails
# # #     if body.assigned and body.assigned != old_assigned and assigned_hr_email:
# # #         background_tasks.add_task(
# # #             sendemail, 
# # #             [user_email], 
# # #             f"JHS Ticket {ticketid} Assigned to {assigned_hr_name}",
# # #             f"Dear {user_name},\n\nTicket {ticketid} assigned to {assigned_hr_name}."
# # #         )
# # #         background_tasks.add_task(
# # #             sendemail, 
# # #             [assigned_hr_email], 
# # #             f"New Assignment: Ticket {ticketid}",
# # #             f"Dear {assigned_hr_name},\n\nTicket {ticketid} assigned to you.\nUser: {user_name}"
# # #         )
    
# # #     # ✅ Close emails with remark included
# # #     if body.status and body.status.lower() == "closed":
# # #         remark_text = f"\nRemark: {body.remark}" if body.remark else ""
        
# # #         if assigned_hr_email:
# # #             background_tasks.add_task(
# # #                 sendemail, 
# # #                 [user_email], 
# # #                 f"JHS Ticket {ticketid} - CLOSED",
# # #                 f"Dear {user_name},\n\nTicket {ticketid} closed.{remark_text}"
# # #             )
# # #             background_tasks.add_task(
# # #                 sendemail, 
# # #                 [assigned_hr_email], 
# # #                 f"Ticket {ticketid} - CLOSED",
# # #                 f"Dear {assigned_hr_name},\n\nTicket {ticketid} marked CLOSED.{remark_text}"
# # #             )
# # #         else:
# # #             background_tasks.add_task(
# # #                 sendemail, 
# # #                 [user_email], 
# # #                 f"JHS Ticket {ticketid} - CLOSED",
# # #                 f"Dear {user_name},\n\nTicket {ticketid} closed.{remark_text}"
# # #             )
    
# # #     return {"message": "Updated", "ticketId": ticketid}


# # # @app.delete("/api/tickets/{ticketid}")
# # # async def delete_ticket(ticketid: str, admin=Depends(get_current_admin)):
# # #     result = ticketscol.delete_one({"id": ticketid})
# # #     if result.deleted_count == 0: raise HTTPException(404, "Ticket not found")
# # #     return {"message": "Deleted"}

# # # # @app.get("/api/tickets/stats")
# # # # async def get_tickets_stats():
# # # #     tickets = list(ticketscol.find({}, {"_id": 0}))
# # # #     stats = {"total": len(tickets), "bystatus": {}, "byhr": {}}
    
# # # #     for t in tickets:
# # # #         status = t.get("status", "Open")
# # # #         hr = t.get("assigned", "Unassigned")
# # # #         stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
# # # #         if hr not in stats["byhr"]:
# # # #             stats["byhr"][hr] = {"Open": 0, "Closed": 0}
# # # #         stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
# # # #     return stats

# # # @app.get("/api/admin/stats")
# # # async def get_admin_stats(current_admin: dict = Depends(get_current_admin)):
# # #     tickets = list(ticketscol.find({}, {"_id": 0}))

# # #     stats = {
# # #         "total": len(tickets),
# # #         "bystatus": {"Open": 0, "Closed": 0},
# # #         "byhr": {}
# # #     }

# # #     for t in tickets:
# # #         status = t.get("status", "Open")
# # #         hr = t.get("assigned", "Unassigned")

# # #         stats["bystatus"][status] += 1

# # #         if hr not in stats["byhr"]:
# # #             stats["byhr"][hr] = {"Open": 0, "Closed": 0}

# # #         stats["byhr"][hr][status] += 1

# # #     return stats


# # # @app.get("/api/tickets/{ticketid}")
# # # async def get_ticket(ticketid: str, admin=Depends(get_current_admin)):
# # #     ticket = ticketscol.find_one({"id": ticketid})
# # #     if not ticket: raise HTTPException(404, "Ticket not found")
# # #     ticket.pop("_id", None)
# # #     return ticket

# # # @app.get("/test-email")
# # # async def test_email(background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# # #     background_tasks.add_task(sendemail, ["your-email@gmail.com"], "JHS HR TEST", "Working!")
# # #     return {"status": "Test sent - check console"}

# # # # @app.get("/", response_class=HTMLResponse)
# # # # async def read_root():
# # # #     with open("static/index.html", "r", encoding="utf-8") as f:
# # # #         return f.read()


# # # @app.get("/", response_class=HTMLResponse)
# # # async def read_root():
# # #     return FileResponse("static/index.html")

# # # @app.get("/admin", response_class=FileResponse)
# # # async def admin_page():
# # #     return FileResponse(os.path.join(frontend_path, "admin.html"))

# # # @app.get("/adminlogin", response_class=HTMLResponse)
# # # async def admin_login_page():
# # #     with open("static/adminlogin.html", "r", encoding="utf-8") as f:
# # #         return f.read()


# # # # if __name__ == "__main__":
# # # #     import uvicorn
# # # #     uvicorn.run(app, host="0.0.0.0", port=8000)


# # # @app.get("/.well-known/{path:path}")
# # # async def ignore_well_known(path: str):
# # #     return {}




# # from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import HTMLResponse, FileResponse
# # from fastapi.staticfiles import StaticFiles
# # from pydantic import BaseModel
# # from pymongo import MongoClient
# # from datetime import datetime, timedelta
# # from typing import Optional, Dict, Any, List
# # from dotenv import load_dotenv
# # import os
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # import logging
# # from jose import JWTError, jwt

# # # Load environment
# # load_dotenv()

# # # FastAPI app
# # app = FastAPI(title="JHS HR Helpdesk API")
# # print("🚀 JHS HR Helpdesk API Running")

# # # Mount static files (handles favicon automatically)
# # app.mount("/static", StaticFiles(directory="static"), name="static")

# # # CORS middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Config
# # SECRET_KEY = os.getenv("JWT_SECRET")
# # ALGORITHM = "HS256"
# # ACCESS_TOKEN_EXPIRE_MINUTES = 60

# # SMTP_SERVER = "smtp.gmail.com"
# # SMTP_PORT = 587
# # SMTP_USER = os.getenv("SMTP_USER")
# # SMTP_PASS = os.getenv("SMTP_PASS")

# # # Database
# # client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
# # db = client["HR_Helpdesk"]
# # ticketscol = db["Tickets"]
# # admins = db["Admins"]

# # # Logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # # HR Email Mapping
# # HR_EMAILS = {
# #     "PAYSLIP": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "HRMS QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "ATTENDANCE": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "SALARY QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "BUDDY REFERRAL": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"},
# #     "OTHER": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"}
# # }

# # # Pydantic Models
# # class TicketCreate(BaseModel):
# #     name: str
# #     email: str
# #     phone: Optional[str] = None
# #     empCode: Optional[str] = None
# #     category: str
# #     issue: str

# # class TicketUpdate(BaseModel):
# #     assigned: Optional[str] = None
# #     status: Optional[str] = None
# #     hrEmail: Optional[str] = None
# #     remark: Optional[str] = None

# # # JWT Functions
# # def get_current_admin(authorization: str = Header(None)):
# #     if not authorization or not authorization.startswith("Bearer "):
# #         raise HTTPException(status_code=401, detail="Missing token")
    
# #     token = authorization.split(" ")[1]
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         if payload.get("role") != "admin":
# #             raise HTTPException(status_code=403, detail="Not authorized")
# #         return payload
# #     except JWTError:
# #         raise HTTPException(status_code=401, detail="Invalid or expired token")

# # def create_access_token(data: dict):
# #     to_encode = data.copy()
# #     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# #     to_encode.update({"exp": expire})
# #     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # # Email Function
# # def sendemail(recipients: List[str], subject: str, body: str):
# #     logger.info(f"🔄 EMAIL → {recipients}, {subject}")
# #     try:
# #         msg = MIMEMultipart()
# #         msg['From'] = SMTP_USER
# #         msg['Subject'] = subject
# #         msg.attach(MIMEText(body, 'plain'))
        
# #         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
# #         server.starttls()
# #         server.login(SMTP_USER, SMTP_PASS)
        
# #         valid_recipients = [r for r in recipients if r and r.strip()]
# #         if valid_recipients:
# #             server.sendmail(SMTP_USER, valid_recipients, msg.as_string())
# #             logger.info(f"✅ EMAILS SENT → {valid_recipients}")
# #         server.quit()
# #     except Exception as e:
# #         logger.error(f"❌ EMAIL FAILED → {str(e)}")

# # # API Routes
# # @app.post("/api/admin/login")
# # async def admin_login(body: Dict[str, Any]):
# #     empCode = body.get("empCode", "").upper().strip()
# #     password = body.get("password")
    
# #     if not empCode or not password:
# #         raise HTTPException(status_code=400, detail="empCode and password required")
    
# #     admin = admins.find_one({"empCodes": empCode, "password": password})
# #     if not admin:
# #         raise HTTPException(status_code=401, detail="Invalid credentials")
    
# #     token = create_access_token({
# #         "sub": empCode,
# #         "role": "admin",
# #         "name": admin.get("name")
# #     })
    
# #     return {
# #         "access_token": token,
# #         "token_type": "bearer",
# #         "name": admin.get("name")
# #     }

# # @app.post("/api/admin/register")
# # async def admin_register(body: Dict[str, Any], admin=Depends(get_current_admin)):
# #     name = body.get("name")
# #     empCode = body.get("empCode")
# #     password = body.get("password")
# #     if not all([name, empCode, password]):
# #         raise HTTPException(status_code=400, detail="Name, empCode, and password required")
# #     if admins.find_one({"empCode": empCode.upper()}):
# #         raise HTTPException(status_code=400, detail="Admin already exists")
# #     admins.insert_one({
# #         "empCode": empCode.upper(),
# #         "password": password,
# #         "name": name,
# #         "createdAt": datetime.utcnow()
# #     })
# #     return {"message": f"Admin {empCode} registered successfully"}

# # @app.get("/api/tickets")
# # async def get_tickets(admin=Depends(get_current_admin)):
# #     return list(ticketscol.find({}, {"_id": 0}).sort("createdAt", -1))

# # @app.post("/api/tickets")
# # async def create_ticket(ticket: TicketCreate, background_tasks: BackgroundTasks):
# #     count = ticketscol.count_documents({})
# #     ticket_id = f"TICKJHSHR{str(count + 1).zfill(2)}"
    
# #     category = ticket.category.upper().strip()
# #     hr_data = HR_EMAILS.get(category)
# #     assigned_name = hr_data["name"] if hr_data else "Unassigned"
# #     assigned_email = hr_data["email"] if hr_data else None
    
# #     ticket_data = {
# #         "id": ticket_id, "name": ticket.name, "email": ticket.email,
# #         "phone": ticket.phone, "empCode": ticket.empCode,
# #         "category": ticket.category, "issue": ticket.issue,
# #         "status": "Open", "assigned": assigned_name, "hrEmail": assigned_email,
# #         "assignedAt": datetime.utcnow() if hr_data else None,
# #         "createdAt": datetime.utcnow(), "remark": ""
# #     }
    
# #     ticketscol.insert_one(ticket_data)
    
# #     # User email
# #     background_tasks.add_task(
# #         sendemail, [ticket.email],
# #         f"JHS HR - Ticket {ticket_id} Created",
# #         f"Dear {ticket.name},\n\nYour ticket {ticket_id} created.\nCategory: {ticket.category}\nAssigned: {assigned_name}\n\nJHS HR Team"
# #     )
    
# #     # HR email
# #     if assigned_email:
# #         background_tasks.add_task(
# #             sendemail, [assigned_email],
# #             f"New Ticket: {ticket_id}",
# #             f"Dear {assigned_name},\n\nTicket {ticket_id} assigned to you.\nEmployee: {ticket.name}\nIssue: {ticket.issue}"
# #         )
    
# #     return {"message": "Ticket created", "ticketId": ticket_id, "assignedTo": assigned_name}

# # @app.put("/api/tickets/{ticketid}")
# # async def update_ticket(ticketid: str, body: TicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     ticket = ticketscol.find_one({"id": ticketid})
# #     if not ticket: 
# #         raise HTTPException(404, "Ticket not found")
    
# #     update_data = {}
# #     old_assigned = ticket.get("assigned")
    
# #     if body.assigned and body.assigned != old_assigned:
# #         update_data["assigned"] = body.assigned
# #         update_data["assignedAt"] = datetime.utcnow()
# #         if body.hrEmail: 
# #             update_data["hrEmail"] = body.hrEmail
    
# #     if body.status and body.status.lower() == "closed" and ticket.get("status", "").lower() != "closed":
# #         update_data["status"] = "Closed"
# #         update_data["closedAt"] = datetime.utcnow()
# #         update_data["remark"] = body.remark
    
# #     if update_data:
# #         ticketscol.update_one({"id": ticketid}, {"$set": update_data})
    
# #     # Send emails
# #     user_email = ticket.get("email")
# #     user_name = ticket.get("name")
# #     assigned_hr_name = body.assigned or ticket.get("assigned", "Unassigned")
    
# #     # Find HR email
# #     assigned_hr_email = None
# #     for data in HR_EMAILS.values():
# #         if data["name"] == assigned_hr_name:
# #             assigned_hr_email = data["email"]
# #             break
    
# #     # Assignment emails
# #     if body.assigned and body.assigned != old_assigned and assigned_hr_email:
# #         background_tasks.add_task(sendemail, [user_email], 
# #             f"Ticket {ticketid} assigned to {assigned_hr_name}",
# #             f"Dear {user_name},\n\nTicket {ticketid} assigned to {assigned_hr_name}.")
# #         background_tasks.add_task(sendemail, [assigned_hr_email], 
# #             f"New Assignment: {ticketid}",
# #             f"Dear {assigned_hr_name},\n\nTicket {ticketid} assigned to you.\nUser: {user_name}")
    
# #     # Close emails
# #     if body.status and body.status.lower() == "closed":
# #         remark_text = f"\nRemark: {body.remark}" if body.remark else ""
# #         if assigned_hr_email:
# #             background_tasks.add_task(sendemail, [user_email], 
# #                 f"Ticket {ticketid} - CLOSED", f"Dear {user_name},\n\nTicket closed.{remark_text}")
# #             background_tasks.add_task(sendemail, [assigned_hr_email], 
# #                 f"Ticket {ticketid} - CLOSED", f"Dear {assigned_hr_name},\n\nTicket marked CLOSED.{remark_text}")
# #         else:
# #             background_tasks.add_task(sendemail, [user_email], 
# #                 f"Ticket {ticketid} - CLOSED", f"Dear {user_name},\n\nTicket closed.{remark_text}")
    
# #     return {"message": "Updated", "ticketId": ticketid}

# # @app.delete("/api/tickets/{ticketid}")
# # async def delete_ticket(ticketid: str, admin=Depends(get_current_admin)):
# #     result = ticketscol.delete_one({"id": ticketid})
# #     if result.deleted_count == 0: 
# #         raise HTTPException(404, "Ticket not found")
# #     return {"message": "Deleted"}

# # @app.get("/api/admin/stats")
# # async def get_admin_stats(admin=Depends(get_current_admin)):
# #     tickets = list(ticketscol.find({}, {"_id": 0}))
# #     stats = {"total": len(tickets), "bystatus": {"Open": 0, "Closed": 0}, "byhr": {}}
    
# #     for t in tickets:
# #         status = t.get("status", "Open")
# #         hr = t.get("assigned", "Unassigned")
# #         stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
# #         if hr not in stats["byhr"]:
# #             stats["byhr"][hr] = {"Open": 0, "Closed": 0}
# #         stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
# #     return stats

# # @app.get("/api/tickets/{ticketid}")
# # async def get_ticket(ticketid: str, admin=Depends(get_current_admin)):
# #     ticket = ticketscol.find_one({"id": ticketid})
# #     if not ticket: 
# #         raise HTTPException(404, "Ticket not found")
# #     ticket.pop("_id", None)
# #     return ticket

# # # Frontend Routes
# # @app.get("/", response_class=HTMLResponse)
# # async def read_root():
# #     return FileResponse("static/index.html")

# # @app.get("/admin", response_class=FileResponse)
# # async def admin_page():
# #     return FileResponse("static/admin.html")

# # @app.get("/adminlogin", response_class=HTMLResponse)
# # async def admin_login_page():
# #     with open("static/adminlogin.html", "r", encoding="utf-8") as f:
# #         return f.read()

# # @app.get("/test-email")
# # async def test_email(background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     background_tasks.add_task(sendemail, ["test@example.com"], "JHS HR TEST", "Working!")
# #     return {"status": "Test email queued"}

# # @app.get("/.well-known/{path:path}")
# # async def ignore_well_known(path: str):
# #     return {}




# # from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import HTMLResponse, FileResponse
# # from fastapi.staticfiles import StaticFiles
# # from pydantic import BaseModel, EmailStr
# # from pymongo import MongoClient
# # from datetime import datetime, timedelta
# # from typing import Optional, Dict, Any, List
# # from dotenv import load_dotenv
# # import os
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # import logging
# # import hashlib
# # from jose import JWTError, jwt

# # # Load environment
# # load_dotenv()

# # # FastAPI app
# # app = FastAPI(title="JHS Unified Helpdesk API")
# # print("🚀 JHS Unified Helpdesk API Running")

# # # Mount static files
# # app.mount("/static", StaticFiles(directory="static"), name="static")

# # # CORS middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Config
# # SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
# # ALGORITHM = "HS256"
# # ACCESS_TOKEN_EXPIRE_MINUTES = 60

# # SMTP_SERVER = "smtp.gmail.com"
# # SMTP_PORT = 587
# # SMTP_USER = os.getenv("SMTP_USER")
# # SMTP_PASS = os.getenv("SMTP_PASS")

# # # Database connections
# # client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

# # # HR Database
# # hr_db = client["HR_Helpdesk"]
# # hr_tickets = hr_db["Tickets"]
# # hr_admins = hr_db["Admins"]

# # # IT Database
# # it_db = client["ithelpdesk"]
# # it_tickets = it_db["tickets"]
# # it_admins = it_db["admins"]
# # it_sessions = it_db["sessions"]
# # it_sequences = it_db["sequences"]

# # # Logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # # HR Email Mapping
# # HR_EMAILS = {
# #     "PAYSLIP": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "HRMS QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "ATTENDANCE": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "SALARY QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "BUDDY REFERRAL": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"},
# #     "OTHER": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"}
# # }

# # # IT Email list
# # IT_EMAILS = ["orinaguha9@gmail.com", "it2@jhs.co.in", "it3@jhs.co.in"]

# # # ==================== PYDANTIC MODELS ====================

# # # HR Models
# # class HRTicketCreate(BaseModel):
# #     name: str
# #     email: str
# #     phone: Optional[str] = None
# #     empCode: Optional[str] = None
# #     category: str
# #     issue: str

# # class HRTicketUpdate(BaseModel):
# #     assigned: Optional[str] = None
# #     status: Optional[str] = None
# #     hrEmail: Optional[str] = None
# #     remark: Optional[str] = None

# # # IT Models
# # # class ITTicketCreate(BaseModel):
# # #     name: str
# # #     email: EmailStr
# # #     phone: Optional[str] = None
# # #     empCode: Optional[str] = None
# # #     assetCode: str
# # #     issues: List[str]
# # #     issueDescription: str
# # #     reportingPartner: str

# # # class ITTicketUpdate(BaseModel):
# # #     assigned: Optional[str] = None
# # #     status: Optional[str] = None
# # #     itEmail: Optional[EmailStr] = None
# # #     remark: Optional[str] = None

# # # IT Models
# # class ITTicketCreate(BaseModel):
# #     name: str
# #     email: EmailStr
# #     phone: str  # Required
# #     assetCode: Optional[str] = ""  # Made optional
# #     empCode: Optional[str] = ""  # Optional
# #     issues: List[str]  # Required list
# #     issueDescription: str  # Required
# #     reportingPartner: str  # Required

# # class ITTicketUpdate(BaseModel):
# #     assigned: Optional[str] = None
# #     status: Optional[str] = None
# #     itEmail: Optional[EmailStr] = None
# #     remark: Optional[str] = None

# # class AdminLogin(BaseModel):
# #     empCode: str
# #     password: str

# # # ==================== UTILITY FUNCTIONS ====================

# # def hash_password(password: str) -> str:
# #     """Hash password using SHA256"""
# #     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# # def verify_password(plain: str, hashed: str) -> bool:
# #     """Verify password against hash"""
# #     return hash_password(plain) == hashed

# # def create_access_token(data: dict):
# #     """Create JWT access token"""
# #     to_encode = data.copy()
# #     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# #     to_encode.update({"exp": expire})
# #     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # def get_current_admin(authorization: str = Header(None)):
# #     """Verify JWT token and return admin info"""
# #     if not authorization or not authorization.startswith("Bearer "):
# #         raise HTTPException(status_code=401, detail="Missing token")
    
# #     token = authorization.split(" ")[1]
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         if payload.get("role") != "admin":
# #             raise HTTPException(status_code=403, detail="Not authorized")
# #         return payload
# #     except JWTError:
# #         raise HTTPException(status_code=401, detail="Invalid or expired token")

# # def sendemail(recipients: List[str], subject: str, body: str):
# #     """Send email to recipients"""
# #     logger.info(f"🔄 EMAIL → {recipients}, {subject}")
# #     try:
# #         msg = MIMEMultipart()
# #         msg['From'] = SMTP_USER
# #         msg['Subject'] = subject
# #         msg.attach(MIMEText(body, 'html'))
        
# #         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
# #         server.starttls()
# #         server.login(SMTP_USER, SMTP_PASS)
        
# #         valid_recipients = [r for r in recipients if r and r.strip()]
# #         if valid_recipients:
# #             server.sendmail(SMTP_USER, valid_recipients, msg.as_string())
# #             logger.info(f"✅ EMAILS SENT → {valid_recipients}")
# #         server.quit()
# #     except Exception as e:
# #         logger.error(f"❌ EMAIL FAILED → {str(e)}")

# # # ==================== AUTHENTICATION ROUTES ====================

# # @app.post("/api/admin/login")
# # async def unified_admin_login(body: AdminLogin):
# #     """
# #     Unified login endpoint for both HR and IT admins.
# #     First checks HR admins, then IT admins.
# #     """
# #     empCode = body.empCode.upper().strip()
# #     password = body.password
    
# #     if not empCode or not password:
# #         raise HTTPException(status_code=400, detail="empCode and password required")
    
# #     logger.info(f"Login attempt for empCode: {empCode}")
    
# #     # Try HR admin first
# #     hr_admin = hr_admins.find_one({"empCodes": empCode, "password": password})
    
# #     if hr_admin:
# #         logger.info(f"HR Admin found: {hr_admin.get('name')}")
# #         token = create_access_token({
# #             "sub": empCode,
# #             "role": "admin",
# #             "type": "hr",
# #             "name": hr_admin.get("name")
# #         })
        
# #         return {
# #             "access_token": token,
# #             "token_type": "bearer",
# #             "name": hr_admin.get("name"),
# #             "helpdesk": "hr"
# #         }
    
# #     # Try IT admin
# #     it_admin = it_admins.find_one({"empCode": empCode})
    
# #     if it_admin:
# #         logger.info(f"IT Admin found: {it_admin.get('name')}")
        
# #         # Verify password
# #         if not verify_password(password, it_admin["password"]):
# #             logger.error("Password verification failed")
# #             raise HTTPException(status_code=401, detail="Invalid password")
        
# #         logger.info("Password verified successfully")
        
# #         token = create_access_token({
# #             "sub": empCode,
# #             "role": "admin",
# #             "type": "it",
# #             "name": it_admin.get("name")
# #         })
        
# #         # Store session in IT sessions collection
# #         session_doc = {
# #             "empCode": empCode,
# #             "token": token,
# #             "isValid": True,
# #             "createdAt": datetime.utcnow(),
# #             "expiresAt": datetime.utcnow() + timedelta(hours=1)
# #         }
        
# #         it_sessions.update_one(
# #             {"empCode": empCode},
# #             {"$set": session_doc},
# #             upsert=True
# #         )
        
# #         logger.info(f"Login successful for IT admin {empCode}")
        
# #         return {
# #             "access_token": token,
# #             "token": token,  # For backward compatibility
# #             "token_type": "bearer",
# #             "empCode": empCode,
# #             "name": it_admin.get("name"),
# #             "helpdesk": "it"
# #         }
    
# #     # No admin found
# #     logger.error(f"Admin not found for empCode: {empCode}")
# #     raise HTTPException(status_code=401, detail="Invalid credentials")

# # # ==================== HR TICKET ROUTES ====================

# # @app.get("/api/tickets")
# # async def get_hr_tickets(admin=Depends(get_current_admin)):
# #     """Get all HR tickets"""
# #     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# # @app.post("/api/tickets")
# # async def create_hr_ticket(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
# #     """Create new HR ticket"""
# #     count = hr_tickets.count_documents({})
# #     ticket_id = f"TICKJHSHR{str(count + 1).zfill(2)}"
    
# #     category = ticket.category.upper().strip()
# #     hr_data = HR_EMAILS.get(category)
# #     assigned_name = hr_data["name"] if hr_data else "Unassigned"
# #     assigned_email = hr_data["email"] if hr_data else None
    
# #     ticket_data = {
# #         "id": ticket_id, "name": ticket.name, "email": ticket.email,
# #         "phone": ticket.phone, "empCode": ticket.empCode,
# #         "category": ticket.category, "issue": ticket.issue,
# #         "status": "Open", "assigned": assigned_name, "hrEmail": assigned_email,
# #         "assignedAt": datetime.utcnow() if hr_data else None,
# #         "createdAt": datetime.utcnow(), "remark": ""
# #     }
    
# #     hr_tickets.insert_one(ticket_data)
    
# #     # Send emails
# #     background_tasks.add_task(
# #         sendemail, [ticket.email],
# #         f"JHS HR - Ticket {ticket_id} Created",
# #         f"<p>Dear {ticket.name},</p><p>Your ticket {ticket_id} created.</p><p>Category: {ticket.category}<br>Assigned: {assigned_name}</p><p>JHS HR Team</p>"
# #     )
    
# #     if assigned_email:
# #         background_tasks.add_task(
# #             sendemail, [assigned_email],
# #             f"New Ticket: {ticket_id}",
# #             f"<p>Dear {assigned_name},</p><p>Ticket {ticket_id} assigned to you.</p><p>Employee: {ticket.name}<br>Issue: {ticket.issue}</p>"
# #         )
    
# #     return {"message": "Ticket created", "ticketId": ticket_id, "assignedTo": assigned_name}

# # @app.put("/api/tickets/{ticketid}")
# # async def update_hr_ticket(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     """Update HR ticket"""
# #     ticket = hr_tickets.find_one({"id": ticketid})
# #     if not ticket: 
# #         raise HTTPException(404, "Ticket not found")
    
# #     update_data = {}
# #     old_assigned = ticket.get("assigned")
    
# #     if body.assigned and body.assigned != old_assigned:
# #         update_data["assigned"] = body.assigned
# #         update_data["assignedAt"] = datetime.utcnow()
# #         if body.hrEmail: 
# #             update_data["hrEmail"] = body.hrEmail
    
# #     if body.status and body.status.lower() == "closed" and ticket.get("status", "").lower() != "closed":
# #         update_data["status"] = "Closed"
# #         update_data["closedAt"] = datetime.utcnow()
# #         update_data["remark"] = body.remark
    
# #     if update_data:
# #         hr_tickets.update_one({"id": ticketid}, {"$set": update_data})
    
# #     return {"message": "Updated", "ticketId": ticketid}

# # @app.delete("/api/tickets/{ticketid}")
# # async def delete_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
# #     """Delete HR ticket"""
# #     result = hr_tickets.delete_one({"id": ticketid})
# #     if result.deleted_count == 0: 
# #         raise HTTPException(404, "Ticket not found")
# #     return {"message": "Deleted"}

# # @app.get("/api/admin/stats")
# # async def get_hr_stats(admin=Depends(get_current_admin)):
# #     """Get HR ticket statistics"""
# #     tickets = list(hr_tickets.find({}, {"_id": 0}))
# #     stats = {"total": len(tickets), "bystatus": {"Open": 0, "Closed": 0}, "byhr": {}}
    
# #     for t in tickets:
# #         status = t.get("status", "Open")
# #         hr = t.get("assigned", "Unassigned")
# #         stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
# #         if hr not in stats["byhr"]:
# #             stats["byhr"][hr] = {"Open": 0, "Closed": 0}
# #         stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
# #     return stats

# # # ==================== IT TICKET ROUTES ====================

# # @app.get("/api/it/tickets")
# # async def get_it_tickets(admin=Depends(get_current_admin)):
# #     """Get all IT tickets"""
# #     tickets_list = list(it_tickets.find({}, {"_id": 0}))
    
# #     # Calculate TAT for closed tickets
# #     for ticket in tickets_list:
# #         if ticket.get('assignedAt') and ticket.get('closedAt'):
# #             try:
# #                 assigned_time = ticket['assignedAt']
# #                 closed_time = ticket['closedAt']
# #                 if isinstance(assigned_time, datetime) and isinstance(closed_time, datetime):
# #                     tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
# #                     ticket['tatHours'] = f"{tat_hours} hrs"
# #             except:
# #                 ticket['tatHours'] = "-"
# #         else:
# #             ticket['tatHours'] = "-"
    
# #     return tickets_list

# # @app.post("/api/it/tickets")
# # async def create_it_ticket(ticket: ITTicketCreate, background_tasks: BackgroundTasks):
# #     """Create new IT ticket"""
# #     sequence = it_sequences.find_one_and_update(
# #         {"_id": "ticket_counter"},
# #         {"$inc": {"seq": 1}},
# #         upsert=True, return_document=True
# #     )
# #     count = sequence['seq']
# #     ticket_id = f"TICKJHSIT{str(count).zfill(1)}"
    
# #     doc = {
# #         "id": ticket_id,
# #         "name": ticket.name,
# #         "email": ticket.email,
# #         "phone": ticket.phone,
# #         "empCode": ticket.empCode,
# #         "assetCode": ticket.assetCode,
# #         "issues": ticket.issues,
# #         "issueDescription": ticket.issueDescription,
# #         "reportingPartner": ticket.reportingPartner,
# #         "status": "Open",
# #         "assigned": "Unassigned",
# #         "itEmail": None,
# #         "createdAt": datetime.utcnow(),
# #         "assignedAt": None,
# #         "remark": None,
# #         "closedAt": None
# #     }
    
# #     it_tickets.insert_one(doc)
    
# #     # Send email
# #     background_tasks.add_task(
# #         sendemail,
# #         [ticket.email] + IT_EMAILS,
# #         f"IT Ticket {ticket_id} Created",
# #         f"<p>Dear {ticket.name},</p><p>Your IT ticket <strong>{ticket_id}</strong> has been created.</p><p><strong>IT Asset:</strong> {ticket.assetCode}</p><p><strong>Issues:</strong> {', '.join(ticket.issues)}</p><p>Regards,<br>JHS IT Helpdesk</p>"
# #     )
    
# #     return {k: v for k, v in doc.items() if k != '_id'}

# # @app.put("/api/it/tickets/{ticket_id}")
# # async def update_it_ticket(ticket_id: str, body: ITTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     """Update IT ticket"""
# #     ticket = it_tickets.find_one({"id": ticket_id})
# #     if not ticket:
# #         raise HTTPException(status_code=404, detail="Ticket not found")
    
# #     update_data = {}
    
# #     if body.assigned is not None:
# #         update_data["assigned"] = body.assigned
# #     if body.itEmail is not None:
# #         update_data["itEmail"] = body.itEmail
    
# #     if body.status:
# #         new_status = body.status.capitalize()
        
# #         if new_status == "Closed" and ticket.get("status") != "Closed":
# #             # Remark is mandatory when closing
# #             if not body.remark or not body.remark.strip():
# #                 raise HTTPException(
# #                     status_code=400,
# #                     detail="Remark is mandatory when closing a ticket"
# #                 )
            
# #             update_data["status"] = "Closed"
# #             update_data["remark"] = body.remark.strip()
# #             update_data["closedAt"] = datetime.utcnow()
# #         else:
# #             update_data["status"] = new_status
    
# #     if "assigned" in update_data and not ticket.get("assignedAt"):
# #         update_data["assignedAt"] = datetime.utcnow()
    
# #     if update_data:
# #         it_tickets.update_one({"id": ticket_id}, {"$set": update_data})
    
# #     return {"message": "Updated", "ticketId": ticket_id}

# # @app.delete("/api/it/tickets/{ticket_id}")
# # async def delete_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
# #     """Delete IT ticket"""
# #     res = it_tickets.delete_one({"id": ticket_id})
# #     if res.deleted_count == 0:
# #         raise HTTPException(status_code=404, detail="Ticket not found")
# #     return {"detail": "Deleted"}

# # @app.get("/api/it/tickets/stats")
# # async def get_it_stats(admin=Depends(get_current_admin)):
# #     """Get IT ticket statistics"""
# #     tickets = list(it_tickets.find({}, {"_id": 0, "status": 1, "assigned": 1}))
# #     total = len(tickets)
# #     by_status = {}
# #     by_it = {}
    
# #     for t in tickets:
# #         s = t.get("status", "Open")
# #         by_status[s] = by_status.get(s, 0) + 1
        
# #         it_person = t.get("assigned", "Unassigned")
# #         if it_person not in by_it:
# #             by_it[it_person] = {"Open": 0, "Closed": 0}
# #         by_it[it_person][s] = by_it[it_person].get(s, 0) + 1
    
# #     return {
# #         "total": total,
# #         "by_status": by_status,
# #         "by_it": by_it
# #     }

# # # ==================== FRONTEND ROUTES ====================

# # @app.get("/", response_class=HTMLResponse)
# # async def read_root():
# #     """HR helpdesk homepage"""
# #     return FileResponse("static/index.html")

# # @app.get("/admin", response_class=FileResponse)
# # async def hr_admin_page():
# #     """HR admin dashboard"""
# #     return FileResponse("static/hradmin.html")

# # @app.get("/it-admin", response_class=FileResponse)
# # async def it_admin_page():
# #     """IT admin dashboard"""
# #     return FileResponse("static/it-admin.html")

# # @app.get("/adminlogin", response_class=HTMLResponse)
# # async def admin_login_page():
# #     """Unified admin login page"""
# #     with open("static/adminlogin.html", "r", encoding="utf-8") as f:
# #         return f.read()

# # @app.get("/.well-known/{path:path}")
# # async def ignore_well_known(path: str):
# #     return {}

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)




# # from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import HTMLResponse, FileResponse
# # from fastapi.staticfiles import StaticFiles
# # from pydantic import BaseModel, EmailStr
# # from pymongo import MongoClient
# # from datetime import datetime, timedelta
# # from typing import Optional, Dict, Any, List
# # from dotenv import load_dotenv
# # import os
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # import logging
# # import hashlib
# # from jose import JWTError, jwt

# # # Load environment
# # load_dotenv()

# # # FastAPI app
# # app = FastAPI(title="JHS Unified Helpdesk API")
# # print("🚀 JHS Unified Helpdesk API Running")

# # # Mount static files
# # app.mount("/static", StaticFiles(directory="static"), name="static")

# # # CORS middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Config
# # SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
# # ALGORITHM = "HS256"
# # ACCESS_TOKEN_EXPIRE_MINUTES = 60

# # SMTP_SERVER = "smtp.gmail.com"
# # SMTP_PORT = 587
# # SMTP_USER = os.getenv("SMTP_USER")
# # SMTP_PASS = os.getenv("SMTP_PASS")

# # # Database connections
# # client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

# # # HR Database
# # hr_db = client["HR_Helpdesk"]
# # hr_tickets = hr_db["Tickets"]
# # hr_admins = hr_db["Admins"]

# # # IT Database
# # it_db = client["ithelpdesk"]
# # it_tickets = it_db["tickets"]
# # it_admins = it_db["admins"]
# # it_sessions = it_db["sessions"]
# # it_sequences = it_db["sequences"]

# # # Logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # # HR Email Mapping
# # HR_EMAILS = {
# #     "PAYSLIP": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "HRMS QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "ATTENDANCE": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "SALARY QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "BUDDY REFERRAL": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"},
# #     "OTHER": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"}
# # }

# # # IT Email list
# # IT_EMAILS = ["orinaguha9@gmail.com", "it2@jhs.co.in", "it3@jhs.co.in"]

# # # ==================== PYDANTIC MODELS ====================

# # # HR Models
# # class HRTicketCreate(BaseModel):
# #     name: str
# #     email: str
# #     phone: Optional[str] = None
# #     empCode: Optional[str] = None
# #     category: str
# #     issue: str

# # class HRTicketUpdate(BaseModel):
# #     assigned: Optional[str] = None
# #     status: Optional[str] = None
# #     hrEmail: Optional[str] = None
# #     remark: Optional[str] = None

# # # IT Models
# # class ITTicketCreate(BaseModel):
# #     name: str
# #     email: EmailStr
# #     phone: str  # Required
# #     assetCode: Optional[str] = ""  # Made optional
# #     empCode: Optional[str] = ""  # Optional
# #     issues: List[str]  # Required list
# #     issueDescription: str  # Required
# #     reportingPartner: str  # Required

# # class ITTicketUpdate(BaseModel):
# #     assigned: Optional[str] = None
# #     status: Optional[str] = None
# #     itEmail: Optional[EmailStr] = None
# #     remark: Optional[str] = None

# # class AdminLogin(BaseModel):
# #     empCode: str
# #     password: str

# # # ==================== UTILITY FUNCTIONS ====================

# # def hash_password(password: str) -> str:
# #     """Hash password using SHA256"""
# #     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# # def verify_password(plain: str, hashed: str) -> bool:
# #     """Verify password against hash"""
# #     return hash_password(plain) == hashed

# # def create_access_token(data: dict):
# #     """Create JWT access token"""
# #     to_encode = data.copy()
# #     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# #     to_encode.update({"exp": expire})
# #     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # def get_current_admin(authorization: str = Header(None)):
# #     """Verify JWT token and return admin info"""
# #     if not authorization or not authorization.startswith("Bearer "):
# #         raise HTTPException(status_code=401, detail="Missing token")
    
# #     token = authorization.split(" ")[1]
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         if payload.get("role") != "admin":
# #             raise HTTPException(status_code=403, detail="Not authorized")
# #         return payload
# #     except JWTError:
# #         raise HTTPException(status_code=401, detail="Invalid or expired token")

# # def sendemail(recipients: List[str], subject: str, body: str):
# #     """Send email to recipients"""
# #     logger.info(f"🔄 EMAIL → {recipients}, {subject}")
# #     try:
# #         msg = MIMEMultipart()
# #         msg['From'] = SMTP_USER
# #         msg['Subject'] = subject
# #         msg.attach(MIMEText(body, 'html'))
        
# #         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
# #         server.starttls()
# #         server.login(SMTP_USER, SMTP_PASS)
        
# #         valid_recipients = [r for r in recipients if r and r.strip()]
# #         if valid_recipients:
# #             server.sendmail(SMTP_USER, valid_recipients, msg.as_string())
# #             logger.info(f"✅ EMAILS SENT → {valid_recipients}")
# #         server.quit()
# #     except Exception as e:
# #         logger.error(f"❌ EMAIL FAILED → {str(e)}")

# # # ==================== AUTHENTICATION ROUTES ====================

# # @app.post("/api/admin/login")
# # async def unified_admin_login(body: AdminLogin):
# #     """
# #     Unified login endpoint for both HR and IT admins.
# #     First checks HR admins, then IT admins.
# #     """
# #     empCode = body.empCode.upper().strip()
# #     password = body.password
    
# #     if not empCode or not password:
# #         raise HTTPException(status_code=400, detail="empCode and password required")
    
# #     logger.info(f"Login attempt for empCode: {empCode}")
    
# #     # Try HR admin first
# #     hr_admin = hr_admins.find_one({"empCodes": empCode, "password": password})
    
# #     if hr_admin:
# #         logger.info(f"HR Admin found: {hr_admin.get('name')}")
# #         token = create_access_token({
# #             "sub": empCode,
# #             "role": "admin",
# #             "type": "hr",
# #             "name": hr_admin.get("name")
# #         })
        
# #         return {
# #             "access_token": token,
# #             "token_type": "bearer",
# #             "name": hr_admin.get("name"),
# #             "helpdesk": "hr"
# #         }
    
# #     # Try IT admin
# #     it_admin = it_admins.find_one({"empCode": empCode})
    
# #     if it_admin:
# #         logger.info(f"IT Admin found: {it_admin.get('name')}")
        
# #         # Verify password
# #         if not verify_password(password, it_admin["password"]):
# #             logger.error("Password verification failed")
# #             raise HTTPException(status_code=401, detail="Invalid password")
        
# #         logger.info("Password verified successfully")
        
# #         token = create_access_token({
# #             "sub": empCode,
# #             "role": "admin",
# #             "type": "it",
# #             "name": it_admin.get("name")
# #         })
        
# #         # Store session in IT sessions collection
# #         session_doc = {
# #             "empCode": empCode,
# #             "token": token,
# #             "isValid": True,
# #             "createdAt": datetime.utcnow(),
# #             "expiresAt": datetime.utcnow() + timedelta(hours=1)
# #         }
        
# #         it_sessions.update_one(
# #             {"empCode": empCode},
# #             {"$set": session_doc},
# #             upsert=True
# #         )
        
# #         logger.info(f"Login successful for IT admin {empCode}")
        
# #         return {
# #             "access_token": token,
# #             "token": token,  # For backward compatibility
# #             "token_type": "bearer",
# #             "empCode": empCode,
# #             "name": it_admin.get("name"),
# #             "helpdesk": "it"
# #         }
    
# #     # No admin found
# #     logger.error(f"Admin not found for empCode: {empCode}")
# #     raise HTTPException(status_code=401, detail="Invalid credentials")

# # # ==================== HR TICKET ROUTES (with /api/hr/ prefix) ====================

# # @app.get("/api/hr/tickets")
# # async def get_hr_tickets(admin=Depends(get_current_admin)):
# #     """Get all HR tickets"""
# #     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# # @app.post("/api/hr/tickets")
# # async def create_hr_ticket(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
# #     """Create new HR ticket"""
# #     count = hr_tickets.count_documents({})
# #     ticket_id = f"TICKJHSHR{str(count + 1).zfill(2)}"
    
# #     category = ticket.category.upper().strip()
# #     hr_data = HR_EMAILS.get(category)
# #     assigned_name = hr_data["name"] if hr_data else "Unassigned"
# #     assigned_email = hr_data["email"] if hr_data else None
    
# #     ticket_data = {
# #         "id": ticket_id, "name": ticket.name, "email": ticket.email,
# #         "phone": ticket.phone, "empCode": ticket.empCode,
# #         "category": ticket.category, "issue": ticket.issue,
# #         "status": "Open", "assigned": assigned_name, "hrEmail": assigned_email,
# #         "assignedAt": datetime.utcnow() if hr_data else None,
# #         "createdAt": datetime.utcnow(), "remark": ""
# #     }
    
# #     hr_tickets.insert_one(ticket_data)
    
# #     # Send emails
# #     background_tasks.add_task(
# #         sendemail, [ticket.email],
# #         f"JHS HR - Ticket {ticket_id} Created",
# #         f"<p>Dear {ticket.name},</p><p>Your ticket {ticket_id} created.</p><p>Category: {ticket.category}<br>Assigned: {assigned_name}</p><p>JHS HR Team</p>"
# #     )
    
# #     if assigned_email:
# #         background_tasks.add_task(
# #             sendemail, [assigned_email],
# #             f"New Ticket: {ticket_id}",
# #             f"<p>Dear {assigned_name},</p><p>Ticket {ticket_id} assigned to you.</p><p>Employee: {ticket.name}<br>Issue: {ticket.issue}</p>"
# #         )
    
# #     return {"message": "Ticket created", "ticketId": ticket_id, "assignedTo": assigned_name}

# # @app.get("/api/hr/tickets/{ticketid}")
# # async def get_single_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
# #     """Get single HR ticket by ID"""
# #     ticket = hr_tickets.find_one({"id": ticketid})
# #     if not ticket:
# #         raise HTTPException(404, "Ticket not found")
# #     ticket.pop("_id", None)
# #     return ticket

# # @app.put("/api/hr/tickets/{ticketid}")
# # async def update_hr_ticket(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     """Update HR ticket"""
# #     ticket = hr_tickets.find_one({"id": ticketid})
# #     if not ticket: 
# #         raise HTTPException(404, "Ticket not found")
    
# #     update_data = {}
# #     old_assigned = ticket.get("assigned")
    
# #     if body.assigned and body.assigned != old_assigned:
# #         update_data["assigned"] = body.assigned
# #         update_data["assignedAt"] = datetime.utcnow()
# #         if body.hrEmail: 
# #             update_data["hrEmail"] = body.hrEmail
    
# #     if body.status and body.status.lower() == "closed" and ticket.get("status", "").lower() != "closed":
# #         update_data["status"] = "Closed"
# #         update_data["closedAt"] = datetime.utcnow()
# #         update_data["remark"] = body.remark
    
# #     if update_data:
# #         hr_tickets.update_one({"id": ticketid}, {"$set": update_data})
    
# #     return {"message": "Updated", "ticketId": ticketid}

# # @app.delete("/api/hr/tickets/{ticketid}")
# # async def delete_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
# #     """Delete HR ticket"""
# #     result = hr_tickets.delete_one({"id": ticketid})
# #     if result.deleted_count == 0: 
# #         raise HTTPException(404, "Ticket not found")
# #     return {"message": "Deleted"}

# # @app.get("/api/hr/admin/stats")
# # async def get_hr_stats(admin=Depends(get_current_admin)):
# #     """Get HR ticket statistics"""
# #     tickets = list(hr_tickets.find({}, {"_id": 0}))
# #     stats = {"total": len(tickets), "bystatus": {"Open": 0, "Closed": 0}, "byhr": {}}
    
# #     for t in tickets:
# #         status = t.get("status", "Open")
# #         hr = t.get("assigned", "Unassigned")
# #         stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
# #         if hr not in stats["byhr"]:
# #             stats["byhr"][hr] = {"Open": 0, "Closed": 0}
# #         stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
# #     return stats

# # # ==================== LEGACY HR ROUTES (for backward compatibility) ====================
# # # These maintain compatibility with existing HR frontend that uses /api/tickets

# # @app.get("/api/tickets")
# # async def get_hr_tickets_legacy(admin=Depends(get_current_admin)):
# #     """Legacy HR route - Get all HR tickets"""
# #     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# # @app.post("/api/tickets")
# # async def create_hr_ticket_legacy(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
# #     """Legacy HR route - Create new HR ticket"""
# #     return await create_hr_ticket(ticket, background_tasks)

# # @app.get("/api/tickets/{ticketid}")
# # async def get_single_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
# #     """Legacy HR route - Get single HR ticket"""
# #     return await get_single_hr_ticket(ticketid, admin)

# # @app.put("/api/tickets/{ticketid}")
# # async def update_hr_ticket_legacy(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     """Legacy HR route - Update HR ticket"""
# #     return await update_hr_ticket(ticketid, body, background_tasks, admin)

# # @app.delete("/api/tickets/{ticketid}")
# # async def delete_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
# #     """Legacy HR route - Delete HR ticket"""
# #     return await delete_hr_ticket(ticketid, admin)

# # @app.get("/api/admin/stats")
# # async def get_hr_stats_legacy(admin=Depends(get_current_admin)):
# #     """Legacy HR route - Get HR statistics"""
# #     return await get_hr_stats(admin)

# # # ==================== IT TICKET ROUTES (with /api/it/ prefix) ====================

# # @app.get("/api/it/tickets")
# # async def get_it_tickets(admin=Depends(get_current_admin)):
# #     """Get all IT tickets"""
# #     tickets_list = list(it_tickets.find({}, {"_id": 0}))
    
# #     # Calculate TAT for closed tickets
# #     for ticket in tickets_list:
# #         if ticket.get('assignedAt') and ticket.get('closedAt'):
# #             try:
# #                 assigned_time = ticket['assignedAt']
# #                 closed_time = ticket['closedAt']
# #                 if isinstance(assigned_time, datetime) and isinstance(closed_time, datetime):
# #                     tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
# #                     ticket['tatHours'] = f"{tat_hours} hrs"
# #             except:
# #                 ticket['tatHours'] = "-"
# #         else:
# #             ticket['tatHours'] = "-"
    
# #     return tickets_list

# # @app.post("/api/it/tickets")
# # async def create_it_ticket(ticket: ITTicketCreate, background_tasks: BackgroundTasks):
# #     """Create new IT ticket"""
# #     sequence = it_sequences.find_one_and_update(
# #         {"_id": "ticket_counter"},
# #         {"$inc": {"seq": 1}},
# #         upsert=True, return_document=True
# #     )
# #     count = sequence['seq']
# #     ticket_id = f"TICKJHSIT{str(count).zfill(1)}"
    
# #     doc = {
# #         "id": ticket_id,
# #         "name": ticket.name,
# #         "email": ticket.email,
# #         "phone": ticket.phone,
# #         "empCode": ticket.empCode,
# #         "assetCode": ticket.assetCode,
# #         "issues": ticket.issues,
# #         "issueDescription": ticket.issueDescription,
# #         "reportingPartner": ticket.reportingPartner,
# #         "status": "Open",
# #         "assigned": "Unassigned",
# #         "itEmail": None,
# #         "createdAt": datetime.utcnow(),
# #         "assignedAt": None,
# #         "remark": None,
# #         "closedAt": None
# #     }
    
# #     it_tickets.insert_one(doc)
    
# #     # Send email
# #     background_tasks.add_task(
# #         sendemail,
# #         [ticket.email] + IT_EMAILS,
# #         f"IT Ticket {ticket_id} Created",
# #         f"<p>Dear {ticket.name},</p><p>Your IT ticket <strong>{ticket_id}</strong> has been created.</p><p><strong>IT Asset:</strong> {ticket.assetCode}</p><p><strong>Issues:</strong> {', '.join(ticket.issues)}</p><p>Regards,<br>JHS IT Helpdesk</p>"
# #     )
    
# #     return {k: v for k, v in doc.items() if k != '_id'}

# # @app.get("/api/it/tickets/{ticket_id}")
# # async def get_single_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
# #     """Get single IT ticket by ID"""
# #     ticket = it_tickets.find_one({"id": ticket_id}, {"_id": 0})
# #     if not ticket:
# #         raise HTTPException(status_code=404, detail="Ticket not found")
# #     return ticket

# # @app.put("/api/it/tickets/{ticket_id}")
# # async def update_it_ticket(ticket_id: str, body: ITTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     """Update IT ticket"""
# #     ticket = it_tickets.find_one({"id": ticket_id})
# #     if not ticket:
# #         raise HTTPException(status_code=404, detail="Ticket not found")
    
# #     update_data = {}
    
# #     if body.assigned is not None:
# #         update_data["assigned"] = body.assigned
# #     if body.itEmail is not None:
# #         update_data["itEmail"] = body.itEmail
    
# #     if body.status:
# #         new_status = body.status.capitalize()
        
# #         if new_status == "Closed" and ticket.get("status") != "Closed":
# #             # Remark is mandatory when closing
# #             if not body.remark or not body.remark.strip():
# #                 raise HTTPException(
# #                     status_code=400,
# #                     detail="Remark is mandatory when closing a ticket"
# #                 )
            
# #             update_data["status"] = "Closed"
# #             update_data["remark"] = body.remark.strip()
# #             update_data["closedAt"] = datetime.utcnow()
# #         else:
# #             update_data["status"] = new_status
    
# #     if "assigned" in update_data and not ticket.get("assignedAt"):
# #         update_data["assignedAt"] = datetime.utcnow()
    
# #     if update_data:
# #         it_tickets.update_one({"id": ticket_id}, {"$set": update_data})
    
# #     return {"message": "Updated", "ticketId": ticket_id}

# # @app.delete("/api/it/tickets/{ticket_id}")
# # async def delete_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
# #     """Delete IT ticket"""
# #     res = it_tickets.delete_one({"id": ticket_id})
# #     if res.deleted_count == 0:
# #         raise HTTPException(status_code=404, detail="Ticket not found")
# #     return {"detail": "Deleted"}

# # @app.get("/api/it/tickets/stats")
# # async def get_it_stats(admin=Depends(get_current_admin)):
# #     """Get IT ticket statistics"""
# #     tickets = list(it_tickets.find({}, {"_id": 0, "status": 1, "assigned": 1}))
# #     total = len(tickets)
# #     by_status = {}
# #     by_it = {}
    
# #     for t in tickets:
# #         s = t.get("status", "Open")
# #         by_status[s] = by_status.get(s, 0) + 1
        
# #         it_person = t.get("assigned", "Unassigned")
# #         if it_person not in by_it:
# #             by_it[it_person] = {"Open": 0, "Closed": 0}
# #         by_it[it_person][s] = by_it[it_person].get(s, 0) + 1
    
# #     return {
# #         "total": total,
# #         "by_status": by_status,
# #         "by_it": by_it
# #     }

# # # ==================== FRONTEND ROUTES ====================

# # @app.get("/", response_class=HTMLResponse)
# # async def read_root():
# #     """HR helpdesk homepage"""
# #     return FileResponse("static/index.html")

# # @app.get("/admin", response_class=FileResponse)
# # async def hr_admin_page():
# #     """HR admin dashboard"""
# #     return FileResponse("static/hradmin.html")

# # @app.get("/it-admin", response_class=FileResponse)
# # async def it_admin_page():
# #     """IT admin dashboard"""
# #     return FileResponse("static/it-admin.html")

# # @app.get("/adminlogin", response_class=HTMLResponse)
# # async def admin_login_page():
# #     """Unified admin login page"""
# #     with open("static/adminlogin.html", "r", encoding="utf-8") as f:
# #         return f.read()

# # @app.get("/.well-known/{path:path}")
# # async def ignore_well_known(path: str):
# #     return {}

# # # ==================== HEALTH CHECK ====================

# # @app.get("/health")
# # async def health_check():
# #     """Health check endpoint"""
# #     return {
# #         "status": "healthy",
# #         "timestamp": datetime.utcnow().isoformat(),
# #         "databases": {
# #             "hr_tickets": hr_tickets.count_documents({}),
# #             "it_tickets": it_tickets.count_documents({})
# #         }
# #     }

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)




# # from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import HTMLResponse, FileResponse
# # from fastapi.staticfiles import StaticFiles
# # from pydantic import BaseModel, EmailStr
# # from pymongo import MongoClient
# # from datetime import datetime, timedelta
# # from typing import Optional, Dict, Any, List
# # from dotenv import load_dotenv
# # import os
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # import logging
# # import hashlib
# # from jose import JWTError, jwt

# # # Load environment
# # load_dotenv()

# # # FastAPI app
# # app = FastAPI(title="JHS Unified Helpdesk API")
# # print("🚀 JHS Unified Helpdesk API Running")

# # # Mount static files
# # app.mount("/static", StaticFiles(directory="static"), name="static")

# # # CORS middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Config
# # SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
# # ALGORITHM = "HS256"
# # ACCESS_TOKEN_EXPIRE_MINUTES = 60

# # SMTP_SERVER = "smtp.gmail.com"
# # SMTP_PORT = 587
# # SMTP_USER = os.getenv("SMTP_USER")
# # SMTP_PASS = os.getenv("SMTP_PASS")

# # # Database connections
# # client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

# # # HR Database
# # hr_db = client["HR_Helpdesk"]
# # hr_tickets = hr_db["Tickets"]
# # hr_admins = hr_db["Admins"]

# # # IT Database
# # it_db = client["ithelpdesk"]
# # it_tickets = it_db["tickets"]
# # it_admins = it_db["admins"]
# # it_sessions = it_db["sessions"]
# # it_sequences = it_db["sequences"]

# # # Logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # # HR Email Mapping
# # HR_EMAILS = {
# #     "PAYSLIP": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "HRMS QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "ATTENDANCE": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "SALARY QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
# #     "BUDDY REFERRAL": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"},
# #     "OTHER": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"}
# # }

# # # IT Email list
# # IT_EMAILS = ["orinaguha9@gmail.com", "it2@jhs.co.in", "it3@jhs.co.in"]

# # # ==================== PYDANTIC MODELS ====================

# # # HR Models
# # class HRTicketCreate(BaseModel):
# #     name: str
# #     email: str
# #     phone: Optional[str] = None
# #     empCode: Optional[str] = None
# #     category: str
# #     issue: str

# # class HRTicketUpdate(BaseModel):
# #     assigned: Optional[str] = None
# #     status: Optional[str] = None
# #     hrEmail: Optional[str] = None
# #     remark: Optional[str] = None

# # # IT Models
# # class ITTicketCreate(BaseModel):
# #     name: str
# #     email: EmailStr
# #     phone: str  # Required
# #     assetCode: Optional[str] = ""  # Made optional
# #     empCode: Optional[str] = ""  # Optional
# #     issues: List[str]  # Required list
# #     issueDescription: str  # Required
# #     reportingPartner: str  # Required

# # class ITTicketUpdate(BaseModel):
# #     assigned: Optional[str] = None
# #     status: Optional[str] = None
# #     itEmail: Optional[EmailStr] = None
# #     remark: Optional[str] = None

# # class AdminLogin(BaseModel):
# #     empCode: str
# #     password: str

# # # ==================== UTILITY FUNCTIONS ====================

# # def hash_password(password: str) -> str:
# #     """Hash password using SHA256"""
# #     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# # def verify_password(plain: str, hashed: str) -> bool:
# #     """Verify password against hash"""
# #     return hash_password(plain) == hashed

# # def create_access_token(data: dict):
# #     """Create JWT access token"""
# #     to_encode = data.copy()
# #     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# #     to_encode.update({"exp": expire})
# #     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # def get_current_admin(authorization: str = Header(None)):
# #     """Verify JWT token and return admin info"""
# #     if not authorization or not authorization.startswith("Bearer "):
# #         raise HTTPException(status_code=401, detail="Missing token")
    
# #     token = authorization.split(" ")[1]
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         if payload.get("role") != "admin":
# #             raise HTTPException(status_code=403, detail="Not authorized")
# #         return payload
# #     except JWTError:
# #         raise HTTPException(status_code=401, detail="Invalid or expired token")

# # def sendemail(recipients: List[str], subject: str, body: str):
# #     """Send email to recipients"""
# #     logger.info(f"🔄 EMAIL → {recipients}, {subject}")
# #     try:
# #         msg = MIMEMultipart()
# #         msg['From'] = SMTP_USER
# #         msg['Subject'] = subject
# #         msg.attach(MIMEText(body, 'html'))
        
# #         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
# #         server.starttls()
# #         server.login(SMTP_USER, SMTP_PASS)
        
# #         valid_recipients = [r for r in recipients if r and r.strip()]
# #         if valid_recipients:
# #             server.sendmail(SMTP_USER, valid_recipients, msg.as_string())
# #             logger.info(f"✅ EMAILS SENT → {valid_recipients}")
# #         server.quit()
# #     except Exception as e:
# #         logger.error(f"❌ EMAIL FAILED → {str(e)}")

# # # ==================== AUTHENTICATION ROUTES ====================

# # @app.post("/api/admin/login")
# # async def unified_admin_login(body: AdminLogin):
# #     """
# #     Unified login endpoint for both HR and IT admins.
# #     First checks HR admins, then IT admins.
# #     """
# #     empCode = body.empCode.upper().strip()
# #     password = body.password
    
# #     if not empCode or not password:
# #         raise HTTPException(status_code=400, detail="empCode and password required")
    
# #     logger.info(f"Login attempt for empCode: {empCode}")
    
# #     # Try HR admin first
# #     hr_admin = hr_admins.find_one({"empCodes": empCode, "password": password})
    
# #     if hr_admin:
# #         logger.info(f"HR Admin found: {hr_admin.get('name')}")
# #         token = create_access_token({
# #             "sub": empCode,
# #             "role": "admin",
# #             "type": "hr",
# #             "name": hr_admin.get("name")
# #         })
        
# #         return {
# #             "access_token": token,
# #             "token_type": "bearer",
# #             "name": hr_admin.get("name"),
# #             "helpdesk": "hr"
# #         }
    
# #     # Try IT admin
# #     it_admin = it_admins.find_one({"empCode": empCode})
    
# #     if it_admin:
# #         logger.info(f"IT Admin found: {it_admin.get('name')}")
        
# #         # Verify password
# #         if not verify_password(password, it_admin["password"]):
# #             logger.error("Password verification failed")
# #             raise HTTPException(status_code=401, detail="Invalid password")
        
# #         logger.info("Password verified successfully")
        
# #         token = create_access_token({
# #             "sub": empCode,
# #             "role": "admin",
# #             "type": "it",
# #             "name": it_admin.get("name")
# #         })
        
# #         # Store session in IT sessions collection
# #         session_doc = {
# #             "empCode": empCode,
# #             "token": token,
# #             "isValid": True,
# #             "createdAt": datetime.utcnow(),
# #             "expiresAt": datetime.utcnow() + timedelta(hours=1)
# #         }
        
# #         it_sessions.update_one(
# #             {"empCode": empCode},
# #             {"$set": session_doc},
# #             upsert=True
# #         )
        
# #         logger.info(f"Login successful for IT admin {empCode}")
        
# #         return {
# #             "access_token": token,
# #             "token": token,  # For backward compatibility
# #             "token_type": "bearer",
# #             "empCode": empCode,
# #             "name": it_admin.get("name"),
# #             "helpdesk": "it"
# #         }
    
# #     # No admin found
# #     logger.error(f"Admin not found for empCode: {empCode}")
# #     raise HTTPException(status_code=401, detail="Invalid credentials")

# # # ==================== HR TICKET ROUTES (with /api/hr/ prefix) ====================

# # @app.get("/api/hr/tickets")
# # async def get_hr_tickets(admin=Depends(get_current_admin)):
# #     """Get all HR tickets"""
# #     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# # @app.post("/api/hr/tickets")
# # async def create_hr_ticket(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
# #     """Create new HR ticket"""
# #     count = hr_tickets.count_documents({})
# #     ticket_id = f"TICKJHSHR{str(count + 1).zfill(2)}"
    
# #     category = ticket.category.upper().strip()
# #     hr_data = HR_EMAILS.get(category)
# #     assigned_name = hr_data["name"] if hr_data else "Unassigned"
# #     assigned_email = hr_data["email"] if hr_data else None
    
# #     ticket_data = {
# #         "id": ticket_id, "name": ticket.name, "email": ticket.email,
# #         "phone": ticket.phone, "empCode": ticket.empCode,
# #         "category": ticket.category, "issue": ticket.issue,
# #         "status": "Open", "assigned": assigned_name, "hrEmail": assigned_email,
# #         "assignedAt": datetime.utcnow() if hr_data else None,
# #         "createdAt": datetime.utcnow(), "remark": ""
# #     }
    
# #     hr_tickets.insert_one(ticket_data)
    
# #     # Send emails
# #     background_tasks.add_task(
# #         sendemail, [ticket.email],
# #         f"JHS HR - Ticket {ticket_id} Created",
# #         f"<p>Dear {ticket.name},</p><p>Your ticket {ticket_id} created.</p><p>Category: {ticket.category}<br>Assigned: {assigned_name}</p><p>JHS HR Team</p>"
# #     )
    
# #     if assigned_email:
# #         background_tasks.add_task(
# #             sendemail, [assigned_email],
# #             f"New Ticket: {ticket_id}",
# #             f"<p>Dear {assigned_name},</p><p>Ticket {ticket_id} assigned to you.</p><p>Employee: {ticket.name}<br>Issue: {ticket.issue}</p>"
# #         )
    
# #     return {"message": "Ticket created", "ticketId": ticket_id, "assignedTo": assigned_name}

# # @app.get("/api/hr/tickets/{ticketid}")
# # async def get_single_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
# #     """Get single HR ticket by ID"""
# #     ticket = hr_tickets.find_one({"id": ticketid})
# #     if not ticket:
# #         raise HTTPException(404, "Ticket not found")
# #     ticket.pop("_id", None)
# #     return ticket

# # @app.put("/api/hr/tickets/{ticketid}")
# # async def update_hr_ticket(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     """Update HR ticket"""
# #     ticket = hr_tickets.find_one({"id": ticketid})
# #     if not ticket: 
# #         raise HTTPException(404, "Ticket not found")
    
# #     update_data = {}
# #     old_assigned = ticket.get("assigned")
# #     old_status = ticket.get("status", "").lower()
    
# #     # Handle reassignment
# #     if body.assigned and body.assigned != old_assigned:
# #         update_data["assigned"] = body.assigned
# #         update_data["assignedAt"] = datetime.utcnow()
# #         if body.hrEmail: 
# #             update_data["hrEmail"] = body.hrEmail
        
# #         # Send reassignment email to new HR person
# #         if body.hrEmail:
# #             background_tasks.add_task(
# #                 sendemail,
# #                 [body.hrEmail],
# #                 f"HR Ticket {ticketid} Assigned to You",
# #                 f"""
# #                 <p>Dear {body.assigned},</p>
# #                 <p>The ticket <strong>{ticketid}</strong> has been assigned to you.</p>
# #                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
# #                 <strong>Category:</strong> {ticket.get('category')}<br>
# #                 <strong>Issue:</strong> {ticket.get('issue')}</p>
# #                 <p>Please review and take necessary action.</p>
# #                 <p>Regards,<br>JHS HR Helpdesk</p>
# #                 """
# #             )
    
# #     # Handle closure
# #     if body.status and body.status.lower() == "closed" and old_status != "closed":
# #         update_data["status"] = "Closed"
# #         update_data["closedAt"] = datetime.utcnow()
# #         update_data["remark"] = body.remark if body.remark else ""
        
# #         # Send closure email to employee
# #         background_tasks.add_task(
# #             sendemail,
# #             [ticket.get('email')],
# #             f"HR Ticket {ticketid} Closed",
# #             f"""
# #             <p>Dear {ticket.get('name')},</p>
# #             <p>Your HR ticket <strong>{ticketid}</strong> has been closed.</p>
# #             <p><strong>Category:</strong> {ticket.get('category')}<br>
# #             <strong>Issue:</strong> {ticket.get('issue')}<br>
# #             <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
# #             <p>If you have any further questions, please feel free to create a new ticket.</p>
# #             <p>Regards,<br>JHS HR Team</p>
# #             """
# #         )
        
# #         # Send closure confirmation to HR person
# #         hr_email = ticket.get('hrEmail')
# #         if hr_email:
# #             background_tasks.add_task(
# #                 sendemail,
# #                 [hr_email],
# #                 f"HR Ticket {ticketid} Closed Confirmation",
# #                 f"""
# #                 <p>Dear {ticket.get('assigned', 'HR Team')},</p>
# #                 <p>You have successfully closed ticket <strong>{ticketid}</strong>.</p>
# #                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
# #                 <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
# #                 <p>Regards,<br>JHS HR Helpdesk</p>
# #                 """
# #             )
    
# #     if update_data:
# #         hr_tickets.update_one({"id": ticketid}, {"$set": update_data})
    
# #     return {"message": "Updated", "ticketId": ticketid}

# # @app.delete("/api/hr/tickets/{ticketid}")
# # async def delete_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
# #     """Delete HR ticket"""
# #     result = hr_tickets.delete_one({"id": ticketid})
# #     if result.deleted_count == 0: 
# #         raise HTTPException(404, "Ticket not found")
# #     return {"message": "Deleted"}

# # @app.get("/api/hr/admin/stats")
# # async def get_hr_stats(admin=Depends(get_current_admin)):
# #     """Get HR ticket statistics"""
# #     tickets = list(hr_tickets.find({}, {"_id": 0}))
# #     stats = {"total": len(tickets), "bystatus": {"Open": 0, "Closed": 0}, "byhr": {}}
    
# #     for t in tickets:
# #         status = t.get("status", "Open")
# #         hr = t.get("assigned", "Unassigned")
# #         stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
# #         if hr not in stats["byhr"]:
# #             stats["byhr"][hr] = {"Open": 0, "Closed": 0}
# #         stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
# #     return stats

# # # ==================== LEGACY HR ROUTES (for backward compatibility) ====================
# # # These maintain compatibility with existing HR frontend that uses /api/tickets

# # @app.get("/api/tickets")
# # async def get_hr_tickets_legacy(admin=Depends(get_current_admin)):
# #     """Legacy HR route - Get all HR tickets"""
# #     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# # @app.post("/api/tickets")
# # async def create_hr_ticket_legacy(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
# #     """Legacy HR route - Create new HR ticket"""
# #     return await create_hr_ticket(ticket, background_tasks)

# # @app.get("/api/tickets/{ticketid}")
# # async def get_single_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
# #     """Legacy HR route - Get single HR ticket"""
# #     return await get_single_hr_ticket(ticketid, admin)

# # @app.put("/api/tickets/{ticketid}")
# # async def update_hr_ticket_legacy(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     """Legacy HR route - Update HR ticket"""
# #     return await update_hr_ticket(ticketid, body, background_tasks, admin)

# # @app.delete("/api/tickets/{ticketid}")
# # async def delete_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
# #     """Legacy HR route - Delete HR ticket"""
# #     return await delete_hr_ticket(ticketid, admin)

# # @app.get("/api/admin/stats")
# # async def get_hr_stats_legacy(admin=Depends(get_current_admin)):
# #     """Legacy HR route - Get HR statistics"""
# #     return await get_hr_stats(admin)

# # # ==================== IT TICKET ROUTES (with /api/it/ prefix) ====================

# # @app.get("/api/it/tickets")
# # async def get_it_tickets(admin=Depends(get_current_admin)):
# #     """Get all IT tickets"""
# #     tickets_list = list(it_tickets.find({}, {"_id": 0}))
    
# #     # Calculate TAT for closed tickets
# #     for ticket in tickets_list:
# #         if ticket.get('assignedAt') and ticket.get('closedAt'):
# #             try:
# #                 assigned_time = ticket['assignedAt']
# #                 closed_time = ticket['closedAt']
# #                 if isinstance(assigned_time, datetime) and isinstance(closed_time, datetime):
# #                     tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
# #                     ticket['tatHours'] = f"{tat_hours} hrs"
# #             except:
# #                 ticket['tatHours'] = "-"
# #         else:
# #             ticket['tatHours'] = "-"
    
# #     return tickets_list

# # @app.post("/api/it/tickets")
# # async def create_it_ticket(ticket: ITTicketCreate, background_tasks: BackgroundTasks):
# #     """Create new IT ticket"""
# #     sequence = it_sequences.find_one_and_update(
# #         {"_id": "ticket_counter"},
# #         {"$inc": {"seq": 1}},
# #         upsert=True, return_document=True
# #     )
# #     count = sequence['seq']
# #     ticket_id = f"TICKJHSIT{str(count).zfill(1)}"
    
# #     doc = {
# #         "id": ticket_id,
# #         "name": ticket.name,
# #         "email": ticket.email,
# #         "phone": ticket.phone,
# #         "empCode": ticket.empCode,
# #         "assetCode": ticket.assetCode,
# #         "issues": ticket.issues,
# #         "issueDescription": ticket.issueDescription,
# #         "reportingPartner": ticket.reportingPartner,
# #         "status": "Open",
# #         "assigned": "Unassigned",
# #         "itEmail": None,
# #         "createdAt": datetime.utcnow(),
# #         "assignedAt": None,
# #         "remark": None,
# #         "closedAt": None
# #     }
    
# #     it_tickets.insert_one(doc)
    
# #     # Send email
# #     background_tasks.add_task(
# #         sendemail,
# #         [ticket.email] + IT_EMAILS,
# #         f"IT Ticket {ticket_id} Created",
# #         f"<p>Dear {ticket.name},</p><p>Your IT ticket <strong>{ticket_id}</strong> has been created.</p><p><strong>IT Asset:</strong> {ticket.assetCode}</p><p><strong>Issues:</strong> {', '.join(ticket.issues)}</p><p>Regards,<br>JHS IT Helpdesk</p>"
# #     )
    
# #     return {k: v for k, v in doc.items() if k != '_id'}

# # @app.get("/api/it/tickets/{ticket_id}")
# # async def get_single_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
# #     """Get single IT ticket by ID"""
# #     ticket = it_tickets.find_one({"id": ticket_id}, {"_id": 0})
# #     if not ticket:
# #         raise HTTPException(status_code=404, detail="Ticket not found")
# #     return ticket

# # @app.put("/api/it/tickets/{ticket_id}")
# # async def update_it_ticket(ticket_id: str, body: ITTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
# #     """Update IT ticket"""
# #     ticket = it_tickets.find_one({"id": ticket_id})
# #     if not ticket:
# #         raise HTTPException(status_code=404, detail="Ticket not found")
    
# #     update_data = {}
# #     old_assigned = ticket.get("assigned")
# #     old_status = ticket.get("status", "").lower()
    
# #     # Handle assignment
# #     if body.assigned is not None and body.assigned != old_assigned:
# #         update_data["assigned"] = body.assigned
        
# #         # Set assignedAt timestamp if not already set
# #         if not ticket.get("assignedAt"):
# #             update_data["assignedAt"] = datetime.utcnow()
        
# #         # Send assignment email to IT person
# #         if body.itEmail:
# #             update_data["itEmail"] = body.itEmail
# #             background_tasks.add_task(
# #                 sendemail,
# #                 [body.itEmail],
# #                 f"IT Ticket {ticket_id} Assigned to You",
# #                 f"""
# #                 <p>Dear {body.assigned},</p>
# #                 <p>The IT ticket <strong>{ticket_id}</strong> has been assigned to you.</p>
# #                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
# #                 <strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
# #                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
# #                 <strong>Description:</strong> {ticket.get('issueDescription')}</p>
# #                 <p>Please review and take necessary action.</p>
# #                 <p>Regards,<br>JHS IT Helpdesk</p>
# #                 """
# #             )
        
# #         # Notify employee about assignment
# #         background_tasks.add_task(
# #             sendemail,
# #             [ticket.get('email')],
# #             f"IT Ticket {ticket_id} Assigned",
# #             f"""
# #             <p>Dear {ticket.get('name')},</p>
# #             <p>Your IT ticket <strong>{ticket_id}</strong> has been assigned to <strong>{body.assigned}</strong>.</p>
# #             <p>Our team is working on resolving your issue.</p>
# #             <p>Regards,<br>JHS IT Helpdesk</p>
# #             """
# #         )
# #     elif body.itEmail is not None:
# #         update_data["itEmail"] = body.itEmail
    
# #     # Handle status change and closure
# #     if body.status:
# #         new_status = body.status.capitalize()
        
# #         if new_status == "Closed" and old_status != "closed":
# #             # Remark is mandatory when closing
# #             if not body.remark or not body.remark.strip():
# #                 raise HTTPException(
# #                     status_code=400,
# #                     detail="Remark is mandatory when closing a ticket"
# #                 )
            
# #             update_data["status"] = "Closed"
# #             update_data["remark"] = body.remark.strip()
# #             update_data["closedAt"] = datetime.utcnow()
            
# #             # Calculate TAT if assignedAt exists
# #             tat_text = "N/A"
# #             if ticket.get("assignedAt"):
# #                 try:
# #                     assigned_time = ticket['assignedAt']
# #                     closed_time = update_data["closedAt"]
# #                     if isinstance(assigned_time, datetime):
# #                         tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
# #                         tat_text = f"{tat_hours} hours"
# #                 except:
# #                     tat_text = "N/A"
            
# #             # Send closure email to employee
# #             background_tasks.add_task(
# #                 sendemail,
# #                 [ticket.get('email')],
# #                 f"IT Ticket {ticket_id} Closed",
# #                 f"""
# #                 <p>Dear {ticket.get('name')},</p>
# #                 <p>Your IT ticket <strong>{ticket_id}</strong> has been successfully resolved and closed.</p>
# #                 <p><strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
# #                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
# #                 <strong>Resolution Remark:</strong> {body.remark}</p>
# #                 <p><strong>Resolution Time:</strong> {tat_text}</p>
# #                 <p>If you face any further issues, please feel free to create a new ticket.</p>
# #                 <p>Regards,<br>JHS IT Helpdesk</p>
# #                 """
# #             )
            
# #             # Send closure confirmation to IT person
# #             it_email = ticket.get('itEmail') or body.itEmail
# #             if it_email:
# #                 background_tasks.add_task(
# #                     sendemail,
# #                     [it_email],
# #                     f"IT Ticket {ticket_id} Closed Confirmation",
# #                     f"""
# #                     <p>Dear {ticket.get('assigned', 'IT Team')},</p>
# #                     <p>You have successfully closed IT ticket <strong>{ticket_id}</strong>.</p>
# #                     <p><strong>Employee:</strong> {ticket.get('name')}<br>
# #                     <strong>Resolution Remark:</strong> {body.remark}<br>
# #                     <strong>Resolution Time:</strong> {tat_text}</p>
# #                     <p>Regards,<br>JHS IT Helpdesk</p>
# #                     """
# #                 )
# #         else:
# #             update_data["status"] = new_status
    
# #     if update_data:
# #         it_tickets.update_one({"id": ticket_id}, {"$set": update_data})
    
# #     return {"message": "Updated", "ticketId": ticket_id}

# # @app.delete("/api/it/tickets/{ticket_id}")
# # async def delete_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
# #     """Delete IT ticket"""
# #     res = it_tickets.delete_one({"id": ticket_id})
# #     if res.deleted_count == 0:
# #         raise HTTPException(status_code=404, detail="Ticket not found")
# #     return {"detail": "Deleted"}

# # @app.get("/api/it/tickets/stats")
# # async def get_it_stats(admin=Depends(get_current_admin)):
# #     """Get IT ticket statistics"""
# #     tickets = list(it_tickets.find({}, {"_id": 0, "status": 1, "assigned": 1}))
# #     total = len(tickets)
# #     by_status = {}
# #     by_it = {}
    
# #     for t in tickets:
# #         s = t.get("status", "Open")
# #         by_status[s] = by_status.get(s, 0) + 1
        
# #         it_person = t.get("assigned", "Unassigned")
# #         if it_person not in by_it:
# #             by_it[it_person] = {"Open": 0, "Closed": 0}
# #         by_it[it_person][s] = by_it[it_person].get(s, 0) + 1
    
# #     return {
# #         "total": total,
# #         "by_status": by_status,
# #         "by_it": by_it
# #     }

# # # ==================== FRONTEND ROUTES ====================

# # @app.get("/", response_class=HTMLResponse)
# # async def read_root():
# #     """HR helpdesk homepage"""
# #     return FileResponse("static/index.html")

# # @app.get("/admin", response_class=FileResponse)
# # async def hr_admin_page():
# #     """HR admin dashboard"""
# #     return FileResponse("static/hradmin.html")

# # @app.get("/it-admin", response_class=FileResponse)
# # async def it_admin_page():
# #     """IT admin dashboard"""
# #     return FileResponse("static/it-admin.html")

# # @app.get("/adminlogin", response_class=HTMLResponse)
# # async def admin_login_page():
# #     """Unified admin login page"""
# #     with open("static/adminlogin.html", "r", encoding="utf-8") as f:
# #         return f.read()

# # @app.get("/.well-known/{path:path}")
# # async def ignore_well_known(path: str):
# #     return {}

# # # ==================== HEALTH CHECK ====================

# # @app.get("/health")
# # async def health_check():
# #     """Health check endpoint"""
# #     return {
# #         "status": "healthy",
# #         "timestamp": datetime.utcnow().isoformat(),
# #         "databases": {
# #             "hr_tickets": hr_tickets.count_documents({}),
# #             "it_tickets": it_tickets.count_documents({})
# #         }
# #     }

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)





# from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel, EmailStr
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# from typing import Optional, Dict, Any, List
# from dotenv import load_dotenv
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import logging
# import hashlib
# from jose import JWTError, jwt

# # Load environment
# load_dotenv()

# # FastAPI app
# app = FastAPI(title="JHS Unified Helpdesk API")
# print("🚀 JHS Unified Helpdesk API Running")

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Config
# SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# SMTP_USER = os.getenv("SMTP_USER")
# SMTP_PASS = os.getenv("SMTP_PASS")

# # Database connections
# client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

# # HR Database
# hr_db = client["HR_Helpdesk"]
# hr_tickets = hr_db["Tickets"]
# hr_admins = hr_db["Admins"]

# # IT Database
# it_db = client["ithelpdesk"]
# it_tickets = it_db["tickets"]
# it_admins = it_db["admins"]
# it_sessions = it_db["sessions"]
# it_sequences = it_db["sequences"]

# # Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # HR Email Mapping
# HR_EMAILS = {
#     "PAYSLIP": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
#     "HRMS QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
#     "ATTENDANCE": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
#     "SALARY QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
#     "BUDDY REFERRAL": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"},
#     "OTHER": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"}
# }

# # IT Email list
# IT_EMAILS = ["orinaguha9@gmail.com", "it2@jhs.co.in", "it3@jhs.co.in"]

# # ==================== PYDANTIC MODELS ====================

# # HR Models
# class HRTicketCreate(BaseModel):
#     name: str
#     email: str
#     phone: Optional[str] = None
#     empCode: Optional[str] = None
#     category: str
#     issue: str

# class HRTicketUpdate(BaseModel):
#     assigned: Optional[str] = None
#     status: Optional[str] = None
#     hrEmail: Optional[str] = None
#     remark: Optional[str] = None

# # IT Models
# class ITTicketCreate(BaseModel):
#     name: str
#     email: EmailStr
#     phone: str  # Required
#     assetCode: Optional[str] = ""  # Made optional
#     empCode: Optional[str] = ""  # Optional
#     issues: List[str]  # Required list
#     issueDescription: str  # Required
#     reportingPartner: str  # Required

# class ITTicketUpdate(BaseModel):
#     assigned: Optional[str] = None
#     status: Optional[str] = None
#     itEmail: Optional[EmailStr] = None
#     remark: Optional[str] = None

# class AdminLogin(BaseModel):
#     empCode: str
#     password: str

# # ==================== UTILITY FUNCTIONS ====================

# def hash_password(password: str) -> str:
#     """Hash password using SHA256"""
#     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# def verify_password(plain: str, hashed: str) -> bool:
#     """Verify password against hash"""
#     return hash_password(plain) == hashed

# def create_access_token(data: dict):
#     """Create JWT access token"""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_current_admin(authorization: str = Header(None)):
#     """Verify JWT token and return admin info"""
#     if not authorization or not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing token")
    
#     token = authorization.split(" ")[1]
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("role") != "admin":
#             raise HTTPException(status_code=403, detail="Not authorized")
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")

# def sendemail(recipients: List[str], subject: str, body: str):
#     """Send email to recipients"""
#     logger.info(f"🔄 EMAIL → {recipients}, {subject}")
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = SMTP_USER
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'html'))
        
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASS)
        
#         valid_recipients = [r for r in recipients if r and r.strip()]
#         if valid_recipients:
#             server.sendmail(SMTP_USER, valid_recipients, msg.as_string())
#             logger.info(f"✅ EMAILS SENT → {valid_recipients}")
#         server.quit()
#     except Exception as e:
#         logger.error(f"❌ EMAIL FAILED → {str(e)}")

# # ==================== AUTHENTICATION ROUTES ====================

# @app.post("/api/admin/login")
# async def unified_admin_login(body: AdminLogin):
#     """
#     Unified login endpoint for both HR and IT admins.
#     First checks HR admins, then IT admins.
#     """
#     empCode = body.empCode.upper().strip()
#     password = body.password
    
#     if not empCode or not password:
#         raise HTTPException(status_code=400, detail="empCode and password required")
    
#     logger.info(f"Login attempt for empCode: {empCode}")
    
#     # Try HR admin first
#     hr_admin = hr_admins.find_one({"empCodes": empCode, "password": password})
    
#     if hr_admin:
#         logger.info(f"HR Admin found: {hr_admin.get('name')}")
#         token = create_access_token({
#             "sub": empCode,
#             "role": "admin",
#             "type": "hr",
#             "name": hr_admin.get("name")
#         })
        
#         return {
#             "access_token": token,
#             "token_type": "bearer",
#             "name": hr_admin.get("name"),
#             "helpdesk": "hr"
#         }
    
#     # Try IT admin
#     it_admin = it_admins.find_one({"empCode": empCode})
    
#     if it_admin:
#         logger.info(f"IT Admin found: {it_admin.get('name')}")
        
#         # Verify password
#         if not verify_password(password, it_admin["password"]):
#             logger.error("Password verification failed")
#             raise HTTPException(status_code=401, detail="Invalid password")
        
#         logger.info("Password verified successfully")
        
#         token = create_access_token({
#             "sub": empCode,
#             "role": "admin",
#             "type": "it",
#             "name": it_admin.get("name")
#         })
        
#         # Store session in IT sessions collection
#         session_doc = {
#             "empCode": empCode,
#             "token": token,
#             "isValid": True,
#             "createdAt": datetime.utcnow(),
#             "expiresAt": datetime.utcnow() + timedelta(hours=1)
#         }
        
#         it_sessions.update_one(
#             {"empCode": empCode},
#             {"$set": session_doc},
#             upsert=True
#         )
        
#         logger.info(f"Login successful for IT admin {empCode}")
        
#         return {
#             "access_token": token,
#             "token": token,  # For backward compatibility
#             "token_type": "bearer",
#             "empCode": empCode,
#             "name": it_admin.get("name"),
#             "helpdesk": "it"
#         }
    
#     # No admin found
#     logger.error(f"Admin not found for empCode: {empCode}")
#     raise HTTPException(status_code=401, detail="Invalid credentials")

# # ==================== HR TICKET ROUTES (with /api/hr/ prefix) ====================

# @app.get("/api/hr/tickets")
# async def get_hr_tickets(admin=Depends(get_current_admin)):
#     """Get all HR tickets"""
#     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# @app.post("/api/hr/tickets")
# async def create_hr_ticket(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
#     """Create new HR ticket"""
#     count = hr_tickets.count_documents({})
#     ticket_id = f"TICKJHSHR{str(count + 1).zfill(2)}"
    
#     category = ticket.category.upper().strip()
#     hr_data = HR_EMAILS.get(category)
#     assigned_name = hr_data["name"] if hr_data else "Unassigned"
#     assigned_email = hr_data["email"] if hr_data else None
    
#     ticket_data = {
#         "id": ticket_id, "name": ticket.name, "email": ticket.email,
#         "phone": ticket.phone, "empCode": ticket.empCode,
#         "category": ticket.category, "issue": ticket.issue,
#         "status": "Open", "assigned": assigned_name, "hrEmail": assigned_email,
#         "assignedAt": datetime.utcnow() if hr_data else None,
#         "createdAt": datetime.utcnow(), "remark": ""
#     }
    
#     hr_tickets.insert_one(ticket_data)
    
#     # Send emails
#     background_tasks.add_task(
#         sendemail, [ticket.email],
#         f"JHS HR - Ticket {ticket_id} Created",
#         f"<p>Dear {ticket.name},</p><p>Your ticket {ticket_id} created.</p><p>Category: {ticket.category}<br>Assigned: {assigned_name}</p><p>JHS HR Team</p>"
#     )
    
#     if assigned_email:
#         background_tasks.add_task(
#             sendemail, [assigned_email],
#             f"New Ticket: {ticket_id}",
#             f"<p>Dear {assigned_name},</p><p>Ticket {ticket_id} assigned to you.</p><p>Employee: {ticket.name}<br>Issue: {ticket.issue}</p>"
#         )
    
#     return {"message": "Ticket created", "ticketId": ticket_id, "assignedTo": assigned_name}

# @app.get("/api/hr/tickets/{ticketid}")
# async def get_single_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
#     """Get single HR ticket by ID"""
#     ticket = hr_tickets.find_one({"id": ticketid})
#     if not ticket:
#         raise HTTPException(404, "Ticket not found")
#     ticket.pop("_id", None)
#     return ticket

# @app.put("/api/hr/tickets/{ticketid}")
# async def update_hr_ticket(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Update HR ticket"""
#     ticket = hr_tickets.find_one({"id": ticketid})
#     if not ticket: 
#         raise HTTPException(404, "Ticket not found")
    
#     update_data = {}
#     old_assigned = ticket.get("assigned")
#     old_status = ticket.get("status", "").lower()
    
#     # Handle reassignment
#     if body.assigned and body.assigned != old_assigned:
#         update_data["assigned"] = body.assigned
#         update_data["assignedAt"] = datetime.utcnow()
#         if body.hrEmail: 
#             update_data["hrEmail"] = body.hrEmail
        
#         # Send reassignment email to new HR person
#         if body.hrEmail:
#             background_tasks.add_task(
#                 sendemail,
#                 [body.hrEmail],
#                 f"HR Ticket {ticketid} Assigned to You",
#                 f"""
#                 <p>Dear {body.assigned},</p>
#                 <p>The ticket <strong>{ticketid}</strong> has been assigned to you.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Category:</strong> {ticket.get('category')}<br>
#                 <strong>Issue:</strong> {ticket.get('issue')}</p>
#                 <p>Please review and take necessary action.</p>
#                 <p>Regards,<br>JHS HR Helpdesk</p>
#                 """
#             )
    
#     # Handle closure
#     if body.status and body.status.lower() == "closed" and old_status != "closed":
#         update_data["status"] = "Closed"
#         update_data["closedAt"] = datetime.utcnow()
#         update_data["remark"] = body.remark if body.remark else ""
        
#         # Send closure email to employee
#         background_tasks.add_task(
#             sendemail,
#             [ticket.get('email')],
#             f"HR Ticket {ticketid} Closed",
#             f"""
#             <p>Dear {ticket.get('name')},</p>
#             <p>Your HR ticket <strong>{ticketid}</strong> has been closed.</p>
#             <p><strong>Category:</strong> {ticket.get('category')}<br>
#             <strong>Issue:</strong> {ticket.get('issue')}<br>
#             <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
#             <p>If you have any further questions, please feel free to create a new ticket.</p>
#             <p>Regards,<br>JHS HR Team</p>
#             """
#         )
        
#         # Send closure confirmation to HR person
#         hr_email = ticket.get('hrEmail')
#         if hr_email:
#             background_tasks.add_task(
#                 sendemail,
#                 [hr_email],
#                 f"HR Ticket {ticketid} Closed Confirmation",
#                 f"""
#                 <p>Dear {ticket.get('assigned', 'HR Team')},</p>
#                 <p>You have successfully closed ticket <strong>{ticketid}</strong>.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
#                 <p>Regards,<br>JHS HR Helpdesk</p>
#                 """
#             )
    
#     if update_data:
#         hr_tickets.update_one({"id": ticketid}, {"$set": update_data})
    
#     return {"message": "Updated", "ticketId": ticketid}

# @app.delete("/api/hr/tickets/{ticketid}")
# async def delete_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
#     """Delete HR ticket"""
#     result = hr_tickets.delete_one({"id": ticketid})
#     if result.deleted_count == 0: 
#         raise HTTPException(404, "Ticket not found")
#     return {"message": "Deleted"}

# @app.get("/api/hr/admin/stats")
# async def get_hr_stats(admin=Depends(get_current_admin)):
#     """Get HR ticket statistics"""
#     tickets = list(hr_tickets.find({}, {"_id": 0}))
#     stats = {"total": len(tickets), "bystatus": {"Open": 0, "Closed": 0}, "byhr": {}}
    
#     for t in tickets:
#         status = t.get("status", "Open")
#         hr = t.get("assigned", "Unassigned")
#         stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
#         if hr not in stats["byhr"]:
#             stats["byhr"][hr] = {"Open": 0, "Closed": 0}
#         stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
#     return stats

# # ==================== LEGACY HR ROUTES (for backward compatibility) ====================
# # These maintain compatibility with existing HR frontend that uses /api/tickets

# @app.get("/api/tickets")
# async def get_hr_tickets_legacy(admin=Depends(get_current_admin)):
#     """Legacy HR route - Get all HR tickets"""
#     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# @app.post("/api/tickets")
# async def create_hr_ticket_legacy(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
#     """Legacy HR route - Create new HR ticket"""
#     return await create_hr_ticket(ticket, background_tasks)

# @app.get("/api/tickets/{ticketid}")
# async def get_single_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
#     """Legacy HR route - Get single HR ticket"""
#     return await get_single_hr_ticket(ticketid, admin)

# @app.put("/api/tickets/{ticketid}")
# async def update_hr_ticket_legacy(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Legacy HR route - Update HR ticket"""
#     return await update_hr_ticket(ticketid, body, background_tasks, admin)

# @app.delete("/api/tickets/{ticketid}")
# async def delete_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
#     """Legacy HR route - Delete HR ticket"""
#     return await delete_hr_ticket(ticketid, admin)

# @app.get("/api/admin/stats")
# async def get_hr_stats_legacy(admin=Depends(get_current_admin)):
#     """Legacy HR route - Get HR statistics"""
#     return await get_hr_stats(admin)

# # ==================== IT TICKET ROUTES (with /api/it/ prefix) ====================
# # IMPORTANT: Stats route MUST come before the dynamic {ticket_id} route

# @app.get("/api/it/tickets")
# async def get_it_tickets(admin=Depends(get_current_admin)):
#     """Get all IT tickets"""
#     tickets_list = list(it_tickets.find({}, {"_id": 0}))
    
#     # Calculate TAT for closed tickets
#     for ticket in tickets_list:
#         if ticket.get('assignedAt') and ticket.get('closedAt'):
#             try:
#                 assigned_time = ticket['assignedAt']
#                 closed_time = ticket['closedAt']
#                 if isinstance(assigned_time, datetime) and isinstance(closed_time, datetime):
#                     tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
#                     ticket['tatHours'] = f"{tat_hours} hrs"
#             except:
#                 ticket['tatHours'] = "-"
#         else:
#             ticket['tatHours'] = "-"
    
#     return tickets_list

# @app.get("/api/it/tickets/stats")
# async def get_it_stats(admin=Depends(get_current_admin)):
#     """Get IT ticket statistics - MUST be before /{ticket_id} route"""
#     tickets = list(it_tickets.find({}, {"_id": 0, "status": 1, "assigned": 1}))
#     total = len(tickets)
#     by_status = {}
#     by_it = {}
    
#     for t in tickets:
#         s = t.get("status", "Open")
#         by_status[s] = by_status.get(s, 0) + 1
        
#         it_person = t.get("assigned", "Unassigned")
#         if it_person not in by_it:
#             by_it[it_person] = {"Open": 0, "Closed": 0}
#         by_it[it_person][s] = by_it[it_person].get(s, 0) + 1
    
#     return {
#         "total": total,
#         "byStatus": by_status,
#         "byIT": by_it
#     }

# @app.post("/api/it/tickets")
# async def create_it_ticket(ticket: ITTicketCreate, background_tasks: BackgroundTasks):
#     """Create new IT ticket"""
#     sequence = it_sequences.find_one_and_update(
#         {"_id": "ticket_counter"},
#         {"$inc": {"seq": 1}},
#         upsert=True, return_document=True
#     )
#     count = sequence['seq']
#     ticket_id = f"TICKJHSIT{str(count).zfill(1)}"
    
#     doc = {
#         "id": ticket_id,
#         "name": ticket.name,
#         "email": ticket.email,
#         "phone": ticket.phone,
#         "empCode": ticket.empCode,
#         "assetCode": ticket.assetCode,
#         "issues": ticket.issues,
#         "issueDescription": ticket.issueDescription,
#         "reportingPartner": ticket.reportingPartner,
#         "status": "Open",
#         "assigned": "Unassigned",
#         "itEmail": None,
#         "createdAt": datetime.utcnow(),
#         "assignedAt": None,
#         "remark": None,
#         "closedAt": None
#     }
    
#     it_tickets.insert_one(doc)
    
#     # Send email
#     background_tasks.add_task(
#         sendemail,
#         [ticket.email] + IT_EMAILS,
#         f"IT Ticket {ticket_id} Created",
#         f"<p>Dear {ticket.name},</p><p>Your IT ticket <strong>{ticket_id}</strong> has been created.</p><p><strong>IT Asset:</strong> {ticket.assetCode}</p><p><strong>Issues:</strong> {', '.join(ticket.issues)}</p><p>Regards,<br>JHS IT Helpdesk</p>"
#     )
    
#     return {k: v for k, v in doc.items() if k != '_id'}

# @app.get("/api/it/tickets/{ticket_id}")
# async def get_single_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
#     """Get single IT ticket by ID"""
#     ticket = it_tickets.find_one({"id": ticket_id}, {"_id": 0})
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#     return ticket

# @app.put("/api/it/tickets/{ticket_id}")
# async def update_it_ticket(ticket_id: str, body: ITTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Update IT ticket"""
#     ticket = it_tickets.find_one({"id": ticket_id})
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
    
#     update_data = {}
#     old_assigned = ticket.get("assigned")
#     old_status = ticket.get("status", "").lower()
    
#     # Handle assignment
#     if body.assigned is not None and body.assigned != old_assigned:
#         update_data["assigned"] = body.assigned
        
#         # Set assignedAt timestamp if not already set
#         if not ticket.get("assignedAt"):
#             update_data["assignedAt"] = datetime.utcnow()
        
#         # Send assignment email to IT person
#         if body.itEmail:
#             update_data["itEmail"] = body.itEmail
#             background_tasks.add_task(
#                 sendemail,
#                 [body.itEmail],
#                 f"IT Ticket {ticket_id} Assigned to You",
#                 f"""
#                 <p>Dear {body.assigned},</p>
#                 <p>The IT ticket <strong>{ticket_id}</strong> has been assigned to you.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
#                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
#                 <strong>Description:</strong> {ticket.get('issueDescription')}</p>
#                 <p>Please review and take necessary action.</p>
#                 <p>Regards,<br>JHS IT Helpdesk</p>
#                 """
#             )
        
#         # Notify employee about assignment
#         background_tasks.add_task(
#             sendemail,
#             [ticket.get('email')],
#             f"IT Ticket {ticket_id} Assigned",
#             f"""
#             <p>Dear {ticket.get('name')},</p>
#             <p>Your IT ticket <strong>{ticket_id}</strong> has been assigned to <strong>{body.assigned}</strong>.</p>
#             <p>Our team is working on resolving your issue.</p>
#             <p>Regards,<br>JHS IT Helpdesk</p>
#             """
#         )
#     elif body.itEmail is not None:
#         update_data["itEmail"] = body.itEmail
    
#     # Handle status change and closure
#     if body.status:
#         new_status = body.status.capitalize()
        
#         if new_status == "Closed" and old_status != "closed":
#             # Remark is mandatory when closing
#             if not body.remark or not body.remark.strip():
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Remark is mandatory when closing a ticket"
#                 )
            
#             update_data["status"] = "Closed"
#             update_data["remark"] = body.remark.strip()
#             update_data["closedAt"] = datetime.utcnow()
            
#             # Calculate TAT if assignedAt exists
#             tat_text = "N/A"
#             if ticket.get("assignedAt"):
#                 try:
#                     assigned_time = ticket['assignedAt']
#                     closed_time = update_data["closedAt"]
#                     if isinstance(assigned_time, datetime):
#                         tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
#                         tat_text = f"{tat_hours} hours"
#                 except:
#                     tat_text = "N/A"
            
#             # Send closure email to employee
#             background_tasks.add_task(
#                 sendemail,
#                 [ticket.get('email')],
#                 f"IT Ticket {ticket_id} Closed",
#                 f"""
#                 <p>Dear {ticket.get('name')},</p>
#                 <p>Your IT ticket <strong>{ticket_id}</strong> has been successfully resolved and closed.</p>
#                 <p><strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
#                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
#                 <strong>Resolution Remark:</strong> {body.remark}</p>
#                 <p><strong>Resolution Time:</strong> {tat_text}</p>
#                 <p>If you face any further issues, please feel free to create a new ticket.</p>
#                 <p>Regards,<br>JHS IT Helpdesk</p>
#                 """
#             )
            
#             # Send closure confirmation to IT person
#             it_email = ticket.get('itEmail') or body.itEmail
#             if it_email:
#                 background_tasks.add_task(
#                     sendemail,
#                     [it_email],
#                     f"IT Ticket {ticket_id} Closed Confirmation",
#                     f"""
#                     <p>Dear {ticket.get('assigned', 'IT Team')},</p>
#                     <p>You have successfully closed IT ticket <strong>{ticket_id}</strong>.</p>
#                     <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                     <strong>Resolution Remark:</strong> {body.remark}<br>
#                     <strong>Resolution Time:</strong> {tat_text}</p>
#                     <p>Regards,<br>JHS IT Helpdesk</p>
#                     """
#                 )
#         else:
#             update_data["status"] = new_status
    
#     if update_data:
#         it_tickets.update_one({"id": ticket_id}, {"$set": update_data})
    
#     return {"message": "Updated", "ticketId": ticket_id}

# @app.delete("/api/it/tickets/{ticket_id}")
# async def delete_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
#     """Delete IT ticket"""
#     res = it_tickets.delete_one({"id": ticket_id})
#     if res.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#     return {"detail": "Deleted"}

# # ==================== FRONTEND ROUTES ====================

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     """HR helpdesk homepage"""
#     return FileResponse("static/index.html")

# @app.get("/admin", response_class=FileResponse)
# async def hr_admin_page():
#     """HR admin dashboard"""
#     return FileResponse("static/hradmin.html")

# @app.get("/it-admin", response_class=FileResponse)
# async def it_admin_page():
#     """IT admin dashboard"""
#     return FileResponse("static/it-admin.html")

# @app.get("/adminlogin", response_class=HTMLResponse)
# async def admin_login_page():
#     """Unified admin login page"""
#     with open("static/adminlogin.html", "r", encoding="utf-8") as f:
#         return f.read()

# @app.get("/.well-known/{path:path}")
# async def ignore_well_known(path: str):
#     return {}

# @app.get("/favicon.ico")
# async def favicon():
#     """Return favicon or 204 No Content"""
#     try:
#         return FileResponse("static/favicon.ico")
#     except:
#         return HTMLResponse(status_code=204)

# # ==================== HEALTH CHECK ====================

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "timestamp": datetime.utcnow().isoformat(),
#         "databases": {
#             "hr_tickets": hr_tickets.count_documents({}),
#             "it_tickets": it_tickets.count_documents({})
#         }
#     }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)




# from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel, EmailStr
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# from typing import Optional, Dict, Any, List
# from dotenv import load_dotenv
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import logging
# import hashlib
# from jose import JWTError, jwt

# # Load environment
# load_dotenv()

# # FastAPI app
# app = FastAPI(title="JHS Unified Helpdesk API")
# print("🚀 JHS Unified Helpdesk API Running")

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Config
# SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# SMTP_SERVER = "sandbox.smtp.mailtrap.io"
# SMTP_PORT = 2525
# SMTP_USER = os.getenv("SMTP_USER")
# SMTP_PASS = os.getenv("SMTP_PASS")

# # Database connections
# client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

# # HR Database
# # hr_db = client["HR_Helpdesk"]
# # hr_tickets = hr_db["Tickets"]
# # hr_admins = hr_db["Admins"]
# # HR Database
# hr_db = client["HR_Helpdesk"]
# hr_tickets = hr_db["Tickets"]
# hr_admins = hr_db["Admins"]
# hr_sequences = hr_db["sequences"]   # NEW


# # IT Database
# it_db = client["ithelpdesk"]
# it_tickets = it_db["tickets"]
# it_admins = it_db["admins"]
# it_sessions = it_db["sessions"]
# it_sequences = it_db["sequences"]

# # Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # HR Email Mapping
# HR_EMAILS = {
#     "PAYSLIP": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "HRMS QUERY": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "ATTENDANCE": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "SALARY QUERY": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "BUDDY REFERRAL": {"name": "Krutika Shivshivkar", "email": "orina.guha@jhsassociates.in"},
#     "OTHER": {"name": "Krutika Shivshivkar", "email": "orina.guha@jhsassociates.in"}
# }

# # IT Email list
# IT_EMAILS = ["orina.guha@jhsassociates.in", "orina.guha2005@gmail.com"]

# # ==================== PYDANTIC MODELS ====================

# # HR Models
# class HRTicketCreate(BaseModel):
#     name: str
#     email: str
#     phone: Optional[str] = None
#     empCode: Optional[str] = None
#     category: str
#     issue: str

# class HRTicketUpdate(BaseModel):
#     assigned: Optional[str] = None
#     status: Optional[str] = None
#     hrEmail: Optional[str] = None
#     remark: Optional[str] = None

# # IT Models
# class ITTicketCreate(BaseModel):
#     name: str
#     email: EmailStr
#     phone: str  # Required
#     assetCode: Optional[str] = ""  # Made optional
#     empCode: Optional[str] = ""  # Optional
#     issues: List[str]  # Required list
#     issueDescription: str  # Required
#     reportingPartner: str  # Required

# class ITTicketUpdate(BaseModel):
#     assigned: Optional[str] = None
#     status: Optional[str] = None
#     itEmail: Optional[EmailStr] = None
#     remark: Optional[str] = None

# class AdminLogin(BaseModel):
#     empCode: str
#     password: str

# # ==================== UTILITY FUNCTIONS ====================

# def hash_password(password: str) -> str:
#     """Hash password using SHA256"""
#     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# def verify_password(plain: str, hashed: str) -> bool:
#     """Verify password against hash"""
#     return hash_password(plain) == hashed

# def create_access_token(data: dict):
#     """Create JWT access token"""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_current_admin(authorization: str = Header(None)):
#     """Verify JWT token and return admin info"""
#     if not authorization or not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing token")
    
#     token = authorization.split(" ")[1]
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("role") != "admin":
#             raise HTTPException(status_code=403, detail="Not authorized")
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")

# def sendemail(recipients: List[str], subject: str, body: str):
#     """Send email to recipients"""
#     logger.info(f"🔄 EMAIL → {recipients}, {subject}")
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = SMTP_USER
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'html'))
        
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASS)
        
#         valid_recipients = [r for r in recipients if r and r.strip()]
#         if valid_recipients:
#             server.sendmail(SMTP_USER, valid_recipients, msg.as_string())
#             logger.info(f"✅ EMAILS SENT → {valid_recipients}")
#         server.quit()
#     except Exception as e:
#         logger.error(f"❌ EMAIL FAILED → {str(e)}")

# # ==================== AUTHENTICATION ROUTES ====================

# @app.post("/api/admin/login")
# async def unified_admin_login(body: AdminLogin):
#     """
#     Unified login endpoint for both HR and IT admins.
#     First checks HR admins, then IT admins.
#     """
#     empCode = body.empCode.upper().strip()
#     password = body.password
    
#     if not empCode or not password:
#         raise HTTPException(status_code=400, detail="empCode and password required")
    
#     logger.info(f"Login attempt for empCode: {empCode}")
    
#     # Try HR admin first
#     hr_admin = hr_admins.find_one({"empCodes": empCode, "password": password})
    
#     if hr_admin:
#         logger.info(f"HR Admin found: {hr_admin.get('name')}")
#         token = create_access_token({
#             "sub": empCode,
#             "role": "admin",
#             "type": "hr",
#             "name": hr_admin.get("name")
#         })
        
#         return {
#             "access_token": token,
#             "token_type": "bearer",
#             "name": hr_admin.get("name"),
#             "helpdesk": "hr"
#         }
    
#     # Try IT admin
#     it_admin = it_admins.find_one({"empCode": empCode})
    
#     if it_admin:
#         logger.info(f"IT Admin found: {it_admin.get('name')}")
        
#         # Verify password
#         if not verify_password(password, it_admin["password"]):
#             logger.error("Password verification failed")
#             raise HTTPException(status_code=401, detail="Invalid password")
        
#         logger.info("Password verified successfully")
        
#         token = create_access_token({
#             "sub": empCode,
#             "role": "admin",
#             "type": "it",
#             "name": it_admin.get("name")
#         })
        
#         # Store session in IT sessions collection
#         session_doc = {
#             "empCode": empCode,
#             "token": token,
#             "isValid": True,
#             "createdAt": datetime.utcnow(),
#             "expiresAt": datetime.utcnow() + timedelta(hours=1)
#         }
        
#         it_sessions.update_one(
#             {"empCode": empCode},
#             {"$set": session_doc},
#             upsert=True
#         )
        
#         logger.info(f"Login successful for IT admin {empCode}")
        
#         return {
#             "access_token": token,
#             "token": token,  # For backward compatibility
#             "token_type": "bearer",
#             "empCode": empCode,
#             "name": it_admin.get("name"),
#             "helpdesk": "it"
#         }
    
#     # No admin found
#     logger.error(f"Admin not found for empCode: {empCode}")
#     raise HTTPException(status_code=401, detail="Invalid credentials")

# # ==================== HR TICKET ROUTES (with /api/hr/ prefix) ====================

# @app.get("/api/hr/tickets")
# async def get_hr_tickets(admin=Depends(get_current_admin)):
#     """Get all HR tickets"""
#     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# @app.post("/api/hr/tickets")
# async def create_hr_ticket(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
#     """Create new HR ticket"""
#     # count = hr_tickets.count_documents({})
#     # ticket_id = f"TICKJHSHR{str(count + 1).zfill(2)}"
#     sequence = hr_sequences.find_one_and_update(
#     {"_id": "hr_ticket_counter"},
#     {"$inc": {"seq": 1}},
#     upsert=True,
#     return_document=True
#     )

#     count = sequence["seq"]
#     ticket_id = f"TICKJHSHR{str(count).zfill(2)}"
    
    
#     category = ticket.category.upper().strip()
#     hr_data = HR_EMAILS.get(category)
#     assigned_name = hr_data["name"] if hr_data else "Unassigned"
#     assigned_email = hr_data["email"] if hr_data else None
    
#     ticket_data = {
#         "id": ticket_id, "name": ticket.name, "email": ticket.email,
#         "phone": ticket.phone, "empCode": ticket.empCode,
#         "category": ticket.category, "issue": ticket.issue,
#         "status": "Open", "assigned": assigned_name, "hrEmail": assigned_email,
#         "assignedAt": datetime.utcnow() if hr_data else None,
#         "createdAt": datetime.utcnow(), "remark": ""
#     }
    
#     hr_tickets.insert_one(ticket_data)
    
#     # Send emails
#     background_tasks.add_task(
#         sendemail, [ticket.email],
#         f"JHS HR - Ticket {ticket_id} Created",
#         f"<p>Dear {ticket.name},</p><p>Your ticket {ticket_id} created.</p><p>Category: {ticket.category}<br>Assigned: {assigned_name}</p><p>JHS HR Team</p>"
#     )
    
#     if assigned_email:
#         background_tasks.add_task(
#             sendemail, [assigned_email],
#             f"New Ticket: {ticket_id}",
#             f"<p>Dear {assigned_name},</p><p>Ticket {ticket_id} assigned to you.</p><p>Employee: {ticket.name}<br>Issue: {ticket.issue}</p>"
#         )
    
#     return {"message": "Ticket created", "ticketId": ticket_id, "assignedTo": assigned_name}

# @app.get("/api/hr/tickets/{ticketid}")
# async def get_single_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
#     """Get single HR ticket by ID"""
#     ticket = hr_tickets.find_one({"id": ticketid})
#     if not ticket:
#         raise HTTPException(404, "Ticket not found")
#     ticket.pop("_id", None)
#     return ticket

# @app.put("/api/hr/tickets/{ticketid}")
# async def update_hr_ticket(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Update HR ticket"""
#     ticket = hr_tickets.find_one({"id": ticketid})
#     if not ticket: 
#         raise HTTPException(404, "Ticket not found")
    
#     update_data = {}
#     old_assigned = ticket.get("assigned")
#     old_status = ticket.get("status", "").lower()
    
#     # Handle reassignment
#     if body.assigned and body.assigned != old_assigned:
#         update_data["assigned"] = body.assigned
#         update_data["assignedAt"] = datetime.utcnow()
#         if body.hrEmail: 
#             update_data["hrEmail"] = body.hrEmail
        
#         # Send reassignment email to new HR person
#         if body.hrEmail:
#             background_tasks.add_task(
#                 sendemail,
#                 [body.hrEmail],
#                 f"HR Ticket {ticketid} Assigned to You",
#                 f"""
#                 <p>Dear {body.assigned},</p>
#                 <p>The ticket <strong>{ticketid}</strong> has been assigned to you.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Category:</strong> {ticket.get('category')}<br>
#                 <strong>Issue:</strong> {ticket.get('issue')}</p>
#                 <p>Please review and take necessary action.</p>
#                 <p>Regards,<br>JHS HR Helpdesk</p>
#                 """
#             )
    
#     # Handle closure
#     if body.status and body.status.lower() == "closed" and old_status != "closed":
#         update_data["status"] = "Closed"
#         update_data["closedAt"] = datetime.utcnow()
#         update_data["remark"] = body.remark if body.remark else ""
        
#         # Send closure email to employee
#         background_tasks.add_task(
#             sendemail,
#             [ticket.get('email')],
#             f"HR Ticket {ticketid} Closed",
#             f"""
#             <p>Dear {ticket.get('name')},</p>
#             <p>Your HR ticket <strong>{ticketid}</strong> has been closed.</p>
#             <p><strong>Category:</strong> {ticket.get('category')}<br>
#             <strong>Issue:</strong> {ticket.get('issue')}<br>
#             <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
#             <p>If you have any further questions, please feel free to create a new ticket.</p>
#             <p>Regards,<br>JHS HR Team</p>
#             """
#         )
        
#         # Send closure confirmation to HR person
#         hr_email = ticket.get('hrEmail')
#         if hr_email:
#             background_tasks.add_task(
#                 sendemail,
#                 [hr_email],
#                 f"HR Ticket {ticketid} Closed Confirmation",
#                 f"""
#                 <p>Dear {ticket.get('assigned', 'HR Team')},</p>
#                 <p>You have successfully closed ticket <strong>{ticketid}</strong>.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
#                 <p>Regards,<br>JHS HR Helpdesk</p>
#                 """
#             )
    
#     if update_data:
#         hr_tickets.update_one({"id": ticketid}, {"$set": update_data})
    
#     return {"message": "Updated", "ticketId": ticketid}

# @app.delete("/api/hr/tickets/{ticketid}")
# async def delete_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
#     """Delete HR ticket"""
#     result = hr_tickets.delete_one({"id": ticketid})
#     if result.deleted_count == 0: 
#         raise HTTPException(404, "Ticket not found")
#     return {"message": "Deleted"}

# @app.get("/api/hr/admin/stats")
# async def get_hr_stats(admin=Depends(get_current_admin)):
#     """Get HR ticket statistics"""
#     tickets = list(hr_tickets.find({}, {"_id": 0}))
#     stats = {"total": len(tickets), "bystatus": {"Open": 0, "Closed": 0}, "byhr": {}}
    
#     for t in tickets:
#         status = t.get("status", "Open")
#         hr = t.get("assigned", "Unassigned")
#         stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
#         if hr not in stats["byhr"]:
#             stats["byhr"][hr] = {"Open": 0, "Closed": 0}
#         stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
#     return stats

# # ==================== LEGACY HR ROUTES (for backward compatibility) ====================
# # These maintain compatibility with existing HR frontend that uses /api/tickets

# @app.get("/api/tickets")
# async def get_hr_tickets_legacy(admin=Depends(get_current_admin)):
#     """Legacy HR route - Get all HR tickets"""
#     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# @app.post("/api/tickets")
# async def create_hr_ticket_legacy(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
#     """Legacy HR route - Create new HR ticket"""
#     return await create_hr_ticket(ticket, background_tasks)

# @app.get("/api/tickets/{ticketid}")
# async def get_single_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
#     """Legacy HR route - Get single HR ticket"""
#     return await get_single_hr_ticket(ticketid, admin)

# @app.put("/api/tickets/{ticketid}")
# async def update_hr_ticket_legacy(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Legacy HR route - Update HR ticket"""
#     return await update_hr_ticket(ticketid, body, background_tasks, admin)

# @app.delete("/api/tickets/{ticketid}")
# async def delete_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
#     """Legacy HR route - Delete HR ticket"""
#     return await delete_hr_ticket(ticketid, admin)

# @app.get("/api/admin/stats")
# async def get_hr_stats_legacy(admin=Depends(get_current_admin)):
#     """Legacy HR route - Get HR statistics"""
#     return await get_hr_stats(admin)

# # ==================== IT TICKET ROUTES (with /api/it/ prefix) ====================
# # IMPORTANT: Stats route MUST come before the dynamic {ticket_id} route

# @app.get("/api/it/tickets")
# async def get_it_tickets(admin=Depends(get_current_admin)):
#     """Get all IT tickets"""
#     tickets_list = list(it_tickets.find({}, {"_id": 0}))
    
#     # Calculate TAT for closed tickets
#     for ticket in tickets_list:
#         if ticket.get('assignedAt') and ticket.get('closedAt'):
#             try:
#                 assigned_time = ticket['assignedAt']
#                 closed_time = ticket['closedAt']
#                 if isinstance(assigned_time, datetime) and isinstance(closed_time, datetime):
#                     tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
#                     ticket['tatHours'] = f"{tat_hours} hrs"
#             except:
#                 ticket['tatHours'] = "-"
#         else:
#             ticket['tatHours'] = "-"
    
#     return tickets_list

# @app.get("/api/it/tickets/stats")
# async def get_it_stats(admin=Depends(get_current_admin)):
#     """Get IT ticket statistics - MUST be before /{ticket_id} route"""
#     tickets = list(it_tickets.find({}, {"_id": 0, "status": 1, "assigned": 1}))
#     total = len(tickets)
#     by_status = {}
#     by_it = {}
    
#     for t in tickets:
#         s = t.get("status", "Open")
#         by_status[s] = by_status.get(s, 0) + 1
        
#         it_person = t.get("assigned", "Unassigned")
#         if it_person not in by_it:
#             by_it[it_person] = {"Open": 0, "Closed": 0}
#         by_it[it_person][s] = by_it[it_person].get(s, 0) + 1
    
#     return {
#         "total": total,
#         "byStatus": by_status,
#         "byIT": by_it
#     }

# @app.post("/api/it/tickets")
# async def create_it_ticket(ticket: ITTicketCreate, background_tasks: BackgroundTasks):
#     """Create new IT ticket"""
#     sequence = it_sequences.find_one_and_update(
#         {"_id": "ticket_counter"},
#         {"$inc": {"seq": 1}},
#         upsert=True, return_document=True
#     )
#     count = sequence['seq']
#     ticket_id = f"TICKJHSIT{str(count).zfill(1)}"
    
#     doc = {
#         "id": ticket_id,
#         "name": ticket.name,
#         "email": ticket.email,
#         "phone": ticket.phone,
#         "empCode": ticket.empCode,
#         "assetCode": ticket.assetCode,
#         "issues": ticket.issues,
#         "issueDescription": ticket.issueDescription,
#         "reportingPartner": ticket.reportingPartner,
#         "status": "Open",
#         "assigned": "Unassigned",
#         "itEmail": None,
#         "createdAt": datetime.utcnow(),
#         "assignedAt": None,
#         "remark": None,
#         "closedAt": None
#     }
    
#     it_tickets.insert_one(doc)
    
#     # Send email
#     background_tasks.add_task(
#         sendemail,
#         [ticket.email] + IT_EMAILS,
#         f"IT Ticket {ticket_id} Created",
#         f"<p>Dear {ticket.name},</p><p>Your IT ticket <strong>{ticket_id}</strong> has been created.</p><p><strong>IT Asset:</strong> {ticket.assetCode}</p><p><strong>Issues:</strong> {', '.join(ticket.issues)}</p><p>Regards,<br>JHS IT Helpdesk</p>"
#     )
    
#     return {k: v for k, v in doc.items() if k != '_id'}

# @app.get("/api/it/tickets/{ticket_id}")
# async def get_single_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
#     """Get single IT ticket by ID"""
#     ticket = it_tickets.find_one({"id": ticket_id}, {"_id": 0})
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#     return ticket

# @app.put("/api/it/tickets/{ticket_id}")
# async def update_it_ticket(ticket_id: str, body: ITTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Update IT ticket"""
#     ticket = it_tickets.find_one({"id": ticket_id})
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
    
#     update_data = {}
#     old_assigned = ticket.get("assigned")
#     old_status = ticket.get("status", "").lower()
    
#     # Handle assignment
#     if body.assigned is not None and body.assigned != old_assigned:
#         update_data["assigned"] = body.assigned
        
#         # Set assignedAt timestamp if not already set
#         if not ticket.get("assignedAt"):
#             update_data["assignedAt"] = datetime.utcnow()
        
#         # Send assignment email to IT person
#         if body.itEmail:
#             update_data["itEmail"] = body.itEmail
#             background_tasks.add_task(
#                 sendemail,
#                 [body.itEmail],
#                 f"IT Ticket {ticket_id} Assigned to You",
#                 f"""
#                 <p>Dear {body.assigned},</p>
#                 <p>The IT ticket <strong>{ticket_id}</strong> has been assigned to you.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
#                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
#                 <strong>Description:</strong> {ticket.get('issueDescription')}</p>
#                 <p>Please review and take necessary action.</p>
#                 <p>Regards,<br>JHS IT Helpdesk</p>
#                 """
#             )
        
#         # Notify employee about assignment
#         background_tasks.add_task(
#             sendemail,
#             [ticket.get('email')],
#             f"IT Ticket {ticket_id} Assigned",
#             f"""
#             <p>Dear {ticket.get('name')},</p>
#             <p>Your IT ticket <strong>{ticket_id}</strong> has been assigned to <strong>{body.assigned}</strong>.</p>
#             <p>Our team is working on resolving your issue.</p>
#             <p>Regards,<br>JHS IT Helpdesk</p>
#             """
#         )
#     elif body.itEmail is not None:
#         update_data["itEmail"] = body.itEmail
    
#     # Handle status change and closure
#     if body.status:
#         new_status = body.status.capitalize()
        
#         if new_status == "Closed" and old_status != "closed":
#             # Remark is mandatory when closing
#             if not body.remark or not body.remark.strip():
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Remark is mandatory when closing a ticket"
#                 )
            
#             update_data["status"] = "Closed"
#             update_data["remark"] = body.remark.strip()
#             update_data["closedAt"] = datetime.utcnow()
            
#             # Calculate TAT if assignedAt exists
#             tat_text = "N/A"
#             if ticket.get("assignedAt"):
#                 try:
#                     assigned_time = ticket['assignedAt']
#                     closed_time = update_data["closedAt"]
#                     if isinstance(assigned_time, datetime):
#                         tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
#                         tat_text = f"{tat_hours} hours"
#                 except:
#                     tat_text = "N/A"
            
#             # Send closure email to employee
#             background_tasks.add_task(
#                 sendemail,
#                 [ticket.get('email')],
#                 f"IT Ticket {ticket_id} Closed",
#                 f"""
#                 <p>Dear {ticket.get('name')},</p>
#                 <p>Your IT ticket <strong>{ticket_id}</strong> has been successfully resolved and closed.</p>
#                 <p><strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
#                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
#                 <strong>Resolution Remark:</strong> {body.remark}</p>
#                 <p><strong>Resolution Time:</strong> {tat_text}</p>
#                 <p>If you face any further issues, please feel free to create a new ticket.</p>
#                 <p>Regards,<br>JHS IT Helpdesk</p>
#                 """
#             )
            
#             # Send closure confirmation to IT person
#             it_email = ticket.get('itEmail') or body.itEmail
#             if it_email:
#                 background_tasks.add_task(
#                     sendemail,
#                     [it_email],
#                     f"IT Ticket {ticket_id} Closed Confirmation",
#                     f"""
#                     <p>Dear {ticket.get('assigned', 'IT Team')},</p>
#                     <p>You have successfully closed IT ticket <strong>{ticket_id}</strong>.</p>
#                     <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                     <strong>Resolution Remark:</strong> {body.remark}<br>
#                     <strong>Resolution Time:</strong> {tat_text}</p>
#                     <p>Regards,<br>JHS IT Helpdesk</p>
#                     """
#                 )
#         else:
#             update_data["status"] = new_status
    
#     if update_data:
#         it_tickets.update_one({"id": ticket_id}, {"$set": update_data})
    
#     return {"message": "Updated", "ticketId": ticket_id}

# @app.delete("/api/it/tickets/{ticket_id}")
# async def delete_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
#     """Delete IT ticket"""
#     res = it_tickets.delete_one({"id": ticket_id})
#     if res.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#     return {"detail": "Deleted"}

# # ==================== FRONTEND ROUTES ====================

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     """HR helpdesk homepage"""
#     return FileResponse("static/index.html")

# @app.get("/admin", response_class=FileResponse)
# async def hr_admin_page():
#     """HR admin dashboard"""
#     return FileResponse("static/hradmin.html")

# @app.get("/it-admin", response_class=FileResponse)
# async def it_admin_page():
#     """IT admin dashboard"""
#     return FileResponse("static/it-admin.html")

# @app.get("/adminlogin", response_class=HTMLResponse)
# async def admin_login_page():
#     """Unified admin login page"""
#     with open("static/adminlogin.html", "r", encoding="utf-8") as f:
#         return f.read()

# @app.get("/.well-known/{path:path}")
# async def ignore_well_known(path: str):
#     return {}

# @app.get("/favicon.ico")
# async def favicon():
#     """Return favicon or 204 No Content"""
#     try:
#         return FileResponse("static/favicon.ico")
#     except:
#         return HTMLResponse(status_code=204)

# # ==================== HEALTH CHECK ====================

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "timestamp": datetime.utcnow().isoformat(),
#         "databases": {
#             "hr_tickets": hr_tickets.count_documents({}),
#             "it_tickets": it_tickets.count_documents({})
#         }
#     }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)











# from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel, EmailStr
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# from typing import Optional, Dict, Any, List
# from dotenv import load_dotenv
# import os
# import time
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import logging
# import hashlib
# from jose import JWTError, jwt

# # Load environment
# load_dotenv()

# # FastAPI app
# app = FastAPI(title="JHS Unified Helpdesk API")
# print("🚀 JHS Unified Helpdesk API Running")

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Config
# SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# SMTP_SERVER = "sandbox.smtp.mailtrap.io"
# SMTP_PORT = 587
# SMTP_USER = os.getenv("SMTP_USER")
# SMTP_PASS = os.getenv("SMTP_PASS")

# # Database connections
# client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

# # HR Database
# hr_db = client["HR_Helpdesk"]
# hr_tickets = hr_db["Tickets"]
# hr_admins = hr_db["Admins"]
# hr_sequences = hr_db["sequences"]   # NEW


# # IT Database
# it_db = client["ithelpdesk"]
# it_tickets = it_db["tickets"]
# it_admins = it_db["admins"]
# it_sessions = it_db["sessions"]
# it_sequences = it_db["sequences"]

# # Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # HR Email Mapping
# HR_EMAILS = {
#     "PAYSLIP": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "HRMS QUERY": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "ATTENDANCE": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "SALARY QUERY": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "BUDDY REFERRAL": {"name": "Krutika Shivshivkar", "email": "orina.guha@jhsassociates.in"},
#     "OTHER": {"name": "Krutika Shivshivkar", "email": "orina.guha@jhsassociates.in"}
# }

# # IT Email list
# IT_EMAILS = ["orina.guha@jhsassociates.in", "orina.guha2005@gmail.com"]

# # ==================== PYDANTIC MODELS ====================

# # HR Models
# class HRTicketCreate(BaseModel):
#     name: str
#     email: str
#     phone: Optional[str] = None
#     empCode: Optional[str] = None
#     category: str
#     issue: str

# class HRTicketUpdate(BaseModel):
#     assigned: Optional[str] = None
#     status: Optional[str] = None
#     hrEmail: Optional[str] = None
#     remark: Optional[str] = None

# # IT Models
# class ITTicketCreate(BaseModel):
#     name: str
#     email: EmailStr
#     phone: str  # Required
#     assetCode: Optional[str] = ""  # Made optional
#     empCode: Optional[str] = ""  # Optional
#     issues: List[str]  # Required list
#     issueDescription: str  # Required
#     reportingPartner: str  # Required

# class ITTicketUpdate(BaseModel):
#     assigned: Optional[str] = None
#     status: Optional[str] = None
#     itEmail: Optional[EmailStr] = None
#     remark: Optional[str] = None

# class AdminLogin(BaseModel):
#     empCode: str
#     password: str

# # ==================== UTILITY FUNCTIONS ====================

# def hash_password(password: str) -> str:
#     """Hash password using SHA256"""
#     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# def verify_password(plain: str, hashed: str) -> bool:
#     """Verify password against hash"""
#     return hash_password(plain) == hashed

# def create_access_token(data: dict):
#     """Create JWT access token"""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_current_admin(authorization: str = Header(None)):
#     """Verify JWT token and return admin info"""
#     if not authorization or not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing token")
    
#     token = authorization.split(" ")[1]
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("role") != "admin":
#             raise HTTPException(status_code=403, detail="Not authorized")
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")

# def sendemail(recipients: List[str], subject: str, body: str):
#     """Send email to recipients"""
#     # Small delay to avoid Mailtrap sandbox rate limit (too many emails per second)
#     time.sleep(1.5)
#     logger.info(f"🔄 EMAIL → {recipients}, {subject}")
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = SMTP_USER
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'html'))
        
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASS)
        
#         valid_recipients = [r for r in recipients if r and r.strip()]
#         if valid_recipients:
#             server.sendmail(SMTP_USER, valid_recipients, msg.as_string())
#             logger.info(f"✅ EMAILS SENT → {valid_recipients}")
#         server.quit()
#     except Exception as e:
#         logger.error(f"❌ EMAIL FAILED → {str(e)}")

# # ==================== AUTHENTICATION ROUTES ====================

# @app.post("/api/admin/login")
# async def unified_admin_login(body: AdminLogin):
#     """
#     Unified login endpoint for both HR and IT admins.
#     First checks HR admins, then IT admins.
#     """
#     empCode = body.empCode.upper().strip()
#     password = body.password
    
#     if not empCode or not password:
#         raise HTTPException(status_code=400, detail="empCode and password required")
    
#     logger.info(f"Login attempt for empCode: {empCode}")
    
#     # Try HR admin first
#     hr_admin = hr_admins.find_one({"empCodes": empCode, "password": password})
    
#     if hr_admin:
#         logger.info(f"HR Admin found: {hr_admin.get('name')}")
#         token = create_access_token({
#             "sub": empCode,
#             "role": "admin",
#             "type": "hr",
#             "name": hr_admin.get("name")
#         })
        
#         return {
#             "access_token": token,
#             "token_type": "bearer",
#             "name": hr_admin.get("name"),
#             "helpdesk": "hr"
#         }
    
#     # Try IT admin
#     it_admin = it_admins.find_one({"empCode": empCode})
    
#     if it_admin:
#         logger.info(f"IT Admin found: {it_admin.get('name')}")
        
#         # Verify password
#         if not verify_password(password, it_admin["password"]):
#             logger.error("Password verification failed")
#             raise HTTPException(status_code=401, detail="Invalid password")
        
#         logger.info("Password verified successfully")
        
#         token = create_access_token({
#             "sub": empCode,
#             "role": "admin",
#             "type": "it",
#             "name": it_admin.get("name")
#         })
        
#         # Store session in IT sessions collection
#         session_doc = {
#             "empCode": empCode,
#             "token": token,
#             "isValid": True,
#             "createdAt": datetime.utcnow(),
#             "expiresAt": datetime.utcnow() + timedelta(hours=1)
#         }
        
#         it_sessions.update_one(
#             {"empCode": empCode},
#             {"$set": session_doc},
#             upsert=True
#         )
        
#         logger.info(f"Login successful for IT admin {empCode}")
        
#         return {
#             "access_token": token,
#             "token": token,  # For backward compatibility
#             "token_type": "bearer",
#             "empCode": empCode,
#             "name": it_admin.get("name"),
#             "helpdesk": "it"
#         }
    
#     # No admin found
#     logger.error(f"Admin not found for empCode: {empCode}")
#     raise HTTPException(status_code=401, detail="Invalid credentials")

# # ==================== HR TICKET ROUTES (with /api/hr/ prefix) ====================

# @app.get("/api/hr/tickets")
# async def get_hr_tickets(admin=Depends(get_current_admin)):
#     """Get all HR tickets"""
#     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# @app.post("/api/hr/tickets")
# async def create_hr_ticket(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
#     """Create new HR ticket"""
#     sequence = hr_sequences.find_one_and_update(
#         {"_id": "hr_ticket_counter"},
#         {"$inc": {"seq": 1}},
#         upsert=True,
#         return_document=True
#     )

#     count = sequence["seq"]
#     ticket_id = f"TICKJHSHR{str(count).zfill(2)}"
    
    
#     category = ticket.category.upper().strip()
#     hr_data = HR_EMAILS.get(category)
#     assigned_name = hr_data["name"] if hr_data else "Unassigned"
#     assigned_email = hr_data["email"] if hr_data else None
    
#     ticket_data = {
#         "id": ticket_id, "name": ticket.name, "email": ticket.email,
#         "phone": ticket.phone, "empCode": ticket.empCode,
#         "category": ticket.category, "issue": ticket.issue,
#         "status": "Open", "assigned": assigned_name, "hrEmail": assigned_email,
#         "assignedAt": datetime.utcnow() if hr_data else None,
#         "createdAt": datetime.utcnow(), "remark": ""
#     }
    
#     hr_tickets.insert_one(ticket_data)
    
#     # Send emails
#     background_tasks.add_task(
#         sendemail, [ticket.email],
#         f"JHS HR - Ticket {ticket_id} Created",
#         f"<p>Dear {ticket.name},</p><p>Your ticket {ticket_id} created.</p><p>Category: {ticket.category}<br>Assigned: {assigned_name}</p><p>JHS HR Team</p>"
#     )
    
#     if assigned_email:
#         background_tasks.add_task(
#             sendemail, [assigned_email],
#             f"New Ticket: {ticket_id}",
#             f"<p>Dear {assigned_name},</p><p>Ticket {ticket_id} assigned to you.</p><p>Employee: {ticket.name}<br>Issue: {ticket.issue}</p>"
#         )
    
#     return {"message": "Ticket created", "ticketId": ticket_id, "assignedTo": assigned_name}

# @app.get("/api/hr/tickets/{ticketid}")
# async def get_single_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
#     """Get single HR ticket by ID"""
#     ticket = hr_tickets.find_one({"id": ticketid})
#     if not ticket:
#         raise HTTPException(404, "Ticket not found")
#     ticket.pop("_id", None)
#     return ticket

# @app.put("/api/hr/tickets/{ticketid}")
# async def update_hr_ticket(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Update HR ticket"""
#     ticket = hr_tickets.find_one({"id": ticketid})
#     if not ticket: 
#         raise HTTPException(404, "Ticket not found")
    
#     update_data = {}
#     old_assigned = ticket.get("assigned")
#     old_status = ticket.get("status", "").lower()
    
#     # Handle reassignment
#     if body.assigned and body.assigned != old_assigned:
#         update_data["assigned"] = body.assigned
#         update_data["assignedAt"] = datetime.utcnow()
#         if body.hrEmail: 
#             update_data["hrEmail"] = body.hrEmail
        
#         # Send reassignment email to new HR person
#         if body.hrEmail:
#             background_tasks.add_task(
#                 sendemail,
#                 [body.hrEmail],
#                 f"HR Ticket {ticketid} Assigned to You",
#                 f"""
#                 <p>Dear {body.assigned},</p>
#                 <p>The ticket <strong>{ticketid}</strong> has been assigned to you.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Category:</strong> {ticket.get('category')}<br>
#                 <strong>Issue:</strong> {ticket.get('issue')}</p>
#                 <p>Please review and take necessary action.</p>
#                 <p>Regards,<br>JHS HR Helpdesk</p>
#                 """
#             )
    
#     # Handle closure
#     if body.status and body.status.lower() == "closed" and old_status != "closed":
#         update_data["status"] = "Closed"
#         update_data["closedAt"] = datetime.utcnow()
#         update_data["remark"] = body.remark if body.remark else ""
        
#         # Send closure email to employee
#         background_tasks.add_task(
#             sendemail,
#             [ticket.get('email')],
#             f"HR Ticket {ticketid} Closed",
#             f"""
#             <p>Dear {ticket.get('name')},</p>
#             <p>Your HR ticket <strong>{ticketid}</strong> has been closed.</p>
#             <p><strong>Category:</strong> {ticket.get('category')}<br>
#             <strong>Issue:</strong> {ticket.get('issue')}<br>
#             <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
#             <p>If you have any further questions, please feel free to create a new ticket.</p>
#             <p>Regards,<br>JHS HR Team</p>
#             """
#         )
        
#         # Send closure confirmation to HR person
#         hr_email = ticket.get('hrEmail')
#         if hr_email:
#             background_tasks.add_task(
#                 sendemail,
#                 [hr_email],
#                 f"HR Ticket {ticketid} Closed Confirmation",
#                 f"""
#                 <p>Dear {ticket.get('assigned', 'HR Team')},</p>
#                 <p>You have successfully closed ticket <strong>{ticketid}</strong>.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
#                 <p>Regards,<br>JHS HR Helpdesk</p>
#                 """
#             )
    
#     if update_data:
#         hr_tickets.update_one({"id": ticketid}, {"$set": update_data})
    
#     return {"message": "Updated", "ticketId": ticketid}

# @app.delete("/api/hr/tickets/{ticketid}")
# async def delete_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
#     """Delete HR ticket"""
#     result = hr_tickets.delete_one({"id": ticketid})
#     if result.deleted_count == 0: 
#         raise HTTPException(404, "Ticket not found")
#     return {"message": "Deleted"}

# @app.get("/api/hr/admin/stats")
# async def get_hr_stats(admin=Depends(get_current_admin)):
#     """Get HR ticket statistics"""
#     tickets = list(hr_tickets.find({}, {"_id": 0}))
#     stats = {"total": len(tickets), "bystatus": {"Open": 0, "Closed": 0}, "byhr": {}}
    
#     for t in tickets:
#         status = t.get("status", "Open")
#         hr = t.get("assigned", "Unassigned")
#         stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
#         if hr not in stats["byhr"]:
#             stats["byhr"][hr] = {"Open": 0, "Closed": 0}
#         stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
#     return stats

# # ==================== LEGACY HR ROUTES (for backward compatibility) ====================
# # These maintain compatibility with existing HR frontend that uses /api/tickets

# @app.get("/api/tickets")
# async def get_hr_tickets_legacy(admin=Depends(get_current_admin)):
#     """Legacy HR route - Get all HR tickets"""
#     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# @app.post("/api/tickets")
# async def create_hr_ticket_legacy(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
#     """Legacy HR route - Create new HR ticket"""
#     return await create_hr_ticket(ticket, background_tasks)

# @app.get("/api/tickets/{ticketid}")
# async def get_single_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
#     """Legacy HR route - Get single HR ticket"""
#     return await get_single_hr_ticket(ticketid, admin)

# @app.put("/api/tickets/{ticketid}")
# async def update_hr_ticket_legacy(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Legacy HR route - Update HR ticket"""
#     return await update_hr_ticket(ticketid, body, background_tasks, admin)

# @app.delete("/api/tickets/{ticketid}")
# async def delete_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
#     """Legacy HR route - Delete HR ticket"""
#     return await delete_hr_ticket(ticketid, admin)

# @app.get("/api/admin/stats")
# async def get_hr_stats_legacy(admin=Depends(get_current_admin)):
#     """Legacy HR route - Get HR statistics"""
#     return await get_hr_stats(admin)

# # ==================== IT TICKET ROUTES (with /api/it/ prefix) ====================
# # IMPORTANT: Stats route MUST come before the dynamic {ticket_id} route

# @app.get("/api/it/tickets")
# async def get_it_tickets(admin=Depends(get_current_admin)):
#     """Get all IT tickets"""
#     tickets_list = list(it_tickets.find({}, {"_id": 0}))
    
#     # Calculate TAT for closed tickets
#     for ticket in tickets_list:
#         if ticket.get('assignedAt') and ticket.get('closedAt'):
#             try:
#                 assigned_time = ticket['assignedAt']
#                 closed_time = ticket['closedAt']
#                 if isinstance(assigned_time, datetime) and isinstance(closed_time, datetime):
#                     tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
#                     ticket['tatHours'] = f"{tat_hours} hrs"
#             except:
#                 ticket['tatHours'] = "-"
#         else:
#             ticket['tatHours'] = "-"
    
#     return tickets_list

# @app.get("/api/it/tickets/stats")
# async def get_it_stats(admin=Depends(get_current_admin)):
#     """Get IT ticket statistics - MUST be before /{ticket_id} route"""
#     tickets = list(it_tickets.find({}, {"_id": 0, "status": 1, "assigned": 1}))
#     total = len(tickets)
#     by_status = {}
#     by_it = {}
    
#     for t in tickets:
#         s = t.get("status", "Open")
#         by_status[s] = by_status.get(s, 0) + 1
        
#         it_person = t.get("assigned", "Unassigned")
#         if it_person not in by_it:
#             by_it[it_person] = {"Open": 0, "Closed": 0}
#         by_it[it_person][s] = by_it[it_person].get(s, 0) + 1
    
#     return {
#         "total": total,
#         "byStatus": by_status,
#         "byIT": by_it
#     }

# @app.post("/api/it/tickets")
# async def create_it_ticket(ticket: ITTicketCreate, background_tasks: BackgroundTasks):
#     """Create new IT ticket"""
#     sequence = it_sequences.find_one_and_update(
#         {"_id": "ticket_counter"},
#         {"$inc": {"seq": 1}},
#         upsert=True, return_document=True
#     )
#     count = sequence['seq']
#     ticket_id = f"TICKJHSIT{str(count).zfill(1)}"
    
#     doc = {
#         "id": ticket_id,
#         "name": ticket.name,
#         "email": ticket.email,
#         "phone": ticket.phone,
#         "empCode": ticket.empCode,
#         "assetCode": ticket.assetCode,
#         "issues": ticket.issues,
#         "issueDescription": ticket.issueDescription,
#         "reportingPartner": ticket.reportingPartner,
#         "status": "Open",
#         "assigned": "Unassigned",
#         "itEmail": None,
#         "createdAt": datetime.utcnow(),
#         "assignedAt": None,
#         "remark": None,
#         "closedAt": None
#     }
    
#     it_tickets.insert_one(doc)
    
#     # Send email
#     background_tasks.add_task(
#         sendemail,
#         [ticket.email] + IT_EMAILS,
#         f"IT Ticket {ticket_id} Created",
#         f"<p>Dear {ticket.name},</p><p>Your IT ticket <strong>{ticket_id}</strong> has been created.</p><p><strong>IT Asset:</strong> {ticket.assetCode}</p><p><strong>Issues:</strong> {', '.join(ticket.issues)}</p><p>Regards,<br>JHS IT Helpdesk</p>"
#     )
    
#     return {k: v for k, v in doc.items() if k != '_id'}

# @app.get("/api/it/tickets/{ticket_id}")
# async def get_single_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
#     """Get single IT ticket by ID"""
#     ticket = it_tickets.find_one({"id": ticket_id}, {"_id": 0})
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#     return ticket

# @app.put("/api/it/tickets/{ticket_id}")
# async def update_it_ticket(ticket_id: str, body: ITTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Update IT ticket"""
#     ticket = it_tickets.find_one({"id": ticket_id})
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
    
#     update_data = {}
#     old_assigned = ticket.get("assigned")
#     old_status = ticket.get("status", "").lower()
    
#     # Handle assignment
#     if body.assigned is not None and body.assigned != old_assigned:
#         update_data["assigned"] = body.assigned
        
#         # Set assignedAt timestamp if not already set
#         if not ticket.get("assignedAt"):
#             update_data["assignedAt"] = datetime.utcnow()
        
#         # Send assignment email to IT person
#         if body.itEmail:
#             update_data["itEmail"] = body.itEmail
#             background_tasks.add_task(
#                 sendemail,
#                 [body.itEmail],
#                 f"IT Ticket {ticket_id} Assigned to You",
#                 f"""
#                 <p>Dear {body.assigned},</p>
#                 <p>The IT ticket <strong>{ticket_id}</strong> has been assigned to you.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
#                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
#                 <strong>Description:</strong> {ticket.get('issueDescription')}</p>
#                 <p>Please review and take necessary action.</p>
#                 <p>Regards,<br>JHS IT Helpdesk</p>
#                 """
#             )
        
#         # Notify employee about assignment
#         background_tasks.add_task(
#             sendemail,
#             [ticket.get('email')],
#             f"IT Ticket {ticket_id} Assigned",
#             f"""
#             <p>Dear {ticket.get('name')},</p>
#             <p>Your IT ticket <strong>{ticket_id}</strong> has been assigned to <strong>{body.assigned}</strong>.</p>
#             <p>Our team is working on resolving your issue.</p>
#             <p>Regards,<br>JHS IT Helpdesk</p>
#             """
#         )
#     elif body.itEmail is not None:
#         update_data["itEmail"] = body.itEmail
    
#     # Handle status change and closure
#     if body.status:
#         new_status = body.status.capitalize()
        
#         if new_status == "Closed" and old_status != "closed":
#             # Remark is mandatory when closing
#             if not body.remark or not body.remark.strip():
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Remark is mandatory when closing a ticket"
#                 )
            
#             update_data["status"] = "Closed"
#             update_data["remark"] = body.remark.strip()
#             update_data["closedAt"] = datetime.utcnow()
            
#             # Calculate TAT if assignedAt exists
#             tat_text = "N/A"
#             if ticket.get("assignedAt"):
#                 try:
#                     assigned_time = ticket['assignedAt']
#                     closed_time = update_data["closedAt"]
#                     if isinstance(assigned_time, datetime):
#                         tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
#                         tat_text = f"{tat_hours} hours"
#                 except:
#                     tat_text = "N/A"
            
#             # Send closure email to employee
#             background_tasks.add_task(
#                 sendemail,
#                 [ticket.get('email')],
#                 f"IT Ticket {ticket_id} Closed",
#                 f"""
#                 <p>Dear {ticket.get('name')},</p>
#                 <p>Your IT ticket <strong>{ticket_id}</strong> has been successfully resolved and closed.</p>
#                 <p><strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
#                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
#                 <strong>Resolution Remark:</strong> {body.remark}</p>
#                 <p><strong>Resolution Time:</strong> {tat_text}</p>
#                 <p>If you face any further issues, please feel free to create a new ticket.</p>
#                 <p>Regards,<br>JHS IT Helpdesk</p>
#                 """
#             )
            
#             # Send closure confirmation to IT person
#             it_email = ticket.get('itEmail') or body.itEmail
#             if it_email:
#                 background_tasks.add_task(
#                     sendemail,
#                     [it_email],
#                     f"IT Ticket {ticket_id} Closed Confirmation",
#                     f"""
#                     <p>Dear {ticket.get('assigned', 'IT Team')},</p>
#                     <p>You have successfully closed IT ticket <strong>{ticket_id}</strong>.</p>
#                     <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                     <strong>Resolution Remark:</strong> {body.remark}<br>
#                     <strong>Resolution Time:</strong> {tat_text}</p>
#                     <p>Regards,<br>JHS IT Helpdesk</p>
#                     """
#                 )
#         else:
#             update_data["status"] = new_status
    
#     if update_data:
#         it_tickets.update_one({"id": ticket_id}, {"$set": update_data})
    
#     return {"message": "Updated", "ticketId": ticket_id}

# @app.delete("/api/it/tickets/{ticket_id}")
# async def delete_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
#     """Delete IT ticket"""
#     res = it_tickets.delete_one({"id": ticket_id})
#     if res.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#     return {"detail": "Deleted"}

# # ==================== FRONTEND ROUTES ====================

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     """HR helpdesk homepage"""
#     return FileResponse("static/index.html")

# @app.get("/admin", response_class=FileResponse)
# async def hr_admin_page():
#     """HR admin dashboard"""
#     return FileResponse("static/hradmin.html")

# @app.get("/it-admin", response_class=FileResponse)
# async def it_admin_page():
#     """IT admin dashboard"""
#     return FileResponse("static/it-admin.html")

# @app.get("/adminlogin", response_class=HTMLResponse)
# async def admin_login_page():
#     """Unified admin login page"""
#     with open("static/adminlogin.html", "r", encoding="utf-8") as f:
#         return f.read()

# @app.get("/.well-known/{path:path}")
# async def ignore_well_known(path: str):
#     return {}

# @app.get("/favicon.ico")
# async def favicon():
#     """Return favicon or 204 No Content"""
#     try:
#         return FileResponse("static/favicon.ico")
#     except:
#         return HTMLResponse(status_code=204)

# # ==================== HEALTH CHECK ====================

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "timestamp": datetime.utcnow().isoformat(),
#         "databases": {
#             "hr_tickets": hr_tickets.count_documents({}),
#             "it_tickets": it_tickets.count_documents({})
#         }
#     }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)





































# from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel, EmailStr
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# from typing import Optional, Dict, Any, List
# from dotenv import load_dotenv
# import os
# import time
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import logging
# import hashlib
# from jose import JWTError, jwt

# # Load environment
# load_dotenv()

# # FastAPI app
# app = FastAPI(title="JHS Unified Helpdesk API")
# print(" JHS Unified Helpdesk API Running")

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Config
# SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# # ---- Brevo SMTP Configuration ----
# # Brevo SMTP relay: smtp-relay.brevo.com on port 587 (STARTTLS)
# SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp-relay.brevo.com")
# SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
# SMTP_USER = os.getenv("SMTP_USER")          # Brevo account login email
# SMTP_PASS = os.getenv("SMTP_PASS")          # Brevo SMTP key (generated in SMTP & API > SMTP tab)
# SENDER_EMAIL = os.getenv("SENDER_EMAIL")    # Your single verified Brevo sender email
# SENDER_NAME = os.getenv("SENDER_NAME", "JHS Helpdesk")

# # Database connections
# client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

# # HR Database
# hr_db = client["HR_Helpdesk"]
# hr_tickets = hr_db["Tickets"]
# hr_admins = hr_db["Admins"]
# hr_sequences = hr_db["sequences"]   # NEW


# # IT Database
# it_db = client["ithelpdesk"]
# it_tickets = it_db["tickets"]
# it_admins = it_db["admins"]
# it_sessions = it_db["sessions"]
# it_sequences = it_db["sequences"]

# # Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # HR Email Mapping
# HR_EMAILS = {
#     "PAYSLIP": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "HRMS QUERY": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "ATTENDANCE": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "SALARY QUERY": {"name": "Janhavi Gamare", "email": "orina.guha@jhsassociates.in"},
#     "BUDDY REFERRAL": {"name": "Krutika Shivshivkar", "email": "orina.guha@jhsassociates.in"},
#     "OTHER": {"name": "Krutika Shivshivkar", "email": "orina.guha@jhsassociates.in"}
# }

# # IT Email list
# IT_EMAILS = ["orina.guha@jhsassociates.in", "orina.guha2005@gmail.com"]

# # ==================== PYDANTIC MODELS ====================

# # HR Models
# class HRTicketCreate(BaseModel):
#     name: str
#     email: str
#     phone: Optional[str] = None
#     empCode: Optional[str] = None
#     category: str
#     issue: str

# class HRTicketUpdate(BaseModel):
#     assigned: Optional[str] = None
#     status: Optional[str] = None
#     hrEmail: Optional[str] = None
#     remark: Optional[str] = None

# # IT Models
# class ITTicketCreate(BaseModel):
#     name: str
#     email: EmailStr
#     phone: str  # Required
#     assetCode: Optional[str] = ""  # Made optional
#     empCode: Optional[str] = ""  # Optional
#     issues: List[str]  # Required list
#     issueDescription: str  # Required
#     reportingPartner: str  # Required

# class ITTicketUpdate(BaseModel):
#     assigned: Optional[str] = None
#     status: Optional[str] = None
#     itEmail: Optional[EmailStr] = None
#     remark: Optional[str] = None

# class AdminLogin(BaseModel):
#     empCode: str
#     password: str

# class TestEmailRequest(BaseModel):
#     to: EmailStr

# # ==================== UTILITY FUNCTIONS ====================

# def hash_password(password: str) -> str:
#     """Hash password using SHA256"""
#     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# def verify_password(plain: str, hashed: str) -> bool:
#     """Verify password against hash"""
#     return hash_password(plain) == hashed

# def create_access_token(data: dict):
#     """Create JWT access token"""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_current_admin(authorization: str = Header(None)):
#     """Verify JWT token and return admin info"""
#     if not authorization or not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing token")
    
#     token = authorization.split(" ")[1]
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("role") != "admin":
#             raise HTTPException(status_code=403, detail="Not authorized")
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")

# def sendemail(recipients: List[str], subject: str, body: str) -> bool:
#     """
#     Send email via Brevo SMTP relay.

#     IMPORTANT (Brevo free tier):
#     - The 'From' address MUST be your single verified sender email
#       (set SENDER_EMAIL in .env). Brevo will reject/bounce emails
#       sent from any other 'From' address.
#     - Recipients ('To') can be ANY email address - no restriction there.
#     - SMTP_USER/SMTP_PASS = your Brevo SMTP login + SMTP key
#       (NOT your Brevo account password - generate the key under
#       SMTP & API > SMTP tab in the Brevo dashboard).

#     Returns True if the send call succeeded, False otherwise.
#     Logs detailed success/failure so you can trace which stage
#     (create / assign / close) failed.
#     """
#     # Small delay to be gentle with rate limits
#     time.sleep(1.5)

#     valid_recipients = [r for r in recipients if r and r.strip()]
#     if not valid_recipients:
#         logger.warning(f"⚠️ EMAIL SKIPPED (no valid recipients) → subject='{subject}'")
#         return False

#     if not SMTP_USER or not SMTP_PASS or not SENDER_EMAIL:
#         logger.error(
#             "❌ EMAIL CONFIG MISSING — check SMTP_USER, SMTP_PASS, "
#             "SENDER_EMAIL in your .env (Brevo SMTP credentials)"
#         )
#         return False

#     logger.info(f"🔄 EMAIL → {valid_recipients}, subject='{subject}'")

#     try:
#         msg = MIMEMultipart()
#         msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
#         msg['To'] = ", ".join(valid_recipients)
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'html'))

#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASS)

#         server.sendmail(SENDER_EMAIL, valid_recipients, msg.as_string())
#         server.quit()

#         logger.info(f"✅ EMAIL SENT → {valid_recipients} | subject='{subject}'")
#         return True

#     except smtplib.SMTPAuthenticationError as e:
#         logger.error(
#             f"❌ EMAIL AUTH FAILED — verify SMTP_USER/SMTP_PASS (Brevo SMTP key). "
#             f"Detail: {str(e)}"
#         )
#         return False
#     except smtplib.SMTPRecipientsRefused as e:
#         logger.error(f"❌ EMAIL RECIPIENTS REFUSED → {valid_recipients} | Detail: {str(e)}")
#         return False
#     except smtplib.SMTPSenderRefused as e:
#         logger.error(
#             f"❌ EMAIL SENDER REFUSED — '{SENDER_EMAIL}' may not be a verified "
#             f"sender in Brevo (Senders & IP > Senders). Detail: {str(e)}"
#         )
#         return False
#     except smtplib.SMTPException as e:
#         logger.error(f"❌ SMTP ERROR → {str(e)}")
#         return False
#     except Exception as e:
#         logger.error(f"❌ EMAIL FAILED → {str(e)}")
#         return False

# # ==================== EMAIL TEST ROUTE ====================

# @app.post("/api/test-email")
# async def test_email(body: TestEmailRequest):
#     """
#     Quick standalone test of Brevo SMTP connectivity.
#     Use this BEFORE testing ticket create/assign/close flows
#     to confirm SMTP_USER, SMTP_PASS, SENDER_EMAIL are correct
#     and Brevo is delivering.

#     POST { "to": "your_test_inbox@gmail.com" }
#     """
#     success = sendemail(
#         [body.to],
#         "JHS Helpdesk - Brevo SMTP Test",
#         f"""
#         <p>This is a test email sent via Brevo SMTP relay.</p>
#         <p>If you received this, your email configuration is working correctly
#         for ticket creation, assignment, and closure notifications.</p>
#         <p>Sent at: {datetime.utcnow().isoformat()} UTC</p>
#         """
#     )
#     if success:
#         return {"status": "sent", "message": "Check inbox/spam folder", "to": body.to}
#     raise HTTPException(
#         status_code=500,
#         detail="Email send failed - check server logs for the exact reason "
#                "(auth error, sender not verified, etc.)"
#     )

# # ==================== AUTHENTICATION ROUTES ====================

# @app.post("/api/admin/login")
# async def unified_admin_login(body: AdminLogin):
#     """
#     Unified login endpoint for both HR and IT admins.
#     First checks HR admins, then IT admins.
#     """
#     empCode = body.empCode.upper().strip()
#     password = body.password
    
#     if not empCode or not password:
#         raise HTTPException(status_code=400, detail="empCode and password required")
    
#     logger.info(f"Login attempt for empCode: {empCode}")
    
#     # Try HR admin first
#     hr_admin = hr_admins.find_one({"empCodes": empCode, "password": password})
    
#     if hr_admin:
#         logger.info(f"HR Admin found: {hr_admin.get('name')}")
#         token = create_access_token({
#             "sub": empCode,
#             "role": "admin",
#             "type": "hr",
#             "name": hr_admin.get("name")
#         })
        
#         return {
#             "access_token": token,
#             "token_type": "bearer",
#             "name": hr_admin.get("name"),
#             "helpdesk": "hr"
#         }
    
#     # Try IT admin
#     it_admin = it_admins.find_one({"empCode": empCode})
    
#     if it_admin:
#         logger.info(f"IT Admin found: {it_admin.get('name')}")
        
#         # Verify password
#         if not verify_password(password, it_admin["password"]):
#             logger.error("Password verification failed")
#             raise HTTPException(status_code=401, detail="Invalid password")
        
#         logger.info("Password verified successfully")
        
#         token = create_access_token({
#             "sub": empCode,
#             "role": "admin",
#             "type": "it",
#             "name": it_admin.get("name")
#         })
        
#         # Store session in IT sessions collection
#         session_doc = {
#             "empCode": empCode,
#             "token": token,
#             "isValid": True,
#             "createdAt": datetime.utcnow(),
#             "expiresAt": datetime.utcnow() + timedelta(hours=1)
#         }
        
#         it_sessions.update_one(
#             {"empCode": empCode},
#             {"$set": session_doc},
#             upsert=True
#         )
        
#         logger.info(f"Login successful for IT admin {empCode}")
        
#         return {
#             "access_token": token,
#             "token": token,  # For backward compatibility
#             "token_type": "bearer",
#             "empCode": empCode,
#             "name": it_admin.get("name"),
#             "helpdesk": "it"
#         }
    
#     # No admin found
#     logger.error(f"Admin not found for empCode: {empCode}")
#     raise HTTPException(status_code=401, detail="Invalid credentials")

# # ==================== HR TICKET ROUTES (with /api/hr/ prefix) ====================

# @app.get("/api/hr/tickets")
# async def get_hr_tickets(admin=Depends(get_current_admin)):
#     """Get all HR tickets"""
#     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# @app.post("/api/hr/tickets")
# async def create_hr_ticket(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
#     """Create new HR ticket"""
#     sequence = hr_sequences.find_one_and_update(
#         {"_id": "hr_ticket_counter"},
#         {"$inc": {"seq": 1}},
#         upsert=True,
#         return_document=True
#     )

#     count = sequence["seq"]
#     ticket_id = f"TICKJHSHR{str(count).zfill(2)}"
    
    
#     category = ticket.category.upper().strip()
#     hr_data = HR_EMAILS.get(category)
#     assigned_name = hr_data["name"] if hr_data else "Unassigned"
#     assigned_email = hr_data["email"] if hr_data else None
    
#     ticket_data = {
#         "id": ticket_id, "name": ticket.name, "email": ticket.email,
#         "phone": ticket.phone, "empCode": ticket.empCode,
#         "category": ticket.category, "issue": ticket.issue,
#         "status": "Open", "assigned": assigned_name, "hrEmail": assigned_email,
#         "assignedAt": datetime.utcnow() if hr_data else None,
#         "createdAt": datetime.utcnow(), "remark": ""
#     }
    
#     hr_tickets.insert_one(ticket_data)
    
#     # Send emails
#     background_tasks.add_task(
#         sendemail, [ticket.email],
#         f"JHS HR - Ticket {ticket_id} Created",
#         f"<p>Dear {ticket.name},</p><p>Your ticket {ticket_id} created.</p><p>Category: {ticket.category}<br>Assigned: {assigned_name}</p><p>JHS HR Team</p>"
#     )
    
#     if assigned_email:
#         background_tasks.add_task(
#             sendemail, [assigned_email],
#             f"New Ticket: {ticket_id}",
#             f"<p>Dear {assigned_name},</p><p>Ticket {ticket_id} assigned to you.</p><p>Employee: {ticket.name}<br>Issue: {ticket.issue}</p>"
#         )
    
#     return {"message": "Ticket created", "ticketId": ticket_id, "assignedTo": assigned_name}

# @app.get("/api/hr/tickets/{ticketid}")
# async def get_single_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
#     """Get single HR ticket by ID"""
#     ticket = hr_tickets.find_one({"id": ticketid})
#     if not ticket:
#         raise HTTPException(404, "Ticket not found")
#     ticket.pop("_id", None)
#     return ticket

# @app.put("/api/hr/tickets/{ticketid}")
# async def update_hr_ticket(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Update HR ticket"""
#     ticket = hr_tickets.find_one({"id": ticketid})
#     if not ticket: 
#         raise HTTPException(404, "Ticket not found")
    
#     update_data = {}
#     old_assigned = ticket.get("assigned")
#     old_status = ticket.get("status", "").lower()
    
#     # Handle reassignment
#     if body.assigned and body.assigned != old_assigned:
#         update_data["assigned"] = body.assigned
#         update_data["assignedAt"] = datetime.utcnow()
#         if body.hrEmail: 
#             update_data["hrEmail"] = body.hrEmail
        
#         # Send reassignment email to new HR person
#         if body.hrEmail:
#             background_tasks.add_task(
#                 sendemail,
#                 [body.hrEmail],
#                 f"HR Ticket {ticketid} Assigned to You",
#                 f"""
#                 <p>Dear {body.assigned},</p>
#                 <p>The ticket <strong>{ticketid}</strong> has been assigned to you.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Category:</strong> {ticket.get('category')}<br>
#                 <strong>Issue:</strong> {ticket.get('issue')}</p>
#                 <p>Please review and take necessary action.</p>
#                 <p>Regards,<br>JHS HR Helpdesk</p>
#                 """
#             )
    
#     # Handle closure
#     if body.status and body.status.lower() == "closed" and old_status != "closed":
#         update_data["status"] = "Closed"
#         update_data["closedAt"] = datetime.utcnow()
#         update_data["remark"] = body.remark if body.remark else ""
        
#         # Send closure email to employee
#         background_tasks.add_task(
#             sendemail,
#             [ticket.get('email')],
#             f"HR Ticket {ticketid} Closed",
#             f"""
#             <p>Dear {ticket.get('name')},</p>
#             <p>Your HR ticket <strong>{ticketid}</strong> has been closed.</p>
#             <p><strong>Category:</strong> {ticket.get('category')}<br>
#             <strong>Issue:</strong> {ticket.get('issue')}<br>
#             <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
#             <p>If you have any further questions, please feel free to create a new ticket.</p>
#             <p>Regards,<br>JHS HR Team</p>
#             """
#         )
        
#         # Send closure confirmation to HR person
#         hr_email = ticket.get('hrEmail')
#         if hr_email:
#             background_tasks.add_task(
#                 sendemail,
#                 [hr_email],
#                 f"HR Ticket {ticketid} Closed Confirmation",
#                 f"""
#                 <p>Dear {ticket.get('assigned', 'HR Team')},</p>
#                 <p>You have successfully closed ticket <strong>{ticketid}</strong>.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
#                 <p>Regards,<br>JHS HR Helpdesk</p>
#                 """
#             )
    
#     if update_data:
#         hr_tickets.update_one({"id": ticketid}, {"$set": update_data})
    
#     return {"message": "Updated", "ticketId": ticketid}

# @app.delete("/api/hr/tickets/{ticketid}")
# async def delete_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
#     """Delete HR ticket"""
#     result = hr_tickets.delete_one({"id": ticketid})
#     if result.deleted_count == 0: 
#         raise HTTPException(404, "Ticket not found")
#     return {"message": "Deleted"}

# @app.get("/api/hr/admin/stats")
# async def get_hr_stats(admin=Depends(get_current_admin)):
#     """Get HR ticket statistics"""
#     tickets = list(hr_tickets.find({}, {"_id": 0}))
#     stats = {"total": len(tickets), "bystatus": {"Open": 0, "Closed": 0}, "byhr": {}}
    
#     for t in tickets:
#         status = t.get("status", "Open")
#         hr = t.get("assigned", "Unassigned")
#         stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
#         if hr not in stats["byhr"]:
#             stats["byhr"][hr] = {"Open": 0, "Closed": 0}
#         stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
#     return stats

# # ==================== LEGACY HR ROUTES (for backward compatibility) ====================
# # These maintain compatibility with existing HR frontend that uses /api/tickets

# @app.get("/api/tickets")
# async def get_hr_tickets_legacy(admin=Depends(get_current_admin)):
#     """Legacy HR route - Get all HR tickets"""
#     return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

# @app.post("/api/tickets")
# async def create_hr_ticket_legacy(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
#     """Legacy HR route - Create new HR ticket"""
#     return await create_hr_ticket(ticket, background_tasks)

# @app.get("/api/tickets/{ticketid}")
# async def get_single_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
#     """Legacy HR route - Get single HR ticket"""
#     return await get_single_hr_ticket(ticketid, admin)

# @app.put("/api/tickets/{ticketid}")
# async def update_hr_ticket_legacy(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Legacy HR route - Update HR ticket"""
#     return await update_hr_ticket(ticketid, body, background_tasks, admin)

# @app.delete("/api/tickets/{ticketid}")
# async def delete_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
#     """Legacy HR route - Delete HR ticket"""
#     return await delete_hr_ticket(ticketid, admin)

# @app.get("/api/admin/stats")
# async def get_hr_stats_legacy(admin=Depends(get_current_admin)):
#     """Legacy HR route - Get HR statistics"""
#     return await get_hr_stats(admin)

# # ==================== IT TICKET ROUTES (with /api/it/ prefix) ====================
# # IMPORTANT: Stats route MUST come before the dynamic {ticket_id} route

# @app.get("/api/it/tickets")
# async def get_it_tickets(admin=Depends(get_current_admin)):
#     """Get all IT tickets"""
#     tickets_list = list(it_tickets.find({}, {"_id": 0}))
    
#     # Calculate TAT for closed tickets
#     for ticket in tickets_list:
#         if ticket.get('assignedAt') and ticket.get('closedAt'):
#             try:
#                 assigned_time = ticket['assignedAt']
#                 closed_time = ticket['closedAt']
#                 if isinstance(assigned_time, datetime) and isinstance(closed_time, datetime):
#                     tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
#                     ticket['tatHours'] = f"{tat_hours} hrs"
#             except:
#                 ticket['tatHours'] = "-"
#         else:
#             ticket['tatHours'] = "-"
    
#     return tickets_list

# @app.get("/api/it/tickets/stats")
# async def get_it_stats(admin=Depends(get_current_admin)):
#     """Get IT ticket statistics - MUST be before /{ticket_id} route"""
#     tickets = list(it_tickets.find({}, {"_id": 0, "status": 1, "assigned": 1}))
#     total = len(tickets)
#     by_status = {}
#     by_it = {}
    
#     for t in tickets:
#         s = t.get("status", "Open")
#         by_status[s] = by_status.get(s, 0) + 1
        
#         it_person = t.get("assigned", "Unassigned")
#         if it_person not in by_it:
#             by_it[it_person] = {"Open": 0, "Closed": 0}
#         by_it[it_person][s] = by_it[it_person].get(s, 0) + 1
    
#     return {
#         "total": total,
#         "byStatus": by_status,
#         "byIT": by_it
#     }

# @app.post("/api/it/tickets")
# async def create_it_ticket(ticket: ITTicketCreate, background_tasks: BackgroundTasks):
#     """Create new IT ticket"""
#     sequence = it_sequences.find_one_and_update(
#         {"_id": "ticket_counter"},
#         {"$inc": {"seq": 1}},
#         upsert=True, return_document=True
#     )
#     count = sequence['seq']
#     ticket_id = f"TICKJHSIT{str(count).zfill(1)}"
    
#     doc = {
#         "id": ticket_id,
#         "name": ticket.name,
#         "email": ticket.email,
#         "phone": ticket.phone,
#         "empCode": ticket.empCode,
#         "assetCode": ticket.assetCode,
#         "issues": ticket.issues,
#         "issueDescription": ticket.issueDescription,
#         "reportingPartner": ticket.reportingPartner,
#         "status": "Open",
#         "assigned": "Unassigned",
#         "itEmail": None,
#         "createdAt": datetime.utcnow(),
#         "assignedAt": None,
#         "remark": None,
#         "closedAt": None
#     }
    
#     it_tickets.insert_one(doc)
    
#     # Send email
#     background_tasks.add_task(
#         sendemail,
#         [ticket.email] + IT_EMAILS,
#         f"IT Ticket {ticket_id} Created",
#         f"<p>Dear {ticket.name},</p><p>Your IT ticket <strong>{ticket_id}</strong> has been created.</p><p><strong>IT Asset:</strong> {ticket.assetCode}</p><p><strong>Issues:</strong> {', '.join(ticket.issues)}</p><p>Regards,<br>JHS IT Helpdesk</p>"
#     )
    
#     return {k: v for k, v in doc.items() if k != '_id'}

# @app.get("/api/it/tickets/{ticket_id}")
# async def get_single_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
#     """Get single IT ticket by ID"""
#     ticket = it_tickets.find_one({"id": ticket_id}, {"_id": 0})
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#     return ticket

# @app.put("/api/it/tickets/{ticket_id}")
# async def update_it_ticket(ticket_id: str, body: ITTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
#     """Update IT ticket"""
#     ticket = it_tickets.find_one({"id": ticket_id})
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
    
#     update_data = {}
#     old_assigned = ticket.get("assigned")
#     old_status = ticket.get("status", "").lower()
    
#     # Handle assignment
#     if body.assigned is not None and body.assigned != old_assigned:
#         update_data["assigned"] = body.assigned
        
#         # Set assignedAt timestamp if not already set
#         if not ticket.get("assignedAt"):
#             update_data["assignedAt"] = datetime.utcnow()
        
#         # Send assignment email to IT person
#         if body.itEmail:
#             update_data["itEmail"] = body.itEmail
#             background_tasks.add_task(
#                 sendemail,
#                 [body.itEmail],
#                 f"IT Ticket {ticket_id} Assigned to You",
#                 f"""
#                 <p>Dear {body.assigned},</p>
#                 <p>The IT ticket <strong>{ticket_id}</strong> has been assigned to you.</p>
#                 <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                 <strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
#                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
#                 <strong>Description:</strong> {ticket.get('issueDescription')}</p>
#                 <p>Please review and take necessary action.</p>
#                 <p>Regards,<br>JHS IT Helpdesk</p>
#                 """
#             )
        
#         # Notify employee about assignment
#         background_tasks.add_task(
#             sendemail,
#             [ticket.get('email')],
#             f"IT Ticket {ticket_id} Assigned",
#             f"""
#             <p>Dear {ticket.get('name')},</p>
#             <p>Your IT ticket <strong>{ticket_id}</strong> has been assigned to <strong>{body.assigned}</strong>.</p>
#             <p>Our team is working on resolving your issue.</p>
#             <p>Regards,<br>JHS IT Helpdesk</p>
#             """
#         )
#     elif body.itEmail is not None:
#         update_data["itEmail"] = body.itEmail
    
#     # Handle status change and closure
#     if body.status:
#         new_status = body.status.capitalize()
        
#         if new_status == "Closed" and old_status != "closed":
#             # Remark is mandatory when closing
#             if not body.remark or not body.remark.strip():
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Remark is mandatory when closing a ticket"
#                 )
            
#             update_data["status"] = "Closed"
#             update_data["remark"] = body.remark.strip()
#             update_data["closedAt"] = datetime.utcnow()
            
#             # Calculate TAT if assignedAt exists
#             tat_text = "N/A"
#             if ticket.get("assignedAt"):
#                 try:
#                     assigned_time = ticket['assignedAt']
#                     closed_time = update_data["closedAt"]
#                     if isinstance(assigned_time, datetime):
#                         tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
#                         tat_text = f"{tat_hours} hours"
#                 except:
#                     tat_text = "N/A"
            
#             # Send closure email to employee
#             background_tasks.add_task(
#                 sendemail,
#                 [ticket.get('email')],
#                 f"IT Ticket {ticket_id} Closed",
#                 f"""
#                 <p>Dear {ticket.get('name')},</p>
#                 <p>Your IT ticket <strong>{ticket_id}</strong> has been successfully resolved and closed.</p>
#                 <p><strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
#                 <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
#                 <strong>Resolution Remark:</strong> {body.remark}</p>
#                 <p><strong>Resolution Time:</strong> {tat_text}</p>
#                 <p>If you face any further issues, please feel free to create a new ticket.</p>
#                 <p>Regards,<br>JHS IT Helpdesk</p>
#                 """
#             )
            
#             # Send closure confirmation to IT person
#             it_email = ticket.get('itEmail') or body.itEmail
#             if it_email:
#                 background_tasks.add_task(
#                     sendemail,
#                     [it_email],
#                     f"IT Ticket {ticket_id} Closed Confirmation",
#                     f"""
#                     <p>Dear {ticket.get('assigned', 'IT Team')},</p>
#                     <p>You have successfully closed IT ticket <strong>{ticket_id}</strong>.</p>
#                     <p><strong>Employee:</strong> {ticket.get('name')}<br>
#                     <strong>Resolution Remark:</strong> {body.remark}<br>
#                     <strong>Resolution Time:</strong> {tat_text}</p>
#                     <p>Regards,<br>JHS IT Helpdesk</p>
#                     """
#                 )
#         else:
#             update_data["status"] = new_status
    
#     if update_data:
#         it_tickets.update_one({"id": ticket_id}, {"$set": update_data})
    
#     return {"message": "Updated", "ticketId": ticket_id}

# @app.delete("/api/it/tickets/{ticket_id}")
# async def delete_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
#     """Delete IT ticket"""
#     res = it_tickets.delete_one({"id": ticket_id})
#     if res.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#     return {"detail": "Deleted"}

# # ==================== FRONTEND ROUTES ====================

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     """HR helpdesk homepage"""
#     return FileResponse("static/index.html")

# @app.get("/admin", response_class=FileResponse)
# async def hr_admin_page():
#     """HR admin dashboard"""
#     return FileResponse("static/hradmin.html")

# @app.get("/it-admin", response_class=FileResponse)
# async def it_admin_page():
#     """IT admin dashboard"""
#     return FileResponse("static/it-admin.html")

# @app.get("/adminlogin", response_class=HTMLResponse)
# async def admin_login_page():
#     """Unified admin login page"""
#     with open("static/adminlogin.html", "r", encoding="utf-8") as f:
#         return f.read()

# @app.get("/.well-known/{path:path}")
# async def ignore_well_known(path: str):
#     return {}

# @app.get("/favicon.ico")
# async def favicon():
#     """Return favicon or 204 No Content"""
#     try:
#         return FileResponse("static/favicon.ico")
#     except:
#         return HTMLResponse(status_code=204)

# # ==================== HEALTH CHECK ====================

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "timestamp": datetime.utcnow().isoformat(),
#         "databases": {
#             "hr_tickets": hr_tickets.count_documents({}),
#             "it_tickets": it_tickets.count_documents({})
#         }
#     }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)










from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import hashlib
from jose import JWTError, jwt

# Load environment
load_dotenv()

# FastAPI app
app = FastAPI(title="JHS Unified Helpdesk API")
print(" JHS Unified Helpdesk API Running")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Config
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---- Brevo SMTP Configuration ----
# Brevo SMTP relay: smtp-relay.brevo.com on port 587 (STARTTLS)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp-relay.brevo.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")          # Brevo account login email
SMTP_PASS = os.getenv("SMTP_PASS")          # Brevo SMTP key (generated in SMTP & API > SMTP tab)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")    # Your single verified Brevo sender email
SENDER_NAME = os.getenv("SENDER_NAME", "JHS Helpdesk")

# Database connections
client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

# HR Database
hr_db = client["HR_Helpdesk"]
hr_tickets = hr_db["Tickets"]
hr_admins = hr_db["Admins"]
hr_sequences = hr_db["sequences"]   # NEW

# IT Database
it_db = client["IT_Helpdesk"]
it_tickets = it_db["Tickets"]
it_admins = it_db["Admins"]
it_sessions = it_db["Sessions"]
it_sequences = it_db["Sequences"]

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HR Email Mapping
HR_EMAILS = {
    "PAYSLIP": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
    "HRMS QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
    "ATTENDANCE": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
    "SALARY QUERY": {"name": "Janhavi Gamare", "email": "janhavi.gamare@jhsassociatesllp.in"},
    "BUDDY REFERRAL": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"},
    "OTHER": {"name": "Krutika Shivshivkar", "email": "krutika.shivshivkar@jhsassociates.in"}
}

# IT Email list
IT_EMAILS = ["mohammad.siddiqui@jhsassociates.in"]

# ==================== PYDANTIC MODELS ====================

# HR Models
class HRTicketCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    empCode: Optional[str] = None
    category: str
    issue: str

class HRTicketUpdate(BaseModel):
    assigned: Optional[str] = None
    status: Optional[str] = None
    hrEmail: Optional[str] = None
    remark: Optional[str] = None

# IT Models
class ITTicketCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str  # Required
    assetCode: Optional[str] = ""  # Made optional
    empCode: Optional[str] = ""  # Optional
    issues: List[str]  # Required list
    issueDescription: str  # Required
    reportingPartner: str  # Required

class ITTicketUpdate(BaseModel):
    assigned: Optional[str] = None
    status: Optional[str] = None
    itEmail: Optional[EmailStr] = None
    remark: Optional[str] = None

class AdminLogin(BaseModel):
    empCode: str
    password: str

class TestEmailRequest(BaseModel):
    to: EmailStr

# ==================== UTILITY FUNCTIONS ====================

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain) == hashed

def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_admin(authorization: str = Header(None)):
    """Verify JWT token and return admin info"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def sendemail(recipients: List[str], subject: str, body: str) -> bool:
    """
    Send email via Brevo SMTP relay.

    IMPORTANT (Brevo free tier):
    - The 'From' address MUST be your single verified sender email
      (set SENDER_EMAIL in .env). Brevo will reject/bounce emails
      sent from any other 'From' address.
    - Recipients ('To') can be ANY email address - no restriction there.
    - SMTP_USER/SMTP_PASS = your Brevo SMTP login + SMTP key
      (NOT your Brevo account password - generate the key under
      SMTP & API > SMTP tab in the Brevo dashboard).

    Returns True if the send call succeeded, False otherwise.
    Logs detailed success/failure so you can trace which stage
    (create / assign / close) failed.
    """
    # Small delay to be gentle with rate limits
    time.sleep(1.5)

    valid_recipients = [r for r in recipients if r and r.strip()]
    if not valid_recipients:
        logger.warning(f"⚠️ EMAIL SKIPPED (no valid recipients) → subject='{subject}'")
        return False

    if not SMTP_USER or not SMTP_PASS or not SENDER_EMAIL:
        logger.error(
            "❌ EMAIL CONFIG MISSING — check SMTP_USER, SMTP_PASS, "
            "SENDER_EMAIL in your .env (Brevo SMTP credentials)"
        )
        return False

    logger.info(f"🔄 EMAIL → {valid_recipients}, subject='{subject}'")

    try:
        msg = MIMEMultipart()
        msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg['To'] = ", ".join(valid_recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)

        server.sendmail(SENDER_EMAIL, valid_recipients, msg.as_string())
        server.quit()

        logger.info(f"✅ EMAIL SENT → {valid_recipients} | subject='{subject}'")
        return True

    except smtplib.SMTPAuthenticationError as e:
        logger.error(
            f"❌ EMAIL AUTH FAILED — verify SMTP_USER/SMTP_PASS (Brevo SMTP key). "
            f"Detail: {str(e)}"
        )
        return False
    except smtplib.SMTPRecipientsRefused as e:
        logger.error(f"❌ EMAIL RECIPIENTS REFUSED → {valid_recipients} | Detail: {str(e)}")
        return False
    except smtplib.SMTPSenderRefused as e:
        logger.error(
            f"❌ EMAIL SENDER REFUSED — '{SENDER_EMAIL}' may not be a verified "
            f"sender in Brevo (Senders & IP > Senders). Detail: {str(e)}"
        )
        return False
    except smtplib.SMTPException as e:
        logger.error(f"❌ SMTP ERROR → {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ EMAIL FAILED → {str(e)}")
        return False

# ==================== EMAIL TEST ROUTE ====================

@app.post("/api/test-email")
async def test_email(body: TestEmailRequest):
    """
    Quick standalone test of Brevo SMTP connectivity.
    Use this BEFORE testing ticket create/assign/close flows
    to confirm SMTP_USER, SMTP_PASS, SENDER_EMAIL are correct
    and Brevo is delivering.

    POST { "to": "your_test_inbox@gmail.com" }
    """
    success = sendemail(
        [body.to],
        "JHS Helpdesk - Brevo SMTP Test",
        f"""
        <p>This is a test email sent via Brevo SMTP relay.</p>
        <p>If you received this, your email configuration is working correctly
        for ticket creation, assignment, and closure notifications.</p>
        <p>Sent at: {datetime.utcnow().isoformat()} UTC</p>
        """
    )
    if success:
        return {"status": "sent", "message": "Check inbox/spam folder", "to": body.to}
    raise HTTPException(
        status_code=500,
        detail="Email send failed - check server logs for the exact reason "
               "(auth error, sender not verified, etc.)"
    )

# ==================== AUTHENTICATION ROUTES ====================

@app.post("/api/admin/login")
async def unified_admin_login(body: AdminLogin):
    """
    Unified login endpoint for both HR and IT admins.
    First checks HR admins, then IT admins.
    """
    empCode = body.empCode.upper().strip()
    password = body.password
    
    if not empCode or not password:
        raise HTTPException(status_code=400, detail="empCode and password required")
    
    logger.info(f"Login attempt for empCode: {empCode}")
    
    # Try HR admin first
    hr_admin = hr_admins.find_one({"empCodes": empCode, "password": password})
    
    if hr_admin:
        logger.info(f"HR Admin found: {hr_admin.get('name')}")
        token = create_access_token({
            "sub": empCode,
            "role": "admin",
            "type": "hr",
            "name": hr_admin.get("name")
        })
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "name": hr_admin.get("name"),
            "helpdesk": "hr"
        }
    
    # Try IT admin
    it_admin = it_admins.find_one({"empCode": empCode})
    
    if it_admin:
        logger.info(f"IT Admin found: {it_admin.get('name')}")
        
        # Verify password
        if not verify_password(password, it_admin["password"]):
            logger.error("Password verification failed")
            raise HTTPException(status_code=401, detail="Invalid password")
        
        logger.info("Password verified successfully")
        
        token = create_access_token({
            "sub": empCode,
            "role": "admin",
            "type": "it",
            "name": it_admin.get("name")
        })
        
        # Store session in IT sessions collection
        session_doc = {
            "empCode": empCode,
            "token": token,
            "isValid": True,
            "createdAt": datetime.utcnow(),
            "expiresAt": datetime.utcnow() + timedelta(hours=1)
        }
        
        it_sessions.update_one(
            {"empCode": empCode},
            {"$set": session_doc},
            upsert=True
        )
        
        logger.info(f"Login successful for IT admin {empCode}")
        
        return {
            "access_token": token,
            "token": token,  # For backward compatibility
            "token_type": "bearer",
            "empCode": empCode,
            "name": it_admin.get("name"),
            "helpdesk": "it"
        }
    
    # No admin found
    logger.error(f"Admin not found for empCode: {empCode}")
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ==================== HR TICKET ROUTES (with /api/hr/ prefix) ====================

@app.get("/api/hr/tickets")
async def get_hr_tickets(admin=Depends(get_current_admin)):
    """Get all HR tickets"""
    return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

@app.post("/api/hr/tickets")
async def create_hr_ticket(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
    """Create new HR ticket"""
    sequence = hr_sequences.find_one_and_update(
        {"_id": "hr_ticket_counter"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )

    count = sequence["seq"]
    ticket_id = f"TICKJHSHR{str(count).zfill(2)}"
    
    
    category = ticket.category.upper().strip()
    hr_data = HR_EMAILS.get(category)
    assigned_name = hr_data["name"] if hr_data else "Unassigned"
    assigned_email = hr_data["email"] if hr_data else None
    
    ticket_data = {
        "id": ticket_id, "name": ticket.name, "email": ticket.email,
        "phone": ticket.phone, "empCode": ticket.empCode,
        "category": ticket.category, "issue": ticket.issue,
        "status": "Open", "assigned": assigned_name, "hrEmail": assigned_email,
        "assignedAt": datetime.utcnow() if hr_data else None,
        "createdAt": datetime.utcnow(), "remark": ""
    }
    
    hr_tickets.insert_one(ticket_data)
    
    # Email to employee - confirmation, now includes the full issue description
    background_tasks.add_task(
        sendemail, [ticket.email],
        f"JHS HR - Ticket {ticket_id} Created",
        f"""
        <p>Dear {ticket.name},</p>
        <p>Your HR ticket <strong>{ticket_id}</strong> has been created.</p>
        <p><strong>Category:</strong> {ticket.category}<br>
        <strong>Issue Description:</strong> {ticket.issue}<br>
        <strong>Assigned To:</strong> {assigned_name}</p>
        <p>Our HR team will get back to you shortly.</p>
        <p>Regards,<br>JHS HR Team</p>
        """
    )
    
    # Email to assigned HR person - full details needed to act on the ticket
    if assigned_email:
        background_tasks.add_task(
            sendemail, [assigned_email],
            f"New Ticket: {ticket_id}",
            f"""
            <p>Dear {assigned_name},</p>
            <p>Ticket <strong>{ticket_id}</strong> has been assigned to you.</p>
            <p><strong>Employee Name:</strong> {ticket.name}<br>
            <strong>Employee Code:</strong> {ticket.empCode or 'N/A'}<br>
            <strong>Phone:</strong> {ticket.phone or 'N/A'}<br>
            <strong>Email:</strong> {ticket.email}<br>
            <strong>Category:</strong> {ticket.category}<br>
            <strong>Issue Description:</strong> {ticket.issue}</p>
            <p>Please review and take necessary action.</p>
            <p>Regards,<br>JHS HR Helpdesk</p>
            """
        )
    
    return {"message": "Ticket created", "ticketId": ticket_id, "assignedTo": assigned_name}

@app.get("/api/hr/tickets/{ticketid}")
async def get_single_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
    """Get single HR ticket by ID"""
    ticket = hr_tickets.find_one({"id": ticketid})
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    ticket.pop("_id", None)
    return ticket

@app.put("/api/hr/tickets/{ticketid}")
async def update_hr_ticket(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
    """Update HR ticket"""
    ticket = hr_tickets.find_one({"id": ticketid})
    if not ticket: 
        raise HTTPException(404, "Ticket not found")
    
    update_data = {}
    old_assigned = ticket.get("assigned")
    old_status = ticket.get("status", "").lower()
    
    # Handle reassignment
    if body.assigned and body.assigned != old_assigned:
        update_data["assigned"] = body.assigned
        update_data["assignedAt"] = datetime.utcnow()
        if body.hrEmail: 
            update_data["hrEmail"] = body.hrEmail
        
        # Send reassignment email to new HR person
        if body.hrEmail:
            background_tasks.add_task(
                sendemail,
                [body.hrEmail],
                f"HR Ticket {ticketid} Assigned to You",
                f"""
                <p>Dear {body.assigned},</p>
                <p>The ticket <strong>{ticketid}</strong> has been assigned to you.</p>
                <p><strong>Employee:</strong> {ticket.get('name')}<br>
                <strong>Category:</strong> {ticket.get('category')}<br>
                <strong>Issue Description:</strong> {ticket.get('issue')}</p>
                <p>Please review and take necessary action.</p>
                <p>Regards,<br>JHS HR Helpdesk</p>
                """
            )
    
    # Handle closure
    if body.status and body.status.lower() == "closed" and old_status != "closed":
        update_data["status"] = "Closed"
        update_data["closedAt"] = datetime.utcnow()
        update_data["remark"] = body.remark if body.remark else ""
        
        # Send closure email to employee - includes remark
        background_tasks.add_task(
            sendemail,
            [ticket.get('email')],
            f"HR Ticket {ticketid} Closed",
            f"""
            <p>Dear {ticket.get('name')},</p>
            <p>Your HR ticket <strong>{ticketid}</strong> has been closed.</p>
            <p><strong>Category:</strong> {ticket.get('category')}<br>
            <strong>Issue Description:</strong> {ticket.get('issue')}<br>
            <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
            <p>If you have any further questions, please feel free to create a new ticket.</p>
            <p>Regards,<br>JHS HR Team</p>
            """
        )
        
        # Send closure confirmation to HR person - includes remark
        hr_email = ticket.get('hrEmail')
        if hr_email:
            background_tasks.add_task(
                sendemail,
                [hr_email],
                f"HR Ticket {ticketid} Closed Confirmation",
                f"""
                <p>Dear {ticket.get('assigned', 'HR Team')},</p>
                <p>You have successfully closed ticket <strong>{ticketid}</strong>.</p>
                <p><strong>Employee:</strong> {ticket.get('name')}<br>
                <strong>Issue Description:</strong> {ticket.get('issue')}<br>
                <strong>Remark:</strong> {body.remark if body.remark else 'N/A'}</p>
                <p>Regards,<br>JHS HR Helpdesk</p>
                """
            )
    
    if update_data:
        hr_tickets.update_one({"id": ticketid}, {"$set": update_data})
    
    return {"message": "Updated", "ticketId": ticketid}

@app.delete("/api/hr/tickets/{ticketid}")
async def delete_hr_ticket(ticketid: str, admin=Depends(get_current_admin)):
    """Delete HR ticket"""
    result = hr_tickets.delete_one({"id": ticketid})
    if result.deleted_count == 0: 
        raise HTTPException(404, "Ticket not found")
    return {"message": "Deleted"}

@app.get("/api/hr/admin/stats")
async def get_hr_stats(admin=Depends(get_current_admin)):
    """Get HR ticket statistics"""
    tickets = list(hr_tickets.find({}, {"_id": 0}))
    stats = {"total": len(tickets), "bystatus": {"Open": 0, "Closed": 0}, "byhr": {}}
    
    for t in tickets:
        status = t.get("status", "Open")
        hr = t.get("assigned", "Unassigned")
        stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
        if hr not in stats["byhr"]:
            stats["byhr"][hr] = {"Open": 0, "Closed": 0}
        stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
    return stats

# ==================== LEGACY HR ROUTES (for backward compatibility) ====================
# These maintain compatibility with existing HR frontend that uses /api/tickets

@app.get("/api/tickets")
async def get_hr_tickets_legacy(admin=Depends(get_current_admin)):
    """Legacy HR route - Get all HR tickets"""
    return list(hr_tickets.find({}, {"_id": 0}).sort("createdAt", -1))

@app.post("/api/tickets")
async def create_hr_ticket_legacy(ticket: HRTicketCreate, background_tasks: BackgroundTasks):
    """Legacy HR route - Create new HR ticket"""
    return await create_hr_ticket(ticket, background_tasks)

@app.get("/api/tickets/{ticketid}")
async def get_single_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
    """Legacy HR route - Get single HR ticket"""
    return await get_single_hr_ticket(ticketid, admin)

@app.put("/api/tickets/{ticketid}")
async def update_hr_ticket_legacy(ticketid: str, body: HRTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
    """Legacy HR route - Update HR ticket"""
    return await update_hr_ticket(ticketid, body, background_tasks, admin)

@app.delete("/api/tickets/{ticketid}")
async def delete_hr_ticket_legacy(ticketid: str, admin=Depends(get_current_admin)):
    """Legacy HR route - Delete HR ticket"""
    return await delete_hr_ticket(ticketid, admin)

@app.get("/api/admin/stats")
async def get_hr_stats_legacy(admin=Depends(get_current_admin)):
    """Legacy HR route - Get HR statistics"""
    return await get_hr_stats(admin)

# ==================== IT TICKET ROUTES (with /api/it/ prefix) ====================
# IMPORTANT: Stats route MUST come before the dynamic {ticket_id} route

@app.get("/api/it/tickets")
async def get_it_tickets(admin=Depends(get_current_admin)):
    """Get all IT tickets"""
    tickets_list = list(it_tickets.find({}, {"_id": 0}))
    
    # Calculate TAT for closed tickets
    for ticket in tickets_list:
        if ticket.get('assignedAt') and ticket.get('closedAt'):
            try:
                assigned_time = ticket['assignedAt']
                closed_time = ticket['closedAt']
                if isinstance(assigned_time, datetime) and isinstance(closed_time, datetime):
                    tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
                    ticket['tatHours'] = f"{tat_hours} hrs"
            except:
                ticket['tatHours'] = "-"
        else:
            ticket['tatHours'] = "-"
    
    return tickets_list

@app.get("/api/it/tickets/stats")
async def get_it_stats(admin=Depends(get_current_admin)):
    """Get IT ticket statistics - MUST be before /{ticket_id} route"""
    tickets = list(it_tickets.find({}, {"_id": 0, "status": 1, "assigned": 1}))
    total = len(tickets)
    by_status = {}
    by_it = {}
    
    for t in tickets:
        s = t.get("status", "Open")
        by_status[s] = by_status.get(s, 0) + 1
        
        it_person = t.get("assigned", "Unassigned")
        if it_person not in by_it:
            by_it[it_person] = {"Open": 0, "Closed": 0}
        by_it[it_person][s] = by_it[it_person].get(s, 0) + 1
    
    return {
        "total": total,
        "byStatus": by_status,
        "byIT": by_it
    }

@app.post("/api/it/tickets")
async def create_it_ticket(ticket: ITTicketCreate, background_tasks: BackgroundTasks):
    """Create new IT ticket"""
    sequence = it_sequences.find_one_and_update(
        {"_id": "ticket_counter"},
        {"$inc": {"seq": 1}},
        upsert=True, return_document=True
    )
    count = sequence['seq']
    ticket_id = f"TICKJHSIT{str(count).zfill(1)}"
    
    doc = {
        "id": ticket_id,
        "name": ticket.name,
        "email": ticket.email,
        "phone": ticket.phone,
        "empCode": ticket.empCode,
        "assetCode": ticket.assetCode,
        "issues": ticket.issues,
        "issueDescription": ticket.issueDescription,
        "reportingPartner": ticket.reportingPartner,
        "status": "Open",
        "assigned": "Unassigned",
        "itEmail": None,
        "createdAt": datetime.utcnow(),
        "assignedAt": None,
        "remark": None,
        "closedAt": None
    }
    
    it_tickets.insert_one(doc)
    
    # Email to employee - simple confirmation with issue description
    background_tasks.add_task(
        sendemail,
        [ticket.email],
        f"IT Ticket {ticket_id} Created",
        f"""
        <p>Dear {ticket.name},</p>
        <p>Your IT ticket <strong>{ticket_id}</strong> has been created.</p>
        <p><strong>IT Asset:</strong> {ticket.assetCode or 'N/A'}<br>
        <strong>Issues:</strong> {', '.join(ticket.issues)}<br>
        <strong>Issue Description:</strong> {ticket.issueDescription}</p>
        <p>Our IT team will get in touch with you shortly.</p>
        <p>Regards,<br>JHS IT Helpdesk</p>
        """
    )
    
    # Email to IT team inbox - full details needed to action the ticket
    # (no specific engineer assigned yet, so addressed generically)
    background_tasks.add_task(
        sendemail,
        IT_EMAILS,
        f"New IT Ticket {ticket_id} Raised",
        f"""
        <p>Dear IT Engineer,</p>
        <p>A new IT ticket <strong>{ticket_id}</strong> has been raised.</p>
        <p><strong>Employee Name:</strong> {ticket.name}<br>
        <strong>Employee Code:</strong> {ticket.empCode or 'N/A'}<br>
        <strong>Phone:</strong> {ticket.phone}<br>
        <strong>Email:</strong> {ticket.email}<br>
        <strong>Reporting Partner:</strong> {ticket.reportingPartner}<br>
        <strong>IT Asset:</strong> {ticket.assetCode or 'N/A'}<br>
        <strong>Issues:</strong> {', '.join(ticket.issues)}<br>
        <strong>Issue Description:</strong> {ticket.issueDescription}</p>
        <p>Please review and take necessary action.</p>
        <p>Regards,<br>JHS IT Helpdesk</p>
        """
    )
    
    return {k: v for k, v in doc.items() if k != '_id'}

@app.get("/api/it/tickets/{ticket_id}")
async def get_single_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
    """Get single IT ticket by ID"""
    ticket = it_tickets.find_one({"id": ticket_id}, {"_id": 0})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.put("/api/it/tickets/{ticket_id}")
async def update_it_ticket(ticket_id: str, body: ITTicketUpdate, background_tasks: BackgroundTasks, admin=Depends(get_current_admin)):
    """Update IT ticket"""
    ticket = it_tickets.find_one({"id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    update_data = {}
    old_assigned = ticket.get("assigned")
    old_status = ticket.get("status", "").lower()
    
    # Handle assignment
    if body.assigned is not None and body.assigned != old_assigned:
        update_data["assigned"] = body.assigned
        
        # Set assignedAt timestamp if not already set
        if not ticket.get("assignedAt"):
            update_data["assignedAt"] = datetime.utcnow()
        
        # Send assignment email to IT person - includes issue description
        if body.itEmail:
            update_data["itEmail"] = body.itEmail
            background_tasks.add_task(
                sendemail,
                [body.itEmail],
                f"IT Ticket {ticket_id} Assigned to You",
                f"""
                <p>Dear {body.assigned},</p>
                <p>The IT ticket <strong>{ticket_id}</strong> has been assigned to you.</p>
                <p><strong>Employee:</strong> {ticket.get('name')}<br>
                <strong>Employee Code:</strong> {ticket.get('empCode') or 'N/A'}<br>
                <strong>Phone:</strong> {ticket.get('phone', 'N/A')}<br>
                <strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
                <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
                <strong>Issue Description:</strong> {ticket.get('issueDescription')}</p>
                <p>Please review and take necessary action.</p>
                <p>Regards,<br>JHS IT Helpdesk</p>
                """
            )
        
        # Notify employee about assignment
        background_tasks.add_task(
            sendemail,
            [ticket.get('email')],
            f"IT Ticket {ticket_id} Assigned",
            f"""
            <p>Dear {ticket.get('name')},</p>
            <p>Your IT ticket <strong>{ticket_id}</strong> has been assigned to <strong>{body.assigned}</strong>.</p>
            <p>Our team is working on resolving your issue.</p>
            <p>Regards,<br>JHS IT Helpdesk</p>
            """
        )
    elif body.itEmail is not None:
        update_data["itEmail"] = body.itEmail
    
    # Handle status change and closure
    if body.status:
        new_status = body.status.capitalize()
        
        if new_status == "Closed" and old_status != "closed":
            # Remark is mandatory when closing
            if not body.remark or not body.remark.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Remark is mandatory when closing a ticket"
                )
            
            update_data["status"] = "Closed"
            update_data["remark"] = body.remark.strip()
            update_data["closedAt"] = datetime.utcnow()
            
            # Calculate TAT if assignedAt exists
            tat_text = "N/A"
            if ticket.get("assignedAt"):
                try:
                    assigned_time = ticket['assignedAt']
                    closed_time = update_data["closedAt"]
                    if isinstance(assigned_time, datetime):
                        tat_hours = round((closed_time - assigned_time).total_seconds() / 3600, 2)
                        tat_text = f"{tat_hours} hours"
                except:
                    tat_text = "N/A"
            
            # Send closure email to employee - includes remark
            background_tasks.add_task(
                sendemail,
                [ticket.get('email')],
                f"IT Ticket {ticket_id} Closed",
                f"""
                <p>Dear {ticket.get('name')},</p>
                <p>Your IT ticket <strong>{ticket_id}</strong> has been successfully resolved and closed.</p>
                <p><strong>Asset Code:</strong> {ticket.get('assetCode', 'N/A')}<br>
                <strong>Issues:</strong> {', '.join(ticket.get('issues', []))}<br>
                <strong>Issue Description:</strong> {ticket.get('issueDescription', 'N/A')}<br>
                <strong>Resolution Remark:</strong> {body.remark}</p>
                <p><strong>Resolution Time:</strong> {tat_text}</p>
                <p>If you face any further issues, please feel free to create a new ticket.</p>
                <p>Regards,<br>JHS IT Helpdesk</p>
                """
            )
            
            # Send closure confirmation to IT person - includes remark
            it_email = ticket.get('itEmail') or body.itEmail
            if it_email:
                background_tasks.add_task(
                    sendemail,
                    [it_email],
                    f"IT Ticket {ticket_id} Closed Confirmation",
                    f"""
                    <p>Dear {ticket.get('assigned', 'IT Team')},</p>
                    <p>You have successfully closed IT ticket <strong>{ticket_id}</strong>.</p>
                    <p><strong>Employee:</strong> {ticket.get('name')}<br>
                    <strong>Issue Description:</strong> {ticket.get('issueDescription', 'N/A')}<br>
                    <strong>Resolution Remark:</strong> {body.remark}<br>
                    <strong>Resolution Time:</strong> {tat_text}</p>
                    <p>Regards,<br>JHS IT Helpdesk</p>
                    """
                )
        else:
            update_data["status"] = new_status
    
    if update_data:
        it_tickets.update_one({"id": ticket_id}, {"$set": update_data})
    
    return {"message": "Updated", "ticketId": ticket_id}

@app.delete("/api/it/tickets/{ticket_id}")
async def delete_it_ticket(ticket_id: str, admin=Depends(get_current_admin)):
    """Delete IT ticket"""
    res = it_tickets.delete_one({"id": ticket_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"detail": "Deleted"}

# ==================== FRONTEND ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """HR helpdesk homepage"""
    return FileResponse("static/index.html")

@app.get("/admin", response_class=FileResponse)
async def hr_admin_page():
    """HR admin dashboard"""
    return FileResponse("static/hradmin.html")

@app.get("/it-admin", response_class=FileResponse)
async def it_admin_page():
    """IT admin dashboard"""
    return FileResponse("static/it-admin.html")

@app.get("/adminlogin", response_class=HTMLResponse)
async def admin_login_page():
    """Unified admin login page"""
    with open("static/adminlogin.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/.well-known/{path:path}")
async def ignore_well_known(path: str):
    return {}

@app.get("/favicon.ico")
async def favicon():
    """Return favicon or 204 No Content"""
    try:
        return FileResponse("static/favicon.ico")
    except:
        return HTMLResponse(status_code=204)

# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "databases": {
            "hr_tickets": hr_tickets.count_documents({}),
            "it_tickets": it_tickets.count_documents({})
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)