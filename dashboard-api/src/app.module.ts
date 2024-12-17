import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MoviesModule } from './movies/movies.module';
import { UnifiedModule } from './unified/unified.module';

@Module({
  imports: [MoviesModule, UnifiedModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
