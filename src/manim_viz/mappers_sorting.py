from __future__ import annotations
from manim import *
from src.core.events import AlgorithmEvent, EventType


def map_compare(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Визуализирует сравнение элементов через индикацию цветом."""
    elements = getattr(scene, "elements", None)
    if not elements or not event.indices:
        return Wait(0.1)
    bars = [elements[i][0] for i in event.indices if 0 <= i < len(elements)]
    return AnimationGroup(*[Indicate(b, color=YELLOW, scale_factor=1.1, run_time=0.6) for b in bars])


def map_swap(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Анимирует физическое перемещение двух элементов массива друг на друга."""
    elements = getattr(scene, "elements", None)
    if not elements or len(event.indices) < 2:
        return Wait(0.1)
    i, j = event.indices[0], event.indices[1]
    obj1, obj2 = elements[i], elements[j]
    p1, p2 = getattr(obj1, "is_pivot", False), getattr(obj2, "is_pivot", False)
    obj1.is_pivot, obj2.is_pivot = p2, p1
    target_x1: float = obj2.get_x()
    target_x2: float = obj1.get_x()
    elements[i], elements[j] = elements[j], elements[i]
    return AnimationGroup(
        obj1.animate.set_x(target_x1).set_color(obj1.get_color()),
        obj2.animate.set_x(target_x2).set_color(obj2.get_color()),
        run_time=0.5
    )


def map_overwrite(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Изменяет высоту столбца и текст под ним при прямой перезаписи значения."""
    elements = getattr(scene, "elements", None)
    if not elements or not event.indices or event.value is None:
        return Wait(0.1)
    idx = event.indices[0]
    group = elements[idx]
    bar, label = group[0], group[1]
    new_val = float(event.value)
    initial_data = getattr(scene, "initial_data", [])
    max_val = max(initial_data) if initial_data else 100
    new_h = (new_val / max_val * 3.5) + 0.5
    new_label = Text(str(int(new_val)), font_size=24).next_to(bar, DOWN, buff=0.2)
    group.submobjects[1] = new_label
    return AnimationGroup(
        bar.animate.stretch_to_fit_height(new_h, about_point=bar.get_bottom()),
        FadeTransform(label, new_label, stretch=False)
    )


def map_pivot(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Подсвечивает выбранный опорный элемент (pivot) в QuickSort."""
    elements = getattr(scene, "elements", None)
    if not elements or not event.indices:
        return Wait(0.1)
    idx = event.indices[0]
    target = elements[idx]
    target.is_pivot = True
    return target[0].animate.set_color(ORANGE).set_stroke(width=4)


def map_split(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Визуализирует разделение диапазона в MergeSort."""
    elements = getattr(scene, "elements", None)
    if not elements or not event.indices:
        return Wait(0.1)
    bars = [elements[i][0] for i in event.indices if 0 <= i < len(elements)]
    return Succession(
        AnimationGroup(*[b.animate.set_color(PURPLE_A) for b in bars], run_time=0.4),
        Wait(0.2),
        AnimationGroup(*[b.animate.set_color(BLUE_C) for b in bars], run_time=0.3)
    )


def map_merge(event: AlgorithmEvent, scene: Any, **_kwargs: Any) -> Animation:
    """Визуализирует процесс слияния подмассивов."""
    elements = getattr(scene, "elements", None)
    if not elements or not event.indices:
        return Wait(0.1)
    bars = [elements[i][0] for i in event.indices if 0 <= i < len(elements)]
    return Succession(
        AnimationGroup(*[b.animate.set_color(TEAL_A) for b in bars], run_time=0.4),
        Wait(0.2),
        AnimationGroup(*[b.animate.set_color(BLUE_C) for b in bars], run_time=0.3)
    )


AnimationMapper = Callable[[AlgorithmEvent, Any], Animation]
EVENT_TO_ANIMATION_SORTING: Dict[EventType, AnimationMapper] = {
    EventType.COMPARE: map_compare,
    EventType.SWAP: map_swap,
    EventType.OVERWRITE: map_overwrite,
    EventType.PIVOT: map_pivot,
    EventType.SPLIT: map_split,
    EventType.MERGE: map_merge,
}
