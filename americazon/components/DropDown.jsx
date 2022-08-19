import React, { useState } from 'react'
import LoadingIcon from './LoadingIcon';

function DropDown({ items, isLoading }) {

  const [value, setValue] = useState('');

  const selectDropdownHandler = (e) => {
    setValue(e.target.value);
  }

  return (
    <>
      <label>
          <>
            {(isLoading) ? 
              <LoadingIcon isLoading={isLoading} />
            : 
            <select value={value} onChange={selectDropdownHandler} className="text-center rounded-md border-2 hover:text-red-600 hover:border-blue-300 transition-color duration-300 cursor-pointer w-full h-full text-2xl"> 
              {items?.map((option) => (
                <option key={`drop_${option}`} value={option}>{option}</option>
              ))}
            </select>}
          </>
        
      </label>
    </>
  )

}

export default DropDown;