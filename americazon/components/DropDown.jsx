import React from 'react'

function DropDown({ items }) {

  return (
    <div className="text-center">
      <select className="text-center" name="Departments">
        {items.map((element, i) => { return <option key={i}>{element}</option> })}
      </select>
    </div>
  )
}

export default DropDown;