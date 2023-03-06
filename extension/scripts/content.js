async function addToPage(asins, result={}) {
  // add COO to the UI
  for (let i = 0; i < asins.length; i++) {
    let productElem = document.querySelector(`[data-asin='${asins[i]}']`)
    if (productElem) {
      let div = document.createElement('div');
      div.textContent = `Country of Origin: ${sessionStorage.getItem(asins[i]) || result[asins[i]] || "Unknown"}`

      div.style.color = "black"
      div.style.padding = "2px"
      div.style.borderRadius = "5px"
      div.style.background = "#febd69"
      div.style.borderWidth = "5px"
      div.style.borderColor = "grey"
      div.style.maxWidth = "90%"
      div.style.marginLeft = "5px"

      productElem.style.marginBottom = "50px"

      productElem.style.height = "90%"

      productElem.appendChild(div)
    }
  }
}

async function getCOO() {
  // get all asins from the page
  const asins = [...new Set(Array.from(document.querySelectorAll("[data-asin]"))
    .map(asin => asin.attributes[0])
    .map(asinData => asinData?.value || "")
    .filter(asinFilt => /([A-Z][0-9])+/.test(asinFilt)))]
  
  // show cached products first
  const asinCache = asins.filter(asin => sessionStorage.getItem(asin) !== null)
  addToPage(asinCache)

  // fetch non cached products
  const asinFetch = asins.filter(asin => sessionStorage.getItem(asin) === null)
  const result = await chrome.runtime.sendMessage({ asins: asinFetch })

  // add to page of fetched results
  addToPage(asinFetch, result);

  // persist to local cache
  if (result) Object.entries(result).forEach(([asin, COO]) => sessionStorage.setItem(asin, COO))

}

setTimeout(function() {
  if (document.readyState === "complete")
    getCOO()
}, 1500)