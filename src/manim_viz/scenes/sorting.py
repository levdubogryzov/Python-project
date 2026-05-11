from __future__ import annotations
import json
from typing import Optional
from manim import *
from src.manim_viz.base_scene import BaseVisualizationScene
from config import ProjectConfig
from src.manim_viz.mappers_sorting import EVENT_TO_ANIMATION_SORTING


class SortingScene(BaseVisualizationScene):
    """Сцена для визуализации алгоритмов сортировки с использованием столбчатых диаграмм."""

    def __init__(self, **kwargs: Any) -> None:
        """Инициализирует базовые атрибуты сцены сортировки."""
        super().__init__(**kwargs)
        self.cfg = ProjectConfig()
        self.elements: list[VGroup] = []
        self.status_label: Optional[Text] = None
        self.initial_data: list[int] = []
        self.latest_file_path: Optional[Path] = None

    def setup(self) -> None:
        """Подготавливает данные и UI перед началом анимации."""
        data_info = self._load_latest_recording() or {}
        self.initial_data = data_info.get("initial_state", [])
        super().setup()
        self._setup_ui_custom()

    def _load_latest_recording(self) -> Optional[dict[str, Any]]:
        """Загружает последний записанный лог, избегая широких исключений."""
        try:
            files = list(self.cfg.RECORDED_DIR.glob("*_events.json"))
            if not files:
                return None
            latest = max(files, key=lambda x: x.stat().st_mtime)
            self.latest_file_path = latest
            with open(latest, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError, ValueError):
            return None

    def _setup_ui_custom(self) -> None:
        """Создает графические элементы: столбцы, подписи и динамический заголовок."""
        if not self.initial_data:
            return

        for mob in self.mobjects[:]:
            if isinstance(mob, Text) and mob.get_center()[1] > 2:
                self.remove(mob)

        if self.latest_file_path:
            raw_name = self.latest_file_path.stem.replace("_events", "").capitalize()
            title_text = f"{raw_name} Sort Visualization"
        else:
            title_text = "Sorting Visualization"

        self.add(Text(title_text, font_size=36, color=BLUE_A).to_edge(UP, buff=0.5))

        self.status_label = Text("Ожидание...", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        self.add(self.status_label)

        n = len(self.initial_data)
        max_val = max(self.initial_data) if self.initial_data else 1
        bar_width = min((config.frame_width - 3.0) / n, 0.8)

        self.elements = []
        bars_group = VGroup()

        for val in self.initial_data:
            h = (val / max_val * 3.5) + 0.5
            bar = Rectangle(
                width=bar_width, height=h, fill_opacity=0.8, color=BLUE_C
            ).set_fill(BLUE_C, opacity=0.8)
            label = Text(str(val), font_size=24, color=WHITE)
            group = VGroup(bar, label)
            self.elements.append(group)
            bars_group.add(bar)

        bars_group.arrange(RIGHT, buff=0.2, aligned_edge=DOWN)

        for group in self.elements:
            bar, label = group[0], group[1]
            label.next_to(bar, DOWN, buff=0.2)
            self.add(group)

        VGroup(*self.elements).move_to(ORIGIN + DOWN * 0.2)

    def construct(self) -> None:
        """Основной цикл проигрывания анимаций из списка событий."""
        events_list = getattr(self, "events", [])
        for event in events_list:
            if event.description and self.status_label:
                new_status = Text(
                    event.description, font_size=24, color=GREY_A
                ).to_edge(DOWN, buff=0.4)
                self.play(FadeTransform(self.status_label, new_status), run_time=0.15)
                self.status_label = new_status

            mapper = EVENT_TO_ANIMATION_SORTING.get(event.type)
            if mapper:
                self.play(mapper(event, self))

            self.wait(0.05)

        success_group = VGroup(*[el for el in self.elements])
        self.play(success_group.animate.set_color(GREEN), run_time=0.5)
