import React from 'react'

const Card = ({name,role}) => {
  return (
    <div className='w-60 h-70 rounded-xl border-zinc-700 bg-zinc-400 border-2 px-4 py-6 hover:scale-110'>
              <div className='w-24 h-24 rounded-full overflow-hidden'>
                <img className='w-full h-full object-cover' src="https://www.shutterstock.com/image-illustration/default-avatar-profile-icon-social-260nw-2221359783.jpg" alt="" />
              </div>
              <h1 className='text-xl font-medium text-black mt-4'>{name}</h1>
              <h1 className='text-lg font-semibold text-zinc-800 mt-1'>{role}</h1>
              <div className='flex items-center justify-center py-2'>
                <button className='text-white bg-blue-400 px-4 py-2 text-md font-semibold rounded-lg cursor-pointer hover:scale-95'>View Profile</button>
              </div>
          </div>
  )
}

export default Card
