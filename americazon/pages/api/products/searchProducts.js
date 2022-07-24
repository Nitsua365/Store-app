// import redis from 'lib/redisClient'
// import redisHashToJSON from 'utils/redisHashToJSON';

import { productIndex } from "lib/algoliaClient";

export default async function handler(req, res) {

    const { method, query } = req;

    switch (method) {
        case 'GET':

            if (!query.searchString || !query.searchString.length)
                res.status(404).json({ message: 'Invalid Search String' })

            const queryResults = await productIndex.search(query.searchString, {
                filters: 'countryoforigin:USA',
                page: query.page,
                hitsPerPage: query.pageMax
            })

            res.status(200).json({ queryResults, results: queryResults.nbHits  });
            break;
        default:
            res.status(404).send(`Bad Request ${method}`)
    }

}