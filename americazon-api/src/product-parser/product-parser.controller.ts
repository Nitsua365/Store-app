import { Body, Controller, Get, Head, Post, Headers } from '@nestjs/common';
import { ProductParserService } from './product-parser.service';

@Controller('product-parser')
export class ProductParserController {
  constructor(private readonly productParserService: ProductParserService) {}

  @Post()
  parseProducts(@Body() req, @Headers() headers) {
    return this.productParserService.parseProducts(req, headers);
  }
}
