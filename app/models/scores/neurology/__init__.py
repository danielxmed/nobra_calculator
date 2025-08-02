"""
Neurology score models
"""

from .abcd2 import Abcd2Request, Abcd2Response
from .four_at import FourAtRequest, FourAtResponse
from .abc2_ich_volume import Abc2IchVolumeRequest, Abc2IchVolumeResponse
from .aspects import AspectsRequest, AspectsResponse
from .ascod_algorithm import AscodAlgorithmRequest, AscodAlgorithmResponse
from .astral_score import AstralScoreRequest, AstralScoreResponse
from .awol_score import AwolScoreRequest, AwolScoreResponse
from .barnes_jewish_dysphagia import BarnesJewishDysphagiaRequest, BarnesJewishDysphagiaResponse
from .canadian_tia_score import CanadianTiaScoreRequest, CanadianTiaScoreResponse
from .cerebral_perfusion_pressure import CerebralPerfusionPressureRequest, CerebralPerfusionPressureResponse
from .clinical_dementia_rating import ClinicalDementiaRatingRequest, ClinicalDementiaRatingResponse
from .ndi import NdiRequest, NdiResponse
from .disease_steps_ms import DiseaseStepsMsRequest, DiseaseStepsMsResponse
from .dragon_score import DragonScoreRequest, DragonScoreResponse
from .embolic_stroke_undetermined_source_esus_criteria import EmbolicStrokeUndeterminedSourceEsusCriteriaRequest, EmbolicStrokeUndeterminedSourceEsusCriteriaResponse
from .neuropathic_pain_scale import NeuropathicPainScaleRequest, NeuropathicPainScaleResponse
from .new_orleans_charity_head_trauma import NewOrleansCharityHeadTraumaRequest, NewOrleansCharityHeadTraumaResponse
from .edss import EdssRequest, EdssResponse
from .fisher_grading_scale import FisherGradingScaleRequest, FisherGradingScaleResponse
from .four_score import FourScoreRequest, FourScoreResponse
from .gcs_pupils_score import GcsPupilsScoreRequest, GcsPupilsScoreResponse
from .glasgow_coma_scale import GlasgowComaScaleRequest, GlasgowComaScaleResponse
from .func_score import FuncScoreRequest, FuncScoreResponse
from .hat_score import HatScoreRequest, HatScoreResponse
from .hints import HintsRequest, HintsResponse
from .hunt_hess_classification import HuntHessClassificationRequest, HuntHessClassificationResponse
from .impact_score import ImpactScoreRequest, ImpactScoreResponse, ImpactScoreResult
from .iwg2_alzheimer_criteria import Iwg2AlzheimerCriteriaRequest, Iwg2AlzheimerCriteriaResponse
from .ich_score import IchScoreRequest, IchScoreResponse
from .los_angeles_motor_scale import LosAngelesMotorScaleRequest, LosAngelesMotorScaleResponse
from .mcdonald_criteria_multiple_sclerosis_2017_revision import (
    McdonaldCriteriaMultipleSclerosis2017RevisionRequest,
    McdonaldCriteriaMultipleSclerosis2017RevisionResponse
)
from .midas import MidasRequest, MidasResponse
from .mtoq_4 import Mtoq4Request, Mtoq4Response
from .modified_fatigue_impact_scale import ModifiedFatigueImpactScaleRequest, ModifiedFatigueImpactScaleResponse
from .modified_fisher_grading_scale import ModifiedFisherGradingScaleRequest, ModifiedFisherGradingScaleResponse
from .modified_hoehn_and_yahr_scale import ModifiedHoehnAndYahrScaleRequest, ModifiedHoehnAndYahrScaleResponse
from .modified_nih_stroke_scale import ModifiedNihStrokeScaleRequest, ModifiedNihStrokeScaleResponse
from .modified_rankin_scale import ModifiedRankinScaleRequest, ModifiedRankinScaleResponse
from .modified_rankin_score_9q import ModifiedRankinScore9QRequest, ModifiedRankinScore9QResponse
from .modified_soar_score import ModifiedSoarScoreRequest, ModifiedSoarScoreResponse
from .moca import MocaRequest, MocaResponse
from .mg_adl import MgAdlRequest, MgAdlResponse
from .nihss import NihssRequest, NihssResponse
from .onls import OnlsRequest, OnlsResponse
from .sudbury_vertigo_risk_score import SudburyVertigoRiskScoreRequest, SudburyVertigoRiskScoreResponse
from .tpa_contraindications import TpaContraindicationsRequest, TpaContraindicationsResponse
from .trunk_impairment_scale import TrunkImpairmentScaleRequest, TrunkImpairmentScaleResponse

