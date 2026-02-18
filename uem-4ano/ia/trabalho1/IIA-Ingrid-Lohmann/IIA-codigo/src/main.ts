import inquirer from 'inquirer';
import { solve } from './solver';
import { performance } from 'perf_hooks';
import { HeuristicOption, InstanceOption, ReportData, SudokuMode } from './shared/types';
import { saveReportToFile } from './shared/reporter';

const main = async () => {
  try {
    const questions = [
      {
        type: 'list',
        name: 'mode',
        message: 'Escolha o modo do problema:',
        choices: [
          { name: 'Parcial (5 variáveis, para análise)', value: 'partial' },
          { name: 'Completo (16 variáveis, 4x4)', value: 'full' },
        ],
      },
      {
        type: 'list',
        name: 'instance',
        message: 'Escolha a instância de teste:',
        choices: (answers: any) => {
          if (answers.mode === 'full') {
            return [
              { name: 'Fácil (Completo)', value: 'full_easy' },
              { name: 'Médio (Completo)', value: 'full_medium' },
              { name: 'Difícil (Completo)', value: 'full_difficult' },
            ];
          }
          return [
            { name: 'Fácil (Parcial)', value: 'easy' },
            { name: 'Médio (Parcial)', value: 'medium' },
            { name: 'Difícil (Parcial)', value: 'difficult' },
          ];
        },
      },
      {
        type: 'list',
        name: 'heuristic',
        message: 'Escolha a heurística para resolver o Sudoku:',
        choices: [
          { name: 'Grau (Heurística de Grau)', value: 'degree' },
          { name: 'MRV (Valores Mínimos Restantes)', value: 'mrv' },
        ],
      },
      {
        type: 'confirm',
        name: 'useAC3',
        message: 'Deseja user o pré-processamento AC-3?',
        default: true,
      }
    ] as const;

    const answers = (await inquirer.prompt(questions)) as unknown as {
      heuristic: HeuristicOption,
      instance: InstanceOption,
      useAC3: boolean;
      mode: SudokuMode,
    };

    const startTime = performance.now();
    const result = solve(answers.heuristic, answers.instance, answers.useAC3, answers.mode);
    const endTime = performance.now();

    const reportData: ReportData = {
      ...answers,
      result,
      duration: endTime - startTime,
    }

    const { content, path } = saveReportToFile(reportData);

    console.log(content);
    console.log(`\n✨ Resultado também foi salvo em: ${path}`);
  } catch (error) {
    console.error("💥 Ocorreu um erro fatal:", error);
  }
}

main();