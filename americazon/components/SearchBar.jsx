import { useState, useCallback } from 'react';
import { useMutation } from 'react-query';

import DropDown from 'components/DropDown';

import fetchSearch from 'utils/fetchSearch';

function SearchBar({ departments }) {

  const [searchString, setSearchString] = useState('')
  const [searched, setSearched] = useState(false)

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
    setSearched(true);
  }

  return (
    <>
      <div className="grid grid-cols-5 justify-center gap-4 p-6 mb-12 border-4 rounded-lg h-24 border-blue-100">
        
        <div className="col-start-1 col-auto">
          <DropDown className="h-full" items={departments} />
        </div>

        <div className="col-start-2 col-end-5 col-auto">
          <input type="search" placeholder='Search' onInput={(e) => setSearchString(e.target.value)} className="rounded-md border-2 w-full flex-auto transition-color duration-300 h-full text-2xl" />
        </div>

        <div className="col-start-5 col-auto">
          <button type="submit" onClick={handleSubmit} className="text-center rounded-md border-2 hover:text-red-600 hover:border-blue-300 
                                            transition-color duration-300 cursor-pointer w-full h-full flex-auto text-2xl">Search</button>
        </div>
      </div>

      {searched && (
        <>
          <h1 className='font-bold text-lg col-span-3'>
            { (searchItems?.data?.results) ? `Number of Results: ${ [ searchItems.data.results ]}` : '' }
          </h1>

          <div className='grid grid-cols-6 gap-2'>
            
            <div className='grid'>
              
            </div>

            <div className='grid grid-cols-4 col-span-5 gap-4 col-auto'>
              {searchItems?.data?.data?.map(item => (
                <div key={item.asin} className="pb-4 pt-4 col-auto border-2 border-slate-500 rounded-lg">
                  <img className='object-cover h-48' src={item.picturereflink} ></img>
                  <h1 className='font-bold text-lg'>{item.productname}</h1>

                  <p className='text-lg col-start-1 col-auto'>{`Country of Origin: ${item.countryoforigin}`}</p>
                  <p className='text-lg col-start-1 col-auto'>{`$${item.price}`}</p>
                  
                  <button onClick={() => handlePageRedirect(item.affiliatelink || item.productpagelink || '')} className='border-4 rounded-lg duration-150 hover:text-red-400 hover:border-blue-400' >Product Page</button>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

    </>
  )
}

export default SearchBar;