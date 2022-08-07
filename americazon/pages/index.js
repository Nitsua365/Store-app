import redis from 'lib/redisClient'
import React, { useRef, useState } from 'react';
import LoadingIcon from 'components/LoadingIcon';

import SearchBar from "components/SearchBar";
import Header from 'components/Header';

import { HomeContext } from 'context/HomeContext';

export default function Home({ departments }) {
  const queryRef = useRef();
  const [isLoading, setIsLoading] = useState(false)

  return (
    <>
      <HomeContext>
        <div>
          <Header />
        </div>
        <div>
          <SearchBar 
            departments={departments} 
            setIsLoading={setIsLoading}
            fetchQuery={queryRef}
          />
        </div>
        {/* <LoadingIcon 
          isLoading={isLoading} 
        /> */}
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