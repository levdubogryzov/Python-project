from __future__ import annotations
import json
from typing import Optional
from manim import *
from src.core.events import AlgorithmEvent
from config import ProjectConfig
from src.pipeline.player import EventPlayer


class BaseVisualizationScene(Scene):
    """Базовый класс для всех сцен визуализации алгоритмов в Manim."""
    def __init__(
            self,
            algorithm_name: Optional[str] = None,
            events: Optional[list[AlgorithmEvent]] = None,
            camera_config: Optional[dict[str, Any]] = None,
            **kwargs: Any,
    ) -> None:
        """Инициализирует сцену, загружая события и настраивая метаданные."""
        super().__init__(**kwargs)
        self.events = events if events is not None else self._load_latest_events()
        self.algorithm_name = algorithm_name if algorithm_name else self._detect_algorithm_name()
        self.camera_config = camera_config or {}
        self.elements: list[VMobject] = []
        self.status_label: Optional[VMobject] = None

    @staticmethod
    def _load_latest_events() -> list[AlgorithmEvent]:
        """Загружает события из последнего созданного JSON-файла лога."""
        cfg = ProjectConfig()
        try:
            files = list(cfg.RECORDED_DIR.glob("*_events.json"))
            if not files:
                return []
            latest_file = max(files, key=lambda x: x.stat().st_mtime)
            player = EventPlayer(latest_file)
            return list(player.play())
        except (FileNotFoundError, OSError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке событий: {e}")
            return []

    @staticmethod
    def _detect_algorithm_name() -> str:
        """Пытается определить название алгоритма на основе имени файла лога."""
        cfg = ProjectConfig()
        try:
            files = list(cfg.RECORDED_DIR.glob("*_events.json"))
            if not files:
                return "Visualization"
            latest_file = max(files, key=lambda x: x.stat().st_mtime)
            return latest_file.stem.replace("_events", "").replace("_", " ").title()
        except (OSError, ValueError):
            return "Visualization"

    def construct(self) -> None:
        """Основной рабочий цикл Manim: настройка, проигрывание и финализация."""
        self._setup_camera()
        self._setup_ui()
        self._play_events()
        self._finalize()

    def _setup_camera(self) -> None:
        """Устанавливает параметры камеры, такие как цвет фона."""
        bg_color = self.camera_config.get("background_color", BLACK)
        self.camera.background_color = bg_color

    def _setup_ui(self) -> None:
        """Отрисовывает заголовок алгоритма и инициализирует статусную строку."""
        title = Text(self.algorithm_name, font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        self.status_label = Text("Initializing...", font_size=24, color=GRAY_A)
        self.status_label.to_edge(DOWN, buff=0.5)
        self.add(self.status_label)

    def _play_events(self) -> None:
        """Заглушка для метода проигрывания событий (переопределяется в наследниках)."""
        pass

    def _finalize(self) -> None:
        """Добавляет задержку в конце видео для комфортного просмотра результата."""
        self.wait(2)
