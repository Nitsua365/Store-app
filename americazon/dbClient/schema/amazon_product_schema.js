import { Entity, Schema } from "redis-om";

class amazon_products extends Entity {}

const amazon_product_schema = new Schema(amazon_products, {
    productname: { type: 'text', textSearch: true },
    department: { type: 'text', textSearch: true },
    manufacturer: { type: 'text', textSearch: true },
    rating: { type: 'point' },
    affiliatelink: { type: 'string' },
    price: { type: 'point' },
    datescrapped: { type: 'date' },
    countryoforigin: { type: 'string' },
    picturereflink: { type: 'string' },
    productpagelink: { type: 'string' }
},  { dataStructure: 'HASH' });

export default amazon_product_schema;