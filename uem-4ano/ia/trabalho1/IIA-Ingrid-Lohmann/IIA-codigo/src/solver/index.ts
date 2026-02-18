import { createSudokuCSP } from "../model/csp";
import { Assignment, HeuristicFunction, HeuristicOption, InstanceOption, SearchMetrics, SudokuMode } from "../shared/types";
import { backtrack } from "./backtracking";
import { ac3 } from "./consistency";
import { selectUnassignedVariable_Degree, selectUnassignedVariable_MRV } from "./heuristics";

const heuristicFunctions: Record<HeuristicOption, HeuristicFunction> = {
  mrv: selectUnassignedVariable_MRV,
  degree: selectUnassignedVariable_Degree,
};

/**
 * Função principal que inicia o processo de resolução do CSP.
 * @param heuristicChoice - Uma string 'mrv' ou 'degree' para selecionar a heurística.
 * @param mode - Uma string 'full' ou 'partial' para selecionar se é um sudoku completo ou não.
 */
export const solve = (
  heuristicChoice: HeuristicOption,
  instanceName: InstanceOption,
  useAC3: boolean,
  mode: SudokuMode,
): { solution: Assignment | null; metrics: SearchMetrics, ac3Logs: string[] } => {
  let ac3Logs: string[] = [];
  const csp = createSudokuCSP(instanceName, mode);
  const initialAssignment: Assignment = {};
  const metrics: SearchMetrics = { nodesVisited: 0, backtracks: 0 };

  if (useAC3) {
    const ac3Result = ac3(csp, mode); 
    ac3Logs = ac3Result.logs; 

    if (!ac3Result.isConsistent) {
      console.log("⚠️ AC-3 detectou que o problema não tem solução.\n");
      return { solution: null, metrics, ac3Logs };
    }
  }

  const heuristic = heuristicFunctions[heuristicChoice];

  const solution = backtrack(initialAssignment, csp, heuristic, metrics, mode);

  return { solution, metrics, ac3Logs };
};