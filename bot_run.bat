@echo off

call %~dp0telegram_bot\venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN=5178073044:AAE89Bbcqi9NSGiKwD_xvi4ke_fxGPYO_do

python bot_telegram.py

pause