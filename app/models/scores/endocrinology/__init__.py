"""
Endocrinology score models
"""

from .ada_risk_calculator import AdaRiskCalculatorRequest, AdaRiskCalculatorResponse
from .ausdrisk import AusdriskRequest, AusdriskResponse
from .basal_energy_expenditure import BasalEnergyExpenditureRequest, BasalEnergyExpenditureResponse
from .beam_value import BeamValueRequest, BeamValueResponse
from .c_peptide_to_glucose_ratio import CPeptideToGlucoseRatioRequest, CPeptideToGlucoseRatioResponse
from .calcium_correction import CalciumCorrectionRequest, CalciumCorrectionResponse
from .cambridge_diabetes_risk_score import CambridgeDiabetesRiskScoreRequest, CambridgeDiabetesRiskScoreResponse
from .canrisk import CanriskRequest, CanriskResponse
from .diabetes_distress_scale import DiabetesDistressScaleRequest, DiabetesDistressScaleResponse
from .dka_mpm_score import DkaMpmScoreRequest, DkaMpmScoreResponse
from .dutch_criteria_familial_hypercholesterolemia import DutchCriteriaFamilialHypercholesterolemiaRequest, DutchCriteriaFamilialHypercholesterolemiaResponse
from .edmonton_obesity_staging_system import EdmontonObesityStagingSystemRequest, EdmontonObesityStagingSystemResponse
from .estimated_average_glucose_eag_hba1c import EstimatedAverageGlucoseEagHba1cRequest, EstimatedAverageGlucoseEagHba1cResponse
from .findrisc import FindriscRequest, FindriscResponse
from .glucose_infusion_rate import GlucoseInfusionRateRequest, GlucoseInfusionRateResponse
from .homa_ir import HomaIrRequest, HomaIrResponse
from .hypoglycemia_risk_score import HypoglycemiaRiskScoreRequest, HypoglycemiaRiskScoreResponse
from .idf_dar_fasting_risk_assessment import IdfDarFastingRiskAssessmentRequest, IdfDarFastingRiskAssessmentResponse
from .mets_ir import MetsIrRequest, MetsIrResponse
from .myxedema_coma_diagnostic_score import MyxedemaComatDiagnosticScoreRequest, MyxedemaComatDiagnosticScoreResponse

__all__ = [
    "AdaRiskCalculatorRequest",
    "AdaRiskCalculatorResponse",
    "AusdriskRequest",
    "AusdriskResponse",
    "BasalEnergyExpenditureRequest",
    "BasalEnergyExpenditureResponse",
    "BeamValueRequest",
    "BeamValueResponse",
    "CPeptideToGlucoseRatioRequest",
    "CPeptideToGlucoseRatioResponse",
    "CalciumCorrectionRequest",
    "CalciumCorrectionResponse",
    "CambridgeDiabetesRiskScoreRequest",
    "CambridgeDiabetesRiskScoreResponse",
    "CanriskRequest",
    "CanriskResponse",
    "DiabetesDistressScaleRequest",
    "DiabetesDistressScaleResponse",
    "DkaMpmScoreRequest",
    "DkaMpmScoreResponse",
    "DutchCriteriaFamilialHypercholesterolemiaRequest",
    "DutchCriteriaFamilialHypercholesterolemiaResponse",
    "EdmontonObesityStagingSystemRequest",
    "EdmontonObesityStagingSystemResponse",
    "EstimatedAverageGlucoseEagHba1cRequest",
    "EstimatedAverageGlucoseEagHba1cResponse",
    "FindriscRequest",
    "FindriscResponse",
    "GlucoseInfusionRateRequest",
    "GlucoseInfusionRateResponse",
    "HomaIrRequest",
    "HomaIrResponse",
    "HypoglycemiaRiskScoreRequest",
    "HypoglycemiaRiskScoreResponse",
    "IdfDarFastingRiskAssessmentRequest",
    "IdfDarFastingRiskAssessmentResponse",
    "MetsIrRequest",
    "MetsIrResponse",
    "MyxedemaComatDiagnosticScoreRequest",
    "MyxedemaComatDiagnosticScoreResponse"
]