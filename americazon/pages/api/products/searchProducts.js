import redis from '../../../lib/redisClient'

export default async function handler(req, res) {

    const { method, body } = req;

    switch (method) {
        case 'GET':
            if (typeof body !== 'string') {
                res.status(400).send(`Body must be type \'string\'`)
            }

            const resp = await redis.call('FT.SEARCH', 'index:amazon_products', body)
            res.status(200).json(resp);
            break;
        default:
            res.status(404).send(`Bad Request ${method}`)
    }

}