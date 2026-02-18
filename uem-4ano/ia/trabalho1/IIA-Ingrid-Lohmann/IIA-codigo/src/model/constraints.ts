import { Assignment, SudokuMode, Variable } from "../shared/types";

export const constraintGraph_partial: Record<Variable, Variable[]> = {
  V1: ['V2', 'V3', 'V4', 'V5'],
  V2: ['V1', 'V3', 'V4', 'V5'],
  V3: ['V1', 'V2', 'V4'],
  V4: ['V1', 'V2', 'V3'],
  V5: ['V1', 'V2'],
};

/**
 * Verifica se uma atribuição parcial satisfaz todas as restrições do Sudoku.
 * @param assignment - O objeto com as variáveis já preenchidas.
 * @returns `true` se as restrições são satisfeitas, `false` caso contrário.
 */
export const areConstraintsSatisfied_partial = (assignment: Assignment): boolean => {
  const firstRowVars: Variable[] = ['V1', 'V2', 'V3', 'V4'];
  const assignedValues = firstRowVars
    .map(v => assignment[v])
    .filter((value): value is number => value !== undefined);
  if (new Set(assignedValues).size !== assignedValues.length) {
    return false;
  }

  if (assignment.V1 !== undefined && assignment.V5 !== undefined && assignment.V1 === assignment.V5) {
    return false;
  }

  const blockVars: Variable[] = ['V1', 'V2', 'V5'];
  const blockValues = blockVars
    .map(v => assignment[v])
    .filter((value): value is number => value !== undefined);
  if (new Set(blockValues).size !== blockValues.length) {
    return false;
  }

  if (assignment.V1 === 1 && assignment.V3 === 2) {
    return false;
  }

  if (assignment.V2 !== undefined && assignment.V4 !== undefined && assignment.V2 === assignment.V4) {
    return false;
  }

  if (
    assignment.V1 !== undefined &&
    assignment.V2 !== undefined &&
    assignment.V3 !== undefined &&
    assignment.V4 !== undefined
  ) {
    if ((assignment.V1 + assignment.V2) === (assignment.V3 + assignment.V4)) {
      return false;
    }
  }

  return true;
};

const areConstraintsSatisfied_full = (assigment: Assignment) => {
  const assignedValues: { variable: Variable, value: number }[] = [];

  for (const variable in assigment) {
    const value = assigment[variable];

    if (value !== undefined) {
      assignedValues.push({ variable, value });
    }
  }

  for (let i = 0; i < assignedValues.length; i++) {
    for (let j = i + 1; j < assignedValues.length; j++) {
      const v1 = assignedValues[i].variable;
      const v2 = assignedValues[j].variable;
      const val1 = assignedValues[i].value;
      const val2 = assignedValues[j].value;

      const row1 = v1[1], col1 = v1[2];
      const row2 = v2[1], col2 = v2[2];

      const block1 = `${Math.floor((parseInt(row1) - 1) / 2)}${Math.floor((parseInt(col1) - 1) / 2)}`;
      const block2 = `${Math.floor((parseInt(row2) - 1) / 2)}${Math.floor((parseInt(col2) - 1) / 2)}`;

      const sameRow = row1 === row2;
      const sameCol = col1 === col2;
      const sameBlock = block1 === block2;

      if ((sameRow || sameCol || sameBlock) && val1 === val2) {
        return false;
      }

    }
  }
  return true;
};

const generateFullGraph = (): Record<Variable, Variable[]> => {
    const graph: Record<Variable, Variable[]> = {};
    const variables: Variable[] = [];
    for (let r = 1; r <= 4; r++) for (let c = 1; c <= 4; c++) variables.push(`C${r}${c}`);

    for (const v1 of variables) {
        graph[v1] = [];
        for (const v2 of variables) {
            if (v1 === v2) continue;
            const r1 = v1[1], c1 = v1[2];
            const r2 = v2[1], c2 = v2[2];
            const b1 = `${Math.floor((parseInt(r1) - 1) / 2)}${Math.floor((parseInt(c1) - 1) / 2)}`;
            const b2 = `${Math.floor((parseInt(r2) - 1) / 2)}${Math.floor((parseInt(c2) - 1) / 2)}`;
            if (r1 === r2 || c1 === c2 || b1 === b2) {
                graph[v1].push(v2);
            }
        }
    }
    return graph;
};

const constraintGraph_full = generateFullGraph();

export const areConstraintsSatisfied = (assignment: Assignment, mode: SudokuMode): boolean => {
    return mode === 'partial' ? areConstraintsSatisfied_partial(assignment) : areConstraintsSatisfied_full(assignment);
};

export const getConstraintGraph = (mode: SudokuMode): Record<Variable, Variable[]> => {
    return mode === 'partial' ? constraintGraph_partial : constraintGraph_full;
};

