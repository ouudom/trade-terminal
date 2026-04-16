from __future__ import annotations


class TradeTerminalError(Exception):
    """Base for all application exceptions."""


class NotFoundError(TradeTerminalError):
    """A requested resource does not exist."""

    def __init__(self, resource: str, identifier: str | int) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} '{identifier}' not found")


class AppValidationError(TradeTerminalError):
    """Business-rule validation failure (distinct from Pydantic schema validation)."""


class ExternalServiceError(TradeTerminalError):
    """A third-party API or external socket call failed."""

    def __init__(self, service: str, detail: str) -> None:
        self.service = service
        super().__init__(f"{service} error: {detail}")


