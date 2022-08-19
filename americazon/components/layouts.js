import React, { useRef } from 'react'

import { useQuery } from 'react-query';

import Header from 'components/Header'
import SearchBar from 'components/SearchBar'
import fetchDepartment from 'utils/fetchDepartment';

export default function Layout({ children }) {
  const queryRef = useRef();

  const { data : departments, isLoading } = useQuery("departments", fetchDepartment, { cacheTime: Infinity })

  return (
    <>
      <div>
        <Header />
      </div>
      <div>
        <SearchBar 
          dropDownLoading={isLoading}
          departments={departments} 
          fetchQuery={queryRef}
        />
      </div>
      <main>{children}</main>
    </>
  )
}