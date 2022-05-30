from app.db.database import Database

def test_database_instance():
    assert Database() != None
    
def test_database_ping():
    database = Database()
    assert database.ping() == True