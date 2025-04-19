from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
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
    
    def _get_project_root(self) -> Path:
        """Get the project root directory."""
        return Path(__file__).parent.parent.parent
    
    def _load_json_data(self, file_path: str) -> List[Document]:
        """Load and process data from JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of Document objects
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        documents = []
        for item in data:
            # Create a document for each item in the JSON
            content = f"Title: {item.get('title', '')}\n"
            content += f"Description: {item.get('description', '')}\n"
            content += f"Technologies: {', '.join(item.get('technologies', []))}\n"
            content += f"Team: {', '.join(item.get('team', []))}\n"
            
            documents.append(Document(
                page_content=content,
                metadata={
                    "id": item.get('id', ''),
                    "title": item.get('title', ''),
                    "url": item.get('url', ''),
                    "source": "hackathon_data"
                }
            ))
        
        return documents
    
    def load_documents(self) -> None:
        """Load and index documents from the configured data source."""
        data_config = self.config.data
        project_root = self._get_project_root()
        
        # Get absolute paths
        source_file = project_root / data_config.source_file
        vector_store_path = project_root / data_config.vector_store_path
        
        if not source_file.exists():
            raise ValueError(f"Data source file not found: {source_file}")
        
        # Load documents from JSON
        documents = self._load_json_data(str(source_file))
        
        if not documents:
            raise ValueError("No documents found in the data source")
        
        # Split documents into chunks
        texts = self.text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = FAISS.from_documents(texts, self.embeddings)
        
        # Save the vector store
        vector_store_path.parent.mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(str(vector_store_path))
    
    def similarity_search(self, query: str, k: int = 50) -> List[Dict[str, Any]]:
        """Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return (default: 50)
            
        Returns:
            List of dictionaries containing document content and metadata
        """
        if self.vector_store is None:
            # Try to load from disk if not in memory
            project_root = self._get_project_root()
            vector_store_path = project_root / self.config.data.vector_store_path
            if vector_store_path.exists():
                self.vector_store = FAISS.load_local(str(vector_store_path), self.embeddings)
            else:
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