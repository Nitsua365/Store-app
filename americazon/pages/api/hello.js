// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import NextCors from 'nextjs-cors';

export default async function handler(req, res) {
  
  // cors middle ware
  await NextCors(req, res, {
    methods: ["GET"],
    origin: '*',
    optionsSuccessStatus: 200,
    preflightContinue: true,
  });

  // respond with valid status
  res.json({ message: "Welcome to the Americazon API" })
}

export const config = {
  api: {
    responseLimit: "1kb"
  }
}