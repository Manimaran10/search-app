import React, { useState, useEffect } from "react";
import "../styles/kb.css";

export default function KnowledgeBase() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [publicUrl, setPublicUrl] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [activeTab, setActiveTab] = useState("all");
  const [showUploadModal, setShowUploadModal] = useState(false);
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';


  // Mock data - replace with actual API call
  useEffect(() => {
    fetchUploadedFiles();
  }, []);

  const fetchUploadedFiles = async () => {
    try {
      const response = await fetch(`${API_URL}/api/files`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setUploadedFiles(data.files || []);
    } catch (error) {
      console.error("Error fetching files:", error);
      setUploadedFiles([]);
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFiles && !publicUrl) return;

    setIsUploading(true);
    try {
      const formData = new FormData();
      if (selectedFiles) {
        for (let i = 0; i < selectedFiles.length; i++) {
          formData.append('files', selectedFiles[i]);
        }
      }
      if (publicUrl) {
        formData.append('publicUrl', publicUrl);
      }

      const response = await fetch(`${API_URL}/api/upload`, {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Upload successful:', result.message);
        
        fetchUploadedFiles(); // Refresh file list
        setSelectedFiles(null);
        setPublicUrl("");
        // Reset file input
        document.getElementById('fileInput').value = '';
        
        // Close modal and show success message
        setShowUploadModal(false);
        alert('Files uploaded successfully!');
      } else {
        throw new Error(`Upload failed with status: ${response.status}`);
      }
    } catch (error) {
      console.error("Upload error:", error);
    } finally {
      setIsUploading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="main-content">
      <div className="kb-container">
        <div className="kb-header">
          <h1>Knowledge Base</h1>
          <div className="kb-actions">
            <button className="btn btn-primary" onClick={() => setShowUploadModal(true)}>
              Upload Files
            </button>
          </div>
        </div>

        

        {/* Upload Modal */}
        {showUploadModal && (
          <div className="upload-modal-overlay" onClick={() => setShowUploadModal(false)}>
            <div className="upload-modal" onClick={(e) => e.stopPropagation()}>
              <div className="upload-modal-header">
                <h3>Upload Files</h3>
                <button 
                  className="close-btn" 
                  onClick={() => setShowUploadModal(false)}
                >
                  ✕
                </button>
              </div>
              <form onSubmit={handleFileUpload} className="upload-form">
                <div className="upload-options">
                  <div className="upload-option">
                    <label htmlFor="fileInput" className="upload-label">
                      📁 Upload Local Files
                    </label>
                    <input 
                      id="fileInput"
                      type="file" 
                      multiple
                      onChange={(e) => setSelectedFiles(e.target.files)}
                      className="file-input"
                    />
                  </div>
                  <div className="upload-option">
                    <label className="upload-label">🌐 Public File URL</label>
                    <input 
                      type="url"
                      placeholder="https://example.com/document.pdf"
                      value={publicUrl}
                      onChange={(e) => setPublicUrl(e.target.value)}
                      className="url-input"
                    />
                  </div>
                </div>
                <div className="upload-modal-actions">
                  <button 
                    type="button" 
                    className="btn btn-secondary"
                    onClick={() => setShowUploadModal(false)}
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    className="upload-btn"
                    disabled={isUploading || (!selectedFiles && !publicUrl)}
                  >
                    {isUploading ? "Uploading..." : "Upload"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* File List */}
        <div className="files-section">
          <h3>Uploaded Files</h3>
          {uploadedFiles.length === 0 ? (
            <div className="empty-state">
              <p>No files uploaded yet</p>
            </div>
          ) : (
            <div className="file-grid">
              {uploadedFiles.map((file) => (
                <div key={file.id} className="file-card">
                  <div className="file-icon">
                    📄
                  </div>
                  <div className="file-info">
                    <h4 className="file-name">{file.name}</h4>
                    <div className="file-meta">
                      <span className="file-type">{file.type}</span>
                      <span className="file-size">{file.size}</span>
                      <span className="file-downloads">📥 {file.downloads}</span>
                      <span className="file-date">{file.uploadDate}</span>
                    </div>
                  </div>
                  <div className="file-actions-menu">
                    <button className="btn-menu">⋯</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
