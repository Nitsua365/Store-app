import redis from 'lib/redisClient'

export default async function handler(req, res) {

    const { method } = req;

    switch (method) {
        case 'GET':
            // get all department names 
            let departments = await redis.keys('amazon_department:*')

            // clean and sort results
            departments = departments.map(n => n.substring(n.indexOf(':') + 1))
            departments.sort((a, b) => a.localeCompare(b));

            res.status(200).json(departments);
            break;
        default:
            res.send("invalid method: " + method);
    }

}