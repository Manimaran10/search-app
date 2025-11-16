#!/usr/bin/env python3
"""
Setup text search index for MongoDB fallback search functionality
"""
import logging
from pymongo import MongoClient, TEXT
from pymongo.errors import OperationFailure
from src.services.db_handler.config import mongodb_config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_text_index():
    """Create text search index for fallback search functionality."""
    try:
        # Connect to MongoDB
        client = MongoClient(
            mongodb_config.connection_string,
            **mongodb_config.get_connection_params()
        )
        
        # Test connection
        client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
        
        # Get database and collection
        database = client[mongodb_config.database_name]
        collection = database[mongodb_config.collection_name]
        
        # Check existing indexes
        existing_indexes = list(collection.list_indexes())
        logger.info(f"Existing indexes: {[idx['name'] for idx in existing_indexes]}")
        
        # Check if text index already exists
        text_index_exists = False
        text_index_name = None
        
        for index in existing_indexes:
            # Check if this is a text index
            key_spec = index.get('key', {})
            if any(value == 'text' for value in key_spec.values()):
                text_index_exists = True
                text_index_name = index['name']
                logger.info(f"Found existing text index: {text_index_name}")
                break
        
        if not text_index_exists:
            # Create new text index
            text_index_fields = [
                ("content", TEXT),
                ("title", TEXT)
            ]
            
            try:
                index_name = collection.create_index(
                    text_index_fields,
                    background=True,
                    default_language='english'
                )
                logger.info(f"Text search index created: {index_name}")
                text_index_name = index_name
            except OperationFailure as e:
                logger.error(f"Failed to create text index: {e}")
                return False
        
        # Verify the index works
        if text_index_name:
            logger.info(f"Text search index available: {text_index_name}")
            logger.info("Text search index verified successfully")
            
        client.close()
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup text index: {e}")
        return False

if __name__ == "__main__":
    print("Setting up MongoDB text search index...")
    success = setup_text_index()
    if success:
        print("✅ Text search index setup completed successfully!")
    else:
        print("❌ Failed to setup text search index")
