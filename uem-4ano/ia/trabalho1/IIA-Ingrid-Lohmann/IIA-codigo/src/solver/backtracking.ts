import { areConstraintsSatisfied } from "../model/constraints";
import { Assignment, CSP, HeuristicFunction, SearchMetrics, SudokuMode } from "../shared/types";

export const backtrack = (
  assignment: Assignment,
  csp: CSP,
  selectVariable: HeuristicFunction,
  metrics: SearchMetrics,
  mode: SudokuMode,
): Assignment | null => {
  metrics.nodesVisited++; 

  if (Object.keys(assignment).length === csp.variables.length) {
    return assignment;
  }

  const unassignedVars = csp.variables.filter(v => !(v in assignment));
  const currentVar = selectVariable(unassignedVars, csp.domains, mode);

  for (const value of csp.domains[currentVar]) {
    const localAssignment = { ...assignment, [currentVar]: value };

    if (areConstraintsSatisfied(localAssignment, mode)) {
      const result = backtrack(localAssignment, csp, selectVariable, metrics, mode);
      if (result !== null) {
        return result;
      }
    }
  }

  metrics.backtracks++;
  return null;
};