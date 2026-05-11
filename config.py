from __future__ import annotations
from pathlib import Path
from typing import Any
from manim import config as manim_config


class ProjectConfig:
    """Глобальные настройки проекта, конфигурация Manim и управление путями данных."""
    BASE_DIR: Path = Path(__file__).resolve().parent
    DATA_DIR: Path = BASE_DIR / "data"
    RECORDED_DIR: Path = DATA_DIR
    MEDIA_DIR: Path = BASE_DIR / "media"
    manim_config.media_dir = str(MEDIA_DIR)
    manim_config.video_dir = str(MEDIA_DIR)
    manim_config.tex_dir = str(MEDIA_DIR)
    manim_config.images_dir = str(MEDIA_DIR)
    manim_config.log_dir = str(MEDIA_DIR)
    DEFAULT_SORTING_ARRAY: list[int] = [64, 34, 25, 12, 22, 11, 90]
    DEFAULT_GRAPH: list[list[tuple[int, float]]] = [
        [(1, 2), (3, 100)],
        [(2, 1), (3, 1)],
        [],
        [(2, 2)]
    ]

    DEFAULT_GRAPH_START: int = 0
    DEFAULT_GRAPH_END: int = 3

    # Качество рендера: ql (480p), qm (720p), qh (1080p)
    _RENDER_QUALITY: str = "qh"
    _RENDER_FPS: int = 60
    _ENABLE_VALIDATION: bool = True

    @property
    def render_quality_flag(self) -> str:
        """Возвращает флаг качества рендера для командной строки Manim."""
        return f"-{self._RENDER_QUALITY}"

    @property
    def render_fps(self) -> int:
        """Возвращает количество кадров в секунду для генерации видео."""
        return self._RENDER_FPS

    @property
    def enable_validation(self) -> bool:
        """Флаг активации проверки потока событий на корректность."""
        return self._ENABLE_VALIDATION

    @classmethod
    def init_dirs(cls) -> None:
        """Создает необходимые директории для данных и медиафайлов, если они отсутствуют."""
        for directory in [cls.RECORDED_DIR, cls.MEDIA_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_camera_config() -> dict[str, Any]:
        """"Возвращает базовые параметры камеры для сцен Manim."""
        return {
            "frame_size": (1920, 1080),
            "fps": 30,
        }

    def get_record_path(self, filename: str) -> Path:
        """Формирует полный путь к файлу записи сценария в директории данных."""
        return self.RECORDED_DIR / filename
