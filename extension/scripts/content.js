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

async function createLoadingElem() {
  let loadingDiv = document.createElement('div')
  loadingDiv.id = "americazon-loading-icon-wrapper"

  loadingDiv.style.position = "absolute"
  loadingDiv.style.top = "0"
  loadingDiv.style.right = "0"
  loadingDiv.style.backgroundColor = "#fefefe"
  loadingDiv.style.margin = "15% auto"
  loadingDiv.style.padding = "20px"
  loadingDiv.style.width = "100%"
  loadingDiv.style.maxWidth = "100px"
  loadingDiv.style.border = "4px solid #888"
  loadingDiv.style.boxShadow = "0 4px 8px 0 rgba(0,0,0,0.2)"

  let img = document.createElement('img')
  img.src = chrome.runtime.getURL("/America128.png")
  img.alt = "Pic"
  
  loadingDiv.appendChild(img)

  return loadingDiv;
}

async function getCOO() {
  // get all asins from the page
  const asins = [...new Set(Array.from(document.querySelectorAll("[data-asin]"))
    .map(asin => asin.attributes[0])
    .map(asinData => asinData?.value || "")
    .filter(asinFilt => /([A-Z][0-9])+/.test(asinFilt)))]

  console.log('fetching products')

  // create the loading div
  let loadingDiv = await createLoadingElem()
  document.firstElementChild.append(loadingDiv)
  
  // show cached products first
  const asinCache = asins.filter(asin => sessionStorage.getItem(asin))
  addToPage(asinCache)

  // fetch non cached products
  const asinFetch = asins.filter(asin => !sessionStorage.getItem(asin))
  const result = await chrome.runtime.sendMessage({ asins: asinFetch })

  // add to page of fetched results
  addToPage(asinFetch, result)

  // remove loading div
  loadingDiv.remove();

  console.log('product fetching done...')

  // persist to local cache
  if (result) Object.entries(result).forEach(([asin, COO]) => sessionStorage.setItem(asin, COO))

}

setTimeout(function() {
  if (document.readyState === "complete") getCOO()
}, 1650)