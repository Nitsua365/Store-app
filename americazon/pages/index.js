import React from 'react';

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

  return {
    props : {
      departments : []
    },
  }
}
