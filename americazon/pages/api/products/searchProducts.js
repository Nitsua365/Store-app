import redis from 'lib/redisClient'
import redisHashToJSON from 'utils/redisHashToJSON';

export default async function handler(req, res) {

    const { method, query } = req;

    switch (method) {
        case 'GET':

            if (!query.searchString || !query.searchString.length)
                res.status(404).json({ message: 'Invalid Search String' })
            

            // redis full text search and levenstein distance
            let leven = await Promise
                                .all( [ redis.call('FT.SEARCH', 'index:amazon_products', query.searchString), 
                                        (await Promise
                                                .all(query.searchString.split(' ')
                                                .map(item => redis.call('FT.SEARCH', 'index:amazon_products', `%${item}%`))))
                                                .flat() ] )

            const results = redisHashToJSON(Array.from(new Set(leven.flat())), 'asin').filter(item => 
                                                    item.countryoforigin.toUpperCase().includes('USA') || 
                                                    item.countryoforigin.toLowerCase().includes('united states') || 
                                                    item.countryoforigin.toLowerCase().includes('states'))


            res.status(200).json({ results: results.length, data: results });
            break;
        default:
            res.status(404).send(`Bad Request ${method}`)
    }

}