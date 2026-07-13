from app.db.database import SessionLocal

def get_db(): #a generator function
    db = SessionLocal() #spawns a new isolated db session-a temp workspace you can queue up transactions
    try:
        yield db#used instead of return- instead of terminating and returning a value, it pauses the function and hnds the active db session
    finally:
        db.close()#this line runs no matter what - finally closes the db session after completeion or error crashing.