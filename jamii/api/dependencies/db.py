from jamii.db.session import SessionLocal

# Dependency that provides a database session to route handlers
def get_db():
    db = SessionLocal()
    try:
        yield db   # provides a database session for use
    finally:
        db.close() # Ensure the session is closed after use
        