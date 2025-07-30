"""
Bush-Francis Catatonia Rating Scale Calculator

Assesses severity of catatonia and screens for catatonia in psychiatric and neurological conditions.
The BFCRS is considered the gold standard for clinical and research purposes for catatonia screening and diagnosis.

References:
1. Bush G, Fink M, Petrides G, Dowling F, Francis A. Catatonia. I. Rating scale and standardized examination. 
   Acta Psychiatr Scand. 1996;93(2):129-36.
2. Bush G, Fink M, Petrides G, Dowling F, Francis A. Catatonia. II. Treatment with lorazepam and 
   electroconvulsive therapy. Acta Psychiatr Scand. 1996;93(2):137-143.
"""

from typing import Dict, Any, List


class BushFrancisCatatoniaRatingScaleCalculator:
    """Calculator for Bush-Francis Catatonia Rating Scale"""
    
    def __init__(self):
        # Define items that are scored as 0 or 3 only (binary items)
        self.binary_items = {
            'withdrawal',  # Item 13
            'passive_obedience',  # Item 17 (Mitgehen)
            'muscle_resistance',  # Item 18 (Gegenhalten)
            'motorically_stuck',  # Item 19 (Ambitendency)
            'grasp_reflex',  # Item 20
            'perseveration'  # Item 21
        }
        
        # Define screening items (first 14)
        self.screening_items = [
            'excitement', 'immobility_stupor', 'mutism', 'staring',
            'posturing_catalepsy', 'grimacing', 'echopraxia_echolalia',
            'stereotypy', 'mannerisms', 'verbigeration', 'rigidity',
            'negativism', 'waxy_flexibility', 'withdrawal'
        ]
        
        # Define additional items (15-23)
        self.additional_items = [
            'impulsivity', 'automatic_obedience', 'passive_obedience',
            'muscle_resistance', 'motorically_stuck', 'grasp_reflex',
            'perseveration', 'combativeness', 'autonomic_abnormality'
        ]
    
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Calculates the Bush-Francis Catatonia Rating Scale score
        
        Args:
            **kwargs: Item scores as keyword arguments (e.g., excitement=2, mutism=1, etc.)
            
        Returns:
            Dict with total score, screening result, item breakdown, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(**kwargs)
        
        # Calculate screening score
        screening_score = self._calculate_screening_score(**kwargs)
        positive_screening_items = self._count_positive_screening_items(**kwargs)
        
        # Determine if screening is positive
        screening_positive = positive_screening_items >= 2
        
        # Calculate total score if all items are provided
        total_score = self._calculate_total_score(**kwargs)
        
        # Get interpretation
        interpretation = self._get_interpretation(screening_positive, total_score)
        
        # Get item breakdown
        item_breakdown = self._get_item_breakdown(**kwargs)
        
        # Get clinical recommendations
        recommendations = self._get_clinical_recommendations(
            screening_positive, total_score, kwargs.get('autonomic_abnormality', 0)
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "screening_score": screening_score,
            "screening_positive": screening_positive,
            "positive_screening_items": positive_screening_items,
            "item_breakdown": item_breakdown,
            "clinical_recommendations": recommendations
        }
    
    def _validate_inputs(self, **kwargs):
        """Validates input parameters"""
        
        # Check that at least screening items are provided
        provided_screening_items = [item for item in self.screening_items if item in kwargs]
        if len(provided_screening_items) < 14:
            missing = [item for item in self.screening_items if item not in kwargs]
            raise ValueError(f"All 14 screening items must be provided. Missing: {', '.join(missing)}")
        
        # Validate each provided item
        for item, score in kwargs.items():
            if not isinstance(score, (int, float)):
                raise ValueError(f"{item} must be a number")
            
            score = int(score)
            
            # Check range
            if score < 0 or score > 3:
                raise ValueError(f"{item} must be between 0 and 3")
            
            # Check binary items
            if item in self.binary_items and score not in [0, 3]:
                raise ValueError(f"{item} must be either 0 (absent) or 3 (present)")
    
    def _calculate_screening_score(self, **kwargs) -> int:
        """Calculates the screening instrument score (first 14 items)"""
        
        score = 0
        for item in self.screening_items:
            if item in kwargs:
                score += kwargs[item]
        
        return score
    
    def _count_positive_screening_items(self, **kwargs) -> int:
        """Counts how many screening items are positive (score >= 1)"""
        
        count = 0
        for item in self.screening_items:
            if item in kwargs and kwargs[item] >= 1:
                count += 1
        
        return count
    
    def _calculate_total_score(self, **kwargs) -> int:
        """Calculates the total BFCRS score (all 23 items)"""
        
        total = 0
        
        # Add screening items
        for item in self.screening_items:
            if item in kwargs:
                total += kwargs[item]
        
        # Add additional items if provided
        for item in self.additional_items:
            if item in kwargs:
                total += kwargs[item]
        
        return total
    
    def _get_interpretation(self, screening_positive: bool, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on screening result and total score
        
        Args:
            screening_positive (bool): Whether screening is positive
            total_score (int): Total BFCRS score
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if not screening_positive:
            return {
                "stage": "Negative Screen",
                "description": "Catatonia unlikely",
                "interpretation": (
                    "Less than 2 items positive in screening instrument. Catatonia is unlikely. "
                    "Consider other diagnoses or re-evaluate if clinical suspicion remains high."
                )
            }
        else:
            severity = self._get_severity_description(total_score)
            return {
                "stage": "Positive Screen",
                "description": f"Catatonia likely present - {severity}",
                "interpretation": (
                    f"Two or more items positive in screening instrument indicates positive screening "
                    f"for catatonia. Total score: {total_score}/69. {severity}. "
                    f"Complete full 23-item assessment if not already done. Consider immediate treatment, "
                    f"particularly if autonomic instability is present. Benzodiazepine trial (lorazepam) "
                    f"is both diagnostic and therapeutic."
                )
            }
    
    def _get_severity_description(self, total_score: int) -> str:
        """Returns severity description based on total score"""
        
        if total_score < 10:
            return "Mild severity"
        elif total_score < 20:
            return "Moderate severity"
        elif total_score < 30:
            return "Severe catatonia"
        else:
            return "Very severe catatonia"
    
    def _get_item_breakdown(self, **kwargs) -> Dict[str, List[Dict[str, Any]]]:
        """
        Creates a breakdown of items by category
        
        Returns:
            Dict with screening and additional items breakdown
        """
        
        screening_breakdown = []
        for item in self.screening_items:
            if item in kwargs:
                screening_breakdown.append({
                    "item": item.replace('_', ' ').title(),
                    "score": kwargs[item],
                    "binary": item in self.binary_items
                })
        
        additional_breakdown = []
        for item in self.additional_items:
            if item in kwargs:
                additional_breakdown.append({
                    "item": item.replace('_', ' ').title(),
                    "score": kwargs[item],
                    "binary": item in self.binary_items
                })
        
        return {
            "screening_items": screening_breakdown,
            "additional_items": additional_breakdown
        }
    
    def _get_clinical_recommendations(self, screening_positive: bool, total_score: int, 
                                     autonomic_abnormality: int) -> Dict[str, List[str]]:
        """
        Provides clinical recommendations based on results
        
        Args:
            screening_positive (bool): Whether screening is positive
            total_score (int): Total BFCRS score
            autonomic_abnormality (int): Score for autonomic abnormality item
            
        Returns:
            Dict with categorized recommendations
        """
        
        recommendations = {
            "immediate_actions": [],
            "diagnostic": [],
            "treatment": [],
            "monitoring": []
        }
        
        if not screening_positive:
            recommendations["diagnostic"] = [
                "Continue to monitor for catatonic signs if clinical suspicion exists",
                "Consider other diagnoses (depression with psychomotor symptoms, parkinsonism, etc.)",
                "Re-evaluate if symptoms change or worsen"
            ]
        else:
            # Immediate actions
            recommendations["immediate_actions"] = [
                "Complete full 23-item BFCRS assessment if not already done",
                "Medical workup to identify underlying causes",
                "Assess for malignant catatonia (fever, autonomic instability)"
            ]
            
            # Diagnostic recommendations
            recommendations["diagnostic"] = [
                "Lorazepam challenge test (1-2mg IV/IM) - diagnostic and therapeutic",
                "CBC, CMP, TSH, B12, folate, urinalysis",
                "Consider brain imaging (CT/MRI) if first episode or focal findings",
                "EEG if seizure activity suspected",
                "Review medications for potential causative agents"
            ]
            
            # Treatment recommendations
            if total_score >= 20 or autonomic_abnormality >= 1:
                recommendations["treatment"] = [
                    "URGENT: Consider intensive care setting if autonomic instability present",
                    "Lorazepam 2mg IM/IV q8h, titrate to effect (up to 16-24mg/day)",
                    "If no response to benzodiazepines within 48-72h, consider ECT",
                    "Discontinue antipsychotics if neuroleptic malignant syndrome suspected",
                    "Supportive care: hydration, nutrition, DVT prophylaxis"
                ]
            else:
                recommendations["treatment"] = [
                    "Lorazepam 1-2mg PO/IM/IV TID, titrate to response",
                    "Monitor response within 24-48 hours",
                    "Consider ECT if no response to adequate benzodiazepine trial",
                    "Address underlying psychiatric or medical condition",
                    "Ensure adequate nutrition and hydration"
                ]
            
            # Monitoring recommendations
            recommendations["monitoring"] = [
                "Re-assess with BFCRS daily during acute treatment",
                "Monitor vital signs closely, especially if autonomic symptoms present",
                "Watch for complications: aspiration, dehydration, rhabdomyolysis",
                "Document response to lorazepam challenge",
                "Consider continuous monitoring if malignant features present"
            ]
        
        return recommendations


def calculate_bush_francis_catatonia_rating_scale(**kwargs) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BushFrancisCatatoniaRatingScaleCalculator()
    return calculator.calculate(**kwargs)