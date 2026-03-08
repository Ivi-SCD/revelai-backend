"""
Shared LLM factory for all agents.

Handles corporate proxy / SSL issues by creating a custom httpx client
when SSL_CERT_FILE doesn't resolve the proxy's certificate chain.
"""

import httpx
from langchain_groq import ChatGroq
from app.core.settings import get_settings


def _build_http_client() -> httpx.AsyncClient:
    """
    Build an httpx AsyncClient that works behind corporate proxies.
    The proxy often injects its own TLS certificate which Python
    doesn't trust. We disable verification for dev environments.

    For production, set SSL_CERT_FILE to the proxy CA bundle instead.
    """
    return httpx.AsyncClient(verify=False)


def get_llm(
    temperature: float = 0.3,
    max_tokens: int = 4096,
    model: str = "meta-llama/llama-4-scout-17b-16e-instruct",
) -> ChatGroq:
    """Return a ChatGroq instance that works behind corporate proxies."""
    settings = get_settings()
    return ChatGroq(
        model=model,
        api_key=settings.GROQ_API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
        http_async_client=_build_http_client(),
    )
