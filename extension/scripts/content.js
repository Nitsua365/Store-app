

async function getASIN() {
  let asins = Array.from(document.querySelectorAll("[data-asin]"))
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