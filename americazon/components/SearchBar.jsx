import DropDown from './DropDown';
import React from 'react'

function SearchBar({ departments }) {
  return (
    <>
      <div className="grid grid-cols-5">
        <div className="col-start-2 w-64">
          <DropDown items={departments} />
        </div>
        <div className="shrink col-start-3">
          <input type="search" className="rounded-md border-2 w-full flex-auto" />
        </div>
        <div className="col-start-4">
          <button className="text-center rounded-md border-2 hover:text-red-600 hover:border-blue-300 
                                            transition-color duration-300 cursor-pointer w-full flex-auto">Search</button>
        </div>
        
      </div>
    </>
  )
}

export default SearchBar;