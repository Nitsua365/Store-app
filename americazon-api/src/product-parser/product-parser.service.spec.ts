import { Test, TestingModule } from '@nestjs/testing';
import { ProductParserService } from './product-parser.service';

describe('ProductParserService', () => {
  let service: ProductParserService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ProductParserService],
    }).compile();

    service = module.get<ProductParserService>(ProductParserService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
