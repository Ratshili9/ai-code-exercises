"""
Module: Advanced Python Features - Custom Decorators & Context Handlers
Demonstrating parameterized decorators, functools.wraps, retry logic, and timing telemetry.
"""
import functools
import time
from typing import Callable, Any, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


def retry(max_attempts: int = 3, delay: float = 0.05, backoff: float = 2.0):
    """
    Decorator that retries a function with exponential backoff on exceptions.
    Preserves original docstrings and signature metadata via @functools.wraps.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt == max_attempts:
                        raise exc
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper  # type: ignore
    return decorator


def timing_benchmark(func: F) -> F:
    """
    Decorator that measures execution time and records performance metrics.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        wrapper.last_execution_time = duration  # type: ignore
        return result
    wrapper.last_execution_time = 0.0  # type: ignore
    return wrapper  # type: ignore


# Example function using advanced decorators
@timing_benchmark
@retry(max_attempts=3, delay=0.01)
def fetch_simulated_api_data(fail_count: int = 0) -> str:
    """Simulate fetching remote data with intermittent network failures."""
    fetch_simulated_api_data.attempts = getattr(fetch_simulated_api_data, "attempts", 0) + 1
    if fetch_simulated_api_data.attempts <= fail_count:
        raise ConnectionError(f"Temporary network failure on attempt {fetch_simulated_api_data.attempts}")
    return "SUCCESS: Payload Received"
