import xpath from 'xpath'
import { DOMParser } from '@xmldom/xmldom';

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

    function filterCOO(str) {
      return str.replace('\n', '').replace('&lrm;', '').trim();
    }

    if (request.asins) {

      let asinURLS = request.asins.map(asin => `https://www.amazon.com/dp/${asin}`)

      // fetch the URLS
      Promise.all(asinURLS.map((url) => fetch(url))).then((req) => {

        // resolve them to text
        Promise.all(req.map((res) => res.text())).then((productsHTML) => {

          // parse productsHTML pages to get necessary data ie: COO and product name
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
            }).parseFromString(html, undefined);
            return {
              countryoforigin: filterCOO(
                xpath.select1(
                  "//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*",
                  productDoc,
                  // @ts-ignore
                )?.firstChild?.data || '',
              ),
              productname: filterCOO(
                // @ts-ignore
                xpath.select1("//*[@id='productTitle']", productDoc)?.firstChild?.data ||
                  '',
              ),
            };
          });
      
          // Map ASINs to product data
          const result = {};
          for (let i = 0; i < request.asins.length; i++) {
            result[request.asins[i]] = products[i];
          }
    
          // send response back to the content script
          sendResponse(result)
        })
      })

    }

    return true;
  }
);