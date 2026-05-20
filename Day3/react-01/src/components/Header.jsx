import React from 'react'

const Header = () => {
  return (
    <div className='h-20 w-full bg-zinc-700 flex justify-between items-center px-10 py-5'>
      <h1 className='text-white font-bold text-2xl'>PROFILE CARD</h1>
      <div className='flex items-center justify-between gap-4 text-gray-400 font-semibold'>
        <button className='border-2 px-4 py-1.5 text-white bg-red-400 border-red-500 rounded-xl'>Sign In</button>
      </div>
    </div>
  )
}

export default Header
