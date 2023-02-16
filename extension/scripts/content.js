const xpath = require("xpath")
const { DOMParser } = require("@xmldom/xmldom")

async function getASIN() {
  // const response = await chrome.runtime.sendMessage({greeting: "hello"});
  // // do something with response here, not outside the function
  // console.log(response);

  let doc = new DOMParser({
    locator: {},
    errorHandler: { 
      warning: function (w) { }, 
      error: function (e) { }, 
      fatalError: function (e) { console.error(e) } 
    }
  }).parseFromString(document.body.innerHTML)

  let asins = xpath.select("//div[@data-index and @data-asin and @data-uuid]", doc)
    .map(asin => asin.attributes[0])
    .map(asinData => asinData?.value || "")
    .filter(asinFilt => /([A-Z][0-9])+/.test(asinFilt))

  const result = await chrome.runtime.sendMessage({
    asins
  })

  console.log(result)

  // for (let i = 0; i < asins.length; i++) {
  //   let productElem = document.querySelector(`[data-asin='${result[asins[i]].countryoforigin}']`)
  //   console.log(productElem)
  //   if (productElem) {
  //     let div = document.createElement('div');
  //     div.innerHTML = `<div>${result[asins[i]].countryoforigin}</div>`
  //     productElem.firstElementChild.appendChild(div)
  //   }
  // }

}

getASIN();