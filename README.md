# MRI_Analysis_XAI

**Explainable AI-Based Cardiac MRI Analysis System for Detecting Myocardial Infarction and Structural Deformities**

This system uses Google's Gemini 2.0 Flash API to analyze cardiac MRI scans and provide detailed, explainable diagnoses with confidence scores, affected regions, clinical findings, and risk assessments.

---

## 🚀 Features

- **AI-Powered Analysis**: Leverages Gemini 2.0 Flash for advanced cardiac MRI interpretation
- **Explainable AI**: Provides detailed reasoning and clinical explanations for every diagnosis
- **Visual Interface**: Clean, intuitive web interface with drag-and-drop upload
- **Comprehensive Reports**: Includes diagnosis, confidence scores, affected regions, clinical findings, and risk assessment
- **Local Deployment**: Runs entirely on your local machine - no cloud deployment needed
- **Fast Processing**: Typical analysis completed in 5-10 seconds

---

## 📋 Prerequisites

- Python 3.9 or higher
- Google Gemini API Key (free tier available)
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/keerthisuryateja1/MRI_Analysis_XAI.git
cd MRI_Analysis_XAI
```

### 2. Set Up Backend

```bash
cd backend
pip install -r requirements.txt
```

### 3. Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key" or "Create API Key"
3. Copy your API key

### 4. Configure Environment Variables

Edit the `.env` file in the `backend` folder:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

⚠️ **Important**: Replace `your_actual_api_key_here` with your actual Gemini API key!

---

## 🎯 Usage

### Start the Backend Server

Open a terminal and run:

```bash
cd backend
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Start the Frontend

Open a **new terminal** and run:

```bash
cd frontend
python -m http.server 8080
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8080...
```

### Access the Application

Open your browser and go to:
```
http://localhost:8080
```

---

## 📸 How to Use

1. **Upload MRI Image**
   - Drag and drop a cardiac MRI image onto the upload zone
   - Or click to browse and select a file
   - Supported formats: JPG, PNG, DICOM

2. **Analyze**
   - Click the "Analyze MRI" button
   - Wait 5-10 seconds for AI analysis

3. **Review Results**
   - **Primary Diagnosis**: Classification (Normal/Myocardial Infarction/Structural Deformity) with confidence score
   - **Risk Assessment**: Risk level (Low/Moderate/High/Critical) with rationale
   - **Affected Regions**: Specific anatomical areas with severity levels
   - **Clinical Findings**: Key abnormalities and observations
   - **AI Explanation**: Detailed reasoning behind the diagnosis

4. **New Analysis**
   - Click "Analyze Another MRI" to process a new image

---

## 📁 Project Structure

```
MRI_Analysis_XAI/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── gemini_analyzer.py      # Gemini API integration
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # API key configuration
├── frontend/
│   └── index.html              # Web interface
├── sample_mris/                # Sample test images (add your own)
└── README.md                   # This file
```

---

## 🧪 Testing with Sample Images

You can test with cardiac MRI images from:

- **Public Datasets**:
  - [ACDC Challenge](https://www.creatis.insa-lyon.fr/Challenge/acdc/)
  - [Cardiac Atlas Project](http://www.cardiacatlas.org/)
  
- **Search for**: "cardiac MRI myocardial infarction" or "cardiac MRI normal" on medical image databases

- **Create `sample_mris/` folder** and add test images there

---

## 🔧 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "gemini_api_configured": true
}
```

### Analyze MRI
```bash
POST http://localhost:8000/analyze
Content-Type: multipart/form-data

file: [MRI image file]
```

Response:
```json
{
  "success": true,
  "image_base64": "...",
  "analysis": {
    "primary_diagnosis": {
      "classification": "Myocardial Infarction",
      "confidence": 87
    },
    "affected_regions": [...],
    "clinical_findings": [...],
    "explanation": "...",
    "risk_assessment": {
      "risk_level": "High",
      "rationale": "..."
    }
  }
}
```

---

## ⚠️ Important Notes

### Medical Disclaimer

**This system is for educational and research purposes only.**

- ❌ **NOT FDA approved** or clinically validated
- ❌ **NOT for medical diagnosis** or treatment decisions
- ❌ **NOT a replacement** for professional medical advice
- ✅ Always consult qualified healthcare professionals for medical decisions

### API Limits

- **Gemini Free Tier**: 60 requests per minute
- For production use, consider upgrading to paid tier
- See [Gemini API Pricing](https://ai.google.dev/pricing)

### Data Privacy

- All processing happens locally or via Gemini API
- Images are not stored permanently
- Ensure compliance with HIPAA/medical data regulations if using real patient data

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
- Ensure `.env` file exists in `backend/` folder
- Check that API key is correctly set (no spaces or quotes)
- Restart the backend server after updating `.env`

### "Connection refused" or CORS errors
- Ensure backend is running on port 8000
- Ensure frontend is running on port 8080
- Check firewall settings

### "Analysis failed"
- Check internet connection (required for Gemini API)
- Verify API key is valid and has quota remaining
- Try with a different image format

### Image not displaying
- Ensure image file is valid (not corrupted)
- Try with JPG or PNG format
- Check image file size (< 20MB recommended)

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👨‍💻 Author

**Keerthi Surya Teja**
- GitHub: [@keerthisuryateja1](https://github.com/keerthisuryateja1)

---

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI for backend framework
- Tailwind CSS for UI components

---

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Open an issue on GitHub
3. Review [Gemini API Documentation](https://ai.google.dev/docs)

---

**⚡ Quick Start Summary:**

```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
# Add your API key to .env file
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
python -m http.server 8080

# Browser
# Open http://localhost:8080
```
