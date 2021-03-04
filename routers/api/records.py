from fastapi import APIRouter, HTTPException
from typing import List
from internal.worksheet import get_worksheet
from models.user import User
from models.record import Record
from routers.authentication import get_current_user

router = APIRouter()

@router.get("/records", response_model=List[Record])
async def get_user_records():
   wks = await get_worksheet()
   all_records = wks.get_all_records()
   records = []
   for item in wks.findall("Federico Reader"):
      # indexes of the Google Spreadsheet are 2 positions higher from regular array indexing
      ri = item.row - 2
      all_records[ri]["SCOT Options"] = all_records[ri]["SCOT Options"].partition(" - ")[0]
      records.append(
            {
               "row": item.row, 
               "faculty_name": all_records[ri]["Faculty Full Name:"],
               "course_name": all_records[ri]["Course Name and Section:"],
               "course_days": all_records[ri]["Course Days"],
               "course_time": all_records[ri]["Course Time:"],
               "options": all_records[ri]["SCOT Options"],
               "email_sent": all_records[ri]["Email Sent"],
               "first_visit": all_records[ri]["First Visit"],
               "report_reviewed": all_records[ri]["Report Reviewed"],
               "report_sent": all_records[ri]["Report Sent"],
               "comments": all_records[ri]["Comments"]
            }
      )
   return records