(async function () {

  // get all asins from the page
  const asins = Array.from(document.querySelectorAll("[data-asin]"))
    .map(asin => asin.attributes[0])
    .map(asinData => asinData?.value || "")
    .filter(asinFilt => /([A-Z][0-9])+/.test(asinFilt))

  // fetch asins that need fetching
  const result = await chrome.runtime.sendMessage({ asins })

  console.log(result)

  // add COO to the UI
  for (let i = 0; i < asins.length; i++) {
    let productElem = document.querySelector(`[data-asin='${asins[i]}']`)
    if (productElem) {
      let div = document.createElement('div');
      div.textContent = `Country of Origin: ${result[asins[i]]}`

      div.style.color = "#2584f7"
      div.style.padding = "2px"
      div.style.marginBottom = "50px"
      div.style.borderRadius = "5px"
      div.style.background = "#79effc"

      productElem
        .lastElementChild
        .lastElementChild
        .appendChild(div)
    }
  }

})();