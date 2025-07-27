"""
4Ts Score for Heparin-Induced Thrombocytopenia Calculator

Diferencia pacientes com TIH daqueles com outras causas de trombocitopenia.
Referência: Lo GK et al., J Thromb Haemost 2006;4(4):759-65
"""

from typing import Dict, Any


class FourTsHitCalculator:
    """Calculadora para o 4Ts Score para TIH"""
    
    def calculate(self, thrombocytopenia_severity: str, timing_onset: str,
                 thrombosis_sequelae: str, other_causes: str) -> Dict[str, Any]:
        """
        Calcula o 4Ts Score para TIH
        
        Args:
            thrombocytopenia_severity: Opções descritivas da magnitude da trombocitopenia
            timing_onset: Opções descritivas do timing da queda das plaquetas  
            thrombosis_sequelae: Opções descritivas da presença de trombose/sequelas
            other_causes: Opções descritivas de outras causas de trombocitopenia
                
        Returns:
            Dict com resultado, interpretação e classificação de risco
        """
        
        # Validações
        self._validate_inputs(thrombocytopenia_severity, timing_onset,
                            thrombosis_sequelae, other_causes)
        
        # Calcular pontuação
        score = 0
        
        # Trombocitopenia (0-2 pontos)
        score += self._score_thrombocytopenia(thrombocytopenia_severity)
        
        # Tempo de início (0-2 pontos)
        score += self._score_timing(timing_onset)
        
        # Trombose/sequelas (0-2 pontos)
        score += self._score_thrombosis(thrombosis_sequelae)
        
        # Outras causas (0-2 pontos) - nota: pontuação inversa
        score += self._score_other_causes(other_causes)
        
        # Obter interpretação
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "pontos",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, thrombocytopenia_severity: str, timing_onset: str,
                        thrombosis_sequelae: str, other_causes: str):
        """Valida os parâmetros de entrada"""
        
        valid_severity = [
            "queda_maior_50_nadir_maior_20",
            "queda_30_50_ou_nadir_10_19", 
            "queda_menor_30_ou_nadir_menor_10"
        ]
        if thrombocytopenia_severity not in valid_severity:
            raise ValueError(f"Gravidade da trombocitopenia deve ser uma das opções válidas")
        
        valid_timing = [
            "inicio_5_10_dias_ou_queda_1_dia_heparina_30_dias",
            "possivel_5_10_dias_ou_inicio_apos_10_dias_ou_heparina_30_100_dias",
            "queda_menor_4_dias_sem_exposicao_recente"
        ]
        if timing_onset not in valid_timing:
            raise ValueError(f"Tempo de início deve ser uma das opções válidas")
        
        valid_thrombosis = [
            "nova_trombose_ou_necrose_cutanea_ou_reacao_sistemica",
            "trombose_progressiva_ou_lesoes_cutaneas_ou_suspeita_trombose",
            "nenhuma_trombose_ou_sequela"
        ]
        if thrombosis_sequelae not in valid_thrombosis:
            raise ValueError(f"Trombose/sequelas deve ser uma das opções válidas")
        
        valid_other = [
            "nenhuma_outra_causa_aparente",
            "outras_causas_possiveis", 
            "outras_causas_definitivas"
        ]
        if other_causes not in valid_other:
            raise ValueError(f"Outras causas deve ser uma das opções válidas")
    
    def _score_thrombocytopenia(self, severity: str) -> int:
        """Calcula pontos para trombocitopenia"""
        mapping = {
            "queda_maior_50_nadir_maior_20": 2,
            "queda_30_50_ou_nadir_10_19": 1,
            "queda_menor_30_ou_nadir_menor_10": 0
        }
        return mapping[severity]
    
    def _score_timing(self, timing: str) -> int:
        """Calcula pontos para tempo de início"""
        mapping = {
            "inicio_5_10_dias_ou_queda_1_dia_heparina_30_dias": 2,
            "possivel_5_10_dias_ou_inicio_apos_10_dias_ou_heparina_30_100_dias": 1,
            "queda_menor_4_dias_sem_exposicao_recente": 0
        }
        return mapping[timing]
    
    def _score_thrombosis(self, thrombosis: str) -> int:
        """Calcula pontos para trombose/sequelas"""
        mapping = {
            "nova_trombose_ou_necrose_cutanea_ou_reacao_sistemica": 2,
            "trombose_progressiva_ou_lesoes_cutaneas_ou_suspeita_trombose": 1,
            "nenhuma_trombose_ou_sequela": 0
        }
        return mapping[thrombosis]
    
    def _score_other_causes(self, other_causes: str) -> int:
        """Calcula pontos para outras causas (pontuação inversa)"""
        mapping = {
            "nenhuma_outra_causa_aparente": 2,
            "outras_causas_possiveis": 1,
            "outras_causas_definitivas": 0
        }
        return mapping[other_causes]
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determina a interpretação baseada no escore
        
        Args:
            score: Escore calculado (0-8)
            
        Returns:
            Dict com interpretação
        """
        
        if score <= 3:
            return {
                "stage": "Baixa Probabilidade",
                "description": "Baixa probabilidade de TIH",
                "interpretation": f"Escore de {score} pontos indica baixa probabilidade de TIH (<5%). Valor preditivo negativo de 99.8%. TIH improvável - considere outras causas de trombocitopenia. Pode dispensar testes adicionais para TIH."
            }
        elif score <= 5:
            return {
                "stage": "Probabilidade Intermediária",
                "description": "Probabilidade intermediária de TIH",
                "interpretation": f"Escore de {score} pontos indica probabilidade intermediária de TIH (~14%). Necessária investigação adicional com testes laboratoriais para TIH (ensaio funcional ou imunológico). Considere suspender heparina até resultado."
            }
        else:  # score >= 6
            return {
                "stage": "Alta Probabilidade",
                "description": "Alta probabilidade de TIH",
                "interpretation": f"Escore de {score} pontos indica alta probabilidade de TIH (~64%). Suspender imediatamente toda heparina. Iniciar anticoagulante não-heparina (argatroban, bivalirudina). Realizar testes confirmatórios para TIH."
            }


def calculate_4ts_hit(thrombocytopenia_severity: str, timing_onset: str,
                     thrombosis_sequelae: str, other_causes: str) -> Dict[str, Any]:
    """
    Função de conveniência para o sistema de carregamento dinâmico
    
    IMPORTANTE: Esta função deve seguir o padrão calculate_{score_id}
    """
    calculator = FourTsHitCalculator()
    return calculator.calculate(thrombocytopenia_severity, timing_onset,
                              thrombosis_sequelae, other_causes)