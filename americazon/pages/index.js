import { QueryClient, QueryClientProvider } from "react-query";

import redis from 'lib/redisClient'

import HomePage from "components/HomePage";

export default function Home({ departments }) {

  const queryClient = new QueryClient();

  return (
    <>
      <QueryClientProvider client={queryClient}>
        <HomePage departments={departments} />
      </QueryClientProvider>
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
                                            !item.toLowerCase().includes('prime'))

  return {
    props : {
      departments
    },
  }
}