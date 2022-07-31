const { MeiliSearch } = require("meilisearch");

const meiliClient = new MeiliSearch({
  host: process.env.MEILI_HOST,
  apiKey: process.env.MEILI_KEY
});

module.exports = {
  meiliClient, 
  productIndex: meiliClient.index("amazon_products") 
}