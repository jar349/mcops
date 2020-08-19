import os
import socket

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from typing import Optional

from mcops import mcrcon


app = FastAPI()
with open("./config/mcops.yaml", "r") as file:
    config = load(file, Loader=Loader)

host = os.environ.get("MCOPS_HOST", "localhost")
port = int(os.environ.get("MCOPS_PORT", 25575))
password = os.environ["MCOPS_PASSWORD"]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Will connect to {host} on port {port}") 
sock.connect((host, port))
result = mcrcon.login(sock, password)

if not result:
    print("Incorrect RCon password")
    exit(1)


class Command(BaseModel):
    namespace: str
    command: str
    event: Optional[dict] = None


@app.get("/help", response_class=PlainTextResponse)
def get_help():
    return "Runs minecraft commands\nTry: `.mc commands`"


@app.get("/ping", response_class=PlainTextResponse)
def get_ping():
    return "pong"

@app.get("/metadata", response_class=JSONResponse)
def get_metadata():
    return {"protocol_version": "1.0"}


@app.post("/handle", response_class=JSONResponse)
def get_response(request: Command):
    namespace = request.namespace
    command = request.command
    event = request.event

    # Print to stdout for logging purposes
    args = {"namespace": namespace, "command": command, "event": event}
    print(f"Got: {args}")

    # figure out what minecraft command they are attempting to run
    parts = command.split()
    mc_cmd = parts[0].lower()

    # the command must either be whitelisted or literally the "commands" command.  Otherwise send back an error message.
    if mc_cmd in config["commands"]:
        response = mcrcon.command(sock, f"{command}")
        return {"message": response}
    elif mc_cmd == "commands":
        msg = "The following commands are whitelisted:"
        for cmd in config["commands"]:
            msg += f"\n - {cmd}"
        return {"message": msg}
    else:
        return {"message": "That command is not whitelisted so you many not run it from Slack"}
