

export default async function handler(req, res) {

    const { method } = req;

    switch (method) {
        case 'GET':
            res.send(`got ${method}`)
            break;
        default:
            res.send("invalid method: " + method);
    }

}