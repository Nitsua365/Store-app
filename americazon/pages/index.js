import redis from 'lib/redisClient'
import React, { useRef } from 'react';

import { useMutation } from 'react-query';

import fetchSearch from 'utils/fetchSearch';

import SearchBar from "components/SearchBar";
import LoadingIcon from 'components/LoadingIcon';
import SearchResults from 'components/SearchResults';
import Header from 'components/Header';

import { HomeContext } from 'context/HomeContext';

export default function Home({ departments }) {
  const queryRef = useRef();
 
  const { mutate, data : searchItems, isLoading } = useMutation(fetchSearch, { 
    mutationKey: "search",
    enabled: false
  })

  return (
    <>
      <HomeContext>
        <div>
          <Header />
        </div>
        <div>
          <SearchBar 
            departments={departments} 
            fetch={mutate}
            fetchQuery={queryRef}
          />
        </div>
        <LoadingIcon 
          isLoading={isLoading} 
        />
        <SearchResults 
          isLoading={isLoading} 
          data={searchItems}
        />
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