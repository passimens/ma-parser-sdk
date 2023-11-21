import logging
from typing import Callable, List, Any, Awaitable

from parser_api.base_parser import BaseParser
from parser_api.error import FormatError
from model_for_tests.Host import Host
from model_for_tests.Port import Port

logger = logging.getLogger(__name__)


class HostPortParser(BaseParser):
    """A simple parser that tries to convert each line of input to a Host or a Port."""

    def __init__(self, result_callback: Callable[[List[Any]], Awaitable[None]]):
        super().__init__(result_callback)
        self._host = None
        self._ports = []

    async def _process_host(self):
        if self._host:
            self._host.ports = self._ports
            await self._result_callback([self._host] + self._ports)
            self._host = None
            self._ports = []

    async def _on_eof(self):
        """Called when EOF is reached."""
        await self._process_host()

    async def _parse_line(
            self,
            line: str,
            ) -> None:
        """Parses a single line of data."""
        parts = line.split(':')
        if parts[0].lower() == 'h':
            await self._process_host()
            self._host = Host(parts[1].strip(), [])
        elif parts[0].lower() == 'p':
            if not self._host:
                raise FormatError(f"Port without host: {line}")
            self._ports.append(Port(self._host, int(parts[1].strip())))
        elif parts[0].strip() == '':
            await self._process_host()
        else:
            raise FormatError(f"Invalid line prefix: {line}")
