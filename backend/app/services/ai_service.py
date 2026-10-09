# backend/app/services/ai_service.py
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from app.settings.app import app_settings


class AIService:
    """Сервис ИИ-анализа на базе Multilingual E5 Large.
    
    Поддерживает загрузку базовой модели из HuggingFace или 
    дообученной версии из локальной папки models/.
    """

    MODEL_NAME = "intfloat/multilingual-e5-large"
    # Используем resolve() для точного определения пути независимо от ОС
    LOCAL_MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "airport-finetuned"

    def __init__(self):
        try:
            # Проверяем наличие дообученной модели
            if self.LOCAL_MODEL_PATH.exists():
                print(f"[AIService] Loading fine-tuned model from {self.LOCAL_MODEL_PATH}")
                self.model = SentenceTransformer(str(self.LOCAL_MODEL_PATH))
            else:
                print(f"[AIService] Loading base model: {self.MODEL_NAME}")
                self.model = SentenceTransformer(self.MODEL_NAME)
            
            # Проверка размерности (используем актуальный метод без warnings)
            actual_dim = self.model.get_embedding_dimension()
            if actual_dim != app_settings.EMBEDDING_DIMENSION:
                raise ValueError(
                    f"Model dimension mismatch: expected {app_settings.EMBEDDING_DIMENSION}, "
                    f"got {actual_dim}. Check your .env and model selection."
                )
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize AIService: {e}")

    def classify_text(self, text: str) -> int | None:
        """Определяет категорию заявки на основе текста.
        
        Пока используется эвристика (словарь ключевых слов).
        В будущем здесь будет вызов ML-классификатора.
        """
        if not text or not text.strip():
            return None
            
        text_lower = text.lower()
        
        # Простая логика классификации
        if any(w in text_lower for w in ["крыша", "течет", "кровля", "протечка"]):
            return 1  # Категория: Кровля/Строительство
        if any(w in text_lower for w in ["свет", "электричество", "лампа", "проводка"]):
            return 2  # Категория: Электрика
            
        return 1  # Дефолтная категория

    def generate_embedding(self, text: str) -> list[float]:
        """Генерирует семантический вектор заданной размерности.
        
        Для моделей семейства E5 используется префикс 'query: ' 
        для улучшения качества поиска.
        """
        if not text:
            return [0.0] * app_settings.EMBEDDING_DIMENSION
            
        # Добавляем префикс для E5 моделей
        vector = self.model.encode(f"query: {text}", normalize_embeddings=True)
        return vector.tolist()

    def save_finetuned_model(self, path: Path = None):
        """Сохраняет текущее состояние модели после дообучения."""
        save_path = path or self.LOCAL_MODEL_PATH
        save_path.mkdir(parents=True, exist_ok=True)
        self.model.save(str(save_path))
        print(f"[AIService] Model saved to {save_path}")