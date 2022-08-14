const { MeiliSearch } = require("meilisearch");

const meiliClient = new MeiliSearch({
  host: process.env.MEILI_HOST,
  apiKey: process.env.MEILI_KEY
});

const productIndex = meiliClient.index("amazon_products")

// update searchable attributes
// productIndex.updateSearchableAttributes([
//   'productname',
//   'department',
//   'manufacturer'
// ])

// // update filters
// productIndex.updateFilterableAttributes([
//   "countryoforigin"
// ])

// // update sortable attributes
// productIndex.updateSortableAttributes([
//   'datescrapped'
// ])

// // max out results
// productIndex.updateSettings({ pagination: { maxTotalHits: 250 }})

module.exports = {
  meiliClient, 
  productIndex  
}