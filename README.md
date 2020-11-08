# TimusBot

This is a telegram bot for real-time leaderboard in group chats.

#### Requirements
- Python >=3.7

#### Installation
1. `git clone https://github.com/GeorgiySurkov/TimusBot.git`
2. `cd TimusBot`
3. `python3 -m venv venv`
4. `venv\Scripts\activate` (Windows) `source venv/bin/activate` (Linux)
5. `pip3 install -r requirements.txt`
6. Install appropriate database driver (`asyncpg` for Postgres, `aiosqlite` for sqlite, `aiomysql` for MySQL)
7. create `.env` file with your settings
8. `python3 main.py`

