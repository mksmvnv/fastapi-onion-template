import uvicorn

from fastapi import FastAPI

from routers.v1 import all_routers
from config.config import settings


app = FastAPI(
    title=settings.app.title,
    version=settings.app.version,
    root_path=settings.app.root_path,
)

for router_v1 in all_routers:
    app.include_router(router_v1)


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=settings.app.port, reload=True)
