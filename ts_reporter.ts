
import * as fs from 'fs';
import * as path from 'path';
import { performance } from 'perf_hooks';

export function logRow(outPath: string, file: string, func: string, values: unknown, result: string, elapsed: number) {
  const dir = path.dirname(outPath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  if (!fs.existsSync(outPath)) {
    fs.writeFileSync(outPath, '| file | function | test values | result | elapsed time |\n|---|---|---|---|---|\n', 'utf8');
  }
  fs.appendFileSync(outPath, `| ${file} | ${func} | ${JSON.stringify(values)} | ${result} | ${elapsed.toFixed(4)}s |\n`, 'utf8');
}

export async function timed<T>(fn: () => Promise<T> | T): Promise<{res: T, elapsed: number}> {
  const start = performance.now();
  const res = await fn();
  const elapsed = (performance.now() - start) / 1000;
  return { res, elapsed };
}
