from database.connection import engine, Base
from database.models.user import User
from database.models.favoriteUser import FavoriteUser
from database.models.blackList import Blacklist
from database.models.searchResult import SearchResult
from database.models.photo import Photo
from database.models.searchstate import SearchState  

def init_db():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы")
    print("Созданные таблицы:")
    print("   - users")
    print("   - favorite_users") 
    print("   - blacklist")
    print("   - search_results")
    print("   - photos")
    print("   - search_state")  

if __name__ == "__main__":
    init_db()