import { useState, useCallback } from 'react';
import { useMutation } from 'react-query';

import DropDown from 'components/DropDown';

import fetchSearch from 'utils/fetchSearch';

function SearchBar({ departments }) {

  const [searchString, setSearchString] = useState('')

  const handlePageRedirect = useCallback((url) => {
    window.open(url);
  }, [])

  const { mutateAsync, data : searchItems } = useMutation(fetchSearch, { 
    mutationKey: "search",
    enabled: false
  })

  const handleSubmit = async (e) => {
    e.preventDefault();
    await mutateAsync({ searchString })
  }

  return (
    <>
      <div className="grid grid-cols-5 justify-center gap-4 p-6 mb-12 border-4 rounded-lg">
        
        <div className="col-start-2 col-auto">
          <DropDown items={departments} />
        </div>

        <div className="col-start-3 col-auto">
          <input type="search" onInput={(e) => setSearchString(e.target.value)} className="rounded-md border-2 w-full flex-auto transition-color duration-300" />
        </div>

        <div className="col-start-4 col-auto">
          <button type="submit" onClick={handleSubmit} className="text-center rounded-md border-2 hover:text-red-600 hover:border-blue-300 
                                            transition-color duration-300 cursor-pointer w-full flex-auto">Search</button>
        </div>
      </div>

      <h1 className='font-bold text-lg col-span-3'>
        { (searchItems?.data?.results) ? `Number of Results: ${ [ searchItems.data.results ]}` : '' }
      </h1>

      <div>
        {searchItems?.data?.data?.map(item => (
            <div key={item.productname} className="pb-4 pt-4">
              <img className='object-cover h-48' src={item.picturereflink} ></img>
              <h1 className='font-bold text-lg'>{item.productname}</h1>
              <p className='text-lg'>{`Country of Origin: ${item.countryoforigin}`}</p>
              <button onClick={(e) => handlePageRedirect(item.affiliatelink || item.productpagelink || '')} className='border-4 rounded-lg duration-150 hover:border-slate-800' >Product Page</button>
            </div>
          )
        )}
      </div>

    </>
  )
}

export default SearchBar;