import { Module } from '@nestjs/common';
import { UnifiedService } from './unified.service';
import { UnifiedController } from './unified.controller';

@Module({
  providers: [UnifiedService],
  controllers: [UnifiedController],
})
export class UnifiedModule {}
