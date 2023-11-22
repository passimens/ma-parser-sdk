import logging

from parser_api.base_parser import BaseParser

logger = logging.getLogger(__name__)


class IntParser(BaseParser):
    """A simple parser that tries to convert each line of input to an integer. If fails - returns ValueError."""

    async def _parse_line(
            self,
            line: str,
            ) -> None:
        """Parses a single line of data."""
        res = int(line)
        await self._result_callback([res])

