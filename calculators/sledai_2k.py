"""
Systemic Lupus Erythematosus Disease Activity Index 2000 (SLEDAI-2K) Calculator

Stratifies severity of SLE based on 24 clinical and laboratory parameters.
Based on the Journal of Rheumatology 2002 publication.

References:
1. Gladman DD, Ibañez D, Urowitz MB. Systemic lupus erythematosus disease 
   activity index 2000. J Rheumatol. 2002;29(2):288-91.
"""

from typing import Dict, Any


class Sledai2kCalculator:
    """Calculator for SLEDAI-2K"""
    
    def __init__(self):
        # Point values for each parameter
        self.scoring = {
            # CNS and vascular (8 points each)
            "seizure": 8,
            "psychosis": 8,
            "organic_brain_syndrome": 8,
            "visual_disturbance": 8,
            "cranial_nerve_disorder": 8,
            "lupus_headache": 8,
            "cva": 8,
            "vasculitis": 8,
            # Musculoskeletal and renal (4 points each)
            "arthritis": 4,
            "myositis": 4,
            "urinary_casts": 4,
            "hematuria": 4,
            "proteinuria": 4,
            "pyuria": 4,
            # Dermatologic and serositis (2 points each)
            "rash": 2,
            "alopecia": 2,
            "mucosal_ulcers": 2,
            "pleurisy": 2,
            "pericarditis": 2,
            # Immunologic (2 points each)
            "low_complement": 2,
            "increased_dna_binding": 2,
            # Constitutional and hematologic (1 point each)
            "fever": 1,
            "thrombocytopenia": 1,
            "leukopenia": 1
        }
    
    def calculate(self, seizure: str, psychosis: str, organic_brain_syndrome: str,
                  visual_disturbance: str, cranial_nerve_disorder: str, lupus_headache: str,
                  cva: str, vasculitis: str, arthritis: str, myositis: str,
                  urinary_casts: str, hematuria: str, proteinuria: str, pyuria: str,
                  rash: str, alopecia: str, mucosal_ulcers: str, pleurisy: str,
                  pericarditis: str, low_complement: str, increased_dna_binding: str,
                  fever: str, thrombocytopenia: str, leukopenia: str) -> Dict[str, Any]:
        """
        Calculates SLEDAI-2K score
        
        Args:
            All parameters are "yes" or "no" strings indicating presence of each feature
            
        Returns:
            Dict with total score and interpretation
        """
        
        # Create parameter dictionary
        parameters = {
            "seizure": seizure,
            "psychosis": psychosis,
            "organic_brain_syndrome": organic_brain_syndrome,
            "visual_disturbance": visual_disturbance,
            "cranial_nerve_disorder": cranial_nerve_disorder,
            "lupus_headache": lupus_headache,
            "cva": cva,
            "vasculitis": vasculitis,
            "arthritis": arthritis,
            "myositis": myositis,
            "urinary_casts": urinary_casts,
            "hematuria": hematuria,
            "proteinuria": proteinuria,
            "pyuria": pyuria,
            "rash": rash,
            "alopecia": alopecia,
            "mucosal_ulcers": mucosal_ulcers,
            "pleurisy": pleurisy,
            "pericarditis": pericarditis,
            "low_complement": low_complement,
            "increased_dna_binding": increased_dna_binding,
            "fever": fever,
            "thrombocytopenia": thrombocytopenia,
            "leukopenia": leukopenia
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate total score
        total_score = 0
        present_features = []
        
        for param, value in parameters.items():
            if value == "yes":
                points = self.scoring[param]
                total_score += points
                present_features.append(f"{param.replace('_', ' ').title()} ({points} points)")
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        result = {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
        
        # Add present features if any
        if present_features:
            result["present_features"] = ", ".join(present_features)
        
        return result
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates all input parameters"""
        
        for param, value in parameters.items():
            if value not in ["yes", "no"]:
                raise ValueError(f"{param} must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines interpretation based on total score
        
        Cut-offs:
        - 0-2: No activity
        - 3-4: Mild activity (threshold for active disease)
        - 5-10: Moderate activity
        - 11-19: High activity
        - ≥20: Very high activity
        """
        
        if score <= 2:
            return {
                "stage": "No Activity",
                "description": "No disease activity",
                "interpretation": "No active disease. Continue routine monitoring and current management."
            }
        elif score <= 4:
            return {
                "stage": "Mild Activity",
                "description": "Mild disease activity",
                "interpretation": "Mild disease activity. Consider treatment adjustment if symptoms are bothersome or if there is organ involvement."
            }
        elif score <= 10:
            return {
                "stage": "Moderate Activity",
                "description": "Moderate disease activity",
                "interpretation": "Moderate disease activity. Treatment modification usually indicated. Consider increasing immunosuppression."
            }
        elif score <= 19:
            return {
                "stage": "High Activity",
                "description": "High disease activity",
                "interpretation": "High disease activity. Significant treatment intensification needed. Consider aggressive immunosuppression."
            }
        else:
            return {
                "stage": "Very High Activity",
                "description": "Very high disease activity",
                "interpretation": "Very high disease activity. Urgent aggressive treatment required. Consider hospitalization and high-dose immunosuppression."
            }


def calculate_sledai_2k(seizure, psychosis, organic_brain_syndrome,
                       visual_disturbance, cranial_nerve_disorder, lupus_headache,
                       cva, vasculitis, arthritis, myositis,
                       urinary_casts, hematuria, proteinuria, pyuria,
                       rash, alopecia, mucosal_ulcers, pleurisy,
                       pericarditis, low_complement, increased_dna_binding,
                       fever, thrombocytopenia, leukopenia) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    """
    calculator = Sledai2kCalculator()
    return calculator.calculate(
        seizure, psychosis, organic_brain_syndrome,
        visual_disturbance, cranial_nerve_disorder, lupus_headache,
        cva, vasculitis, arthritis, myositis,
        urinary_casts, hematuria, proteinuria, pyuria,
        rash, alopecia, mucosal_ulcers, pleurisy,
        pericarditis, low_complement, increased_dna_binding,
        fever, thrombocytopenia, leukopenia
    )