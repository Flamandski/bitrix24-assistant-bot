from modules.database import init_db
from modules.telegram_bot import run_bot

def main():
    print("🚀 Запуск Bitrix24 Assistant Bot...")
    init_db()
    run_bot()

if __name__ == "__main__":
    main()