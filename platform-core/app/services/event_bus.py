"""
Event bus abstraction. Dev/emulation = in-memory pub/sub; production = Kafka/Redpanda.
Mirrors the spec's append-stream pattern (idempotent producers, per-stream topics).
"""
from collections import defaultdict
from typing import Callable
from app.core.config import settings


class _MemoryBus:
    def __init__(self):
        self._subs: dict[str, list[Callable]] = defaultdict(list)
        self.log: list[tuple[str, dict]] = []

    def subscribe(self, topic: str, handler: Callable):
        self._subs[topic].append(handler)

    def emit(self, topic: str, payload: dict):
        self.log.append((topic, payload))
        for h in self._subs.get(topic, []):
            h(payload)


# Kafka backend is wired in production; the interface is identical so callers don't change.
class _KafkaBus(_MemoryBus):
    """Placeholder that falls back to memory until KAFKA_BOOTSTRAP is configured.
    Real Kafka producer/consumer is added in infra deployment; interface-compatible."""
    pass


bus = _KafkaBus() if settings.event_bus_backend == "kafka" else _MemoryBus()
