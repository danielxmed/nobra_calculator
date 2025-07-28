"""
AKIN Classification for Acute Kidney Injury (AKI) Calculator

Classifies severity of acute kidney injury based on serum creatinine and urine output 
criteria within 48 hours. The AKIN classification was developed to improve upon the 
RIFLE criteria and provides a standardized framework for diagnosing and staging AKI.

The AKIN classification requires:
1. Changes occurring within 48 hours
2. Adequate hydration status
3. Exclusion of urinary tract obstruction
4. At least two creatinine measurements within the same 48-hour period

References:
- Mehta RL, Kellum JA, Shah SV, et al. Acute Kidney Injury Network: report of an 
  initiative to improve outcomes in acute kidney injury. Crit Care. 2007;11(2):R31.
- Lopes JA, Jorge S. The RIFLE and AKIN classifications for acute kidney injury: 
  a critical and comprehensive review. Clin Kidney J. 2013;6(1):8-14.
"""

from typing import Dict, Any, Optional


class AkinCalculator:
    """Calculator for AKIN Classification for Acute Kidney Injury"""
    
    def __init__(self):
        # AKIN stage definitions
        self.STAGE_DEFINITIONS = {
            0: {
                "name": "No AKI",
                "description": "No acute kidney injury",
                "mortality_risk": "Baseline"
            },
            1: {
                "name": "Stage 1",
                "description": "Mild AKI",
                "mortality_risk": "Increased"
            },
            2: {
                "name": "Stage 2", 
                "description": "Moderate AKI",
                "mortality_risk": "Significantly increased"
            },
            3: {
                "name": "Stage 3",
                "description": "Severe AKI",
                "mortality_risk": "Markedly increased"
            }
        }
    
    def calculate(self, current_creatinine: float, baseline_creatinine: Optional[float] = None,
                 creatinine_increase: Optional[float] = None, urine_output_6h: Optional[float] = None,
                 urine_output_12h: Optional[float] = None, urine_output_24h: Optional[float] = None,
                 anuria_12h: Optional[str] = None, on_rrt: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates AKIN stage using the provided parameters
        
        Args:
            current_creatinine (float): Current serum creatinine in mg/dL
            baseline_creatinine (Optional[float]): Baseline creatinine in mg/dL
            creatinine_increase (Optional[float]): Absolute increase in creatinine in mg/dL
            urine_output_6h (Optional[float]): Urine output over 6 hours in mL/kg
            urine_output_12h (Optional[float]): Urine output over 12 hours in mL/kg
            urine_output_24h (Optional[float]): Urine output over 24 hours in mL/kg
            anuria_12h (Optional[str]): "yes" or "no" for anuria for 12 hours
            on_rrt (Optional[str]): "yes" or "no" for renal replacement therapy
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(current_creatinine, baseline_creatinine, creatinine_increase,
                            urine_output_6h, urine_output_12h, urine_output_24h, anuria_12h, on_rrt)
        
        # Check if on RRT (automatically Stage 3)
        if on_rrt and on_rrt.lower() == 'yes':
            stage = 3
            criteria_met = ["On renal replacement therapy"]
            interpretation = self._get_interpretation(stage, criteria_met, current_creatinine, 
                                                   baseline_creatinine, on_rrt=True)
            return self._format_result(stage, interpretation, criteria_met)
        
        # Calculate stage based on creatinine and urine output criteria
        creatinine_stage, creatinine_criteria = self._assess_creatinine_criteria(
            current_creatinine, baseline_creatinine, creatinine_increase)
        
        urine_stage, urine_criteria = self._assess_urine_criteria(
            urine_output_6h, urine_output_12h, urine_output_24h, anuria_12h)
        
        # Final stage is the highest of creatinine or urine criteria
        final_stage = max(creatinine_stage, urine_stage)
        
        # Combine criteria met
        criteria_met = []
        if creatinine_criteria:
            criteria_met.extend(creatinine_criteria)
        if urine_criteria:
            criteria_met.extend(urine_criteria)
        
        if not criteria_met:
            criteria_met = ["No AKI criteria met"]
        
        # Get interpretation
        interpretation = self._get_interpretation(final_stage, criteria_met, current_creatinine, 
                                               baseline_creatinine)
        
        return self._format_result(final_stage, interpretation, criteria_met)
    
    def _validate_inputs(self, current_creatinine: float, baseline_creatinine: Optional[float],
                        creatinine_increase: Optional[float], urine_output_6h: Optional[float],
                        urine_output_12h: Optional[float], urine_output_24h: Optional[float],
                        anuria_12h: Optional[str], on_rrt: Optional[str]):
        """Validates input parameters"""
        
        # Validate current creatinine
        if not isinstance(current_creatinine, (int, float)):
            raise ValueError("Current creatinine must be a number")
        
        if current_creatinine < 0.1 or current_creatinine > 15.0:
            raise ValueError("Current creatinine must be between 0.1 and 15.0 mg/dL")
        
        # Validate baseline creatinine
        if baseline_creatinine is not None:
            if not isinstance(baseline_creatinine, (int, float)):
                raise ValueError("Baseline creatinine must be a number")
            
            if baseline_creatinine < 0.1 or baseline_creatinine > 15.0:
                raise ValueError("Baseline creatinine must be between 0.1 and 15.0 mg/dL")
        
        # Validate creatinine increase
        if creatinine_increase is not None:
            if not isinstance(creatinine_increase, (int, float)):
                raise ValueError("Creatinine increase must be a number")
            
            if creatinine_increase < 0.0 or creatinine_increase > 10.0:
                raise ValueError("Creatinine increase must be between 0.0 and 10.0 mg/dL")
        
        # Validate urine outputs
        for uo_name, uo_value, max_val in [
            ("6h urine output", urine_output_6h, 50.0),
            ("12h urine output", urine_output_12h, 100.0),
            ("24h urine output", urine_output_24h, 200.0)
        ]:
            if uo_value is not None:
                if not isinstance(uo_value, (int, float)):
                    raise ValueError(f"{uo_name} must be a number")
                
                if uo_value < 0.0 or uo_value > max_val:
                    raise ValueError(f"{uo_name} must be between 0.0 and {max_val} mL/kg")
        
        # Validate categorical inputs
        for param_name, param_value in [("anuria_12h", anuria_12h), ("on_rrt", on_rrt)]:
            if param_value is not None:
                if not isinstance(param_value, str):
                    raise ValueError(f"{param_name} must be a string")
                
                if param_value.lower() not in ['yes', 'no']:
                    raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _assess_creatinine_criteria(self, current_creatinine: float, 
                                  baseline_creatinine: Optional[float],
                                  creatinine_increase: Optional[float]) -> tuple[int, list]:
        """Assesses creatinine-based AKIN criteria"""
        
        stage = 0
        criteria = []
        
        # If we have baseline creatinine, calculate fold increase
        if baseline_creatinine is not None and baseline_creatinine > 0:
            fold_increase = current_creatinine / baseline_creatinine
            
            if fold_increase >= 3.0:
                stage = max(stage, 3)
                criteria.append(f"Creatinine ≥3x baseline ({fold_increase:.1f}x)")
            elif fold_increase >= 2.0:
                stage = max(stage, 2)
                criteria.append(f"Creatinine 2-3x baseline ({fold_increase:.1f}x)")
            elif fold_increase >= 1.5:
                stage = max(stage, 1)
                criteria.append(f"Creatinine 1.5-2x baseline ({fold_increase:.1f}x)")
        
        # Check absolute increase criteria
        if creatinine_increase is not None and creatinine_increase >= 0.3:
            stage = max(stage, 1)
            criteria.append(f"Absolute creatinine increase ≥0.3 mg/dL ({creatinine_increase:.1f} mg/dL)")
        
        # Stage 3 specific criteria: Cr ≥4.0 mg/dL with acute increase ≥0.5 mg/dL
        if (current_creatinine >= 4.0 and creatinine_increase is not None and 
            creatinine_increase >= 0.5):
            stage = max(stage, 3)
            criteria.append(f"Creatinine ≥4.0 mg/dL with acute increase ≥0.5 mg/dL")
        
        return stage, criteria
    
    def _assess_urine_criteria(self, urine_output_6h: Optional[float],
                             urine_output_12h: Optional[float], 
                             urine_output_24h: Optional[float],
                             anuria_12h: Optional[str]) -> tuple[int, list]:
        """Assesses urine output-based AKIN criteria"""
        
        stage = 0
        criteria = []
        
        # Check anuria for 12 hours (Stage 3)
        if anuria_12h and anuria_12h.lower() == 'yes':
            stage = max(stage, 3)
            criteria.append("Anuria for 12 hours")
            return stage, criteria
        
        # Convert urine outputs to hourly rates if needed
        # Stage 3: <0.3 mL/kg/hr for ≥24 hours
        if urine_output_24h is not None:
            hourly_rate_24h = urine_output_24h / 24
            if hourly_rate_24h < 0.3:
                stage = max(stage, 3)
                criteria.append(f"Urine output <0.3 mL/kg/hr for ≥24 hours ({hourly_rate_24h:.2f} mL/kg/hr)")
        
        # Stage 2: <0.5 mL/kg/hr for >12 hours
        if urine_output_12h is not None:
            hourly_rate_12h = urine_output_12h / 12
            if hourly_rate_12h < 0.5:
                stage = max(stage, 2)
                criteria.append(f"Urine output <0.5 mL/kg/hr for >12 hours ({hourly_rate_12h:.2f} mL/kg/hr)")
        
        # Stage 1: <0.5 mL/kg/hr for >6 hours
        if urine_output_6h is not None:
            hourly_rate_6h = urine_output_6h / 6
            if hourly_rate_6h < 0.5:
                stage = max(stage, 1)
                criteria.append(f"Urine output <0.5 mL/kg/hr for >6 hours ({hourly_rate_6h:.2f} mL/kg/hr)")
        
        return stage, criteria
    
    def _get_interpretation(self, stage: int, criteria_met: list, current_creatinine: float,
                          baseline_creatinine: Optional[float], on_rrt: bool = False) -> str:
        """
        Determines the interpretation based on the AKIN stage
        
        Args:
            stage (int): AKIN stage (0-3)
            criteria_met (list): List of criteria that were met
            current_creatinine (float): Current creatinine value
            baseline_creatinine (Optional[float]): Baseline creatinine if available
            on_rrt (bool): Whether patient is on RRT
            
        Returns:
            str: Clinical interpretation
        """
        
        stage_info = self.STAGE_DEFINITIONS.get(stage, self.STAGE_DEFINITIONS[0])
        
        interpretation_parts = []
        
        # Stage and description
        if stage == 0:
            interpretation_parts.append("No acute kidney injury by AKIN criteria.")
        else:
            interpretation_parts.append(f"AKIN {stage_info['name']}: {stage_info['description']}.")
        
        # Current creatinine
        interpretation_parts.append(f"Current creatinine: {current_creatinine:.1f} mg/dL.")
        
        if baseline_creatinine is not None:
            interpretation_parts.append(f"Baseline creatinine: {baseline_creatinine:.1f} mg/dL.")
        
        # Criteria met
        if criteria_met and criteria_met != ["No AKI criteria met"]:
            interpretation_parts.append(f"Criteria met: {'; '.join(criteria_met)}.")
        elif stage == 0:
            interpretation_parts.append("No AKIN criteria met.")
        
        # Clinical recommendations based on stage
        if stage == 0:
            interpretation_parts.append(
                "MANAGEMENT: Continue routine monitoring. Ensure adequate hydration and "
                "avoid nephrotoxic medications."
            )
        elif stage == 1:
            interpretation_parts.append(
                "MANAGEMENT: Close monitoring required. Consider nephrology consultation. "
                "Review medications and optimize fluid status. Monitor creatinine daily."
            )
        elif stage == 2:
            interpretation_parts.append(
                "MANAGEMENT: Intensive monitoring required. Nephrology consultation recommended. "
                "Daily creatinine monitoring. Consider underlying causes and optimize management."
            )
        elif stage == 3:
            if on_rrt:
                interpretation_parts.append(
                    "MANAGEMENT: Patient on renal replacement therapy. Continue RRT as indicated. "
                    "Nephrology management essential. Monitor for complications."
                )
            else:
                interpretation_parts.append(
                    "MANAGEMENT: Urgent nephrology consultation required. Consider renal replacement "
                    "therapy. Intensive monitoring. Address underlying causes aggressively."
                )
        
        # Additional context
        interpretation_parts.append(
            "IMPORTANT: AKIN classification requires changes within 48 hours, adequate hydration, "
            "and exclusion of urinary obstruction. Use with clinical context."
        )
        
        return " ".join(interpretation_parts)
    
    def _format_result(self, stage: int, interpretation: str, criteria_met: list) -> Dict[str, Any]:
        """Formats the final result"""
        
        stage_info = self.STAGE_DEFINITIONS.get(stage, self.STAGE_DEFINITIONS[0])
        
        return {
            "result": stage_info["name"],
            "unit": "stage",
            "interpretation": interpretation,
            "stage": stage_info["name"],
            "stage_description": stage_info["description"],
            "stage_number": stage,
            "criteria_met": criteria_met,
            "mortality_risk": stage_info["mortality_risk"]
        }


def calculate_akin(current_creatinine: float, baseline_creatinine: Optional[float] = None,
                  creatinine_increase: Optional[float] = None, urine_output_6h: Optional[float] = None,
                  urine_output_12h: Optional[float] = None, urine_output_24h: Optional[float] = None,
                  anuria_12h: Optional[str] = None, on_rrt: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_akin pattern
    """
    calculator = AkinCalculator()
    return calculator.calculate(
        current_creatinine=current_creatinine,
        baseline_creatinine=baseline_creatinine,
        creatinine_increase=creatinine_increase,
        urine_output_6h=urine_output_6h,
        urine_output_12h=urine_output_12h,
        urine_output_24h=urine_output_24h,
        anuria_12h=anuria_12h,
        on_rrt=on_rrt
    )