from app.db.session import SessionLocal
from app.db.seed import seed_data


def run() -> None:
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    run()