import React, { useRef } from 'react';

import { useMutation } from 'react-query';

import fetchSearch from 'utils/fetchSearch';

import SearchBar from "components/SearchBar";
import LoadingIcon from 'components/LoadingIcon';
import SearchResults from 'components/SearchResults';
import Header from 'components/Header';

export default function HomePage({ departments }) {
  const queryRef = useRef();
 
  const { mutate, data : searchItems, isLoading } = useMutation(fetchSearch, { 
    mutationKey: "search",
    enabled: false
  })

  return (
    <>
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
    </>
  )
}
