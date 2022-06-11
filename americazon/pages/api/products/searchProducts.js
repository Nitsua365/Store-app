import { searchProducts } from '../../../dbClient/utils/amazon_products'

export default async function handler(req, res) {

    const { method, body } = req;

    switch (method) {
        case 'GET':
            const result = await searchProducts(body);
            res.status(200).json(result);
            break;
        default:
            res.status(404).send(`Bad Request ${method}`)
    }

}