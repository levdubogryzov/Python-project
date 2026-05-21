from __future__ import annotations
import json
from typing import Optional
from manim import *
from src.manim_viz.base_scene import BaseVisualizationScene
from config import ProjectConfig
from src.manim_viz.mappers_graph import EVENT_TO_ANIMATION_GRAPH


class GraphScene(BaseVisualizationScene):
    """Сцена визуализации графовых алгоритмов с использованием направленных ребер."""
    def _setup_ui(self) -> None:
        """Инициализирует визуальные объекты графа: узлы, стрелки-ребра и метки дистанций."""
        super()._setup_ui()
        cfg = ProjectConfig()
        adj_list = self._extract_adjacency_list() or cfg.DEFAULT_GRAPH
        if not adj_list:
            return
        node_count = len(adj_list)
        radius = 2.4
        self.nodes: List[VMobject] = []
        self.labels: List[VMobject] = []
        self.edges_map: dict[tuple[int, int], VMobject] = {}
        node_positions = []
        ui_elements = VGroup()
        for i in range(node_count):
            angle = 2 * PI * i / node_count - PI / 2
            pos = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
            node_positions.append(pos)
            node_color = BLUE if i == cfg.DEFAULT_GRAPH_START else (RED if i == cfg.DEFAULT_GRAPH_END else GREEN)
            circle = Circle(radius=0.4, color=node_color, fill_opacity=0.2).move_to(pos)
            index_label = Text(str(i), font_size=24, color=WHITE).move_to(pos)
            label_text = "0.0" if i == cfg.DEFAULT_GRAPH_START else "inf"
            dist_label = Text(label_text, font_size=20, color=BLUE).next_to(circle, UP, buff=0.1)
            self.nodes.append(circle)
            self.labels.append(dist_label)
            ui_elements.add(circle, index_label, dist_label)
        edges_group = VGroup()
        for u, neighbors in enumerate(adj_list):
            for v, weight in neighbors:
                if v < node_count:
                    arrow = Arrow(
                        node_positions[u],
                        node_positions[v],
                        buff=0.4,
                        color=GRAY,
                        stroke_width=3,
                        max_tip_length_to_length_ratio=0.15
                    ).set_z_index(-1)
                    w_text = Text(str(weight), font_size=16, color=YELLOW).move_to(arrow.get_center() + UP * 0.15)
                    edges_group.add(arrow, w_text)
                    self.edges_map[(u, v)] = arrow
        final_vis = VGroup(ui_elements, edges_group)
        final_vis.move_to(ORIGIN).shift(UP * 0.1)
        self.add(final_vis)

    @staticmethod
    def _extract_adjacency_list() -> Optional[List[Any]]:
        """Извлекает структуру графа из метаданных последнего записанного сценария."""
        try:
            cfg = ProjectConfig()
            json_files = list(cfg.RECORDED_DIR.glob("*_events.json"))
            if not json_files:
                return None
            latest = max(json_files, key=lambda x: x.stat().st_mtime)
            with open(latest, "r", encoding="utf-8") as f:
                content = json.load(f)
                state = content.get("initial_state", {})
                return state.get("adjacency_list") if isinstance(state, dict) else None
        except (ImportError, json.JSONDecodeError, OSError, AttributeError):
            return None

    def _play_events(self) -> None:
        """Проигрывает последовательность анимаций, маппируя события на объекты сцены."""
        for event in self.events:
            if event.description and self.status_label:
                new_status = Text(
                    event.description,
                    font_size=24,
                    color=GREY_A
                ).move_to(self.status_label.get_center())

                self.play(FadeTransform(self.status_label, new_status), run_time=0.2)
                self.status_label = new_status
            mapper = EVENT_TO_ANIMATION_GRAPH.get(event.type)
            if mapper:
                animation = mapper(event, self)
                self.play(animation, run_time=0.4)

            self.wait(0.05)
