# AI Knowledge Base Search App

A modern web application for AI-powered knowledge base management with search capabilities.

## Features

- 🏠 **Home Page**: Search interface with AI-powered results
- 📚 **Knowledge Base**: File upload and management system
- 🔍 **Smart Search**: Search through uploaded documents and knowledge base
- 📁 **File Upload**: Support for local files and public URLs
- 🎨 **Modern UI**: Clean, responsive design inspired by modern applications

## Project Structure

```
search-app/
├── src/                    # React frontend
│   ├── components/         # Reusable components
│   ├── pages/             # Page components
│   └── styles/            # CSS files
├── backend/               # Python Flask backend
│   └── src/
│       └── controllers/   # API endpoints
└── public/               # Static assets
```

## Setup Instructions

### Prerequisites

- Node.js 16+ 
- Python 3.9+
- npm or yarn

### Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd /Users/dharan-19096/VisualStudioProjects/search-app
   ```

2. **Install dependencies:**
   ```bash
   # Frontend dependencies
   npm install
   
   # Backend dependencies
   cd backend
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   cd ..
   ```

3. **Start the development servers:**
   ```bash
   # Option 1: Use the automated script
   ./start-dev.sh
   
   # Option 2: Start manually
   # Terminal 1 - Backend
   cd backend/src/controllers && python app_controller.py
   
   # Terminal 2 - Frontend
   npm start
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## API Endpoints

### Search
- `GET /api/search?q={query}` - Search the knowledge base

### Files
- `GET /api/files` - Get all uploaded files
- `POST /api/upload` - Upload files (supports both local files and URLs)

### System
- `GET /status` - Check application status
- `GET /app` - Get application information

## Usage

### Home Page
1. Enter your search query in the search bar
2. View results displayed above the search interface
3. Each result shows content and categorized metadata

### Knowledge Base
1. Upload files using the "Upload Files" section
2. Support for local file upload or public URL links
3. View all uploaded files in the file grid
4. Filter and search through uploaded documents

## Development

### Frontend (React)
- Built with React 18+ and React Router
- Responsive design with modern CSS
- Component-based architecture

### Backend (Flask)
- RESTful API with Flask
- CORS enabled for cross-origin requests
- File upload handling with Werkzeug
- Mock database for development

## Configuration

### Environment Variables
- `UPLOAD_FOLDER`: Directory for uploaded files (default: 'uploads')
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)

### Proxy Configuration
The frontend is configured to proxy API requests to `http://localhost:5000` during development.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
