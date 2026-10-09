# backend/scripts/train_model.py
import os
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# Пример данных: (текст_1, текст_2, метка_схожести)
# В реальности эти данные должны быть выгружены из вашей БД исторических заявок
train_examples = [
    InputExample(texts=["Течет крыша в терминале", "Протечка кровли в зоне вылета"], label=1.0),
    InputExample(texts=["Не горит свет на парковке", "Отсутствие освещения P3"], label=1.0),
    InputExample(texts=["Течет крыша", "Сломался кондиционер"], label=0.0),
]

def train():
    print("Starting fine-tuning process...")
    model = SentenceTransformer('intfloat/multilingual-e5-large')
    
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    train_loss = losses.CosineSimilarityLoss(model)
    
    # Обучаем всего 1 эпоху для примера
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        warmup_steps=100
    )
    
    model.save("models/airport-finetuned")
    print("Model saved to models/airport-finetuned")

if __name__ == "__main__":
    train()