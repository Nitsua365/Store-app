(async function () {

  // get all asins from the page
  const asins = Array.from(document.querySelectorAll("[data-asin]"))
    .map(asin => asin.attributes[0])
    .map(asinData => asinData?.value || "")
    .filter(asinFilt => /([A-Z][0-9])+/.test(asinFilt))

  console.log(asins)

  // fetch asins that need fetching
  const result = await chrome.runtime.sendMessage({ asins })

  console.log(result)

  // add COO to the UI
  for (let i = 0; i < asins.length; i++) {
    let productElem = document.querySelector(`[data-asin='${asins[i]}']`)
    if (productElem) {
      let div = document.createElement('div');
      div.textContent = `Country of Origin: ${result[asins[i]]}`

      div.style.color = "Red"
      div.style.paddingBottom = "4px"
      div.style.marginBottom = "2px"

      productElem.firstElementChild.firstElementChild.firstElementChild.appendChild(div)
    }
  }

})();

getASIN();