import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from PIL import Image
import time

load_dotenv()

class GeminiMRIAnalyzer:
    def __init__(self):
        """Initialize Gemini API with your API key"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        # Use gemini-2.5-flash - latest stable model with excellent vision capabilities
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.last_request_time = 0
        self.min_request_interval = 3  # Minimum 3 seconds between requests
        
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
            # Rate limiting: ensure minimum interval between requests
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            if time_since_last_request < self.min_request_interval:
                wait_time = self.min_request_interval - time_since_last_request
                print(f"Rate limiting: waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            
            prompt = self.create_prompt()
            
            # Generate response
            print("Sending request to Gemini API...")
            response = self.model.generate_content([prompt, image])
            self.last_request_time = time.time()
            
            # Get response text
            response_text = response.text.strip()
            print(f"Raw Gemini response:\n{response_text}\n")  # Debug output
            
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
            
            # Validate required fields
            if "primary_diagnosis" not in analysis:
                analysis["primary_diagnosis"] = {
                    "classification": "Inconclusive",
                    "confidence": 0
                }
            
            if "affected_regions" not in analysis:
                analysis["affected_regions"] = []
            
            if "clinical_findings" not in analysis:
                analysis["clinical_findings"] = ["Unable to determine clinical findings"]
            
            if "explanation" not in analysis:
                analysis["explanation"] = "Analysis completed but detailed explanation not available."
            
            if "risk_assessment" not in analysis:
                analysis["risk_assessment"] = {
                    "risk_level": "Unknown",
                    "rationale": "Risk assessment not available"
                }
            
            return analysis
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error during analysis: {error_msg}")
            
            # Check for rate limit error
            if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                return {
                    "error": "Rate limit exceeded",
                    "details": "You've hit the Gemini API rate limit. Please wait 60 seconds and try again.",
                    "suggestion": "The free tier allows 15 requests per minute. Wait a moment before trying again.",
                    "primary_diagnosis": {
                        "classification": "Rate Limit",
                        "confidence": 0
                    },
                    "affected_regions": [],
                    "clinical_findings": ["Rate limit exceeded - please wait"],
                    "explanation": "API rate limit reached. Free tier: 15 requests/min. Please wait 60 seconds.",
                    "risk_assessment": {
                        "risk_level": "Unknown",
                        "rationale": "Cannot assess due to rate limiting"
                    }
                }
            
            # Check for JSON parsing error
            if "json" in error_msg.lower():
                return {
                    "error": "Failed to parse AI response",
                    "details": f"JSON parsing failed: {error_msg}",
                    "primary_diagnosis": {
                        "classification": "Parsing Error",
                        "confidence": 0
                    },
                    "affected_regions": [],
                    "clinical_findings": ["Response parsing failed"],
                    "explanation": f"The AI response could not be parsed as JSON: {error_msg}",
                    "risk_assessment": {
                        "risk_level": "Unknown",
                        "rationale": "Cannot assess due to parsing error"
                    }
                }
            
            # General error
            return {
                "error": str(e),
                "details": "Failed to analyze MRI image",
                "primary_diagnosis": {
                    "classification": "Error",
                    "confidence": 0
                },
                "affected_regions": [],
                "clinical_findings": ["Analysis failed"],
                "explanation": f"An error occurred during analysis: {str(e)}",
                "risk_assessment": {
                    "risk_level": "Unknown",
                    "rationale": "Could not assess risk due to error"
                }
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
