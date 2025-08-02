"""
Liver Decompensation Risk after Hepatectomy for Hepatocellular Carcinoma (HCC) Calculator

Predicts risk of liver decompensation after hepatectomy for hepatocellular carcinoma.
Based on hierarchical interaction of portal hypertension, hepatectomy extent, and MELD score.

References:
1. Cescon M, Colecchia A, Cucchetti A, Peri E, Montrone L, Berretta M, et al. 
   Value of transient elastography measured with FibroScan in predicting the outcome 
   of hepatic resection for hepatocellular carcinoma. Ann Surg. 2012 Nov;256(5):706-12.
2. Cucchetti A, Ercolani G, Vivarelli M, Cescon M, Ravaioli M, La Barba G, et al. 
   Impact of model for end-stage liver disease (MELD) score on prognosis after 
   hepatectomy for hepatocellular carcinoma on cirrhosis. Liver Transpl. 2006 Jun;12(6):966-71.
"""

from typing import Dict, Any


class LiverDecompensationRiskHccCalculator:
    """Calculator for Liver Decompensation Risk after Hepatectomy for HCC"""
    
    def __init__(self):
        # Risk rates from the original study
        self.LOW_RISK_RATE = 4.9
        self.INTERMEDIATE_RISK_RATE = 28.6
        self.HIGH_RISK_RATE = 60.0
        
        # Additional clinical outcomes
        self.CLINICAL_OUTCOMES = {
            "low_risk": {
                "decompensation_rate": 4.9,
                "median_los": 7,
                "mortality_rate": 4.4
            },
            "intermediate_risk": {
                "decompensation_rate": 28.6,
                "median_los": 8,
                "mortality_rate": 9.0
            },
            "high_risk": {
                "decompensation_rate": 60.0,
                "median_los": 11,
                "mortality_rate": 25.0
            }
        }
    
    def calculate(
        self,
        portal_hypertension: str,
        hepatectomy_extent: str,
        meld_score_category: str = None
    ) -> Dict[str, Any]:
        """
        Calculates the liver decompensation risk after hepatectomy for HCC
        
        Args:
            portal_hypertension (str): "yes" or "no"
            hepatectomy_extent (str): "minor" or "major"
            meld_score_category (str): "9_or_less" or "greater_than_9" (optional)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(portal_hypertension, hepatectomy_extent, meld_score_category)
        
        # Determine risk category based on hierarchical algorithm
        risk_category = self._determine_risk_category(
            portal_hypertension, hepatectomy_extent, meld_score_category
        )
        
        # Get risk rate and interpretation
        risk_data = self.CLINICAL_OUTCOMES[risk_category]
        interpretation = self._get_interpretation(
            risk_category, portal_hypertension, hepatectomy_extent, meld_score_category
        )
        
        return {
            "result": risk_data["decompensation_rate"],
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, portal_hypertension, hepatectomy_extent, meld_score_category):
        """Validates input parameters"""
        
        if portal_hypertension not in ["yes", "no"]:
            raise ValueError("Portal hypertension must be 'yes' or 'no'")
        
        if hepatectomy_extent not in ["minor", "major"]:
            raise ValueError("Hepatectomy extent must be 'minor' or 'major'")
        
        if meld_score_category is not None and meld_score_category not in ["9_or_less", "greater_than_9"]:
            raise ValueError("MELD score category must be '9_or_less' or 'greater_than_9'")
        
        # MELD score category is only required for specific scenarios
        if (portal_hypertension == "no" and hepatectomy_extent == "minor" and 
            meld_score_category is None):
            raise ValueError("MELD score category is required when portal hypertension is 'no' and hepatectomy is 'minor'")
    
    def _determine_risk_category(self, portal_hypertension, hepatectomy_extent, meld_score_category):
        """
        Determines risk category based on hierarchical algorithm
        
        Risk stratification logic:
        - High Risk: Major resection + Portal hypertension
        - Low Risk: No portal hypertension + Minor resection + MELD ≤9
        - Intermediate Risk: All other combinations
        """
        
        # High Risk: Major resection with portal hypertension
        if hepatectomy_extent == "major" and portal_hypertension == "yes":
            return "high_risk"
        
        # Low Risk: No portal hypertension, minor resection, MELD ≤9
        if (portal_hypertension == "no" and 
            hepatectomy_extent == "minor" and 
            meld_score_category == "9_or_less"):
            return "low_risk"
        
        # Intermediate Risk: All other combinations
        # - No portal hypertension + major resection
        # - No portal hypertension + minor resection + MELD >9
        # - Portal hypertension + minor resection
        return "intermediate_risk"
    
    def _get_interpretation(self, risk_category, portal_hypertension, hepatectomy_extent, meld_score_category):
        """
        Provides detailed interpretation based on risk category and parameters
        """
        
        outcomes = self.CLINICAL_OUTCOMES[risk_category]
        
        # Build parameter description
        portal_status = "portal hypertension present" if portal_hypertension == "yes" else "no portal hypertension"
        resection_type = f"{hepatectomy_extent} hepatectomy"
        
        meld_status = ""
        if meld_score_category:
            if meld_score_category == "9_or_less":
                meld_status = ", MELD score ≤9"
            else:
                meld_status = ", MELD score >9"
        
        parameter_summary = f"{portal_status}, {resection_type}{meld_status}"
        
        if risk_category == "low_risk":
            return {
                "stage": "Low Risk",
                "stage_description": "Low risk of liver decompensation",
                "interpretation":
                    f"Low Risk Classification: {outcomes['decompensation_rate']:.1f}% liver decompensation rate. "
                    f"Clinical parameters: {parameter_summary}. "
                    f"Expected outcomes: median length of stay {outcomes['median_los']} days, "
                    f"liver-related mortality risk {outcomes['mortality_rate']:.1f}%. "
                    f"Management: These patients represent the optimal candidates for hepatectomy with "
                    f"minimal perioperative risk. Standard surgical care with routine postoperative monitoring. "
                    f"Excellent prognosis with low complication rates. Continue standard hepatology follow-up "
                    f"for HCC surveillance and liver function monitoring."
            }
        
        elif risk_category == "intermediate_risk":
            return {
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate risk of liver decompensation",
                "interpretation":
                    f"Intermediate Risk Classification: {outcomes['decompensation_rate']:.1f}% liver decompensation rate. "
                    f"Clinical parameters: {parameter_summary}. "
                    f"Expected outcomes: median length of stay {outcomes['median_los']} days, "
                    f"liver-related mortality risk {outcomes['mortality_rate']:.1f}%. "
                    f"Management: Enhanced perioperative monitoring recommended. Consider intensive care unit "
                    f"admission for major resections. Close monitoring of liver function tests, coagulation "
                    f"parameters, and clinical signs of decompensation. Early recognition and management of "
                    f"complications essential. Multidisciplinary team involvement with hepatology consultation "
                    f"for optimal perioperative care."
            }
        
        else:  # high_risk
            return {
                "stage": "High Risk",
                "stage_description": "High risk of liver decompensation",
                "interpretation":
                    f"High Risk Classification: {outcomes['decompensation_rate']:.1f}% liver decompensation rate. "
                    f"Clinical parameters: {parameter_summary}. "
                    f"Expected outcomes: median length of stay {outcomes['median_los']} days, "
                    f"liver-related mortality risk {outcomes['mortality_rate']:.1f}%. "
                    f"Management: CRITICAL - Carefully reconsider surgical candidacy. If surgery proceeds, "
                    f"mandatory intensive care unit admission and aggressive perioperative monitoring. "
                    f"Consider alternative treatments including liver transplantation, ablation, or "
                    f"transarterial chemoembolization. If surgery is performed, ensure availability of "
                    f"immediate hepatology consultation, blood products, and potential for emergent "
                    f"interventions. Detailed informed consent regarding high morbidity and mortality risks. "
                    f"Multidisciplinary tumor board discussion strongly recommended."
            }


def calculate_liver_decompensation_risk_hcc(
    portal_hypertension: str,
    hepatectomy_extent: str,
    meld_score_category: str = None
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_liver_decompensation_risk_hcc pattern
    """
    calculator = LiverDecompensationRiskHccCalculator()
    return calculator.calculate(portal_hypertension, hepatectomy_extent, meld_score_category)