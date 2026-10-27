"""Typed application settings loaded from environment variables."""

import math
import os
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Settings:
    """Environment-backed settings for model and Azure service integrations."""

    openai_api_key: str | None = field(default=None, repr=False)
    openai_model: str = "gpt-4o-mini"
    openai_timeout: float = 30.0
    cosmos_endpoint: str | None = None
    cosmos_key: str | None = field(default=None, repr=False)
    cosmos_database: str | None = None
    cosmos_container: str | None = None
    azure_search_endpoint: str | None = None
    azure_search_key: str | None = field(default=None, repr=False)
    azure_search_index: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from the process environment without reading files."""
        timeout_value = os.getenv("OPENAI_TIMEOUT", "30")
        try:
            timeout = float(timeout_value)
        except ValueError as error:
            raise ValueError("OPENAI_TIMEOUT must be a number") from error
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("OPENAI_TIMEOUT must be a finite number greater than 0")

        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_timeout=timeout,
            cosmos_endpoint=os.getenv("COSMOS_ENDPOINT"),
            cosmos_key=os.getenv("COSMOS_KEY"),
            cosmos_database=os.getenv("COSMOS_DATABASE"),
            cosmos_container=os.getenv("COSMOS_CONTAINER"),
            azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            azure_search_key=os.getenv("AZURE_SEARCH_KEY"),
            azure_search_index=os.getenv("AZURE_SEARCH_INDEX"),
        )

    def validate_for(self, service: str) -> None:
        """Raise an actionable error when a service's settings are missing."""
        required_variables = {
            "openai": {
                "OPENAI_API_KEY": self.openai_api_key,
            },
            "cosmos": {
                "COSMOS_ENDPOINT": self.cosmos_endpoint,
                "COSMOS_KEY": self.cosmos_key,
                "COSMOS_DATABASE": self.cosmos_database,
                "COSMOS_CONTAINER": self.cosmos_container,
            },
            "search": {
                "AZURE_SEARCH_ENDPOINT": self.azure_search_endpoint,
                "AZURE_SEARCH_KEY": self.azure_search_key,
                "AZURE_SEARCH_INDEX": self.azure_search_index,
            },
        }
        if service not in required_variables:
            raise ValueError(
                f"Unknown service {service!r}; expected one of "
                f"{', '.join(required_variables)}"
            )

        missing = [
            name for name, value in required_variables[service].items() if not value
        ]
        if missing:
            raise ValueError(
                f"Missing configuration for {service}: {', '.join(missing)}"
            )
