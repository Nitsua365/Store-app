import { useCallback } from 'react';

import Image from 'next/image';


export default function SearchResults({ data, isLoading }) {

  const handlePageRedirect = useCallback((url) => {
    window.open(url);
  }, [])
  
  return (
    !isLoading && (
      <>
        {data && (
          <h1 className='font-bold text-lg col-span-3'>
            { (data?.results && data?.results !== 0) ? `Number of Results: ${ [ data?.results ]}` : 'Sorry no products found' }
          </h1>
        )}

        <div className='grid grid-cols-6 gap-2'>
          
          <div className='grid'>
            
          </div>

          <div className='grid grid-cols-4 col-span-5 gap-4'>
            {data?.queryResults?.hits?.map(item => (
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
    ) 
  )
}