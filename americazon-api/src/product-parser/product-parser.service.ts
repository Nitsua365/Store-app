import { Injectable } from '@nestjs/common';
import axios, { AxiosResponse } from 'axios';

import { select1 } from 'xpath';
import { DOMParser } from '@xmldom/xmldom';

@Injectable()
export class ProductParserService {
  async parseProducts(body, headers) {
    function filterCOO(str) {
      return str.replace('\n', '').replace('&lrm;', '').trim();
    }

    const req: AxiosResponse[] = await Promise.all(
      body.urls.map((url: string) => axios.get(url, { responseType: 'text' })),
    );

    const productsHTML = req.map((res) => res.data);

    const products = productsHTML.map((html) => {
      const productDoc = new DOMParser({
        locator: {},
        errorHandler: {
          warning: function (w) {},
          error: function (e) {},
          fatalError: function (e) {
            console.error(e);
          },
        },
      }).parseFromString(html);
      return {
        countryoforigin: filterCOO(
          select1(
            "//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*",
            productDoc,
            // @ts-ignore
          )?.firstChild?.data || '',
        ),
        productname: filterCOO(
          // @ts-ignore
          select1("//*[@id='productTitle']", productDoc)?.firstChild?.data ||
            '',
        ),
      };
    });

    const ASINtoProduct = {};
    for (let i = 0; i < body.asins.length; i++) {
      ASINtoProduct[body.asins[i]] = products[i];
    }

    return ASINtoProduct;
  }
}
