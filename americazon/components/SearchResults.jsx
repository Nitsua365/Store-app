import { useCallback, useEffect } from 'react';

import Image from 'next/image';
import Pagination from './Pagination';
import { useHomeContext } from 'context/HomeContext';

export default function SearchResults({ data, isLoading }) {
  
  const { setStateVar } = useHomeContext()

  const handlePageRedirect = (url) => {
    const newURL = (new URL(url))
    
    newURL.searchParams.set('tag', 'amerizon02-20')
    newURL.searchParams.set('linkCode', 'll1')

    console.log(newURL.toString())
    
    window.open(newURL.toString());
  }

  useEffect(() => {
    if (data && !isLoading) {
      setStateVar('totalPages', data.queryResults?.nbPages)
    }
  }, [data, isLoading])
  
  return (
    !isLoading && (
      <>
        <div>
          {data && (
            <h1 className='font-bold text-lg'>
              { (data?.results && data?.results !== 0) ? `Number of Results: ${ [ data?.results ]}` : 'Sorry no products found' }
            </h1>
          )}

          <div className='grid grid-cols-4 gap-4'>
            {data?.queryResults?.hits?.map(item => (

              <div /* onClick={() => handlePageRedirect(item.affiliatelink || item.productpagelink || '')} */
                   key={`${item.productname}_${item.asin}`} 
                   className="pb-4 pt-4 col-auto border-2 border-slate-500 rounded-lg transition-all duration-150 hover:border-blue-400 hover:shadow-2xl">

                <Image width={200} height={200} className="w-48 h-48" src={item.picturereflink} alt="Not Found" />
                <h1 className='font-bold text-lg'>{item.productname.length < 75 ? item.productname : `${item.productname.substring(0, 75)}...`}</h1>

                <p className='text-lg col-start-1 col-auto pt-2 pb-2'>{`Country of Origin: ${item.countryoforigin}`}</p>
                {/* <p className='text-lg col-start-1 col-auto'>{`$${parseFloat(item.price).toFixed(2)}`}</p> */}
                
                <button onClick={() => handlePageRedirect(item.affiliatelink || item.productpagelink || '')} 
                        className='border-4 rounded-lg text-center pt-4 pb-4 w-full duration-150 hover:text-red-400 hover:border-blue-400' >
                        Product Page
                </button>
              </div>
            ))}
          </div>
        </div>

        {data?.results && data?.results !== 0 && (
          <div key={`paginate_${data?.queryResults?.page}_${data?.results}`}>
            <Pagination 
              totalResults={data?.results} 
            />
          </div>
        )}
      </>
    ) 
  )
}