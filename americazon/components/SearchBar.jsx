import React, { useState, useCallback } from 'react';
import { useMutation } from 'react-query';

import Image from 'next/image';

import DropDown from 'components/DropDown';

import fetchSearch from 'utils/fetchSearch';

function SearchBar({ departments }) {

  const [searchString, setSearchString] = useState('')
  const [searched, setSearched] = useState(false)

  const handlePageRedirect = useCallback((url) => {
    window.open(url);
  }, [])

  const { mutateAsync, data : searchItems, isLoading } = useMutation(fetchSearch, { 
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

      {isLoading && (
        <div className='grid grid-cols-9 justify-center'>
          <div className='col-start-5'>
            <svg role="status" className="h-32 w-32 animate-spin mr-2 text-gray-100 dark:text-gray-100 dark:fill-gray-900" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
            </svg>
          </div>
        </div>
      )}
      
      {searched && !isLoading && (
        <>
          <h1 className='font-bold text-lg col-span-3'>
            { (searchItems?.results && searchItems?.results !== 0) ? `Number of Results: ${ [ searchItems?.results ]}` : 'Sorry no products found' }
          </h1>

          <div className='grid grid-cols-6 gap-2'>
            
            <div className='grid'>
              
            </div>

            <div className='grid grid-cols-4 col-span-5 gap-4 col-auto'>
              {searchItems?.data?.map(item => (
                <div key={item.asin} className="pb-4 pt-4 col-auto border-2 border-slate-500 rounded-lg">
                  <Image width={200} height={200} className="w-48 h-48" src={item.picturereflink} alt="Not Found" />
                  <h1 className='font-bold text-lg'>{item.productname}</h1>

                  <p className='text-lg col-start-1 col-auto'>{`Country of Origin: ${item.countryoforigin}`}</p>
                  <p className='text-lg col-start-1 col-auto'>{`$${parseFloat(item.price).toFixed(2)}`}</p>
                  
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