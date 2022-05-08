import React, {useState} from 'react'

function DropDown({ items }) {

  const [isDropped, setisDropped] = useState(false);

  const dropDown = (e) => {
    e.preventDefault();
    setisDropped(!isDropped);
  }

  return (
    <>
      <select onClick={dropDown} className="text-center rounded-md border-2 hover:text-red-600 hover:border-blue-300 
                                            transition-color duration-300 cursor-pointer w-full flex-auto"> 
        {/* <h1 className="font-light"> */}
          Departments ↓
        {/* </h1> */}
      </select>
    </>
  )

}

export default DropDown;