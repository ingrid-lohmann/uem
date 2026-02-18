import { areConstraintsSatisfied, getConstraintGraph } from '../model/constraints';
import { CSP, SudokuMode, Variable } from '../shared/types';

const hasSupport = (Vi: Variable, x: number, Vj: Variable, csp: CSP, mode: SudokuMode): boolean => {
  for (const y of csp.domains[Vj]) {
    if (areConstraintsSatisfied({ [Vi]: x, [Vj]: y }, mode)) {
      return true;
    }
  }
  return false; 
}

const revise = (Vi: Variable, Vj: Variable, csp: CSP, mode: SudokuMode): { revised: boolean; removedValue: number | null } => {
  const domain_i = [...csp.domains[Vi]]; 

  for (const x of domain_i) {
    if (!hasSupport(Vi, x, Vj, csp, mode)) {
      csp.domains[Vi] = csp.domains[Vi].filter(val => val !== x);
      return {revised: true, removedValue: x};
    }
  }
  return { revised: false, removedValue: null };
}

/**
 * Executa o algoritmo AC-3 para garantir a consistência de arco.
 * Modifica o CSP diretamente, removendo valores dos domínios.
 * @returns `true` se o CSP ainda for consistente, `false` se uma inconsistência foi encontrada.
 */
export const ac3 = (csp: CSP, mode: SudokuMode): { isConsistent: boolean; logs: string[] } => {
  const logs: string[] = [];
  const queue: [Variable, Variable][] = [];
  const constraintGraph = getConstraintGraph(mode);

  for (const v of csp.variables) {
    for (const neighbor of constraintGraph[v]) {
      queue.push([v, neighbor]);
    }
  }

  while (queue.length > 0) {
    const [Vi, Vj] = queue.shift()!;
    const { revised, removedValue } = revise(Vi, Vj, csp, mode);

    if (revised) {
      logs.push(`  ❌ [AC-3] Removendo valor ${removedValue} do domínio de ${Vi} (conflito com ${Vj})`);
      if (csp.domains[Vi].length === 0) {
        return { isConsistent: false, logs }; 
      }

      for (const Vk of constraintGraph[Vi]) {
        if (Vk !== Vj) {
          queue.push([Vk, Vi]);
        }
      }
    }
  }

  return { isConsistent: true, logs }; 
}