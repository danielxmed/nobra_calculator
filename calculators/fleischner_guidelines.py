"""
Fleischner Society Guidelines for Incidental Pulmonary Nodules Calculator

Provides follow-up recommendations for incidentally detected pulmonary nodules on CT.

References:
- MacMahon H, et al. Radiology. 2017;284(1):228-243.
- Bankier AA, et al. Radiology. 2017;285(2):584-600.
"""

from typing import Dict, Any, Optional


class FleischnerGuidelinesCalculator:
    """Calculator for Fleischner Society Guidelines for Pulmonary Nodules"""
    
    def __init__(self):
        # Define follow-up recommendations based on 2017 guidelines
        # Structure: nodule_type -> number -> size -> risk -> recommendation
        self.RECOMMENDATIONS = {
            "solid": {
                "single": {
                    "less_than_6mm": {
                        "low": "No routine follow-up",
                        "high": "Optional CT at 12 months"
                    },
                    "6_to_8mm": {
                        "low": "CT at 6-12 months, then consider CT at 18-24 months",
                        "high": "CT at 6-12 months, then CT at 18-24 months"
                    },
                    "greater_than_8mm": {
                        "low": "Consider CT at 3 months, PET/CT, or tissue sampling",
                        "high": "Consider CT at 3 months, PET/CT, or tissue sampling"
                    }
                },
                "multiple": {
                    "less_than_6mm": {
                        "low": "No routine follow-up",
                        "high": "Optional CT at 12 months"
                    },
                    "6_to_8mm": {
                        "low": "CT at 3-6 months, then consider CT at 18-24 months",
                        "high": "CT at 3-6 months, then consider CT at 18-24 months"
                    },
                    "greater_than_8mm": {
                        "low": "CT at 3-6 months, then consider CT at 18-24 months",
                        "high": "CT at 3-6 months, then consider CT at 18-24 months"
                    }
                }
            },
            "subsolid": {
                "single": {
                    "less_than_6mm": {
                        "low": "No routine follow-up",
                        "high": "No routine follow-up"
                    },
                    "6_to_8mm": {
                        "low": "CT at 6-12 months to confirm persistence, then CT every 2 years until 5 years",
                        "high": "CT at 6-12 months to confirm persistence, then CT every 2 years until 5 years"
                    },
                    "greater_than_8mm": {
                        "low": "CT at 6-12 months to confirm persistence, then CT every 2 years until 5 years",
                        "high": "CT at 6-12 months to confirm persistence, then CT every 2 years until 5 years"
                    }
                },
                "multiple": {
                    "less_than_6mm": {
                        "low": "CT at 3-6 months. If stable, consider CT at 2 and 4 years",
                        "high": "CT at 3-6 months. If stable, consider CT at 2 and 4 years"
                    },
                    "6_to_8mm": {
                        "low": "CT at 3-6 months. Subsequent management based on most suspicious nodule",
                        "high": "CT at 3-6 months. Subsequent management based on most suspicious nodule"
                    },
                    "greater_than_8mm": {
                        "low": "CT at 3-6 months. Subsequent management based on most suspicious nodule",
                        "high": "CT at 3-6 months. Subsequent management based on most suspicious nodule"
                    }
                }
            }
        }
        
        # Special considerations for part-solid nodules
        self.PART_SOLID_NOTES = {
            "6_to_8mm": "For part-solid nodules with solid component <6mm, follow subsolid guidelines",
            "greater_than_8mm": "For part-solid nodules with solid component ≥6mm, consider PET/CT or tissue sampling"
        }
    
    def calculate(self, nodule_type: str, nodule_number: str, size_category: str, 
                 risk_level: str, subsolid_features: Optional[str] = None) -> Dict[str, Any]:
        """
        Determines follow-up recommendation based on Fleischner Guidelines
        
        Args:
            nodule_type: Type of nodule (solid, subsolid)
            nodule_number: Number of nodules (single, multiple)
            size_category: Size category (less_than_6mm, 6_to_8mm, greater_than_8mm)
            risk_level: Patient risk level (low, high)
            subsolid_features: Features if subsolid (ground_glass, part_solid)
            
        Returns:
            Dict with recommendation and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(nodule_type, nodule_number, size_category, risk_level, subsolid_features)
        
        # Get base recommendation
        recommendation = self.RECOMMENDATIONS[nodule_type][nodule_number][size_category][risk_level]
        
        # Add special considerations for part-solid nodules
        additional_info = ""
        if nodule_type == "subsolid" and subsolid_features == "part_solid":
            if size_category in self.PART_SOLID_NOTES:
                additional_info = f" {self.PART_SOLID_NOTES[size_category]}"
        
        # Build interpretation
        interpretation = self._build_interpretation(nodule_type, nodule_number, 
                                                  size_category, risk_level, 
                                                  recommendation, additional_info)
        
        return {
            "result": recommendation,
            "unit": "",
            "interpretation": interpretation,
            "stage": self._get_stage_description(nodule_type, size_category, risk_level),
            "stage_description": f"{nodule_type.capitalize()} nodule, {size_category.replace('_', ' ')}"
        }
    
    def _validate_inputs(self, nodule_type: str, nodule_number: str, size_category: str,
                        risk_level: str, subsolid_features: Optional[str]):
        """Validates input parameters"""
        
        valid_nodule_types = ["solid", "subsolid"]
        if nodule_type not in valid_nodule_types:
            raise ValueError(f"Invalid nodule type. Must be one of: {valid_nodule_types}")
        
        valid_numbers = ["single", "multiple"]
        if nodule_number not in valid_numbers:
            raise ValueError(f"Invalid nodule number. Must be one of: {valid_numbers}")
        
        valid_sizes = ["less_than_6mm", "6_to_8mm", "greater_than_8mm"]
        if size_category not in valid_sizes:
            raise ValueError(f"Invalid size category. Must be one of: {valid_sizes}")
        
        valid_risks = ["low", "high"]
        if risk_level not in valid_risks:
            raise ValueError(f"Invalid risk level. Must be one of: {valid_risks}")
        
        if nodule_type == "subsolid" and subsolid_features:
            valid_features = ["ground_glass", "part_solid"]
            if subsolid_features not in valid_features:
                raise ValueError(f"Invalid subsolid features. Must be one of: {valid_features}")
    
    def _build_interpretation(self, nodule_type: str, nodule_number: str, 
                            size_category: str, risk_level: str, 
                            recommendation: str, additional_info: str) -> str:
        """Builds detailed interpretation"""
        
        # Format size for display
        size_display = size_category.replace("_", " ").replace("mm", " mm")
        
        # Build risk factors description
        risk_desc = "low risk (minimal/no smoking, no other risk factors)" if risk_level == "low" else \
                   "high risk (heavy smoking, family history, suspicious features)"
        
        # Build base interpretation
        interpretation = f"For {nodule_number} {nodule_type} nodule(s) {size_display} in {risk_desc} patient: {recommendation}."
        
        # Add additional information if present
        if additional_info:
            interpretation += additional_info
        
        # Add general notes
        if size_category == "greater_than_8mm":
            interpretation += " Consider multidisciplinary discussion for optimal management."
        
        return interpretation
    
    def _get_stage_description(self, nodule_type: str, size_category: str, risk_level: str) -> str:
        """Gets concise stage description"""
        
        if size_category == "less_than_6mm" and risk_level == "low":
            return "Low risk - No follow-up"
        elif size_category == "less_than_6mm" and risk_level == "high":
            return "Low risk - Optional follow-up"
        elif size_category == "6_to_8mm":
            return "Intermediate risk - Follow-up recommended"
        else:  # greater_than_8mm
            return "High risk - Active management"


def calculate_fleischner_guidelines(nodule_type: str, nodule_number: str, 
                                  size_category: str, risk_level: str,
                                  subsolid_features: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_fleischner_guidelines pattern
    """
    calculator = FleischnerGuidelinesCalculator()
    return calculator.calculate(nodule_type, nodule_number, size_category, 
                              risk_level, subsolid_features)