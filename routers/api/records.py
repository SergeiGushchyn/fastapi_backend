from fastapi import APIRouter, HTTPException
from typing import List
from internal.worksheet import get_worksheet
from routers.authentication import get_current_user

router = APIRouter()

def get_assigned_record(record):
   record["SCOT Options"] = record["SCOT Options"].partition(" - ")[0]
   return {
      "faculty_name": record["Faculty Full Name:"],
      "options": record["SCOT Options"],
      "email_sent": record["Email Sent"],
      "first_visit": record["First Visit"],
      "report_reviewed": record["Report Reviewed"],
      "report_sent": record["Report Sent"]
   }

@router.get("/records")
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

@router.get("/unassigned")
async def get_unassigned_records():
   wks = await get_worksheet()
   all_records = wks.get_all_records()
   unassigned_records = []
   for record in all_records:
      if not record["Assigned SCOT"]:
         record["SCOT Options"] = record["SCOT Options"].partition(" - ")[0]
         unassigned_records.append(
            {
               "faculty_name": record["Faculty Full Name:"],
               "course_name": record["Course Name and Section:"],
               "course_days": record["Course Days"],
               "course_time": record["Course Time:"],
               "options": record["SCOT Options"]
            }
         )
   return unassigned_records

@router.get("/assigned")
async def get_assigned_records():
   wks = await get_worksheet()
   all_records = wks.get_all_records()
   assigned_records = {}
   for record in all_records:
      if record["Assigned SCOT"]:
         if record["Assigned SCOT"] in assigned_records:
            assigned_records[record["Assigned SCOT"]].append(get_assigned_record(record))
         else:
            assigned_records[record["Assigned SCOT"]] = []
            assigned_records[record["Assigned SCOT"]].append(get_assigned_record(record))
   return assigned_records