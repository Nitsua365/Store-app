import redis from 'lib/redisClient'

import HomePage from "components/HomePage";

import { HomeContext } from 'context/HomeContext';

export default function Home({ departments }) {
  return (
    <>
      <HomeContext>
        <HomePage departments={departments} />
      </HomeContext>
    </>
  )
}

export async function getStaticProps() {

  let departments = await redis.keys('amazon_department:*')

  // clean and sort results
  departments = departments.map(n => n.substring(n.indexOf(':') + 1))
  departments.sort((a, b) => a.localeCompare(b));

  departments = departments.filter(item => !item.toLowerCase().includes('amazon') && 
                                            !item.toLowerCase().includes('alexa') && 
                                            !item.toLowerCase().includes('prime') &&
                                            !item.includes('AWS'))

  return {
    props : {
      departments
    },
  }
}

// export const config = {
//   runtime: 'experimental-edge',
// }