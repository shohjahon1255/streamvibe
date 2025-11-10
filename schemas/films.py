from pydantic import BaseModel

class FilmsModel(BaseModel):
    title: str
    description: str
    video_url: str
    year: int
    languages: list
    genres: list