import { Client } from "redis-om";

const client = new Client();

const connect = async () => {
    if (!client.isOpen()) {
        await client.open(process.env.REDIS_URL)
    }
};

export { connect, client };