import uvicorn

from fastapi import FastAPI

from routers.v1 import all_routers
from utils.constants import TITLE, VERSION, API_PREFIX


app = FastAPI(
    title=TITLE,
    version=VERSION,
    root_path=API_PREFIX,
)

for router_v1 in all_routers:
    app.include_router(router_v1)


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8005, reload=True)
