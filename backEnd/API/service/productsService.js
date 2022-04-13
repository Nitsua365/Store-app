const dbClient = require("../../databaseClient/dbClient")
const PrismaClient = require('@prisma/client');
const prisma = new PrismaClient.PrismaClient();

module.exports = {
  getAllProductDepartments : async () => {
    return (await dbClient.query("SELECT name FROM amazon_department")).rows.map(d => d.name);
  },
  getProducts : async (body) => {
    const { name, manufacturer } = body;
    
    return await prisma.amazon_products.findMany({
      where : {
        OR: [
          {
            productname: {
              contains : name
            },
          },
          {
            manufacturer: {
              contains: manufacturer
            },
          }
        ]
      },
      orderBy: { 
        productname : 'asc'
      }
    }
    )

  }
}

