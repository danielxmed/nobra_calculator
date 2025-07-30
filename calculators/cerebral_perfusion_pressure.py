"""
Cerebral Perfusion Pressure Calculator

Calculates cerebral perfusion pressure (CPP), the net pressure gradient that drives 
oxygen delivery to cerebral tissue. Critical parameter in neurocritical care.

References:
1. Carney N, Totten AM, O'Reilly C, Ullman JS, Hawryluk GW, Bell MJ, et al. 
   Guidelines for the management of severe traumatic brain injury, fourth edition. 
   Neurosurgery. 2017;80(1):6-15. doi: 10.1227/NEU.0000000000001432.
2. Kirkman MA, Smith M. Intracranial pressure monitoring, cerebral perfusion 
   pressure estimation, and ICP/CPP-guided therapy: a standard of care or optional 
   extra after brain injury? Br J Anaesth. 2014;112(1):35-46. doi: 10.1093/bja/aet418.
3. Rosner MJ, Rosner SD, Johnson AH. Cerebral perfusion pressure: management 
   protocol and clinical results. J Neurosurg. 1995;83(6):949-62. 
   doi: 10.3171/jns.1995.83.6.0949.
"""

from typing import Dict, Any


class CerebralPerfusionPressureCalculator:
    """Calculator for Cerebral Perfusion Pressure"""
    
    def __init__(self):
        # Clinical interpretation ranges
        self.interpretation_ranges = [
            {
                "min": 0, "max": 30,
                "category": "Critical",
                "description": "Critically low cerebral perfusion",
                "risk_level": "Critical",
                "urgency": "Immediate intervention required"
            },
            {
                "min": 30, "max": 50,
                "category": "Severely Low",
                "description": "High risk of cerebral ischemia",
                "risk_level": "High Risk",
                "urgency": "Urgent intervention needed"
            },
            {
                "min": 50, "max": 60,
                "category": "Low",
                "description": "Below optimal range",
                "risk_level": "Moderate Risk",
                "urgency": "Consider interventions"
            },
            {
                "min": 60, "max": 80,
                "category": "Optimal",
                "description": "Target range for cerebral perfusion",
                "risk_level": "Low Risk",
                "urgency": "Maintain current management"
            },
            {
                "min": 80, "max": 100,
                "category": "Adequate",
                "description": "Adequate cerebral perfusion",
                "risk_level": "Low Risk",
                "urgency": "Monitor for complications"
            },
            {
                "min": 100, "max": 999,  # Upper limit set high for calculation
                "category": "High",
                "description": "Elevated cerebral perfusion pressure",
                "risk_level": "Moderate Risk",
                "urgency": "Balance perfusion with pressure management"
            }
        ]
    
    def calculate(
        self,
        mean_arterial_pressure: float,
        intracranial_pressure: float
    ) -> Dict[str, Any]:
        """
        Calculates cerebral perfusion pressure
        
        Args:
            mean_arterial_pressure: Mean arterial pressure in mmHg
            intracranial_pressure: Intracranial pressure in mmHg
            
        Returns:
            Dict with CPP value, interpretation, and management recommendations
        """
        
        # Validate inputs
        self._validate_inputs(mean_arterial_pressure, intracranial_pressure)
        
        # Calculate CPP
        cpp = mean_arterial_pressure - intracranial_pressure
        
        # Get clinical assessment
        assessment = self._get_clinical_assessment(cpp)
        
        # Get management recommendations
        management = self._get_management_recommendations(cpp, mean_arterial_pressure, intracranial_pressure)
        
        # Get detailed breakdown
        calculation_breakdown = self._get_calculation_breakdown(
            mean_arterial_pressure, intracranial_pressure, cpp
        )
        
        return {
            "result": {
                "cpp_value": round(cpp, 1),
                "map_value": mean_arterial_pressure,
                "icp_value": intracranial_pressure,
                "clinical_category": assessment["category"],
                "risk_level": assessment["risk_level"],
                "urgency": assessment["urgency"],
                "is_adequate": cpp >= 60,
                "is_critical": cpp < 50,
                "management_recommendations": management,
                "calculation_breakdown": calculation_breakdown
            },
            "unit": "mmHg",
            "interpretation": assessment["interpretation"],
            "stage": assessment["category"],
            "stage_description": assessment["description"]
        }
    
    def _validate_inputs(self, map_value: float, icp_value: float):
        """Validates input parameters"""
        
        if not isinstance(map_value, (int, float)) or map_value < 30 or map_value > 200:
            raise ValueError("Mean arterial pressure must be a number between 30-200 mmHg")
        
        if not isinstance(icp_value, (int, float)) or icp_value < 0 or icp_value > 80:
            raise ValueError("Intracranial pressure must be a number between 0-80 mmHg")
        
        if icp_value >= map_value:
            raise ValueError("ICP cannot be greater than or equal to MAP")
    
    def _get_clinical_assessment(self, cpp: float) -> Dict[str, str]:
        """Gets clinical assessment based on CPP value"""
        
        for range_info in self.interpretation_ranges:
            if range_info["min"] <= cpp < range_info["max"]:
                return self._format_assessment(range_info, cpp)
        
        # Handle edge cases
        if cpp < 0:
            return {
                "category": "Critical",
                "description": "Negative cerebral perfusion pressure",
                "risk_level": "Critical",
                "urgency": "Immediate intervention required",
                "interpretation": f"CPP {cpp:.1f} mmHg: Negative cerebral perfusion pressure indicates critical condition. ICP exceeds MAP. Immediate aggressive intervention required to prevent brain death."
            }
        
        # Default fallback
        return {
            "category": "Unknown",
            "description": "Value requires clinical assessment",
            "risk_level": "Unknown",
            "urgency": "Clinical assessment needed",
            "interpretation": f"CPP {cpp:.1f} mmHg: Value outside typical ranges. Clinical assessment required."
        }
    
    def _format_assessment(self, range_info: Dict, cpp: float) -> Dict[str, str]:
        """Formats clinical assessment with detailed interpretation"""
        
        interpretation_map = {
            "Critical": f"CPP {cpp:.1f} mmHg: Critical risk of cerebral ischemia and brain death. Immediate aggressive intervention required to increase MAP (vasopressors, fluid resuscitation) and/or reduce ICP (osmotic therapy, positioning, surgical decompression). Consider emergency neurosurgical consultation.",
            "Severely Low": f"CPP {cpp:.1f} mmHg: High risk of cerebral ischemia and secondary brain injury. Urgent intervention needed to optimize cerebral perfusion. Consider vasopressor support, ICP-lowering measures, and close neurological monitoring.",
            "Low": f"CPP {cpp:.1f} mmHg: Below optimal range. May indicate risk of ischemia, especially in patients with impaired autoregulation. Consider interventions to improve cerebral perfusion while monitoring neurological status.",
            "Optimal": f"CPP {cpp:.1f} mmHg: Optimal range for cerebral perfusion in most patients. Maintain current management strategies while continuing to monitor for changes. Target range for TBI management.",
            "Adequate": f"CPP {cpp:.1f} mmHg: Adequate cerebral perfusion. Continue monitoring for potential complications of elevated pressures while maintaining adequate cerebral blood flow. Balance perfusion needs with hemodynamic stability.",
            "High": f"CPP {cpp:.1f} mmHg: Elevated cerebral perfusion pressure. While perfusion is adequate, consider potential complications of high pressures including increased risk of cerebral edema and respiratory complications. Balance perfusion needs with pressure management."
        }
        
        return {
            "category": range_info["category"],
            "description": range_info["description"],
            "risk_level": range_info["risk_level"],
            "urgency": range_info["urgency"],
            "interpretation": interpretation_map.get(range_info["category"], f"CPP {cpp:.1f} mmHg: Clinical assessment required.")
        }
    
    def _get_management_recommendations(self, cpp: float, map_value: float, icp_value: float) -> Dict[str, Any]:
        """Gets specific management recommendations based on CPP and components"""
        
        recommendations = {
            "primary_interventions": [],
            "monitoring": [],
            "considerations": []
        }
        
        # CPP-based recommendations
        if cpp < 30:
            recommendations["primary_interventions"].extend([
                "Immediate aggressive intervention required",
                "Consider emergency vasopressor support",
                "Urgent ICP reduction measures (osmotic therapy, positioning)",
                "Emergency neurosurgical consultation",
                "Consider decompressive craniectomy if indicated"
            ])
        elif cpp < 50:
            recommendations["primary_interventions"].extend([
                "Urgent optimization of cerebral perfusion",
                "Consider vasopressor support if MAP low",
                "ICP-lowering interventions as appropriate",
                "Close neurological monitoring"
            ])
        elif cpp < 60:
            recommendations["primary_interventions"].extend([
                "Consider interventions to improve CPP",
                "Monitor neurological status closely",
                "Optimize MAP and ICP management"
            ])
        elif cpp <= 80:
            recommendations["primary_interventions"].extend([
                "Maintain current management",
                "Continue monitoring CPP trends",
                "Optimize other neurological parameters"
            ])
        else:
            recommendations["primary_interventions"].extend([
                "Monitor for complications of elevated pressures",
                "Balance perfusion needs with pressure management",
                "Consider gradual optimization if excessive"
            ])
        
        # Component-specific recommendations
        if icp_value > 20:
            recommendations["considerations"].append("Elevated ICP (>20 mmHg) - consider ICP-lowering interventions")
        
        if map_value < 65:
            recommendations["considerations"].append("Low MAP (<65 mmHg) - consider vasopressor support")
        
        if map_value > 110:
            recommendations["considerations"].append("High MAP (>110 mmHg) - monitor for complications")
        
        # General monitoring recommendations
        recommendations["monitoring"].extend([
            "Continuous CPP monitoring preferred",
            "Monitor neurological examinations",
            "Assess cerebral autoregulation if possible",
            "Consider individual patient factors (age, comorbidities)"
        ])
        
        return recommendations
    
    def _get_calculation_breakdown(self, map_value: float, icp_value: float, cpp: float):
        """Provides detailed calculation breakdown"""
        
        return {
            "formula": "CPP = MAP - ICP",
            "components": {
                "mean_arterial_pressure": {
                    "value": map_value,
                    "unit": "mmHg",
                    "normal_range": "70-100 mmHg",
                    "description": "Driving pressure for cerebral blood flow"
                },
                "intracranial_pressure": {
                    "value": icp_value,
                    "unit": "mmHg",
                    "normal_range": "5-15 mmHg (adults)",
                    "description": "Pressure opposing cerebral blood flow"
                }
            },
            "result": {
                "cpp_value": round(cpp, 1),
                "unit": "mmHg",
                "normal_range": "60-80 mmHg",
                "critical_threshold": "<50 mmHg"
            },
            "clinical_context": {
                "autoregulation_range": "50-150 mmHg (healthy brain)",
                "tbi_target_range": "60-70 mmHg",
                "measurement_notes": "MAP measured at tragus level, ICP via invasive monitoring"
            }
        }


def calculate_cerebral_perfusion_pressure(
    mean_arterial_pressure: float,
    intracranial_pressure: float
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CerebralPerfusionPressureCalculator()
    return calculator.calculate(
        mean_arterial_pressure=mean_arterial_pressure,
        intracranial_pressure=intracranial_pressure
    )