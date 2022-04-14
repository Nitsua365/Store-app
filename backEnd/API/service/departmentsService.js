const dbClient = require("../../databaseClient/dbClient")

module.exports = {
    getAllProductDepartments : async () => {
        return (await dbClient.query("SELECT name FROM amazon_department")).rows.map(d => d.name);
    }
}