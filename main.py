

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import Optional, Dict, Any, List
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="JHS HR Helpdesk API")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
print(os.getenv("MONGO_CONNECTION_STRING"))
db = client["HR_Helpdesk"]
ticketscol = db["Tickets"]
admins = db["Admins"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

HR_EMAILS = {
    # 'Janhavi Gamare': 'janhavi.gamare@jhsassociatesllp.in', 
    # 'Darshan Shah': 'darshan.shah@jhsassociates.in', 
    # 'Krutika Shivshivkar': 'krutika.shivshivkar@jhsassociates.in', 
    # 'Fiza Kudalkar': 'fiza.kudalkar@jhsassociates.in'
    'Janhavi Gamare': 'vasugadde1100@gmaul.com', 
    'Darshan Shah': 'vasugadde0203@gmail.com', 
    'Krutika Shivshivkar': 'vasugadde1234@gmail.com', 
    'Fiza Kudalkar': 'vasugadde1100@gmail.com'
}

class TicketCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    empCode: Optional[str] = None
    category: str
    issue: str

class TicketUpdate(BaseModel):
    assigned: Optional[str] = None
    status: Optional[str] = None
    hrEmail: Optional[str] = None

# ✅ FIXED: Corrected sendemail function
def sendemail(recipients: List[str], subject: str, body: str):
    logger.info(f"🔄 EMAIL ATTEMPT → Recipients: {recipients}, Subject: {subject}")
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        
        valid_recipients = [r for r in recipients if r and r.strip()]
        logger.info(f"📧 Valid recipients: {valid_recipients}")
        
        if valid_recipients:
            server.sendmail(SMTP_USER, valid_recipients, msg.as_string())
            logger.info(f"✅ EMAILS SENT → {valid_recipients}")
        else:
            logger.warning("⚠️ No valid recipients")
        server.quit()
    except Exception as e:
        logger.error(f"❌ EMAIL FAILED → {str(e)}")

@app.post("/api/admin/login")
async def admin_login(body: Dict[str, Any]):
    empCode = body.get("empCode")
    password = body.get("password")
    if not empCode or not password:
        raise HTTPException(status_code=400, detail="empCode and password required")
    admin = admins.find_one({"empCode": empCode.upper()})
    if not admin or admin.get("password") != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "empCode": empCode.upper()}

@app.post("/api/admin/register")
async def admin_register(body: Dict[str, Any]):
    name = body.get("name")
    empCode = body.get("empCode")
    password = body.get("password")
    if not all([name, empCode, password]):
        raise HTTPException(status_code=400, detail="Name, empCode, and password required")
    if admins.find_one({"empCode": empCode.upper()}):
        raise HTTPException(status_code=400, detail="Admin already exists")
    admins.insert_one({
        "empCode": empCode.upper(),
        "password": password,
        "name": name,
        "createdAt": datetime.utcnow()
    })
    return {"message": f"Admin {empCode} registered successfully"}

@app.get("/api/tickets")
async def get_tickets():
    return list(ticketscol.find({}, {"_id": 0}).sort("createdAt", -1))

@app.post("/api/tickets")
async def create_ticket(ticket: TicketCreate, background_tasks: BackgroundTasks):
    count = ticketscol.count_documents({})
    ticket_id = f"TICKJHSHR{str(count + 1).zfill(2)}"
    
    ticket_data = {
        "id": ticket_id, "name": ticket.name, "email": ticket.email,
        "phone": ticket.phone, "empCode": ticket.empCode,
        "category": ticket.category, "issue": ticket.issue,
        "status": "Open", "assigned": "Unassigned", "hrEmail": None,
        "createdAt": datetime.utcnow()
    }
    
    ticketscol.insert_one(ticket_data)
    
    user_subject = f"JHS HR - Ticket {ticket_id} Created"
    user_body = f"Dear {ticket.name},\n\nTicket {ticket_id} created successfully.\nCategory: {ticket.category}\nIssue: {ticket.issue}\n\nHR will contact you soon.\n\nJHS HR Team"
    
    hr_subject = f"New HR Ticket: {ticket_id}"
    hr_body = f"New ticket {ticket_id}\nUser: {ticket.name} ({ticket.email})\nIssue: {ticket.issue}"
    
    background_tasks.add_task(sendemail, [ticket.email], user_subject, user_body)
    background_tasks.add_task(sendemail, list(HR_EMAILS.values()), hr_subject, hr_body)
    
    return {"message": f"Ticket {ticket_id} created", "ticketId": ticket_id}


