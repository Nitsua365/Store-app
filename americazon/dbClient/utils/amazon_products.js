import amazon_product_schema from "../schema/amazon_product_schema";
import { client, connect } from "../redisClient";
import { Repository } from "redis-om";

const searchProducts = async (searchString) => {
    await connect();

    const repository = new Repository(amazon_product_schema, client);

    console.log(repository);

    // await repository.createIndex();
    
    const result = await repository.search()
        .where('productname').match(searchString)
        .or('department').match(searchString)
        .or('manufacturer').match(searchString)
        .return.all();

    return result;
}

export { searchProducts };