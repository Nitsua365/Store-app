const PrismaClient = require('@prisma/client');
const prisma = new PrismaClient.PrismaClient();
const stringSimilarity = require('string-similarity');

module.exports = {
  getProducts : async (body) => {
    const { name, manufacturer, department } = body;
    
    let products = await prisma.amazon_products.findMany({
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
          },
          {
            department: {
              contains: department
            }
          },
        ]
      },
    }
    )

    return products.sort((a, b) => {
      return (stringSimilarity.compareTwoStrings(b.productname, name) - stringSimilarity.compareTwoStrings(a.productname, name) || stringSimilarity.compareTwoStrings(b.manufacturer, manufacturer) - stringSimilarity.compareTwoStrings(a.manufacturer, manufacturer));
    })

  }
}

