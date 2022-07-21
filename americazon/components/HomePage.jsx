import React, { useEffect, useRef } from 'react';

import { useMutation } from 'react-query';

import fetchSearch from 'utils/fetchSearch';

import SearchBar from "components/SearchBar";
import LoadingIcon from 'components/loadingIcon';
import SearchResults from 'components/SearchResults';
import { useHomeContext } from 'context/HomeContext';

export default function HomePage({ departments }) {
  const queryRef = useRef();
 
  const { mutate, data : searchItems, isLoading } = useMutation(fetchSearch, { 
    mutationKey: "search",
    enabled: false
  })

  return (
    <>
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
