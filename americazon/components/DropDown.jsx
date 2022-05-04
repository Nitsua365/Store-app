import React from 'react'

function DropDown({ items }) {
  return (
    <>
      <select value={"Departments"}>
        {
          items.forEach(item => <option className="bg-slate-300" value={item.charAt(0).toLowerCase() + item.slice(1)}>item</option>)
        }
      </select>
    </>
  )
}

export default DropDown