import React from 'react'
import InfoIconTooltip from 'components/InfoIconTooltip';

function Header() {
  return (
    <>
      <div className='flex flex-row items-center justify-center'>
        <h1 className='text-4xl text-center font-bold font-sans size mt-2'>americazon.shop</h1>
        <InfoIconTooltip iconSize="large">
          As an Amazon Associate I earn from qualifying purchases
        </InfoIconTooltip>
      </div>
      <h3 className='text-center text-lg font-light font-sans'>The search engine for made in the USA</h3>
    </>
  )
}

export default Header