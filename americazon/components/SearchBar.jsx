import DropDown from './DropDown';
import React from 'react'
import axios from 'axios'

function SearchBar({ departments }) {
  return (
    <>
      <DropDown items={departments} />
      <div className='Main-SearchBar'>
        <input></input>
      </div>
    </>
  )
}

export default SearchBar;