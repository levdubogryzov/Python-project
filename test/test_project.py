import pytest
from src.algorithms.sorting.shell import ShellSort
from src.algorithms.sorting.quick import QuickSort
from src.algorithms.sorting.merge import MergeSort
from src.algorithms.graph.dijkstra import Dijkstra
from src.algorithms.graph.a_star import AStar
from src.algorithms.graph.bellman_ford import BellmanFord
from src.validation.validator import AlgorithmValidator
from src.core.exceptions import InvalidInputError, NegativeCycleError
from src.pipeline.schemas import EventRecord
from src.pipeline.recorder import EventRecorder
from src.pipeline.player import EventPlayer
from src.core.events import EventType, AlgorithmEvent


@pytest.mark.parametrize("algo_class", [ShellSort, QuickSort, MergeSort])
@pytest.mark.parametrize("data", [[6, 2, 8], [1, 2, 3], [3, 2, 1], [5]])
def test_sorting_algorithms(algo_class, data):
    """Проверка всех алгоритмов сортировки и их валидация."""
    algo = algo_class(data)
    events = list(algo.run())
    assert sorted(data) == algo._data
    v = AlgorithmValidator()
    assert v.validate_sorting(events, data) is True


@pytest.fixture
def sample_graph():
    """Фикстура стандартного ориентированного графа."""
    return [[(1, 1.0), (2, 4.0)], [(2, 2.0)], []]


def test_graph_algorithms_full(sample_graph):
    """Комплексная проверка графовых алгоритмов и их свойств."""
    d = Dijkstra(sample_graph)
    list(d.run())
    assert d.data == [0, 1, 2]
    assert d.distances[1] == 1.0
    assert d.distances[2] == 3.0

    bf = BellmanFord(sample_graph)
    list(bf.run())
    assert bf.distances[2] == 3.0


def test_astar_variants(sample_graph):
    """Проверка работы A* в разных сценариях."""
    algo_same = AStar(sample_graph, start=0, end=0)
    list(algo_same.run())
    assert algo_same.distances[0] == 0

    algo_full = AStar(sample_graph, start=0, end=2)
    list(algo_full.run())
    assert algo_full.distances[2] == 3.0


def test_negative_cycle_bf():
    """Проверка детекции отрицательного цикла."""
    graph = [[(1, 1)], [(2, -5)], [(0, 1)]]
    with pytest.raises(NegativeCycleError):
        list(BellmanFord(graph).run())


def test_all_invalid_inputs():
    """Проверка обработки всех типов некорректных входных данных."""
    with pytest.raises(InvalidInputError):
        ShellSort("not a list")
    with pytest.raises(InvalidInputError):
        Dijkstra([[(1, -1)]])
    with pytest.raises(InvalidInputError):
        AStar([[]], start=5)


def test_validator_comprehensive_coverage():
    """Проверяем validator.py через все возможные ошибки."""
    v = AlgorithmValidator()

    assert v.validate_sorting([], [3, 1, 2]) is False

    bad_type_evt = [AlgorithmEvent(event_type=EventType.RELAX, indices=[0])]
    assert v.validate_sorting(bad_type_evt, [1, 2]) is False

    out_of_range_evt = [AlgorithmEvent(event_type=EventType.COMPARE, indices=[10])]
    assert v.validate_sorting(out_of_range_evt, [1, 2]) is False

    bad_swap_evt = [AlgorithmEvent(event_type=EventType.SWAP, indices=[0])]
    assert v.validate_sorting(bad_swap_evt, [1, 2]) is False

    bad_overwrite_evt = [AlgorithmEvent(event_type=EventType.OVERWRITE, indices=[], value=10)]
    assert v.validate_sorting(bad_overwrite_evt, [1, 2]) is False
    bad_overwrite_val = [AlgorithmEvent(event_type=EventType.OVERWRITE, indices=[0], value=None)]
    assert v.validate_sorting(bad_overwrite_val, [1, 2]) is False

    graph = [[(1, 1.0)]]

    assert v.validate_graph("not_a_dict", graph, 0) is False
    assert v.validate_graph({0: 0.0}, graph, 10) is False
    assert v.validate_graph({0: 0.0, 1: 1.0}, graph, 0) is False
    assert v.validate_graph({0: 5.0}, graph, 0) is False

    complex_graph = [[(1, 1.0)], []]
    bad_distances = {0: 0.0, 1: 10.0}
    assert v.validate_graph(bad_distances, complex_graph, 0) is False

    inf_distances = {0: float('inf'), 1: 5.0}
    assert v.validate_graph(inf_distances, complex_graph, 0) is False


def test_pipeline_io_full_coverage(tmp_path):
    """Проверка Recorder и Player с обработкой ошибок."""
    path = tmp_path / "data.json"
    rec = EventRecorder(path)

    def broken_gen():
        yield AlgorithmEvent(event_type=EventType.VISIT, indices=[0])
        raise ValueError("Simulated Error")

    rec.record(broken_gen(), "Test", {"data": [1]})
    assert path.exists()

    p = EventPlayer(path)
    assert len(list(p.play())) == 1

    with pytest.raises(FileNotFoundError):
        EventPlayer("missing_file_path.json")


def test_core_repr_and_schemas():
    """Покрытие строковых представлений и Pydantic конвертации."""
    ev = AlgorithmEvent(event_type=EventType.COMPARE, indices=[0, 1])
    assert "COMPARE" in repr(ev)

    data = {"step_id": 0, "event_type": "visit", "indices": [0]}
    record = EventRecord.model_validate(data)
    assert record.to_event().type == EventType.VISIT
