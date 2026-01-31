pkg install python git -y
git clone https://github.com/username/telegram-info-bot
cd telegram-info-bot
pip install -r requirements.txt
cp .env.example .env
nano .env   # isi BOT_TOKEN
python bot.py