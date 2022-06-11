import redis from "redis-om"

export default async function handler(req, res) {

    const { method } = req;

    switch (method) {
        case 'GET':
            res.status(200).json(            
                await prisma.amazon_department.findMany({
                    where : { 
                        NOT: [{scrapelink : null }] 
                    },
                    select: {
                        name: true
                    }
                })
            )
            break;
        default:
            res.status(405).json({
                message: `operation ${method} is not allowed`
            })
            break;
    }

}