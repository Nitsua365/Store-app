import xpath from 'xpath'
import { DOMParser } from '@xmldom/xmldom';

const COO_XPATH = "//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*"

const dom_parser = new DOMParser({
  locator: {},
  errorHandler: {
    warning: function (w) {},
    error: function (e) {},
    fatalError: function (e) { console.error(e) },
}})

const parseCOO = async (html) => {
  const filterCOO = (str) => str.replace('\n', '').replace('&lrm;', '').trim()
  return filterCOO(xpath.select1(COO_XPATH, dom_parser.parseFromString(html, "text/html"))?.firstChild?.data || '')
}

const parseBulk = async (p_HTML) => {
  const productCOOPromises = p_HTML.map((html) => parseCOO(html));
  const productCOO = await Promise.all(productCOOPromises);
  return productCOO;
}

const fetchASIN = async (asins) => {

  if (!asins.length) return;
  
  // get the asin URLs
  const asinURLS = asins.map(asin => `https://www.amazon.com/dp/${asin}`)

  // resolve them to text
  const fetch_start = performance.now()
  const productsHTML = await Promise.all(
    (await Promise.all(asinURLS.map((url) => fetch(url))))
      .filter(res => res.ok)
      .map((res) => res.text()))
  console.log(`FETCH TIME: ${(performance.now() - fetch_start)}`)
  
  
  // parse productsHTML pages to get necessary data ie: COO
  const parse_start = performance.now()
  const productCOO = await parseBulk(productsHTML);
  console.log(`PARSE TIME: ${(performance.now() - parse_start)}`)

  // create the result
  const result = {}
  for (let i = 0; i < asins.length; i++) {
    result[asins[i]] = productCOO[i] || ""
  }

  console.log(`FETCHED RESULT COUNT: ${productCOO.length}`)

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
  const { status, active, url } = tab
  if (/https:\/\/.*amazon.com\/(?:s|b|gp).*/.test(url) && changeInfo.status === 'complete' && status === 'complete' && active) {
    chrome.scripting.executeScript({
      target: { tabId },
      files: ["content-bundle.js"]
    })
  }
});