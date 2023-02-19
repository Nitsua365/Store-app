import xpath from 'xpath'
import { DOMParser } from '@xmldom/xmldom';

const fetchASIN = async (asins) => {

  const filterCOO = (str) => str.replace('\n', '').replace('&lrm;', '').trim()

  if (!asins.length) return;

  // get the URL that need to be fetched
  // const getAsinCache = await Promise.all(asins.map(asin => chrome.storage.session.get([asin])))
  // const asinFetch = asins.filter((asin, idx) => !Object.keys(getAsinCache[idx]).length)

  // console.log(getAsinCache)
  // console.log(asinFetch)
  
  // get the asin URLs
  const asinURLS = asins.map(asin => `https://www.amazon.com/dp/${asin}`)
  
  // fetch the URLS
  const req = await Promise.all(asinURLS.map((url) => fetch(url)))

  // resolve them to text
  const productsHTML = await Promise.all(req.map((res) => res.text()))
    
  // parse productsHTML pages to get necessary data ie: COO
  const productCOO = productsHTML.map((html) => {
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
    return filterCOO(
        xpath.select1(
          "//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*",
          productDoc,
          // @ts-ignore
        )?.firstChild?.data || '',
      );
  });

  // await Promise.all(asinFetch.map((asin, idx) => chrome.storage.session.set({ [asin] : productCOO[idx] })))

  // Map ASINs to product data
  // const cache = await Promise.all(asins.map(asin => chrome.storage.session.get([asin])))

  const result = {}
  for (let i = 0; i < asins.length; i++) {
    result[asins[i]] = productCOO[i] || "Unknown"
  }

  // send response back to the content script
  return result;

}

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.asins) fetchASIN(request.asins).then(res => sendResponse(res))
    return true;
  }
);

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.status === "complete" && tab.active) {
    chrome.scripting.executeScript({
      target: { tabId }, 
      files: ["dist/content-bundle.js"]
    })
  }
});