from __future__ import annotations
import sys
import subprocess
from pathlib import Path
from typing import Callable, Any, List, Dict

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

from src.algorithms.sorting.shell import ShellSort
from src.algorithms.sorting.quick import QuickSort
from src.algorithms.sorting.merge import MergeSort
from src.algorithms.graph.dijkstra import Dijkstra
from src.algorithms.graph.a_star import AStar
from src.algorithms.graph.bellman_ford import BellmanFord
from src.validation.validator import AlgorithmValidator
from src.core.exceptions import InvalidInputError, NegativeCycleError
from src.pipeline.recorder import EventRecorder
from src.pipeline.player import EventPlayer
from config import ProjectConfig

console = Console()


def run_and_record_sorting(
    algo_name: str,
    algo_instance: Any,
    initial_data: List[int],
    config: ProjectConfig
) -> Path:
    original_data = list(initial_data)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task1 = progress.add_task(f"Выполнение {algo_name}...")
        events = list(algo_instance.run())
        progress.advance(task1)

        task2 = progress.add_task("Проверка потока...")
        validator = AlgorithmValidator()
        if not validator.validate_sorting(events, original_data):
            for err in validator.errors:
                console.print(f"  [red]Ошибка верификации: {err}")
        progress.advance(task2)

        task3 = progress.add_task("Запись данных...")
        clean_name = algo_name.lower().replace('sort', '')
        output_path = config.get_record_path(f"{clean_name}_events.json")

        recorder = EventRecorder(output_path)
        recorder.record(
            iter(events),
            algorithm_name=algo_name,
            initial_state=original_data
        )
        progress.advance(task3)

    return output_path


def run_and_record_graph(
        algo_name: str,
        algo_instance: Any,
        graph: List[List[Any]],
        config: ProjectConfig
) -> Path:
    """Запускает графовый алгоритм, проверяет результат и записывает лог событий."""
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
    ) as progress:
        task1 = progress.add_task(f"Выполнение {algo_name}...")
        try:
            events = list(algo_instance.run())
            distances = getattr(algo_instance, "distances", {})
            progress.advance(task1)

            task2 = progress.add_task("Проверка результата...")
            validator = AlgorithmValidator()
            if not validator.validate_graph(distances, graph, config.DEFAULT_GRAPH_START):
                for err in validator.errors:
                    console.print(f"  [red]Внимание: {err}")
            progress.advance(task2)

            task3 = progress.add_task("Запись данных...")
            filename = f"{algo_name.lower()}_events.json"
            output_path = config.get_record_path(filename)

            recorder = EventRecorder(output_path)
            recorder.record(iter(events), algorithm_name=algo_name, initial_state={"adjacency_list": graph})
            progress.advance(task3)
            return output_path
        except (InvalidInputError, NegativeCycleError) as exc:
            console.print(f"[red][ОШИБКА] {algo_name}: {exc}")
            raise


def run_visualization(scene_type: str, algo_name: str) -> None:
    """Запуск рендера с гарантированной очисткой мусора даже при ошибках."""
    import time
    import shutil
    cfg = ProjectConfig()
    scene_map = {
        "sorting": ("src/manim_viz/scenes/sorting.py", "SortingScene"),
        "graph": ("src/manim_viz/scenes/graph.py", "GraphScene"),
    }
    file_path, scene_name = scene_map[scene_type]
    output_name = f"{algo_name}_{time.strftime('%d%b_%H%M')}"
    console.print(f"[cyan]Запуск рендера {output_name}...")
    try:
        subprocess.run(
            [
                sys.executable, "-m", "manim",
                cfg.render_quality_flag,
                file_path,
                scene_name,
                "--disable_caching",
                "-o", output_name,
                "--media_dir", str(cfg.MEDIA_DIR),
            ],
            check=True,
        )
        console.print(f"[green]Рендер завершен успешно!")
    except subprocess.CalledProcessError as exc:
        console.print(f"[red]Ошибка Manim (код {exc.returncode}). Проверьте лог сцены.")
    except Exception as exc:
        console.print(f"[red]Ошибка при запуске визуализации: {exc}")
    finally:
        garbage_folders = ["partial_movie_files", "Tex", "texts", "logs"]
        for folder_name in garbage_folders:
            for path in cfg.MEDIA_DIR.rglob(folder_name):
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
        console.print("[dim]Временные файлы очищены.[/]")


def verify_playback(json_path: Path) -> bool:
    """Выполняет тестовое чтение записанного файла для верификации пайплайна."""
    try:
        player = EventPlayer(json_path)
        events = list(player.play())
        console.print(f"  [green]OK: Прочитано {len(events)} событий.")
        return True
    except Exception as exc:
        console.print(f"  [red]Ошибка верификации: {exc}")
        return False


def show_menu() -> str:
    """Отображает главное меню выбора алгоритмов."""
    console.print(Panel.fit("Algorithm Visualizer", style="bold blue"))
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Алгоритм")
    table.add_column("Тип")

    table.add_row("1", "Shell Sort", "Sorting")
    table.add_row("2", "Quick Sort", "Sorting")
    table.add_row("3", "Merge Sort", "Sorting")
    table.add_row("4", "Dijkstra", "Graph")
    table.add_row("5", "Bellman-Ford", "Graph")
    table.add_row("6", "A*", "Graph")
    table.add_row("0", "Выход", "System")

    console.print(table)
    return Prompt.ask("Выбор", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")


def main() -> None:
    """Точка входа: управление жизненным циклом приложения."""
    config = ProjectConfig()
    config.init_dirs()

    algo_map: Dict[str, tuple[str, Callable, str]] = {
        "1": ("ShellSort", lambda: ShellSort(config.DEFAULT_SORTING_ARRAY.copy()), "sorting"),
        "2": ("QuickSort", lambda: QuickSort(config.DEFAULT_SORTING_ARRAY.copy()), "sorting"),
        "3": ("MergeSort", lambda: MergeSort(config.DEFAULT_SORTING_ARRAY.copy()), "sorting"),
        "4": ("Dijkstra", lambda: Dijkstra(
            config.DEFAULT_GRAPH, start=config.DEFAULT_GRAPH_START
        ), "graph"),
        "5": ("BellmanFord", lambda: BellmanFord(
            config.DEFAULT_GRAPH, start=config.DEFAULT_GRAPH_START
        ), "graph"),
        "6": ("AStar", lambda: AStar(
            config.DEFAULT_GRAPH,
            start=config.DEFAULT_GRAPH_START,
            end=config.DEFAULT_GRAPH_END
        ), "graph"),
    }

    while True:
        choice = show_menu()
        if choice == "0":
            break

        name, factory, s_type = algo_map[choice]
        try:
            if s_type == "sorting":
                path = run_and_record_sorting(name, factory(), config.DEFAULT_SORTING_ARRAY, config)
            else:
                path = run_and_record_graph(name, factory(), config.DEFAULT_GRAPH, config)

            verify_playback(path)
            if Confirm.ask("Начать визуализацию?", default=True):
                run_visualization(s_type, name)
            input("Нажмите Enter для продолжения...")
        except Exception as exc:
            console.print(f"[red]Ошибка приложения: {exc}")
            input()


if __name__ == "__main__":
    main()
