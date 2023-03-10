import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ProductsController } from './products/products.controller';
import { ProductsService } from './products/products.service';
import { UsersController } from './users/users.controller';
import { UsersService } from './users/users.service';
import { UsersModule } from './users/users.module';
import { ProductsModule } from './products/products.module';
import { AuthController } from './auth/auth.controller';
import { AuthService } from './auth/auth.service';
import { AuthModule } from './auth/auth.module';
import { ProductParserController } from './product-parser/product-parser.controller';
import { ProductParserService } from './product-parser/product-parser.service';
import { ProductParserModule } from './product-parser/product-parser.module';

@Module({
  imports: [UsersModule, ProductsModule, AuthModule, ProductParserModule],
  controllers: [
    AppController,
    ProductsController,
    UsersController,
    AuthController,
    ProductParserController,
  ],
  providers: [
    AppService,
    ProductsService,
    UsersService,
    AuthService,
    ProductParserService,
  ],
})
export class AppModule {}
