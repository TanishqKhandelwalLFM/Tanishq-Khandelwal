import React from 'react'

const Card = ({title,body}) => {
  return (
    <div className='w-50 h-80 border-2 border-white bg-zinc-600 px-4 py-10 overflow-hidden'>
          <h1 className='font-bold text-white '>{title}</h1>
          <p>{body}</p>
        </div>
    
  )
}

export default Card
