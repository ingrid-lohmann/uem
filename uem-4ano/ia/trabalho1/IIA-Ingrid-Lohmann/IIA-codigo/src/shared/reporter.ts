import { writeFileSync, existsSync, mkdirSync } from 'fs';
import { Assignment, ReportData } from './types';
import { heuristicLabels, instanceLabels, modeLabels } from './utils';

const formatSudokuGrid = (solution: Assignment): string => {
  const grid: (number | string)[][] = Array(4).fill(0).map(() => Array(4).fill('?'));

  for (const variable in solution) {
    const value = solution[variable];
    // Verifica se a variável corresponde ao padrão C<linha><coluna>
    if (variable.startsWith('C') && value !== undefined) {
      const row = parseInt(variable[1], 10) - 1;
      const col = parseInt(variable[2], 10) - 1;
      // Garante que as coordenadas estão dentro dos limites do tabuleiro 4x4
      if (row >= 0 && row < 4 && col >= 0 && col < 4) {
        grid[row][col] = value;
      }
    }
  }

  const lines: string[] = [];
  const separator = "   +---+---+---+---+";
  lines.push("\n   --- Tabuleiro Final ---");
  lines.push(separator);
  for (let i = 0; i < 4; i++) {
    let line = "   |";
    for (let j = 0; j < 4; j++) {
      line += ` ${grid[i][j]} |`;
    }
    lines.push(line);
    lines.push(separator);
  }
  return lines.join('\n');
}

export const saveReportToFile = (data: ReportData): { content: string; path: string } => {
  const { instance, heuristic, useAC3, result, duration, mode } = data;
  const { ac3Logs } = result;

  const outputLines: string[] = [];
  const modeLabel = modeLabels[mode];
  const heuristicLabel = heuristicLabels[heuristic];
  const instanceLabel = instanceLabels[instance];

  outputLines.push(`✔ Modo do Problema: ${modeLabel}`);
  outputLines.push(`✔ Escolha a instância de teste: ${instanceLabel}`);
  outputLines.push(`✔ Escolha a heurística para resolver o Sudoku: ${heuristicLabel}`);
  outputLines.push(`✔ Deseja usar o pré-processamento AC-3? ${useAC3 ? 'Yes' : 'No'}`);
  outputLines.push(`\n🚀 Iniciando resolvedor...`);
  if (useAC3) {
    outputLines.push(`\n⚙️ Rodando AC-3 para pré-processamento...`);
    if (ac3Logs && ac3Logs.length > 0) {
      outputLines.push(...ac3Logs);
    } else {
      outputLines.push("   [AC-3] Nenhum domínio foi reduzido.");
    }
  }
  outputLines.push("\n-----------------------------------------");
  if (result.solution) {
    outputLines.push("✅ Solução Encontrada:");
    outputLines.push(JSON.stringify(result.solution, null, 2));

    if (mode === 'full') {
      outputLines.push(formatSudokuGrid(result.solution));
    }

  } else {
    outputLines.push("🛑 Nenhuma solução foi encontrada.");
  }
  outputLines.push("\n📊 Métricas de Desempenho:");
  outputLines.push(`   ⏱️  Tempo de Execução: ${duration.toFixed(3)} ms`);
  outputLines.push(`   🪢  Nós Visitados: ${result.metrics.nodesVisited}`);
  outputLines.push(`   ↩️  Backtracks: ${result.metrics.backtracks}`);
  outputLines.push("-----------------------------------------");

  const outputContent = outputLines.join('\n');

  const outputDir = './output';
  const ac3Part = useAC3 ? '_ac3' : '';
  const filename = `${instance}_${heuristic}${ac3Part}.txt`;
  const fullPath = `${outputDir}/${filename}`;

  if (!existsSync(outputDir)) {
    mkdirSync(outputDir);
  }

  writeFileSync(fullPath, outputContent);

  return { content: outputContent, path: fullPath };
};