import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    token: str = os.getenv("TOKEN", default="123:abc")
    path_to_creds: str = os.getenv("PATH_TO_CREDS", default="client.json")
    tabel_id: str = os.getenv("TABLE_ID", default="abc")


settings = Settings()
