// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

export default async function handler(req, res) {
  // respond with valid status
  res.status(200).json({ message: "Welcome to the Americazon API" });
}

export const config = {
  api: {
    responseLimit: "1kb"
  }
}