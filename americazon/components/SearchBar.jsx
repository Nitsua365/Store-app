import DropDown from './DropDown';
import React, { useEffect, useState } from 'react'
import axios from 'axios';

function SearchBar({ departments }) {

  const [searched, setSearched] = useState(false);
  const [items, setItems] = useState([]);
  const [searchString, setSearchString] = useState('');
  const [numResults, setNumResults] = useState(0);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSearched(true);
  }

  useEffect(() => {
    (async () => {
      if (searched) {
        const result = await axios.get('http://localhost:3000/api/products/searchProducts', { params : { searchString } })
        setItems(result.data.data);
        setNumResults(result.data.results);
        setSearched(false);
      }
    })();
  }, [searched])

  return (
    <>
      <div className="grid grid-cols-5 h-12">
        
        <div className="col-start-2 w-64 h-8">
          <DropDown items={departments} />
        </div>

        <div className="col-start-3 h-8">
          <input type="search" onInput={(e) => setSearchString(e.target.value)} className="rounded-md border-2 w-full flex-auto" />
        </div>

        <div className="col-start-4 h-8">
          <button type="submit" onClick={handleSubmit} className="text-center rounded-md border-2 hover:text-red-600 hover:border-blue-300 
                                            transition-color duration-300 cursor-pointer w-full flex-auto">Search</button>
        </div>
      </div>

      <h1 className='font-bold text-lg col-span-3'>
        { (numResults) ? `Number of Results: ${numResults}` : '' }
      </h1>

      <div>
        {items.map(item => {
            return (
              <div key={item.productname} className="pb-4 pt-4">
                <h1 className='font-bold text-lg'>{item.productname}</h1>
                <p className='text-lg'>{`Country of Origin: ${item.countryoforigin}`}</p>
              </div>
            )
          }
        )}
      </div>

    </>
  )
}

export default SearchBar;