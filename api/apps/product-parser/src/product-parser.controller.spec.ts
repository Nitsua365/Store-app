import { Test, TestingModule } from '@nestjs/testing';
import { ProductParserController } from './product-parser.controller';
import { ProductParserService } from './product-parser.service';

describe('ProductParserController', () => {
  let productParserController: ProductParserController;

  beforeEach(async () => {
    const app: TestingModule = await Test.createTestingModule({
      controllers: [ProductParserController],
      providers: [ProductParserService],
    }).compile();

    productParserController = app.get<ProductParserController>(ProductParserController);
  });

  describe('root', () => {
    it('should return "Hello World!"', () => {
      expect(productParserController.getHello()).toBe('Hello World!');
    });
  });
});
