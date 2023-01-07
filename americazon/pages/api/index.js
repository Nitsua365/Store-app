// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import NextCors from 'nextjs-cors';

export default async function handler(req, res) {

  await NextCors(req, res, {
    // Options
    methods: ['GET'],
    origin: ['http://192.168.0.199'],
    optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
 });

  // respond with valid status
  res.status(200).json({ message: "Welcome to the Americazon API" });
}

export const config = {
  api: {
    responseLimit: "1kb"
  }
}