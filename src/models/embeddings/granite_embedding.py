from __future__  import annotations

import numpy as np
import os
import sys

from contextlib import contextmanager
from langchain_core.embeddings import Embeddings
from langchain_core.runnables.config import run_in_executor
from llama_cpp import Llama
from typing import List, Optional

# llama-cpp output a warning to indicate it automatically defaulted to embedding
# mode this is annoying. So here's an end to that mess.
@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(os.devnull, 'w') as fnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = fnull
        sys.stderr = fnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

class GraniteEmbeddings(Embeddings):
    """Custom Granite embedding model integration using llama-cpp-python."""

    model_path: str # Path to the local GGUF model file
    n_ctx: int = 512 # Default context size for embeddings
    n_threads: Optional[int] = None # Number of CPU threads
    chunk_size: int = 1000 # Maximum number of texts to embed in each batch
    _client: Llama  # Internal llama-cpp client

    def __init__(self, model_path: str, n_ctx: int = 512, 
                n_threads: Optional[int] = None, chunk_size: int = 1000) -> None:
        """
        Initialize the GraniteEmbeddings with model parameters.

        Args:
            model_path (str): Path to the local GGUF model file.
            n_ctx (int): Context size for embeddings.
            n_threads (Optional[int]): Number of CPU threads to use.
            chunk_size (int): Number of texts to embed in each batch.
        """

        super().__init__()
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.chunk_size = chunk_size
        self._client = Llama(
            model_path=self.model_path,
            embedding=True,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            verbose=False,
        )

    def _get_embedding(self, text: str) -> List[float]:
        with suppress_stdout_stderr():
            response = self._client.create_embedding(text)
        return np.array(response['data'][0]['embedding'], dtype='float32').tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed search docs. 

        Args:
            texts (List[str]): List of texts to embed. 
        
        Returns:
            List[List[float]]: List of embeddings, one per text.
        """
        embeddings: List[List[float]] = []
        
        for i in range(0, len(texts), self.chunk_size):
            batch = texts[i : i + self.chunk_size]
            for text in batch:
                embeddings.append(self._get_embedding(text))
        
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """
        Embed query text. Simply calls embed_documents for the single string.

        Args:
            text (str): The query text to embed.

        Returns:
            List[float]: The embedding vector for the query.
        """
        return self.embed_documents([text])[0]

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Asynchronous document embedding.

        Args:
            texts (List[str]): List of texts to embed.
        Returns:
            List[List[float]]: List of embeddings, one per text.
        """
        return await run_in_executor(None, self.embed_documents, texts)

    async def aembed_query(self, text: str) -> List[float]:
        """
        Asynchronous query embedding.

        Args:
            text (str): The query text to embed.

        Returns:
            List[float]: The embedding vector for the query.
        """
        return await run_in_executor(None, self.embed_query, text)