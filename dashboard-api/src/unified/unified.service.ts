import { Injectable } from '@nestjs/common';
import { readFileSync } from 'fs';
import * as path from 'path';

@Injectable()
export class UnifiedService {
  getUnifiedData(): any {
    const filePath = path.join(__dirname, '../../src/data/unified.json');
    const jsonData = readFileSync(filePath, 'utf-8');
    return JSON.parse(jsonData);
  }
}
