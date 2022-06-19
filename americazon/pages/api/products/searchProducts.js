import redis from '../../../lib/redisClient'

export default async function handler(req, res) {

    const { method, query } = req;


    switch (method) {
        case 'GET':
            const resp = await redis.call('FT.SEARCH', 'index:amazon_products', query.searchString, 'LIMIT', '0', '200')

            // get the asins
            let filter = resp.filter(m => { if (!Array.isArray(m)) return m; })
            filter.splice(0, 1);

            // get the arrays of data and squash them into a list of JSON objects
            let arrays = resp.filter(m => { if (Array.isArray(m)) return m; }).map(obj => {
                const keys = obj.filter((obj, filIdx) => { if (filIdx % 2 == 0 ) { return obj; } })
                const values = obj.filter((obj, valIdx) => { if (valIdx % 2 == 1) { return obj; } })
                
                let zipped = {}
                keys.forEach((key, idx) => zipped[key] = values[idx] ? values[idx] : '' )

                return zipped;
            })
            
            // zip the asins and the data together
            const zipped = filter.map((obj, idx) => ({ asin: obj.substring(obj.indexOf(':') + 1), ...arrays[idx] }))

            res.status(200).json({ results: zipped.length, data: zipped });
            break;
        default:
            res.status(404).send(`Bad Request ${method}`)
    }

}

export const config = {
    api: {
        responseLimit: false,
    },
}