from typing import Dict, List
import logging
from ..config import get_groq_api_key
from .rag.retriever import retrieve_relevant_context
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsultationService:
    def __init__(self):
        self.groq_api_key = get_groq_api_key()
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Ayurvedic condition descriptions
        self.condition_info = {
            "Diabetes": "In Ayurveda, diabetes (Prameha) is primarily seen as a Kapha disorder with possible Pitta involvement.",
            "Hypertension": "Hypertension in Ayurveda (Rakta Gata Vata) is often related to Vata and Pitta imbalances.",
            "Arthritis": "Arthritis (Sandhivata) is typically viewed as a Vata disorder affecting the joints.",
            "Digestive Issues": "Digestive problems can involve all three doshas, with specific symptoms indicating the primary dosha imbalance.",
            "Respiratory Problems": "Respiratory issues often involve Kapha dosha, with possible Vata and Pitta complications.",
            "Skin Conditions": "Skin disorders (Kushtha) can involve all three doshas, but often have a strong Pitta component.",
            "Sleep Disorders": "Sleep issues are often related to Vata imbalance, though other doshas may be involved.",
            "Stress/Anxiety": "Anxiety and stress primarily affect Vata dosha, leading to mental and physical imbalances."
        }
        
    def get_personalized_recommendations(self, consultation_data: Dict) -> Dict:
        try:
            if not consultation_data:
                raise ValueError("Consultation data is missing")

            prompt = self._create_consultation_prompt(consultation_data)
            
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "openai/gpt-oss-120b",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 2048
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=45
            )
            
            if response.status_code != 200:
                logger.error(f"API call failed: {response.text}")
                return self._get_default_recommendations(consultation_data)
            
            content = response.json()['choices'][0]['message']['content']
            return self._parse_consultation_response(content)
            
        except Exception as e:
            logger.error(f"Error in consultation service: {str(e)}")
            return self._get_default_recommendations(consultation_data)
    
    def _get_reference_material(self, data: Dict) -> str:
        """Retrieve relevant chunks from the RAG knowledge base to ground
        the LLM's response. Combines dosha, primary concerns, and medical conditions."""
        try:
            dosha_profile = data.get('dosha_profile') or {}
            primary_dosha = dosha_profile.get('primary_dosha', '')
            concerns = data.get('concerns', {}).get('primary_concerns', '')
            
            conditions = data.get('medical_history', {}).get('conditions', [])
            conditions_text = ""
            if isinstance(conditions, list):
                conditions_text = " ".join([c for c in conditions if c and c != "None"])
            elif isinstance(conditions, str):
                conditions_text = conditions

            query = f"{primary_dosha} dosha {concerns} {conditions_text}".strip()
            if not query:
                query = "Ayurvedic dosha balance diet and lifestyle"

            chunks = retrieve_relevant_context(query, top_k=3)
            if not chunks:
                return "No specific reference material retrieved."

            return "\n\n".join(chunks)
        except Exception as e:
            logger.error(f"Error retrieving reference material: {str(e)}")
            return "No specific reference material retrieved."

    def _create_consultation_prompt(self, data: Dict) -> str:
        personal = data.get('personal_info', {})
        medical = data.get('medical_history', {})
        lifestyle = data.get('lifestyle', {})
        concerns = data.get('concerns', {})
        dosha_info = data.get('dosha_profile', {})

        reference_material = self._get_reference_material(data)

        return f"""
        As an expert Ayurvedic doctor and consultant, provide detailed personalized recommendations for the patient based on their dosha profile and concerns.

        Reference Material (Authentic Ayurvedic source texts to ground your guidance; treat as trusted medical reference):
        {reference_material}

        Patient Details (strictly patient data):
        - Personal Info: {personal}
        - Medical History: {medical}
        - Current Lifestyle: {lifestyle}
        - Primary Health Concerns: {concerns}
        - Dosha Profile: {dosha_info}

        Please structure your response strictly using these exact headers so each section is clearly identifiable for the patient report:

        Dosha Profile Analysis:
        - Detailed analysis of their dosha constitution and how current symptoms relate to doshic imbalance.

        Diet:
        - Specific foods, tastes (Rasas), and dietary habits to favor.
        - Specific foods and habits to avoid.

        Lifestyle:
        - Daily routine adjustments (Dinacharya), waking, meal timings, and physical exercise.

        Herbal Remedies:
        - Traditional Ayurvedic herbs (e.g. Triphala, Ashwagandha, Brahmi, etc.) suitable for this profile with preparation and dosage tips.

        Panchakarma and Body Therapies:
        - Recommended body therapies (e.g. Abhyanga with warm oils, Shirodhara) or home therapies.

        Stress Management:
        - Pranayama (breathwork), meditation, or calming practices to support mental balance.

        Monitoring and Adjustments:
        - Signs of positive progress, seasonal advice, and when to seek certified medical care.

        Important Considerations:
        - Safety precautions and general guidance.
        """
    
    def _get_default_recommendations(self, consultation_data: Dict) -> Dict:
        return {
            "status": "error",
            "message": "Unable to generate personalized recommendations. Please consult a practitioner."
        }
    
    def _parse_consultation_response(self, response: str) -> Dict:
        return {"recommendations": response.split("\n")}
