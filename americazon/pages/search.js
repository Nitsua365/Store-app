import React from 'react'

import SearchResults from 'components/SearchResults';

import { productIndex } from "lib/meiliClient";

import { HomeContext } from 'context/HomeContext';


export default function Search({ data }) {

  console.log(data)

  return (
    <>
      <HomeContext>
        <SearchResults 
          isLoading={false} 
          data={data}
        />
      </HomeContext>
    </>
  )
}

export async function getServerSideProps(context) {

  const { s, pg, ps } = context.query

  const queryResults = await productIndex.search(s, {
    filter: ['countryoforigin = USA'],
    offset: parseInt(ps) * parseInt(pg),
    limit: parseInt(ps)
  })

  return {
    props: {
      data: { queryResults, results: queryResults.estimatedTotalHits }
    }
  }
}