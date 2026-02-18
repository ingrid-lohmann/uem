import { getConstraintGraph } from "../model/constraints";
import { Domain, SudokuMode, Variable } from "../shared/types";

// --- HEURÍSTICA DE MRV ---
export const selectUnassignedVariable_MRV = (
  unassignedVars: Variable[],
  domains: Record<Variable, Domain>,
  mode: SudokuMode,
): Variable => {
  
  if (unassignedVars.length === 0) {
    throw new Error("A função de heurística foi chamada sem variáveis livres.");
  }

  let bestVar: Variable | null = null;
  let minDomainSize = Infinity;

  for (const v of unassignedVars) {
    const currentDomainSize = domains[v].length;

    if (currentDomainSize < minDomainSize) {
      minDomainSize = currentDomainSize;
      bestVar = v;
    }
  }
  return bestVar!;
};

// --- HEURÍSTICA DE GRAU ---
export const selectUnassignedVariable_Degree = (
  unassignedVars: Variable[],
  domains: Record<Variable, Domain>,
  mode: SudokuMode,
): Variable => {
  if (unassignedVars.length === 0) {
    throw new Error("A função de heurística de grau foi chamada sem variáveis livres.");
  }

  const constraintGraph = getConstraintGraph(mode);

  let bestVar: Variable | null = null;
  let maxDegree = -1;

  for (const v of unassignedVars) {
    const degree = constraintGraph[v].filter(neighbor => 
      unassignedVars.includes(neighbor)
    ).length;

    if (degree > maxDegree) {
      maxDegree = degree;
      bestVar = v;
    }
  }

  return bestVar!;
};