import { readFileSync } from 'node:fs';
import { parseThresholds } from '../src/thresholds.ts';

const tables = JSON.parse(readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(parseThresholds(tables)));