__all__ = [
    "Abcd2Request",
    "Abcd2Response",
    "FourAtRequest",
    "FourAtResponse",
    "Abc2IchVolumeRequest",
    "Abc2IchVolumeResponse",
    "AspectsRequest",
    "AspectsResponse",
    "AscodAlgorithmRequest",
    "AscodAlgorithmResponse",
    "AstralScoreRequest",
    "AstralScoreResponse",
    "AwolScoreRequest",
    "AwolScoreResponse",
    "BarnesJewishDysphagiaRequest",
    "BarnesJewishDysphagiaResponse",
    "CanadianTiaScoreRequest",
    "CanadianTiaScoreResponse",
    "CerebralPerfusionPressureRequest",
    "CerebralPerfusionPressureResponse",
    "ClinicalDementiaRatingRequest",
    "ClinicalDementiaRatingResponse",
    "NdiRequest",
    "NdiResponse",
    "DiseaseStepsMsRequest",
    "DiseaseStepsMsResponse",
    "DragonScoreRequest",
    "DragonScoreResponse",
    "EmbolicStrokeUndeterminedSourceEsusCriteriaRequest",
    "EmbolicStrokeUndeterminedSourceEsusCriteriaResponse",
    "NeuropathicPainScaleRequest",
    "NeuropathicPainScaleResponse",
    "NewOrleansCharityHeadTraumaRequest",
    "NewOrleansCharityHeadTraumaResponse",
    "EdssRequest",
    "EdssResponse",
    "FisherGradingScaleRequest",
    "FisherGradingScaleResponse",
    "FourScoreRequest",
    "FourScoreResponse",
    "GcsPupilsScoreRequest",
    "GcsPupilsScoreResponse",
    "GlasgowComaScaleRequest",
    "GlasgowComaScaleResponse",
    "FuncScoreRequest",
    "FuncScoreResponse",
    "HatScoreRequest",
    "HatScoreResponse",
    "HintsRequest",
    "HintsResponse",
    "HuntHessClassificationRequest",
    "HuntHessClassificationResponse",
    "ImpactScoreRequest",
    "ImpactScoreResponse",
    "ImpactScoreResult",
    "Iwg2AlzheimerCriteriaRequest",
    "Iwg2AlzheimerCriteriaResponse",
    "IchScoreRequest",
    "IchScoreResponse",
    "LosAngelesMotorScaleRequest",
    "LosAngelesMotorScaleResponse",
    "McdonaldCriteriaMultipleSclerosis2017RevisionRequest",
    "McdonaldCriteriaMultipleSclerosis2017RevisionResponse",
    "MidasRequest",
    "MidasResponse",
    "Mtoq4Request",
    "Mtoq4Response",
    "ModifiedFatigueImpactScaleRequest",
    "ModifiedFatigueImpactScaleResponse",
    "ModifiedFisherGradingScaleRequest",
    "ModifiedFisherGradingScaleResponse",
    "ModifiedHoehnAndYahrScaleRequest",
    "ModifiedHoehnAndYahrScaleResponse",
    "ModifiedNihStrokeScaleRequest",
    "ModifiedNihStrokeScaleResponse",
    "ModifiedRankinScaleRequest",
    "ModifiedRankinScaleResponse",
    "ModifiedRankinScore9QRequest",
    "ModifiedRankinScore9QResponse",
    "ModifiedSoarScoreRequest",
    "ModifiedSoarScoreResponse",
    "MocaRequest",
    "MocaResponse",
    "MgAdlRequest",
    "MgAdlResponse",
    "NihssRequest",
    "NihssResponse",
    "OnlsRequest",
    "OnlsResponse",
    "SudburyVertigoRiskScoreRequest",
    "SudburyVertigoRiskScoreResponse",
    "TpaContraindicationsRequest",
    "TpaContraindicationsResponse",
    "TrunkImpairmentScaleRequest",
    "TrunkImpairmentScaleResponse"
]
