from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from database import Base, engine
from routers.crew import crew_router
from routers.film_actor import film_actor_router
from routers.films import film_router
from routers.users import user_router
from routers.wish_list import wish_list_router
from utils.slowapi_configuration import limiter

app = FastAPI(docs_url='/', title='StreamVibe API', description='StreamVibe API', version='1.0.0')


Base.metadata.create_all(bind=engine)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(user_router, tags=['Auth'], prefix='/auth')
app.include_router(film_router, tags=['Films'], prefix='/films')
app.include_router(wish_list_router, tags=['Wish List'], prefix='/wish_list')
app.include_router(crew_router, tags=['Crew'], prefix='/crew')
app.include_router(film_actor_router, tags=['Film Actor'], prefix='/film_actor')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)