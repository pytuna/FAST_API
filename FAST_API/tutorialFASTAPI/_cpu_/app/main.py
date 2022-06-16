from typing import Union
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
import platform
import cpuinfo
import psutil
app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates/")
@app.get("/")
async def get_cpu(request: Request):
    cpu = int(psutil.cpu_percent())
    ram = int(psutil.virtual_memory()[2])
    return templates.TemplateResponse('cpu.html',context={'request': request, 'CPU': cpu, "RAM": ram})

if __name__ == '__main__':
    uvicorn.run(app,debug = True)