import logging

from base_parser import BaseParser

logger = logging.getLogger(__name__)


class IntStrParser(BaseParser):
    """A simple parser that tries to convert each line of input to an integer. If fails - returns the line as is."""

    async def _parse_line(
            self,
            line: str,
            ) -> None:
        """Parses a single line of data."""
        try:
            res = int(line)
        except ValueError:
            res = line
        await self._result_callback([res])

