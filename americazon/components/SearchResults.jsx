import { useEffect } from 'react';

import Pagination from './Pagination';
import { useHomeContext } from 'context/HomeContext';
import InfoIconTooltip from './InfoIconTooltip';

export default function SearchResults({ data, isLoading }) {
  
  const { setStateVar } = useHomeContext()

  const handlePageRedirect = (url) => {
    const newURL = (new URL(url))
    
    newURL.searchParams.set('tag', 'amerizon02-20')
    newURL.searchParams.set('linkCode', 'll1')
    
    window.open(newURL.toString())
  }

  useEffect(() => {
    if (data && !isLoading) {
      setStateVar('totalPages', Math.ceil(data?.results / data.queryResults.limit))
    }
  }, [data, isLoading])
  
  return (
    !isLoading && (
      <>
        <div>
          {data && (
            <h1 className='font-bold text-lg mb-4'>
              { (data?.results && data?.results !== 0) ? `Number of Results: ${ [ data?.results ]}` : 'Sorry no products found' }
            </h1>
          )}

          <div className='grid grid-cols-4 gap-4'>
            {data?.queryResults?.hits?.map(item => (

              <div /* onClick={() => handlePageRedirect(item.affiliatelink || item.productpagelink || '')} */
                   key={`${item.productname}_${item.asin}`} 
                   className="container pb-4 pt-4 border-2 border-slate-500 rounded-lg transition-all duration-150 hover:border-blue-400 hover:shadow-2xl">

                <div className='ml-28 mr-28 max-w-100 max-h-100 justify-center'>
                  <img className="justify-center max-w-200 max-h-auto" src={item.picturereflink} alt="Not Found" width="200" height="200" />
                </div>

                <h1 className='font-bold text-lg mt-2'>{item.productname.length < 75 ? item.productname : `${item.productname.substring(0, 75)}...`}</h1>

                <p className='text-lg mt-2 mb-2'>{`Country of Origin: ${item.countryoforigin}`}</p>
                {/* <p className='text-lg col-start-1 col-auto'>{`$${parseFloat(item.price).toFixed(2)}`}</p> */}
                
                <span className='align-bottom'>
                  <button onClick={() => handlePageRedirect(item.affiliatelink || item.productpagelink || '')} 
                          className='border-4 rounded-lg align-bottom text-center pt-4 pb-4 w-full duration-150 hover:text-red-600 hover:border-blue-400' >
                    <div className='flex flex-row text-center'>
                      <div className='flex-auto justify-center ml-8'>
                        Product Page
                      </div>
                      <div className='flex justify-end mr-1'>
                        <InfoIconTooltip>
                          We earn a small commission off of qualifying Amazon.com affiliate sales
                        </InfoIconTooltip>
                      </div>
                    </div>
                  </button>
                </span>
                
              </div>
            ))}
          </div>
        </div>

        <div className='mt-2'>
          {data?.results && data?.results !== 0 && (
            <>
              <div key={`paginate_${data?.queryResults?.page}_${data?.results}`}>
                <Pagination totalResults={data?.results} />
              </div>
            </>
          )}
          {data?.results && (<div className='mt-6 mb-3 text-center border-t-2 border-slate-400'>
            <div className='mt-2 mb-1'>
              We are a participant in the <strong>Amazon Services LLC Associates Program</strong>,<br />
              an affiliate advertising program designed to provide a means for us<br />
              to earn fees by linking to Amazon.com and affiliated sites
            </div>
          </div>)}
        </div>

        
      </>
    ) 
  )
}