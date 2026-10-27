"""Search helpers for an Azure AI Search index."""

import os
from typing import Any

from config.settings import Settings


class SearchService:
    """Run text searches against an Azure AI Search index."""

    def __init__(
        self,
        endpoint: str | None = None,
        key: str | None = None,
        index_name: str | None = None,
        search_client: Any | None = None,
        settings: Settings | None = None,
    ) -> None:
        if search_client is not None:
            self._search_client = search_client
            return

        endpoint = (
            endpoint
            or (settings.azure_search_endpoint if settings else None)
            or os.getenv("AZURE_SEARCH_ENDPOINT")
        )
        key = (
            key
            or (settings.azure_search_key if settings else None)
            or os.getenv("AZURE_SEARCH_KEY")
        )
        index_name = (
            index_name
            or (settings.azure_search_index if settings else None)
            or os.getenv("AZURE_SEARCH_INDEX")
        )
        missing = [
            name
            for name, value in (
                ("AZURE_SEARCH_ENDPOINT", endpoint),
                ("AZURE_SEARCH_KEY", key),
                ("AZURE_SEARCH_INDEX", index_name),
            )
            if not value
        ]
        if missing:
            raise ValueError(
                f"Missing Azure AI Search configuration: {', '.join(missing)}"
            )

        try:
            from azure.core.credentials import AzureKeyCredential
            from azure.search.documents import SearchClient
        except ImportError as error:
            raise RuntimeError(
                "Azure AI Search support requires the "
                "'azure-search-documents' package"
            ) from error

        self._search_client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(key),
        )

    def search(self, query: str, top: int = 5) -> list[dict[str, Any]]:
        """Return up to ``top`` matching documents."""
        if not query.strip():
            raise ValueError("query must not be empty")
        if top < 1:
            raise ValueError("top must be at least 1")

        results = self._search_client.search(search_text=query, top=top)
        return [dict(result) for result in results]
