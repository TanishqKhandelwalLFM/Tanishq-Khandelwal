import React from 'react'

const Header = () => {
  return (
        <div className='flex justify-between items-center px-8 py-8 border-white border-b-2'>
            <p className='text-white text-2xl font-bold'>Gallery Search</p>
            <button className='text-white text-lg px-4 py-2 rounded-xl bg-red-500 font-bold'>Sign In</button>
        </div>
  )
}

export default Header
