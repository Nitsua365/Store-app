import React, { useEffect } from 'react';

import { useRouter } from 'next/router'

import DropDown from 'components/DropDown';
import { useHomeContext } from 'context/HomeContext';


function SearchBar({ departments, fetchQuery, dropDownLoading }) {

  const { pageSize, setStateVar } = useHomeContext();
  const router = useRouter();

  const handleSubmit = (e) => {
    e.preventDefault();

    if (fetchQuery.current) {
      setStateVar('currentPage', 0)
      setStateVar('searchQuery', fetchQuery.current)
      router.push({ pathname: '/search', query: { s: fetchQuery.current, pg: 0, ps: pageSize } })
    }
    
  }

  return (
    <>
      <div className="grid grid-cols-5 justify-center gap-4 p-6 mb-12 border-4 rounded-lg h-24 border-blue-100">
        
        <div className="col-start-1 col-auto">
          <DropDown className="h-full" items={departments} isLoading={dropDownLoading} />
        </div>

        <div className="col-start-2 col-end-5 col-auto">
          <input type="search" placeholder='Search' onInput={(e) => { 
            fetchQuery.current = e.target.value;
            setStateVar('searchQuery', e.target.value)
           }} className="rounded-md border-2 w-full flex-auto transition-color duration-300 h-full text-2xl" />
        </div>

        <div className="col-start-5 col-auto">
          <button type="submit" onKeyDown={e => e.key === "Enter" && handleSubmit(e)} onClick={handleSubmit} className="text-center rounded-md border-2 hover:text-red-600 hover:border-blue-300 
                                            transition-color duration-300 cursor-pointer w-full h-full flex-auto text-2xl">Search</button>
        </div>
      </div>
    </>
  )
}

export default SearchBar;