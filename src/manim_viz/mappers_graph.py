from __future__ import annotations
from typing import Protocol, cast
from manim import *
from src.core.events import AlgorithmEvent, EventType


class GraphAnimationMapper(Protocol):
    """Интерфейс для функций анимации графов."""
    def __call__(self, event: AlgorithmEvent, scene: Any, **kwargs: Any) -> Animation: ...


def map_update(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Обновляет текстовые метки узлов (дистанции в графах)."""
    labels = getattr(scene, "labels", None)
    if event.value is None or not labels or not event.indices:
        return Wait(0.1)

    animations = []
    for idx in event.indices:
        if 0 <= idx < len(labels):
            val = float(event.value)
            txt = "∞" if val == float('inf') else f"{val:.0f}"
            new_text = Text(txt, font_size=20, color=YELLOW)
            new_text.move_to(labels[idx].get_center())

            scene.remove(labels[idx])
            labels[idx] = new_text
            animations.append(FadeIn(new_text, run_time=0.2))

    return cast(Animation, AnimationGroup(*animations, lag_ratio=0)) if animations else Wait(0.1)


def map_relax(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Вспышка ребра при релаксации (Dijkstra/Bellman-Ford)."""
    edges = getattr(scene, "edges", None)
    if not edges or len(event.indices) < 2:
        return Wait(0.1)

    u, v = event.indices[0], event.indices[1]
    edge = edges.get((u, v)) or edges.get((v, u))
    return cast(Animation, Flash(edge, color=ORANGE, run_time=0.5, flash_radius=0.6)) if edge else Wait(0.1)


def map_visit(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Помечает узлы или элементы как посещённые."""
    animations = []
    for attr in ["elements", "nodes"]:
        coll = getattr(scene, attr, None)
        if coll:
            for i in event.indices:
                if 0 <= i < len(coll):
                    animations.append(coll[i].animate.set_color(BLUE))
    return cast(Animation, AnimationGroup(*animations, lag_ratio=0)) if animations else Wait(0.1)


def map_state_change(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Обновление статус-бара внизу экрана."""
    status_label = getattr(scene, "status_label", None)
    if not status_label or not event.description:
        return Wait(0.1)

    new_text = Text(event.description, font_size=26, color=WHITE)
    new_text.move_to(status_label.get_center())
    return Transform(status_label, new_text, run_time=0.3)


EVENT_TO_ANIMATION_GRAPH: dict[EventType, GraphAnimationMapper] = {
    EventType.UPDATE: cast(GraphAnimationMapper, map_update),
    EventType.VISIT: cast(GraphAnimationMapper, map_visit),
    EventType.RELAX: cast(GraphAnimationMapper, map_relax),
    EventType.HEURISTIC: cast(GraphAnimationMapper, map_update),
    EventType.STATE_CHANGE: cast(GraphAnimationMapper, map_state_change),
    EventType.PARTITION: cast(GraphAnimationMapper, map_state_change),
    EventType.MERGE: cast(GraphAnimationMapper, map_state_change),
    EventType.SPLIT: cast(GraphAnimationMapper, map_state_change),
}
