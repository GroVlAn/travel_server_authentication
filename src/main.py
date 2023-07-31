import uvicorn

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from auth.router import router as auth_router

version = '0.0.1'

app = FastAPI(
    title='Travel guide authentication',
    version=version,
)

origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


main_router = APIRouter(
    prefix=f'/auth/app/v{version}',
    tags=['main']
)


@main_router.get('/welcome')
async def welcome():
    return 'Welcome to authentication of travel guide'

app.include_router(
    main_router
)

app.include_router(
    auth_router
)


if __name__ == '__main__':
    uvicorn.run(app="main:app", host='localhost', port=8001, reload=True)
