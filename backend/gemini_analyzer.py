import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from PIL import Image

load_dotenv()

class GeminiMRIAnalyzer:
    def __init__(self):
        """Initialize Gemini API with your API key"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def create_prompt(self):
        """Create structured prompt for MRI analysis"""
        return """You are an expert cardiac radiologist analyzing cardiac MRI scans.

Analyze this cardiac MRI image and provide a detailed assessment in JSON format.

Your analysis should include:

1. PRIMARY_DIAGNOSIS: 
   - classification: "Normal" or "Myocardial Infarction" or "Structural Deformity" or "Inconclusive"
   - confidence: number between 0-100

2. AFFECTED_REGIONS:
   - List specific anatomical areas affected (e.g., "anterior wall of left ventricle", "septal wall", "apex")
   - For each region, note severity: "mild", "moderate", or "severe"

3. CLINICAL_FINDINGS:
   - List key abnormalities observed
   - Signal intensity changes
   - Wall motion abnormalities
   - Structural changes

4. EXPLANATION:
   - Detailed reasoning for the diagnosis
   - Specific visual features that support the diagnosis
   - Clinical significance of findings
   - Recommended follow-up or additional tests if needed

5. RISK_ASSESSMENT:
   - risk_level: "Low", "Moderate", "High", or "Critical"
   - rationale: brief explanation

Return ONLY valid JSON with this exact structure:
{
  "primary_diagnosis": {
    "classification": "string",
    "confidence": number
  },
  "affected_regions": [
    {
      "location": "string",
      "severity": "string"
    }
  ],
  "clinical_findings": [
    "string"
  ],
  "explanation": "string",
  "risk_assessment": {
    "risk_level": "string",
    "rationale": "string"
  }
}

Be precise, clinical, and evidence-based in your analysis."""

    def analyze_mri(self, image: Image.Image):
        """
        Analyze MRI image using Gemini
        
        Args:
            image: PIL Image object
            
        Returns:
            dict: Analysis results
        """
        try:
            prompt = self.create_prompt()
            
            # Generate response
            response = self.model.generate_content([prompt, image])
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            analysis = json.loads(response_text)
            
            return analysis
            
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return raw response with error
            return {
                "error": "Failed to parse JSON response",
                "raw_response": response.text,
                "parse_error": str(e)
            }
        except Exception as e:
            return {
                "error": str(e),
                "details": "Failed to analyze MRI image"
            }
    
    def analyze_with_history(self, image: Image.Image, patient_history: str = None):
        """
        Analyze MRI with additional patient history context
        
        Args:
            image: PIL Image object
            patient_history: Optional patient medical history
            
        Returns:
            dict: Analysis results
        """
        prompt = self.create_prompt()
        
        if patient_history:
            prompt += f"\n\nPatient History: {patient_history}\n\nConsider this history in your analysis."
        
        try:
            response = self.model.generate_content([prompt, image])
            response_text = response.text.strip()
            
            # Clean JSON markers
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            analysis = json.loads(response_text)
            
            return analysis
            
        except Exception as e:
            return {
                "error": str(e),
                "details": "Failed to analyze MRI image with history"
            }
