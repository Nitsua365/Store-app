import redis from 'lib/redisClient'
import NextCors from 'nextjs-cors';

export default async function handler(req, res) {

    await NextCors(req, res, {
        // Options
        methods: ['GET'],
        origin: 'http://localhost:3000',
        optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
     });

    const { method, query } = req;

    switch (method) {
        case 'GET':
            const resp = await redis.call('FT.SEARCH', 'index:amazon_products', query.searchString, 'LIMIT', '0', '200')

            // get the ASIN's
            let filter = resp.filter(m => (!Array.isArray(m)))
            const [ totalResults ] = filter.splice(0, 1)

            // get the arrays of data and squash them into a list of JSON objects
            let arrays = resp.filter(m => Array.isArray(m)).map(obj => {
                const keys = obj.filter((obj, filIdx) => (filIdx % 2 == 0) )
                const values = obj.filter((obj, valIdx) => (valIdx % 2 == 1 || !obj))

                let zipped = {}
                keys.forEach((key, idx) => zipped[key] = values[idx])

                return zipped;
            })
            
            // zip the asins and the data together
            const zipped = filter
                            .map((obj, idx) => ({ asin: obj.substring(obj.indexOf(':') + 1), ...arrays[idx] }))
                            .filter(item => item.countryoforigin.toUpperCase().includes('USA') || 
                                            item.countryoforigin.toLowerCase().includes('united states') || 
                                            item.countryoforigin.toLowerCase().includes('states'))

            res.status(200).json({ results: zipped.length, data: zipped });
            break;
        default:
            res.status(404).send(`Bad Request ${method}`)
    }

}