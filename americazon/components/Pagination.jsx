import { useHomeContext } from 'context/HomeContext';

import { useRouter } from 'next/router';
import { useEffect } from 'react';

export default function Pagination({ totalResults }) {

    const { 
      currentPage, 
      pageSize, 
      totalPages,
      setStateVar 
    } = useHomeContext()

    const router = useRouter()

    return (totalPages > 1 && (
      <div className="flex items-center mb-3">
        <span className="text-sm m-3 text-gray-700 dark:text-gray-400">
          Showing <span className="font-semibold text-gray-900 dark:text-gray">{(currentPage * pageSize) + 1}</span> to <span className="font-semibold text-gray-900 dark:text-gray">{(((currentPage * pageSize) + pageSize) < totalResults) ? (currentPage * pageSize) + pageSize : totalResults}</span> of <span className="font-semibold text-gray-900 dark:text-gray">{totalResults}</span> Entries
        </span>
        <div className="inline-flex mt-2 xs:mt-0">
          <button onClick={() => { 
                if (currentPage > 0) {
                  const currPage = ((currentPage > 0) ? currentPage - 1 : 0)
                  setStateVar('currentPage', currPage)
                  router.replace({ pathname: '/search', query: { s : router.query.s, pg : currPage, ps: pageSize }})
                }
              }} className="inline-flex items-center py-2 px-4 text-sm font-medium text-red rounded transition-color duration-300 border-2 border-gray-400 dark:hover:border-blue-400 dark:hover:text-red-500">
              <svg aria-hidden="true" className="mr-2 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clipRule="evenodd"></path></svg>
              Prev
          </button>
          <button onClick={() => { 
                if (currentPage < (totalPages - 1)) {
                  const currPage = ((currentPage < (totalPages - 1)) ? currentPage + 1 : currentPage)
                  setStateVar('currentPage', currPage)
                  router.replace({ pathname: '/search', query: { s : router.query.s, pg : currPage, ps: pageSize }})
                }
              }} className="inline-flex items-center py-2 px-4 text-sm font-medium text-red rounded transition-color duration-300 border-2 border-gray-400 dark:hover:border-blue-400 dark:hover:text-red-500">
              Next
              <svg aria-hidden="true" className="ml-2 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd"></path></svg>
          </button>
        </div>
      </div>
    ))
}