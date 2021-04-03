from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from pydantic import BaseModel
from internal.worksheet import get_worksheet
from routers.authentication import get_current_user
from internal.column_indexes import col_ind
from models.user import User

import psycopg2

router = APIRouter()

class RecordData(BaseModel):
   row: int
   column: str
   data: str

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
async def get_user_records(user: User = Depends(get_current_user)):
   wks = await get_worksheet()
   all_records = wks.get_all_records()
   records = []
   for item in wks.findall(user.first_name + " " + user.last_name):
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

@router.post("/records")
async def post_user_record(record_data: RecordData, user: User = Depends(get_current_user)):
   try:
      wks = await get_worksheet()
      wks.update_cell(record_data.row, col_ind[record_data.column], record_data.data)
      return "Success"
   except psycopg2.Error as e:
      raise HTTPException(
      status_code=status.HTTP_500_SERVER_ERROR,
      detail="Server Error",
      headers={"WWW-Authenticate": "Bearer"},
   )

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