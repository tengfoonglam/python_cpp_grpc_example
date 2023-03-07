import docker
import subprocess
import time

from arithmetic_python_client import MaxClient, PerformPrimeNumberDecompositionClient

from threading import Event
from typing import Callable, Generator, List, NewType, Tuple, Union

IntGenerator = NewType('IntGenerator', Generator[int, None, None])
ConfiguredMaxClient = NewType('ConfiguredMaxClient', Tuple[MaxClient, Event, Callable[[List[Tuple[int, bool]]],
                                                                                      Generator[int, None, None]]])
ConfiguredPrimeClient = NewType('ConfiguredPrimeClient', Tuple[PerformPrimeNumberDecompositionClient, List[int], Event])


class ArithmeticServerProcess:
    def __init__(self, process: Union[subprocess.Popen, docker.models.containers.Container]) -> None:
        self._process = process

    def kill(self) -> None:
        try:
            self._process.kill()
        except docker.errors.APIError:
            # Handle case where docker container is used and already killed during pytest
            pass
        time.sleep(0.2)    # Provide some time for kill to be processed
