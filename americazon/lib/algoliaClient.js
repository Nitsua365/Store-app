const algoliasearch = require('algoliasearch')

const client = algoliasearch('NNQKCWQ55R', process.env.ALGOLIA_KEY)

const amazon_product_index = client.initIndex('amazon_products')

amazon_product_index.setSettings({
    attributesForFaceting: [
      'countryoforigin'
    ]
  }).then(() => {
    // done
  });

module.exports = {
    productIndex: amazon_product_index
}