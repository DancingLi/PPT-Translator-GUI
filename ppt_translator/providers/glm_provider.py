"""GLM (Zhipu AI) provider implementation."""
from __future__ import annotations

import os

from .base import OpenAICompatibleProvider


class GLMProvider(OpenAICompatibleProvider):
    """Translate through GLM's OpenAI compatible API."""

    api_key_env = "GLM_API_KEY"
    default_base_url = "https://open.bigmodel.cn/api/paas/v4/"

    def __init__(self, model: str, **kwargs) -> None:
        base_url = kwargs.pop("base_url", None) or os.getenv("GLM_API_BASE", self.default_base_url)
        super().__init__(model=model, base_url=base_url, **kwargs)
