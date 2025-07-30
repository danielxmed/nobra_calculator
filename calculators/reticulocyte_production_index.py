"""
Reticulocyte Production Index (RPI) Calculator

Assesses bone marrow response to anemia by correcting reticulocyte count for 
degree of anemia and maturation time.

References:
1. Koepke JA. Laboratory hematology practice. New York: Churchill Livingstone; 1989.
2. Hillman RS, Ault KA. Hematology in clinical practice. New York: McGraw-Hill; 2002.
3. Nathan DG, Orkin SH, Look AT, Ginsburg D. Nathan and Oski's Hematology of Infancy 
   and Childhood. 6th ed. Philadelphia: W.B. Saunders; 2003.
4. Bain BJ. Blood Cells: A Practical Guide. 4th ed. Oxford: Blackwell Publishing; 2006.
"""

from typing import Dict, Any, Optional


class ReticulocyteProductionIndexCalculator:
    """Calculator for Reticulocyte Production Index (RPI)"""
    
    def __init__(self):
        # Maturation factors based on hematocrit levels
        self.MATURATION_FACTORS = {
            "severe": {"min_hct": 0, "max_hct": 20, "factor": 2.5},
            "moderate": {"min_hct": 20, "max_hct": 25, "factor": 2.0},
            "mild": {"min_hct": 25, "max_hct": 35, "factor": 1.5},
            "normal": {"min_hct": 35, "max_hct": 100, "factor": 1.0}
        }
        
        # Normal RPI range
        self.NORMAL_RPI_MIN = 0.5
        self.NORMAL_RPI_MAX = 2.5
        
        # Clinical interpretation thresholds
        self.THRESHOLDS = {
            "very_low": 0.5,
            "inadequate": 2.0,
            "borderline": 3.0
        }
    
    def calculate(
        self,
        reticulocyte_percentage: float,
        measured_hematocrit: float,
        normal_hematocrit: float,
        rbc_count: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates the Reticulocyte Production Index (RPI)
        
        Args:
            reticulocyte_percentage: Reticulocyte percentage from lab report (%)
            measured_hematocrit: Patient's measured hematocrit (%)
            normal_hematocrit: Normal hematocrit reference value (%)
            rbc_count: Red blood cell count for absolute calculation (×10⁶/μL, optional)
            
        Returns:
            Dict with RPI value and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(reticulocyte_percentage, measured_hematocrit, normal_hematocrit, rbc_count)
        
        # Calculate corrected reticulocyte percentage
        corrected_reticulocyte = self._calculate_corrected_reticulocyte(
            reticulocyte_percentage, measured_hematocrit, normal_hematocrit
        )
        
        # Get maturation factor based on hematocrit
        maturation_factor = self._get_maturation_factor(measured_hematocrit)
        
        # Calculate RPI
        rpi_value = corrected_reticulocyte / maturation_factor["factor"]
        
        # Calculate absolute reticulocyte count if RBC count provided
        absolute_count = None
        if rbc_count is not None:
            absolute_count = self._calculate_absolute_reticulocyte_count(reticulocyte_percentage, rbc_count)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(rpi_value, measured_hematocrit)
        
        return {
            "result": round(rpi_value, 2),
            "unit": "index",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "calculation_details": {
                "reticulocyte_percentage": reticulocyte_percentage,
                "corrected_reticulocyte_percentage": round(corrected_reticulocyte, 2),
                "maturation_factor": maturation_factor["factor"],
                "maturation_level": maturation_factor["level"],
                "hematocrit_severity": self._assess_anemia_severity(measured_hematocrit),
                "absolute_reticulocyte_count": round(absolute_count, 0) if absolute_count else None,
                "bone_marrow_response": interpretation["bone_marrow_response"],
                "clinical_significance": interpretation["clinical_significance"]
            }
        }
    
    def _validate_inputs(
        self, 
        retic_pct: float, 
        measured_hct: float, 
        normal_hct: float, 
        rbc_count: Optional[float]
    ):
        """Validates input parameters"""
        
        # Validate reticulocyte percentage
        if not isinstance(retic_pct, (int, float)) or retic_pct < 0 or retic_pct > 50:
            raise ValueError("Reticulocyte percentage must be between 0 and 50%")
        
        # Validate measured hematocrit
        if not isinstance(measured_hct, (int, float)) or measured_hct < 5 or measured_hct > 65:
            raise ValueError("Measured hematocrit must be between 5 and 65%")
        
        # Validate normal hematocrit
        if not isinstance(normal_hct, (int, float)) or normal_hct < 35 or normal_hct > 50:
            raise ValueError("Normal hematocrit must be between 35 and 50%")
        
        # Validate RBC count if provided
        if rbc_count is not None:
            if not isinstance(rbc_count, (int, float)) or rbc_count < 1.0 or rbc_count > 8.0:
                raise ValueError("RBC count must be between 1.0 and 8.0 ×10⁶/μL")
    
    def _calculate_corrected_reticulocyte(
        self, 
        retic_pct: float, 
        measured_hct: float, 
        normal_hct: float
    ) -> float:
        """
        Calculates corrected reticulocyte percentage
        
        Args:
            retic_pct: Reticulocyte percentage
            measured_hct: Patient's hematocrit
            normal_hct: Normal hematocrit reference
            
        Returns:
            Corrected reticulocyte percentage
        """
        return retic_pct * (measured_hct / normal_hct)
    
    def _get_maturation_factor(self, hematocrit: float) -> Dict[str, Any]:
        """
        Determines maturation factor based on hematocrit level
        
        Args:
            hematocrit: Patient's hematocrit value
            
        Returns:
            Dict with maturation factor and severity level
        """
        
        for level, params in self.MATURATION_FACTORS.items():
            if params["min_hct"] <= hematocrit < params["max_hct"]:
                return {
                    "factor": params["factor"],
                    "level": level,
                    "description": f"Hematocrit {hematocrit}% - {level} anemia"
                }
        
        # Default to normal if outside ranges
        return {
            "factor": 1.0,
            "level": "normal",
            "description": f"Hematocrit {hematocrit}% - normal range"
        }
    
    def _calculate_absolute_reticulocyte_count(self, retic_pct: float, rbc_count: float) -> float:
        """
        Calculates absolute reticulocyte count
        
        Args:
            retic_pct: Reticulocyte percentage
            rbc_count: RBC count in ×10⁶/μL
            
        Returns:
            Absolute reticulocyte count in cells/μL
        """
        return (retic_pct / 100) * rbc_count * 1000000
    
    def _assess_anemia_severity(self, hematocrit: float) -> str:
        """
        Assesses anemia severity based on hematocrit
        
        Args:
            hematocrit: Patient's hematocrit value
            
        Returns:
            Anemia severity classification
        """
        
        if hematocrit >= 35:
            return "No anemia or mild anemia"
        elif hematocrit >= 25:
            return "Mild to moderate anemia"
        elif hematocrit >= 20:
            return "Moderate anemia"
        else:
            return "Severe anemia"
    
    def _get_interpretation(self, rpi_value: float, hematocrit: float) -> Dict[str, Any]:
        """
        Determines the interpretation based on RPI value and clinical context
        
        Args:
            rpi_value: Calculated RPI value
            hematocrit: Patient's hematocrit for context
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine stage based on RPI value
        if rpi_value < self.THRESHOLDS["very_low"]:
            stage = "Very Low Response"
            description = "Very decreased reticulocyte production"
            bone_marrow_response = "Severely impaired"
            clinical_significance = "Bone marrow failure or severe deficiency"
            
            interpretation = (
                f"RPI of {rpi_value:.2f} is <0.5, indicating very decreased reticulocyte "
                f"production. This suggests bone marrow failure, severe nutritional deficiency, "
                f"or other causes of impaired erythropoiesis requiring immediate evaluation."
            )
            
        elif rpi_value < self.THRESHOLDS["inadequate"]:
            stage = "Inadequate Response"
            description = "Inadequate bone marrow response"
            bone_marrow_response = "Impaired"
            clinical_significance = "Hypoproliferative anemia"
            
            interpretation = (
                f"RPI of {rpi_value:.2f} is <2.0, indicating inadequate bone marrow response "
                f"to anemia. This suggests hypoproliferative anemia due to bone marrow "
                f"dysfunction, nutritional deficiencies, chronic disease, or renal failure."
            )
            
        elif rpi_value < self.THRESHOLDS["borderline"]:
            stage = "Borderline Response"
            description = "Borderline bone marrow response"
            bone_marrow_response = "Borderline"
            clinical_significance = "Early recovery or mild dysfunction"
            
            interpretation = (
                f"RPI of {rpi_value:.2f} is borderline (2.0-3.0), indicating a marginal "
                f"bone marrow response. This may suggest early recovery from bone marrow "
                f"suppression, mild nutritional deficiency, or transition phase in treatment."
            )
            
        else:
            stage = "Appropriate Response"
            description = "Appropriate bone marrow response"
            bone_marrow_response = "Normal"
            clinical_significance = "Hemolytic or hemorrhagic anemia"
            
            interpretation = (
                f"RPI of {rpi_value:.2f} is >3.0, indicating appropriate bone marrow response "
                f"to anemia. This suggests hemolytic anemia, acute blood loss, or other causes "
                f"of increased red cell destruction with compensatory reticulocytosis."
            )
        
        # Add hematocrit context
        anemia_severity = self._assess_anemia_severity(hematocrit)
        interpretation += f" Patient has {anemia_severity.lower()} (Hct {hematocrit}%)."
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "bone_marrow_response": bone_marrow_response,
            "clinical_significance": clinical_significance
        }


def calculate_reticulocyte_production_index(
    reticulocyte_percentage: float,
    measured_hematocrit: float,
    normal_hematocrit: float,
    rbc_count: Optional[float] = None
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ReticulocyteProductionIndexCalculator()
    return calculator.calculate(
        reticulocyte_percentage=reticulocyte_percentage,
        measured_hematocrit=measured_hematocrit,
        normal_hematocrit=normal_hematocrit,
        rbc_count=rbc_count
    )