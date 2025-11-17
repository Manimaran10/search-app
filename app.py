#!/usr/bin/env python3
"""
Hugging Face Spaces entry point for AI Knowledge Base Vector Search Application
"""

import os
import sys

# Add the backend source to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Import the Flask app
from app_controller import app

if __name__ == "__main__":
    # Get port from environment (Hugging Face Spaces uses different ports)
    port = int(os.environ.get("PORT", 7860))  # HF Spaces default port
    
    print(f"🚀 Starting AI Knowledge Base on port {port}")
    print("📱 Frontend: Integrated with Flask")
    print("🔗 Backend API: Available at /api/*")
    
    # Run the Flask app
    app.run(
        host="0.0.0.0",  # Listen on all interfaces for HF Spaces
        port=port,
        debug=False  # Disable debug in production
    )