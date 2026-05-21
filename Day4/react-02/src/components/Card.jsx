import React from 'react'

const Card = ({res,url,name,download}) => {
  return (
        <div className='w-80 h-80 border-2 border-white rounded-xl overflow-hidden relative'>
            <a target='_blank' href={download}>
                <img className='w-full h-full' src={url} alt="" />
            </a>
            <p className='absolute bottom-4 left-4 text-white text-xl font-bold'>{name}</p>
            <button className='text-white rounded-xl px-3 py-1.5 absolute top-2 right-2 bg-blue-400'>Add</button>
        </div>
  )
}

export default Card
