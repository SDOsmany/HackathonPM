from typing import List, Dict, Any, Optional
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)
from src.config.config import ConfigManager

class VectorDB:
    """Vector database for document storage and retrieval."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the vector database.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager.config
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=self.config.openai.api_key
        )
        self.vector_store: Optional[FAISS] = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def _get_loader(self, file_path: str):
        """Get the appropriate document loader based on file extension."""
        file_ext = Path(file_path).suffix.lower()
        if file_ext == '.txt':
            return TextLoader(file_path)
        elif file_ext == '.pdf':
            return PDFLoader(file_path)
        elif file_ext == '.docx':
            return Docx2txtLoader(file_path)
        elif file_ext == '.md':
            return UnstructuredMarkdownLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    
    def load_documents(self, directory_path: str) -> None:
        """Load and index documents from a directory.
        
        Args:
            directory_path: Path to the directory containing documents
        """
        documents = []
        directory = Path(directory_path)
        
        if not directory.exists():
            raise ValueError(f"Directory not found: {directory_path}")
        
        # Load all supported documents
        for file_path in directory.glob("**/*"):
            if file_path.is_file():
                try:
                    loader = self._get_loader(str(file_path))
                    documents.extend(loader.load())
                except ValueError:
                    continue  # Skip unsupported file types
        
        if not documents:
            raise ValueError("No documents found in the specified directory")
        
        # Split documents into chunks
        texts = self.text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = FAISS.from_documents(texts, self.embeddings)
    
    def similarity_search(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of dictionaries containing document content and metadata
        """
        if self.vector_store is None:
            raise ValueError("No documents have been loaded. Call load_documents() first.")
        
        # Perform similarity search
        docs = self.vector_store.similarity_search(query, k=k)
        
        # Format results
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        return results
    
    def save_index(self, path: str) -> None:
        """Save the vector store index to disk.
        
        Args:
            path: Path to save the index
        """
        if self.vector_store is None:
            raise ValueError("No documents have been loaded. Call load_documents() first.")
        
        self.vector_store.save_local(path)
    
    def load_index(self, path: str) -> None:
        """Load a vector store index from disk.
        
        Args:
            path: Path to load the index from
        """
        self.vector_store = FAISS.load_local(path, self.embeddings)