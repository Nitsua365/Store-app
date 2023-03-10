import { Injectable } from '@nestjs/common';

@Injectable()
export class ProductParserService {
  getHello(): string {
    return 'Hello World!';
  }
}
