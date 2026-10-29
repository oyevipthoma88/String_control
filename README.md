# APEX Session Control Bot

A safe, production-ready Telegram session manager built with Telethon 1.45, PyMongo Async, and uvloop.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/oyevipthoma88/String_control)

## Features
- Generate Telethon string sessions
- View account info
- List active sessions
- Terminate other sessions
- Logout / invalidate a session
- Graceful SIGTERM handling for Heroku/VPS
- uvloop 2-4x faster async

## Environment Variables
| Key | Required | Description |
|---|---|---|
| API_ID | Yes | my.telegram.org/apps |
| API_HASH | Yes | my.telegram.org/apps |
| BOT_TOKEN | Yes | BotFather |
| SUDOERS | No | Space-separated IDs |
| MONGO_URL | No | MongoDB URL |
| LOG_GROUP_ID | No | Log group ID |
| MUST_JOIN | No | Force-sub channel |

## VPS Deploy
    sudo apt update && sudo apt install python3.12 python3.12-venv git -y
    git clone https://github.com/oyevipthoma88/String_control
    cd String_control
    python3.12 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    cp example.env .env && nano .env
    python -m bot

## Heroku Deploy
Click the Deploy to Heroku button above, fill env vars, deploy.

## Disclaimer
Yeh bot sirf apne account ke liye hai. Session string kisi ke saath share mat karo.
