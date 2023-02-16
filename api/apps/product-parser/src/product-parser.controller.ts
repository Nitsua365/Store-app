import { Controller, Get } from '@nestjs/common';
import { ProductParserService } from './product-parser.service';

@Controller('product-parser')
export class ProductParserController {
  constructor(private readonly productParserService: ProductParserService) {}

  @Get()
  getHello(): string {
    return this.productParserService.getHello();
  }
}
