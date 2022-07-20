import React, { useRef } from 'react';

import { useMutation } from 'react-query';

import fetchSearch from 'utils/fetchSearch';

import SearchBar from "components/SearchBar";
import LoadingIcon from 'components/loadingIcon';
import SearchResults from 'components/SearchResults';

export default function HomePage({ departments }) {

  const queryRef = useRef();

  const { mutateAsync, data : searchItems, isLoading } = useMutation(fetchSearch, { 
    mutationKey: "search",
    enabled: false
  })

  return (
    <>
      <div>
        <SearchBar 
          departments={departments} 
          fetch={mutateAsync}
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
