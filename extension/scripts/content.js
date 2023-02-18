(async function () {

  // get all asins from the page
  const asins = [...new Set(Array.from(document.querySelectorAll("[data-asin]"))
    .map(asin => asin.attributes[0])
    .map(asinData => asinData?.value || "")
    .filter(asinFilt => /([A-Z][0-9])+/.test(asinFilt)))]

  // fetch asins that need fetching
  const result = await chrome.runtime.sendMessage({ asins })

  // add COO to the UI
  for (let i = 0; i < asins.length; i++) {
    let productElem = document.querySelector(`[data-asin='${asins[i]}']`)
    if (productElem) {
      let div = document.createElement('div');
      div.textContent = `Country of Origin: ${result[asins[i]]}`

      div.style.color = "black"
      div.style.padding = "2px"
      div.style.borderRadius = "5px"
      div.style.background = "#febd69"
      div.style.borderWidth = "5px"
      div.style.borderColor = "grey"
      div.style.maxWidth = "90%"
      div.style.marginLeft = "5px"

      productElem.style.marginBottom = "50px"

      productElem.appendChild(div)
    }
  }

})();