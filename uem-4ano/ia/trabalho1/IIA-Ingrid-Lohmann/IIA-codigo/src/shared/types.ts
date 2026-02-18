export type SudokuMode = 'partial' | 'full';

export type Variable = string;

export type Domain = number[];

export interface CSP {
  variables: Variable[];
  domains: Record<Variable, Domain>;
}

export type Assignment = Partial<Record<Variable, number>>;

export type HeuristicOption = 'mrv' | 'degree';

export type InstanceOption = 'easy' | 'medium' | 'difficult';

export type HeuristicFunction = (
  unassignedVars: Variable[],
  domains: Record<Variable, Domain>,
  mode: SudokuMode
) => Variable;

export type SearchMetrics = {
  nodesVisited: number;
  backtracks: number;
};

export type ReportData = {
  instance: InstanceOption;
  heuristic: HeuristicOption;
  useAC3: boolean;
  mode: SudokuMode;
  result: {
    solution: Assignment | null;
    metrics: SearchMetrics;
    ac3Logs: string[];
  };
  duration: number;
};