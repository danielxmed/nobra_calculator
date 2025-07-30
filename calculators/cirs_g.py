"""
Cumulative Illness Rating Scale-Geriatric (CIRS-G) Calculator

Quantifies burden of illness in elderly patients by systematically rating the severity 
of medical conditions across multiple organ systems.

References:
- Miller MD, Paradis CF, Houck PR, et al. Psychiatry Res. 1992;41(3):237-248.
- Linn BS, Linn MW, Gurel L. J Am Geriatr Soc. 1968;16(5):622-626.
- Salvi F, Miller MD, Grilli A, et al. J Am Geriatr Soc. 2008;56(10):1926-1931.
"""

from typing import Dict, Any


class CirsGCalculator:
    """Calculator for Cumulative Illness Rating Scale-Geriatric (CIRS-G)"""
    
    def __init__(self):
        # Organ system names for reference
        self.ORGAN_SYSTEMS = [
            "heart", "vascular", "hematopoietic", "respiratory", "eent",
            "upper_gi", "lower_gi", "liver_pancreas_biliary", "renal",
            "genitourinary", "musculoskeletal_skin", "neurologic", "endocrine_breast"
        ]
        
        # Severity level descriptions
        self.SEVERITY_LEVELS = {
            0: {"label": "No problem", "description": "No disease or symptoms in this organ system"},
            1: {"label": "Mild", "description": "Mild disease with minimal symptoms or well-controlled conditions"},
            2: {"label": "Moderate", "description": "Moderate disease requiring ongoing management, some functional limitation"},
            3: {"label": "Severe", "description": "Severe disease significantly impacting daily activities"},
            4: {"label": "Extremely severe", "description": "Life-threatening condition or end-stage disease"}
        }
    
    def calculate(self, heart: int, vascular: int, hematopoietic: int, respiratory: int,
                  eent: int, upper_gi: int, lower_gi: int, liver_pancreas_biliary: int,
                  renal: int, genitourinary: int, musculoskeletal_skin: int,
                  neurologic: int, endocrine_breast: int) -> Dict[str, Any]:
        """
        Calculates CIRS-G assessment and indices
        
        Args:
            heart (int): Heart system score (0-4)
            vascular (int): Vascular system score (0-4)
            hematopoietic (int): Blood/lymphatic system score (0-4)
            respiratory (int): Respiratory system score (0-4)
            eent (int): Eyes, ears, nose, throat score (0-4)
            upper_gi (int): Upper GI system score (0-4)
            lower_gi (int): Lower GI system score (0-4)
            liver_pancreas_biliary (int): Hepatobiliary system score (0-4)
            renal (int): Renal system score (0-4)
            genitourinary (int): Genitourinary system score (0-4)
            musculoskeletal_skin (int): Musculoskeletal/skin score (0-4)
            neurologic (int): Neurologic system score (0-4)
            endocrine_breast (int): Endocrine/breast system score (0-4)
            
        Returns:
            Dict with total score, indices, and detailed analysis
        """
        
        # Collect all scores
        scores = [
            heart, vascular, hematopoietic, respiratory, eent,
            upper_gi, lower_gi, liver_pancreas_biliary, renal,
            genitourinary, musculoskeletal_skin, neurologic, endocrine_breast
        ]
        
        # Validations
        self._validate_inputs(scores)
        
        # Calculate indices
        total_score = self._calculate_total_score(scores)
        severity_index = self._calculate_severity_index(scores)
        comorbidity_index = self._calculate_comorbidity_index(scores)
        
        # Get burden category
        burden_category = self._get_burden_category(total_score)
        
        # Generate system analysis
        system_analysis = self._analyze_organ_systems(scores)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(total_score, severity_index, comorbidity_index)
        
        # Get clinical recommendations
        recommendations = self._get_clinical_recommendations(total_score, comorbidity_index, scores)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation,
            "stage": burden_category["stage"],
            "stage_description": burden_category["description"],
            "total_score": total_score,
            "severity_index": round(severity_index, 2),
            "comorbidity_index": comorbidity_index,
            "affected_systems": system_analysis["affected_count"],
            "severe_systems": system_analysis["severe_count"],
            "system_breakdown": system_analysis["breakdown"],
            "burden_assessment": burden_category,
            "clinical_recommendations": recommendations,
            "prognosis_indicators": self._get_prognosis_indicators(total_score, comorbidity_index),
            "care_complexity": self._assess_care_complexity(total_score, comorbidity_index)
        }
    
    def _validate_inputs(self, scores):
        """Validates input parameters"""
        
        if len(scores) != 13:
            raise ValueError("Exactly 13 organ system scores must be provided")
        
        for i, score in enumerate(scores):
            if not isinstance(score, int) or not 0 <= score <= 4:
                system_name = self.ORGAN_SYSTEMS[i] if i < len(self.ORGAN_SYSTEMS) else f"System {i+1}"
                raise ValueError(f"{system_name} score must be an integer between 0 and 4")
    
    def _calculate_total_score(self, scores):
        """Calculates total CIRS-G score"""
        return sum(scores)
    
    def _calculate_severity_index(self, scores):
        """Calculates severity index (total score / number of affected systems)"""
        affected_systems = sum(1 for score in scores if score > 0)
        
        if affected_systems == 0:
            return 0.0
        
        return sum(scores) / affected_systems
    
    def _calculate_comorbidity_index(self, scores):
        """Calculates comorbidity index (number of systems with score ≥ 3)"""
        return sum(1 for score in scores if score >= 3)
    
    def _analyze_organ_systems(self, scores):
        """Analyzes organ system involvement"""
        
        affected_count = sum(1 for score in scores if score > 0)
        severe_count = sum(1 for score in scores if score >= 3)
        
        breakdown = []
        for i, score in enumerate(scores):
            if score > 0:
                system_name = self.ORGAN_SYSTEMS[i].replace("_", " ").title()
                severity = self.SEVERITY_LEVELS[score]
                breakdown.append({
                    "system": system_name,
                    "score": score,
                    "severity": severity["label"],
                    "description": severity["description"]
                })
        
        return {
            "affected_count": affected_count,
            "severe_count": severe_count,
            "breakdown": breakdown
        }
    
    def _get_burden_category(self, total_score):
        """Determines burden category based on total score"""
        
        if total_score <= 6:
            return {
                "stage": "Low Burden",
                "description": "Minimal illness burden",
                "risk_level": "low"
            }
        elif total_score <= 12:
            return {
                "stage": "Mild Burden", 
                "description": "Mild illness burden",
                "risk_level": "mild"
            }
        elif total_score <= 20:
            return {
                "stage": "Moderate Burden",
                "description": "Moderate illness burden", 
                "risk_level": "moderate"
            }
        elif total_score <= 30:
            return {
                "stage": "High Burden",
                "description": "High illness burden",
                "risk_level": "high"
            }
        else:
            return {
                "stage": "Very High Burden",
                "description": "Very high illness burden",
                "risk_level": "very_high"
            }
    
    def _get_interpretation(self, total_score, severity_index, comorbidity_index):
        """Get comprehensive clinical interpretation"""
        
        burden_category = self._get_burden_category(total_score)
        
        if total_score <= 6:
            return (f"CIRS-G total score of {total_score} indicates minimal illness burden. "
                   f"Patient has good overall health status with few or mild medical conditions. "
                   f"Prognosis is generally favorable with low risk of adverse outcomes.")
        
        elif total_score <= 12:
            return (f"CIRS-G total score of {total_score} indicates mild illness burden. "
                   f"Patient has some health conditions but generally well-managed. "
                   f"Severity index of {severity_index:.2f} suggests conditions are on average mild to moderate. "
                   f"Overall prognosis remains good with appropriate medical management.")
        
        elif total_score <= 20:
            return (f"CIRS-G total score of {total_score} indicates moderate illness burden. "
                   f"Patient has multiple health conditions or more severe single conditions. "
                   f"With {comorbidity_index} severe conditions (score ≥3), comprehensive care coordination is important. "
                   f"May impact daily activities and require regular medical follow-up.")
        
        elif total_score <= 30:
            return (f"CIRS-G total score of {total_score} indicates high illness burden. "
                   f"Patient has multiple severe conditions with {comorbidity_index} systems scored as severe or extremely severe. "
                   f"Significant impact on function and quality of life expected. "
                   f"Requires intensive medical management and multidisciplinary care approach.")
        
        else:
            return (f"CIRS-G total score of {total_score} indicates very high illness burden. "
                   f"Patient has extensive comorbidities with {comorbidity_index} severely affected systems. "
                   f"May indicate poor prognosis and need for intensive medical management. "
                   f"Consider palliative care consultation and advance care planning.")
    
    def _get_clinical_recommendations(self, total_score, comorbidity_index, scores):
        """Get clinical recommendations based on CIRS-G assessment"""
        
        recommendations = []
        
        if total_score <= 6:
            recommendations.extend([
                "Focus on preventive care and health maintenance",
                "Annual comprehensive health assessments",
                "Encourage healthy lifestyle and activity",
                "Monitor for early signs of disease progression"
            ])
        
        elif total_score <= 12:
            recommendations.extend([
                "Regular monitoring of existing conditions",
                "Optimize management of chronic diseases",
                "Consider comprehensive geriatric assessment",
                "Coordinate care between specialties as needed"
            ])
        
        elif total_score <= 20:
            recommendations.extend([
                "Comprehensive geriatric assessment recommended",
                "Multidisciplinary care team coordination",
                "Regular reassessment of disease burden",
                "Consider medication review and optimization"
            ])
        
        elif total_score <= 30:
            recommendations.extend([
                "Intensive medical management required",
                "Multidisciplinary team approach essential",
                "Frequent monitoring and reassessment",
                "Consider geriatric or palliative care consultation"
            ])
        
        else:
            recommendations.extend([
                "Intensive multidisciplinary care required",
                "Consider palliative care consultation",
                "Advance care planning discussions",
                "Focus on comfort and quality of life"
            ])
        
        # Add specific recommendations based on severe systems
        if comorbidity_index >= 3:
            recommendations.append("Multiple severe conditions require specialized care coordination")
        
        # Check for specific high-risk combinations
        if scores[0] >= 3 and scores[3] >= 3:  # Heart and respiratory
            recommendations.append("Cardiopulmonary conditions require close monitoring")
        
        if scores[11] >= 3:  # Neurologic
            recommendations.append("Neurologic conditions may require specialized rehabilitation")
        
        return recommendations
    
    def _get_prognosis_indicators(self, total_score, comorbidity_index):
        """Get prognosis indicators based on CIRS-G scores"""
        
        if total_score <= 6:
            return {
                "mortality_risk": "Low",
                "functional_decline_risk": "Low", 
                "hospitalization_risk": "Low",
                "care_needs": "Minimal"
            }
        elif total_score <= 12:
            return {
                "mortality_risk": "Low to Moderate",
                "functional_decline_risk": "Low to Moderate",
                "hospitalization_risk": "Moderate", 
                "care_needs": "Basic to Moderate"
            }
        elif total_score <= 20:
            return {
                "mortality_risk": "Moderate",
                "functional_decline_risk": "Moderate",
                "hospitalization_risk": "Moderate to High",
                "care_needs": "Moderate to High"
            }
        elif total_score <= 30:
            return {
                "mortality_risk": "High",
                "functional_decline_risk": "High",
                "hospitalization_risk": "High",
                "care_needs": "High"
            }
        else:
            return {
                "mortality_risk": "Very High",
                "functional_decline_risk": "Very High", 
                "hospitalization_risk": "Very High",
                "care_needs": "Very High"
            }
    
    def _assess_care_complexity(self, total_score, comorbidity_index):
        """Assess care complexity based on CIRS-G findings"""
        
        if total_score <= 6 and comorbidity_index == 0:
            return {
                "complexity_level": "Low",
                "care_setting": "Outpatient primary care",
                "specialist_needs": "Minimal",
                "coordination_requirements": "Basic"
            }
        elif total_score <= 12 and comorbidity_index <= 1:
            return {
                "complexity_level": "Moderate",
                "care_setting": "Outpatient with specialist involvement",
                "specialist_needs": "Limited",
                "coordination_requirements": "Moderate"
            }
        elif total_score <= 20 and comorbidity_index <= 2:
            return {
                "complexity_level": "High",
                "care_setting": "Multidisciplinary outpatient care",
                "specialist_needs": "Multiple specialties",
                "coordination_requirements": "High"
            }
        else:
            return {
                "complexity_level": "Very High",
                "care_setting": "Intensive multidisciplinary care",
                "specialist_needs": "Multiple specialties with frequent visits",
                "coordination_requirements": "Very High"
            }


def calculate_cirs_g(heart: int, vascular: int, hematopoietic: int, respiratory: int,
                     eent: int, upper_gi: int, lower_gi: int, liver_pancreas_biliary: int,
                     renal: int, genitourinary: int, musculoskeletal_skin: int,
                     neurologic: int, endocrine_breast: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CirsGCalculator()
    return calculator.calculate(
        heart, vascular, hematopoietic, respiratory, eent,
        upper_gi, lower_gi, liver_pancreas_biliary, renal,
        genitourinary, musculoskeletal_skin, neurologic, endocrine_breast
    )