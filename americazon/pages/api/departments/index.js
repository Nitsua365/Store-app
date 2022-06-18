import redis from '../../../lib/redisClient'

export default async function handler(req, res) {

    const { method } = req;

    switch (method) {
        case 'GET':
            let departments = await redis.keys('amazon_department:*')

            departments = departments.map(n => n.substring(n.indexOf(':') + 1))

            res.json(departments);
            break;
        default:
            res.send("invalid method: " + method);
    }

}