@app.put("/api/tickets/{ticketid}")
async def update_ticket(ticketid: str, body: TicketUpdate, background_tasks: BackgroundTasks):
    ticket = ticketscol.find_one({"id": ticketid})
    if not ticket: 
        raise HTTPException(404, "Ticket not found")
    
    logger.info(f"🔄 UPDATE → Ticket: {ticketid}, Body: {body}")
    
    update_data = {}
    old_assigned = ticket.get("assigned")
    if body.assigned and body.assigned != old_assigned:
        update_data["assigned"] = body.assigned
        update_data["assignedAt"] = datetime.utcnow()
        if body.hrEmail: 
            update_data["hrEmail"] = body.hrEmail
    
    if body.status and body.status.lower() == "closed" and ticket.get("status", "").lower() != "closed":
        update_data["status"] = "Closed"
        update_data["closedAt"] = datetime.utcnow()
    
    if update_data:
        ticketscol.update_one({"id": ticketid}, {"$set": update_data})
    
    user_email = ticket.get("email")
    user_name = ticket.get("name")
    assigned_hr_name = body.assigned or ticket.get("assigned", "Unassigned")
    assigned_hr_email = HR_EMAILS.get(assigned_hr_name) if assigned_hr_name != "Unassigned" else None
    
    # Assignment emails
    if body.assigned and body.assigned != old_assigned and assigned_hr_email:
        background_tasks.add_task(sendemail, [user_email], 
            f"JHS Ticket {ticketid} Assigned to {assigned_hr_name}",
            f"Dear {user_name},\n\nTicket {ticketid} assigned to {assigned_hr_name}.")
        background_tasks.add_task(sendemail, [assigned_hr_email], 
            f"New Assignment: Ticket {ticketid}",
            f"Dear {assigned_hr_name},\n\nTicket {ticketid} assigned to you.\nUser: {user_name}")
    
    # Close emails
    if body.status and body.status.lower() == "closed":
        if assigned_hr_email:
            background_tasks.add_task(sendemail, [user_email], 
                f"JHS Ticket {ticketid} - CLOSED",
                f"Dear {user_name},\n\nTicket {ticketid} closed.")
            background_tasks.add_task(sendemail, [assigned_hr_email], 
                f"Ticket {ticketid} - CLOSED",
                f"Dear {assigned_hr_name},\n\nTicket {ticketid} marked CLOSED.")
        else:
            background_tasks.add_task(sendemail, [user_email], 
                f"JHS Ticket {ticketid} - CLOSED",
                f"Dear {user_name},\n\nTicket {ticketid} closed.")
    
    return {"message": "Updated", "ticketId": ticketid}

@app.delete("/api/tickets/{ticketid}")
async def delete_ticket(ticketid: str):
    result = ticketscol.delete_one({"id": ticketid})
    if result.deleted_count == 0: raise HTTPException(404, "Ticket not found")
    return {"message": "Deleted"}

@app.get("/api/tickets/stats")
async def get_tickets_stats():
    tickets = list(ticketscol.find({}, {"_id": 0}))
    stats = {"total": len(tickets), "bystatus": {}, "byhr": {}}
    
    for t in tickets:
        status = t.get("status", "Open")
        hr = t.get("assigned", "Unassigned")
        stats["bystatus"][status] = stats["bystatus"].get(status, 0) + 1
        
        if hr not in stats["byhr"]:
            stats["byhr"][hr] = {"Open": 0, "Closed": 0}
        stats["byhr"][hr][status] = stats["byhr"][hr].get(status, 0) + 1
    
    return stats

@app.get("/api/tickets/{ticketid}")
async def get_ticket(ticketid: str):
    ticket = ticketscol.find_one({"id": ticketid})
    if not ticket: raise HTTPException(404, "Ticket not found")
    ticket.pop("_id", None)
    return ticket

@app.get("/test-email")
async def test_email(background_tasks: BackgroundTasks):
    background_tasks.add_task(sendemail, ["your-email@gmail.com"], "JHS HR TEST", "Working!")
    return {"status": "Test sent - check console"}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    with open("static/admin.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/adminlogin", response_class=HTMLResponse)
async def admin_login_page():
    with open("static/adminlogin.html", "r", encoding="utf-8") as f:
        return f.read()


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
