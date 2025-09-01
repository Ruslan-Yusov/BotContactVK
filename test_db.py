from database.repositories import (
    get_or_create_user, 
    update_search_state, 
    get_search_state,
    reset_search_state,
    clear_user_data
)
from database.connection import SessionLocal

def test_search_state():
    db = SessionLocal()
    
    try:
        # Создаем тестового пользователя
        user = get_or_create_user(db, vk_id=999888, username="Test User 3")
        
        print("1. Тестирование создания состояния поиска...")
        # Создаем состояние поиска
        search_params = {
            'age_from': 20,
            'age_to': 30,
            'city': 'Москва',
            'sex': 'female'
        }
        success = update_search_state(
            db=db,
            user_id=user.id,
            last_viewed_vk_id=123456,
            search_offset=10,
            search_params=search_params
        )
        print(f"   Состояние поиска создано: {success}")
        
        print("2. Тестирование получения состояния поиска...")
        # Получаем состояние
        state = get_search_state(db, user.id)
        print(f"   Состояние поиска: {state}")
        
        print("3. Тестирование обновления состояния...")
        # Обновляем состояние
        success = update_search_state(
            db=db,
            user_id=user.id,
            last_viewed_vk_id=654321,
            search_offset=15
        )
        print(f"   Состояние обновлено: {success}")
        
        # Снова получаем
        state = get_search_state(db, user.id)
        print(f"   Обновленное состояние: {state}")
        
        print("4. Тестирование сброса состояния...")
        # Сбрасываем состояние
        success = reset_search_state(db, user.id)
        print(f"   Состояние сброшено: {success}")
        
        # Проверяем сброс
        state = get_search_state(db, user.id)
        print(f"   Состояние после сброса: {state}")
        
        print("5. Очистка тестовых данных...")
        success = clear_user_data(db, user.id)
        print(f"   Данные очищены: {success}")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_search_state()