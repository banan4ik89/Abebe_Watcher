# trust_system.py
import time

# ===================== ТЕМЫ И СЛОВА =====================
THEMES = {
    "security": {
        "good": [
            "access", "protocol", "secure", "password",
            "authorization", "verification", "encrypted"
        ],
        "bad": [
            "hack", "crack", "bypass", "exploit", "steal"
        ]
    },
    "company": {
        "good": [
            "employee", "department", "archive",
            "system", "database", "internal"
        ],
        "bad": [
            "intruder", "spy", "leak", "traitor"
        ]
    },
    "abebe": {
        "good": [
            "abebe", "assistant", "helper", "guardian"
        ],
        "bad": [
            "virus", "fake", "stupid", "bot"
        ]
    }
}

# ===================== КЛАСС СИСТЕМЫ =====================
class TrustSystem:
    def __init__(self):
        self.trust = 0
        self.suspicion = 0

        self.history = []          # история введённых слов
        self.last_input_time = 0   # для анти-спама

        self.max_value = 100

    # ===================== АНАЛИЗ ВВОДА =====================
    def analyze_input(self, text: str) -> str:
        """
        Возвращает:
        'trust' | 'suspicion' | 'neutral'
        """
        text = text.lower().strip()

        # пустой ввод — подозрительно
        if not text:
            return "suspicion"

        # повтор слова — подозрительно
        if text in self.history:
            return "suspicion"

        # слишком быстрый ввод (спам)
        now = time.time()
        if now - self.last_input_time < 0.8:
            return "suspicion"

        # анализ по темам
        for theme_name, theme in THEMES.items():
            if text in theme["good"]:
                return "trust"
            if text in theme["bad"]:
                return "suspicion"

        return "neutral"

    # ===================== ПРИМЕНЕНИЕ РЕЗУЛЬТАТА =====================
    def apply_result(self, result: str):
        if result == "trust":
            self.trust += 15
            self.suspicion -= 5

        elif result == "suspicion":
            self.suspicion += 20
            self.trust -= 5

        elif result == "neutral":
            self.suspicion += 5

        self._clamp()

    # ===================== ОСНОВНОЙ МЕТОД =====================
    def process_input(self, text: str) -> str:
        """
        Главный метод:
        - анализирует ввод
        - изменяет шкалы
        - сохраняет историю
        - возвращает результат
        """
        result = self.analyze_input(text)
        self.apply_result(result)

        self.history.append(text.lower())
        self.last_input_time = time.time()

        return result

    # ===================== СОСТОЯНИЯ =====================
    def is_trusted(self) -> bool:
        return self.trust >= self.max_value

    def is_suspicious(self) -> bool:
        return self.suspicion >= self.max_value

    def get_state(self) -> str:
        """
        Возвращает текущее состояние для AbebeWatcher:
        'happy' | 'angry' | 'neutral'
        """
        if self.is_suspicious():
            return "angry"
        elif self.trust >= 70:
            return "happy"
        else:
            return "neutral"

    # ===================== ВНУТРЕННЕЕ =====================
    def _clamp(self):
        self.trust = max(0, min(self.max_value, self.trust))
        self.suspicion = max(0, min(self.max_value, self.suspicion))

    # ===================== ОТЛАДКА =====================
    def debug_state(self) -> str:
        return f"TRUST={self.trust}% | SUSPICION={self.suspicion}%"

