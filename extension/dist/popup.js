/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./scripts/content.js":
/*!****************************!*\
  !*** ./scripts/content.js ***!
  \****************************/
/***/ (() => {



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

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
/*!**********************!*\
  !*** ./src/popup.js ***!
  \**********************/
__webpack_require__(/*! ../scripts/content */ "./scripts/content.js")
})();

/******/ })()
;
//# sourceMappingURL=popup.js.map