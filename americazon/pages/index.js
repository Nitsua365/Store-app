import React from 'react';
import redis from 'lib/redisClient'

import { QueryClient, QueryClientProvider } from "react-query";

import SearchBar from "components/SearchBar";

const queryClient = new QueryClient();


export default function Home({ departments }) {

  return (
    <>
      <QueryClientProvider client={queryClient}>
        <div>
          <SearchBar departments={departments} />
        </div>
      </QueryClientProvider>
    </>
  )
}

export async function getStaticProps() {

  let departments = await redis.keys('amazon_department:*')

  // clean and sort results
  departments = departments.map(n => n.substring(n.indexOf(':') + 1))
  departments.sort((a, b) => a.localeCompare(b));

  departments = departments.filter(item => !item.toLowerCase().includes('amazon') && !item.toLowerCase().includes('alexa') && !item.toLowerCase().includes('prime'))

  return {
    props : {
      departments
    },
  }
}
