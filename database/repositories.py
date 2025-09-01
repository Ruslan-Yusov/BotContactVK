from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.connection import SessionLocal
from database.models.user import User
from database.models.favoriteUser import FavoriteUser
from database.models.blackList import Blacklist
from database.models.searchResult import SearchResult
from database.models.photo import Photo
from database.models.searchstate import SearchState  
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
import json

def get_db():
    """Возвращает сессию базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def commit_changes(db: Session):
    """Фиксирует изменения в БД с обработкой ошибок"""
    try:
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Ошибка при сохранении в БД: {e}")
        return False

def get_or_create_user(db: Session, vk_id: int, username: str = None, city: str = None, age: int = None, sex: str = None):
    """Получает пользователя или создает нового"""
    user = db.query(User).filter(User.vk_id == vk_id).first()
    if not user:
        user = User(vk_id=vk_id, username=username, city=city, age=age, sex=sex)
        db.add(user)
        if commit_changes(db):
            return user
        return None
    return user

def add_to_favorites(db: Session, user_id: int, vk_id: int, name: str, profile_url: str):
    """Добавляет пользователя в избранное"""
    if not is_in_favorites(db, user_id, vk_id):
        favorite = FavoriteUser(user_id=user_id, vk_id=vk_id, name=name, profile_url=profile_url)
        db.add(favorite)
        return commit_changes(db)
    return False

def remove_from_favorites(db: Session, user_id: int, vk_id: int):
    """Удаляет пользователя из избранного"""
    favorite = db.query(FavoriteUser).filter(
        FavoriteUser.user_id == user_id, 
        FavoriteUser.vk_id == vk_id
    ).first()
    
    if favorite:
        db.delete(favorite)
        return commit_changes(db)
    return False

def get_favorites(db: Session, user_id: int):
    """Получает список избранных пользователей"""
    return db.query(FavoriteUser).filter(FavoriteUser.user_id == user_id).all()

def is_in_favorites(db: Session, user_id: int, vk_id: int):
    """Проверяет, есть ли пользователь в избранном"""
    return db.query(FavoriteUser).filter(
        FavoriteUser.user_id == user_id, 
        FavoriteUser.vk_id == vk_id
    ).first() is not None

def add_to_blacklist(db: Session, user_id: int, vk_id: int, name: str = None, profile_url: str = None):
    """Добавляет пользователя в черный список"""
    if not is_in_blacklist(db, user_id, vk_id):
        blacklisted = Blacklist(user_id=user_id, vk_id=vk_id, name=name, profile_url=profile_url)
        db.add(blacklisted)
        return commit_changes(db)
    return False

def remove_from_blacklist(db: Session, user_id: int, vk_id: int):
    """Удаляет пользователя из черного списка"""
    blacklisted = db.query(Blacklist).filter(
        Blacklist.user_id == user_id, 
        Blacklist.vk_id == vk_id
    ).first()
    
    if blacklisted:
        db.delete(blacklisted)
        return commit_changes(db)
    return False

def get_blacklist(db: Session, user_id: int):
    """Получает список пользователей в черном списке"""
    return db.query(Blacklist).filter(Blacklist.user_id == user_id).all()

def is_in_blacklist(db: Session, user_id: int, vk_id: int):
    """Проверяет, есть ли пользователь в черном списке"""
    return db.query(Blacklist).filter(
        Blacklist.user_id == user_id, 
        Blacklist.vk_id == vk_id
    ).first() is not None

def save_search_result(db: Session, user_id: int, vk_id: int, name: str, profile_url: str, photos: List[Tuple[str, int]]):
    """
    Сохраняет результат поиска с фотографиями
    
    Args:
        user_id: ID пользователя бота
        vk_id: ID найденного пользователя VK
        name: Имя пользователя
        profile_url: Ссылка на профиль
        photos: Список кортежей (url_фото, количество_лайков)
    """
    existing = db.query(SearchResult).filter(
        SearchResult.user_id == user_id,
        SearchResult.vk_id == vk_id
    ).first()
    
    if not existing:
        search_result = SearchResult(
            user_id=user_id,
            vk_id=vk_id,
            name=name,
            profile_url=profile_url
        )
        db.add(search_result)
        
        for photo_url, likes in photos:
            photo = Photo(
                search_result=search_result,
                photo_url=photo_url,
                likes=likes
            )
            db.add(photo)
        
        return commit_changes(db)
    return False

def get_search_results(db: Session, user_id: int):
    """Получает все результаты поиска для пользователя"""
    return db.query(SearchResult).filter(SearchResult.user_id == user_id).all()

def get_search_result_with_photos(db: Session, user_id: int, vk_id: int):
    """Получает результат поиска с фотографиями"""
    return db.query(SearchResult).filter(
        SearchResult.user_id == user_id,
        SearchResult.vk_id == vk_id
    ).first()

def update_search_state(db: Session, user_id: int, last_viewed_vk_id: int = None, 
                       search_offset: int = None, search_params: Dict[str, Any] = None):
    """
    Обновляет состояние поиска для пользователя
    """
    # Убираем импорт from database.models.searchState import SearchState - он уже есть выше
    
    search_state = db.query(SearchState).filter(SearchState.user_id == user_id).first()
    
    if not search_state:
        search_state = SearchState(user_id=user_id)
        db.add(search_state)
    
    if last_viewed_vk_id is not None:
        search_state.last_viewed_vk_id = last_viewed_vk_id
    if search_offset is not None:
        search_state.search_offset = search_offset
    if search_params is not None:
        search_state.search_params = json.dumps(search_params, ensure_ascii=False)
    
    search_state.last_updated = datetime.utcnow()
    
    return commit_changes(db)

def get_search_state(db: Session, user_id: int):
    """
    Получает состояние поиска для пользователя
    """
    # Убираем импорт from database.models.searchState import SearchState
    
    search_state = db.query(SearchState).filter(SearchState.user_id == user_id).first()
    
    if search_state:
        try:
            params = json.loads(search_state.search_params) if search_state.search_params else {}
        except:
            params = {}
        
        return {
            'last_viewed_vk_id': search_state.last_viewed_vk_id,
            'search_offset': search_state.search_offset,
            'search_params': params,
            'last_updated': search_state.last_updated
        }
    else:
        return {
            'last_viewed_vk_id': None,
            'search_offset': 0,
            'search_params': {},
            'last_updated': datetime.utcnow()
        }

def reset_search_state(db: Session, user_id: int):
    """
    Сбрасывает состояние поиска для пользователя
    """
    # Убираем импорт from database.models.searchState import SearchState
    
    search_state = db.query(SearchState).filter(SearchState.user_id == user_id).first()
    if search_state:
        db.delete(search_state)
        return commit_changes(db)
    return True

def get_user_relationships(db: Session, user_id: int, target_vk_id: int):
    """
    Проверяет отношения между пользователями
    
    Returns:
        dict: Статусы отношений
    """
    return {
        'in_favorites': is_in_favorites(db, user_id, target_vk_id),
        'in_blacklist': is_in_blacklist(db, user_id, target_vk_id),
        'in_search_results': get_search_result_with_photos(db, user_id, target_vk_id) is not None
    }

def clear_user_data(db: Session, user_id: int):
    """Очищает все данные пользователя (для тестирования)"""
    try:
        db.query(FavoriteUser).filter(FavoriteUser.user_id == user_id).delete()
        db.query(Blacklist).filter(Blacklist.user_id == user_id).delete()

        search_results = db.query(SearchResult).filter(SearchResult.user_id == user_id).all()
        for result in search_results:
            db.query(Photo).filter(Photo.search_result_id == result.id).delete()
        db.query(SearchResult).filter(SearchResult.user_id == user_id).delete()
        

        db.query(User).filter(User.id == user_id).delete()
        return commit_changes(db)
    
    except Exception as e:
        print(f"Ошибка при очистке данных пользователя: {e}")
        db.rollback()
        return False