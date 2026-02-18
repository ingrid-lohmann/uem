import { readFileSync } from "fs";
import { CSP, Domain, InstanceOption, SudokuMode, Variable } from "../shared/types";

const getVariables = (mode: SudokuMode): Variable[] => {
  if (mode === 'partial') {
    return ['V1', 'V2', 'V3', 'V4', 'V5'];
  }

  const variables: Variable[] = [];
  const rowsCols = [1, 2, 3, 4];

  for (const row of rowsCols) {
    for (const col of rowsCols) {
      variables.push(`C${row}${col}`);
    }
  }
  return variables;
}

export const createSudokuCSP = (instanceName: InstanceOption, mode: SudokuMode): CSP => {
  const variables: Variable[] = getVariables(mode);
  const domains = {} as Record<Variable, Domain>;

  for (const v of variables) {
    domains[v] = [1, 2, 3, 4];
  }

  try {
    const filePath = `./src/instances/${mode}/${instanceName}.json`;
    const fileContent = readFileSync(filePath, 'utf-8');
    const instanceConfig = JSON.parse(fileContent);

    for (const varName in instanceConfig) {
      const value = instanceConfig[varName];
      if (typeof value === 'number') {
        domains[varName as Variable] = [value];
      } else if (Array.isArray(value)) {
        domains[varName as Variable] = value;
      }
    }
  } catch (error) {
    console.error(`⚠️ Erro ao carregar a instância '${instanceName}.json'. Verifique se o arquivo existe.`);
    throw error;
  }

  return { variables, domains };
};
