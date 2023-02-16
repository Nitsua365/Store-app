import { NestFactory } from '@nestjs/core';
import { ProductParserModule } from './product-parser.module';

async function bootstrap() {
  const app = await NestFactory.create(ProductParserModule);
  await app.listen(3000);
}
bootstrap();
