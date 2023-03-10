import { Test, TestingModule } from '@nestjs/testing';
import { ProductParserController } from './product-parser.controller';

describe('ProductParserController', () => {
  let controller: ProductParserController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ProductParserController],
    }).compile();

    controller = module.get<ProductParserController>(ProductParserController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
