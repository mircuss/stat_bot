import gspread
import datetime
from gspread import Worksheet
from gspread.exceptions import WorksheetNotFound
from pydantic import BaseModel
from config import settings


client = gspread.service_account(filename=settings.path_to_creds)
sh = client.open_by_key(settings.tabel_id)


class Company(BaseModel):
    name: str
    spend: int
    sub_count: int
    sub_price: int | None
    url: str


class GoogleSheets:
    def find_table_by_date(self, date: str) -> Worksheet | None:
        current_index = 0
        while True:
            try:
                ws = sh.get_worksheet(current_index)
                if ws.title == date:
                    return ws
                current_index += 1
            except WorksheetNotFound:
                return None

    def get_data(self, date: str = None):
        if not date:
            date = datetime.datetime.today().strftime("%d/%m/%Y")
        ws = self.find_table_by_date(date=date)
        if not ws:
            return None
        data = ws.get_all_values()
        companys = [Company(name=row[1],
                            spend=int(row[5]),
                            sub_count=int(row[6]),
                            sub_price=int(row[7]),
                            url=row[8]) for row in data]
        return companys

    async def filter_geo(self, filter: str, date: str | None):
        companys = self.get_data(date=date)
        if not companys:
            return None
        spend = 0
        sub = 0
        for company in companys:
            if filter in company.name:
                spend += company.spend
                sub += company.sub_count
        if sub == 0:
            return [spend, sub, 0]
        return [spend, sub, spend/sub]

    async def filter_project(self, filter: str, date: str | None):
        companys = self.get_data(date=date)
        if not companys:
            return None
        spend = 0
        sub = 0
        for company in companys:
            if filter in company.name:
                spend += company.spend
                sub += company.sub_count
        if sub == 0:
            return [spend, sub, 0]
        return [spend, sub, spend/sub]

    async def filter_buyer(self, filter: str, date: str | None):
        companys = self.get_data(date=date)
        if not companys:
            return None
        spend = 0
        sub = 0
        for company in companys:
            if filter in company.name:
                spend += company.spend
                sub += company.sub_count
        if sub == 0:
            return [spend, sub, 0]
        return [spend, sub, spend/sub]
