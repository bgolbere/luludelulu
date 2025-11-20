from app.database import engine, SessionLocal, Base
from app import models

# Create tables FIRST
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("✓ Tables created")

print("\nTesting database connection...")
db = SessionLocal()

# Create test user
user = models.User(telegram_id=999, username="testuser")
db.add(user)
db.commit()
print("✓ Created test user")

# Query back
users = db.query(models.User).all()
print(f"✓ Found {len(users)} users")

for u in users:
    print(f"  - {u.telegram_id}: {u.username} (Lu: {u.lu_balance})")

db.close()
print("\n✓ Database working!")
