import { Controller, Get } from '@nestjs/common';
import { UnifiedService } from './unified.service';

@Controller('unified')
export class UnifiedController {
  constructor(private readonly unifiedService: UnifiedService) {}

  @Get()
  getUnifiedData() {
    return this.unifiedService.getUnifiedData();
  }
}
