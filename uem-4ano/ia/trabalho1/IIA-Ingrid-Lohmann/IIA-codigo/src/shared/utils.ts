import type { HeuristicOption, InstanceOption, SudokuMode } from "./types";

export const instanceLabels: Record<InstanceOption, string> = {
  easy: 'Fácil',
  medium: 'Médio',
  difficult: 'Difícil',
};

export const heuristicLabels: Record<HeuristicOption, string> = {
  degree: 'Grau (Heurística de Grau)',
  mrv: 'MRV (Valores Mínimos Restantes)',
};

export const modeLabels: Record<SudokuMode, string> = {
  partial: 'Parcial (5 variáveis)',
  full: 'Completo (4x4)',
};