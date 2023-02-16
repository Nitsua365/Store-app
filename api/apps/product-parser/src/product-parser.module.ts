import { Module } from '@nestjs/common';
import { ProductParserController } from './product-parser.controller';
import { ProductParserService } from './product-parser.service';

@Module({
  imports: [],
  controllers: [ProductParserController],
  providers: [ProductParserService],
})
export class ProductParserModule {}
