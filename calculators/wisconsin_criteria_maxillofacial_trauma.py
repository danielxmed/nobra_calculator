"""
Wisconsin Criteria for Maxillofacial Trauma CT Calculator

Clinical decision rule to predict the need for CT imaging after maxillofacial trauma.

References:
1. Koller KE, Sabatino MJ, Skalski KA, et al. Implementation of clinical decision 
   rules for emergency department patients with facial trauma. AEM Educ Train. 
   2018;2(4):269-275. doi: 10.1002/aet2.10103
2. Dreyer SJ, Wolf SJ, Mayglothling J, et al. Clinical policy: critical issues in 
   the evaluation and management of patients presenting to the emergency department 
   with acute blunt facial trauma. Ann Emerg Med. 2023;82(1):94-114. 
   doi: 10.1016/j.annemergmed.2023.03.032
3. Hopper RA, Salemy S, Sze RW. Diagnosis of midface fractures with CT: what the 
   surgeon needs to know. Radiographics. 2006;26(3):783-793. doi: 10.1148/rg.263055031
"""

from typing import Dict, Any


class WisconsinCriteriaMaxillofacialTraumaCalculator:
    """Calculator for Wisconsin Criteria for Maxillofacial Trauma CT"""
    
    def __init__(self):
        # High-risk criteria for CT imaging
        self.HIGH_RISK_CRITERIA = [
            "high_energy_mechanism",
            "facial_deformity", 
            "malocclusion",
            "facial_numbness",
            "periorbital_swelling",
            "diplopia",
            "palpable_step_off",
            "epistaxis"
        ]
        
        # Criteria descriptions for clinical interpretation
        self.CRITERIA_DESCRIPTIONS = {
            "high_energy_mechanism": "High-energy mechanism of injury",
            "facial_deformity": "Visible facial deformity or asymmetry",
            "malocclusion": "Dental malocclusion or inability to open mouth",
            "facial_numbness": "Facial numbness or altered sensation",
            "periorbital_swelling": "Significant periorbital swelling or hematoma",
            "diplopia": "Double vision or diplopia",
            "palpable_step_off": "Palpable step-off deformity of facial bones",
            "epistaxis": "Epistaxis or nasal deformity"
        }
    
    def calculate(self, high_energy_mechanism: str, facial_deformity: str, malocclusion: str,
                 facial_numbness: str, periorbital_swelling: str, diplopia: str,
                 palpable_step_off: str, epistaxis: str) -> Dict[str, Any]:
        """
        Calculates Wisconsin Criteria recommendation for CT imaging
        
        Args:
            high_energy_mechanism (str): High-energy mechanism present ("yes"/"no")
            facial_deformity (str): Visible facial deformity present ("yes"/"no")
            malocclusion (str): Dental malocclusion present ("yes"/"no")
            facial_numbness (str): Facial numbness present ("yes"/"no")
            periorbital_swelling (str): Periorbital swelling present ("yes"/"no")
            diplopia (str): Double vision present ("yes"/"no")
            palpable_step_off (str): Palpable step-off present ("yes"/"no")
            epistaxis (str): Epistaxis or nasal deformity present ("yes"/"no")
            
        Returns:
            Dict with CT recommendation and clinical interpretation
        """
        
        # Validate inputs
        parameters = {
            "high_energy_mechanism": high_energy_mechanism,
            "facial_deformity": facial_deformity,
            "malocclusion": malocclusion,
            "facial_numbness": facial_numbness,
            "periorbital_swelling": periorbital_swelling,
            "diplopia": diplopia,
            "palpable_step_off": palpable_step_off,
            "epistaxis": epistaxis
        }
        
        self._validate_inputs(parameters)
        
        # Count positive criteria
        positive_criteria = self._count_positive_criteria(parameters)
        
        # Determine CT recommendation
        recommendation = self._get_recommendation(positive_criteria)
        
        # Get detailed interpretation
        interpretation = self._get_interpretation(positive_criteria, parameters)
        
        # Generate detailed assessment
        detailed_assessment = self._generate_detailed_assessment(positive_criteria, parameters)
        
        return {
            "result": recommendation["result"],
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"],
            "positive_criteria_count": positive_criteria["count"],
            "positive_criteria": positive_criteria["criteria"],
            "detailed_assessment": detailed_assessment
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        for param_name, param_value in parameters.items():
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value.lower() not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _count_positive_criteria(self, parameters: Dict[str, str]) -> Dict[str, Any]:
        """
        Counts positive high-risk criteria
        
        Args:
            parameters (Dict): Dictionary of all parameters
            
        Returns:
            Dict with count and list of positive criteria
        """
        
        positive_criteria = []
        
        for criterion in self.HIGH_RISK_CRITERIA:
            if parameters[criterion].lower() == "yes":
                positive_criteria.append({
                    "criterion": criterion,
                    "description": self.CRITERIA_DESCRIPTIONS[criterion]
                })
        
        return {
            "count": len(positive_criteria),
            "criteria": positive_criteria
        }
    
    def _get_recommendation(self, positive_criteria: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines CT imaging recommendation based on Wisconsin Criteria
        
        Args:
            positive_criteria (Dict): Results from positive criteria count
            
        Returns:
            Dict with recommendation result
        """
        
        if positive_criteria["count"] == 0:
            return {
                "result": "CT not indicated"
            }
        else:
            return {
                "result": "CT indicated"
            }
    
    def _get_interpretation(self, positive_criteria: Dict[str, Any], 
                          parameters: Dict[str, str]) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on criteria
        
        Args:
            positive_criteria (Dict): Results from positive criteria count
            parameters (Dict): All input parameters
            
        Returns:
            Dict with interpretation details
        """
        
        if positive_criteria["count"] == 0:
            return {
                "stage": "Low Risk",
                "stage_description": "CT not indicated",
                "interpretation": "No high-risk criteria present according to the Wisconsin Criteria. "
                               "CT imaging is not indicated for facial fracture evaluation. Clinical "
                               "observation and symptomatic treatment are appropriate. Consider plain "
                               "radiographs if specific clinical concerns warrant imaging. Monitor for "
                               "development of concerning symptoms and reassess if clinical status changes."
            }
        else:
            criteria_list = [criterion["description"] for criterion in positive_criteria["criteria"]]
            criteria_text = ", ".join(criteria_list)
            
            return {
                "stage": "High Risk",
                "stage_description": "CT indicated",
                "interpretation": f"One or more high-risk criteria present: {criteria_text}. According to "
                               f"the Wisconsin Criteria, CT imaging is indicated to evaluate for significant "
                               f"facial fractures. Proceed with facial CT with coronal and sagittal "
                               f"reconstructions. Consider consultation with oral and maxillofacial surgery, "
                               f"plastic surgery, or otolaryngology based on suspected injury pattern and "
                               f"institutional protocols."
            }
    
    def _generate_detailed_assessment(self, positive_criteria: Dict[str, Any], 
                                    parameters: Dict[str, str]) -> Dict[str, Any]:
        """
        Generates detailed clinical assessment and recommendations
        
        Args:
            positive_criteria (Dict): Results from positive criteria count
            parameters (Dict): All input parameters
            
        Returns:
            Dict with detailed assessment
        """
        
        assessment = {
            "criteria_analysis": self._analyze_criteria_patterns(positive_criteria, parameters),
            "clinical_recommendations": self._get_clinical_recommendations(positive_criteria, parameters),
            "imaging_recommendations": self._get_imaging_recommendations(positive_criteria),
            "consultation_recommendations": self._get_consultation_recommendations(positive_criteria, parameters),
            "follow_up_recommendations": self._get_follow_up_recommendations(positive_criteria),
            "patient_education": self._get_patient_education_points(positive_criteria)
        }
        
        return assessment
    
    def _analyze_criteria_patterns(self, positive_criteria: Dict[str, Any], 
                                 parameters: Dict[str, str]) -> Dict[str, Any]:
        """Analyzes patterns in positive criteria to suggest injury types"""
        
        analysis = {
            "total_criteria": len(self.HIGH_RISK_CRITERIA),
            "positive_count": positive_criteria["count"],
            "negative_count": len(self.HIGH_RISK_CRITERIA) - positive_criteria["count"],
            "risk_level": "low" if positive_criteria["count"] == 0 else "high"
        }
        
        # Analyze injury pattern suggestions
        injury_patterns = []
        
        if parameters["diplopia"] == "yes" or parameters["periorbital_swelling"] == "yes":
            injury_patterns.append("Orbital fracture (floor, medial wall, or complex)")
        
        if parameters["malocclusion"] == "yes" or parameters["palpable_step_off"] == "yes":
            injury_patterns.append("Mandibular or maxillary fracture")
        
        if parameters["epistaxis"] == "yes":
            injury_patterns.append("Nasal fracture or nasoethmoid complex injury")
        
        if parameters["facial_numbness"] == "yes":
            injury_patterns.append("Infraorbital nerve injury (orbital floor fracture)")
        
        if parameters["facial_deformity"] == "yes":
            injury_patterns.append("Complex facial fracture with displacement")
        
        if parameters["high_energy_mechanism"] == "yes":
            injury_patterns.append("High-energy trauma with potential for multiple fractures")
        
        analysis["suspected_injury_patterns"] = injury_patterns
        
        return analysis
    
    def _get_clinical_recommendations(self, positive_criteria: Dict[str, Any], 
                                    parameters: Dict[str, str]) -> list:
        """Generates clinical management recommendations"""
        
        recommendations = []
        
        if positive_criteria["count"] == 0:
            recommendations.extend([
                "Clinical observation and symptomatic treatment",
                "Pain management with appropriate analgesics",
                "Ice application for swelling and pain relief",
                "Soft diet if oral trauma present",
                "Return precautions for worsening symptoms"
            ])
        else:
            recommendations.extend([
                "Obtain facial CT with bone windows and reconstructions",
                "Complete neurological examination including cranial nerves",
                "Ophthalmologic examination if orbital involvement suspected",
                "Assess for concurrent cervical spine or intracranial injury",
                "Pain management and tetanus prophylaxis as indicated"
            ])
            
            # Specific recommendations based on positive criteria
            if parameters["diplopia"] == "yes":
                recommendations.append("Urgent ophthalmology consultation for diplopia evaluation")
            
            if parameters["malocclusion"] == "yes":
                recommendations.append("Oral and maxillofacial surgery consultation for dental occlusion")
            
            if parameters["facial_numbness"] == "yes":
                recommendations.append("Document extent and distribution of sensory deficits")
        
        return recommendations
    
    def _get_imaging_recommendations(self, positive_criteria: Dict[str, Any]) -> list:
        """Generates imaging-specific recommendations"""
        
        if positive_criteria["count"] == 0:
            return [
                "CT imaging not indicated by Wisconsin Criteria",
                "Consider plain radiographs only if specific clinical indication",
                "Reassess need for imaging if clinical status changes"
            ]
        else:
            return [
                "Facial CT with bone windows (1-3mm slice thickness)",
                "Coronal and sagittal reconstructions essential",
                "Include orbital, maxillary, and mandibular regions",
                "Consider CT angiography if vascular injury suspected",
                "Avoid plain radiographs - CT is preferred modality"
            ]
    
    def _get_consultation_recommendations(self, positive_criteria: Dict[str, Any], 
                                       parameters: Dict[str, str]) -> list:
        """Generates specialist consultation recommendations"""
        
        consultations = []
        
        if positive_criteria["count"] > 0:
            consultations.append("Oral and maxillofacial surgery for facial fracture management")
            
            if parameters["diplopia"] == "yes" or parameters["periorbital_swelling"] == "yes":
                consultations.append("Ophthalmology for orbital injury evaluation")
            
            if parameters["epistaxis"] == "yes":
                consultations.append("Otolaryngology for nasal/sinus injury assessment")
            
            if parameters["facial_deformity"] == "yes":
                consultations.append("Plastic surgery for soft tissue reconstruction")
        
        return consultations if consultations else ["No immediate specialist consultation required"]
    
    def _get_follow_up_recommendations(self, positive_criteria: Dict[str, Any]) -> list:
        """Generates follow-up care recommendations"""
        
        if positive_criteria["count"] == 0:
            return [
                "Follow up in 24-48 hours or sooner if symptoms worsen",
                "Return immediately for vision changes, severe pain, or numbness",
                "Primary care follow-up in 1 week for symptom resolution"
            ]
        else:
            return [
                "Close follow-up with treating specialist within 1-2 days",
                "Monitor for complications (infection, nerve dysfunction)",
                "Long-term follow-up for functional and aesthetic outcomes",
                "Consider physical therapy for TMJ dysfunction if present"
            ]
    
    def _get_patient_education_points(self, positive_criteria: Dict[str, Any]) -> list:
        """Generates patient education recommendations"""
        
        education = [
            "Apply ice for 15-20 minutes every hour for first 24 hours",
            "Take pain medications as prescribed",
            "Avoid hard or chewy foods",
            "Sleep with head elevated to reduce swelling"
        ]
        
        if positive_criteria["count"] > 0:
            education.extend([
                "Follow up with specialists as recommended",
                "Report any vision changes immediately",
                "Monitor for signs of infection (fever, increased pain)",
                "Expect some swelling and bruising for 1-2 weeks"
            ])
        else:
            education.extend([
                "Symptoms should improve over 3-5 days",
                "Return if pain worsens or new symptoms develop",
                "Most minor facial injuries heal without complications"
            ])
        
        return education


def calculate_wisconsin_criteria_maxillofacial_trauma(high_energy_mechanism, facial_deformity, malocclusion,
                                                    facial_numbness, periorbital_swelling, diplopia,
                                                    palpable_step_off, epistaxis) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_wisconsin_criteria_maxillofacial_trauma pattern
    """
    calculator = WisconsinCriteriaMaxillofacialTraumaCalculator()
    return calculator.calculate(
        high_energy_mechanism, facial_deformity, malocclusion, facial_numbness,
        periorbital_swelling, diplopia, palpable_step_off, epistaxis
    )