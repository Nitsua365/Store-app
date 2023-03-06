import xpath from 'xpath'
import { DOMParser } from '@xmldom/xmldom';

const fetchASIN = async (asins) => {

  const filterCOO = (str) => str.replace('\n', '').replace('&lrm;', '').trim()
  const parseCOO = async (html) => filterCOO(
    xpath.select1("//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*",
    new DOMParser({
      locator: {},
      errorHandler: {
        warning: function (w) {},
        error: function (e) {},
        fatalError: function (e) { console.error(e) },
      },
    }).parseFromString(html, 'text/html'),
    )?.firstChild?.data || '',
  )

  if (!asins.length) return;
  
  // get the asin URLs
  const asinURLS = asins.map(asin => `https://www.amazon.com/dp/${asin}`)
  
  // fetch the URLS
  const fTime = performance.now()
  const req = await Promise.all(asinURLS.map((url) => fetch(url)))
  console.log(`fetch time: ${(performance.now() - fTime)}`);

  // resolve them to text
  const t1 = performance.now()
  const productsHTML = await Promise.all(req.map((res) => res.text()))
  console.log(`text time: ${performance.now() - t1}`);
    
  const t2 = performance.now()
  // parse productsHTML pages to get necessary data ie: COO
  const productCOO = await Promise.all(productsHTML.map(parseCOO))
  console.log(`parsing HTML: ${performance.now() - t2}`);

  // create the result 
  const result = {}
  for (let i = 0; i < asins.length; i++) {
    result[asins[i]] = productCOO[i] || ""
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
  const { status, active, url } = tab
  if (/https:\/\/.*amazon.com.*/.test(url) && changeInfo.status === "complete" && status === "complete" && active) {
    // console.log("EXECUTING AMAZON: " + url)
    chrome.scripting.executeScript({
      target: { tabId }, 
      files: ["dist/content-bundle.js"]
    })
  }
});