import axios from 'axios';
import React, { useState } from 'react'
import Card from './Card';

const Form = ({query,setQuery,result,setResult}) => {
    
    const UNSPLASH_KEY = import.meta.env.VITE_UNSPLASH_KEY
    const submithandler = async (e) => {
    e.preventDefault();

    if(query === '')
        return 

    const res = await axios.get(
        'https://api.unsplash.com/search/photos',
        {
            params: {
                query,
                per_page: 20,
                page : 1
            },
            headers: {
                Authorization: `Client-ID ${UNSPLASH_KEY}`
            }
        }
    )

    setResult(res.data.results);
    

    setQuery('');
}
  return (
    <div className='h-8/10'>
      <form onSubmit={(e)=>{
        submithandler(e)
      }} className='flex justify-center items-center gap-6 py-8' action="">
        <input value={query} onChange={(e)=>{
            setQuery(e.target.value)
        }} className='border-2 border-white text-white px-8 py-2 outline-none cursor-pointer text-lg rounded-xl' placeholder='Search any image' type="text" />
        <button className='text-white bg-red-500 px-4 py-2 text-lg  rounded-xl hover:scale-95'>
          Search
        </button>
      </form>

      {
        result && result.length > 0 ? ( <div className=' scroller flex flex-wrap px-8 py-4 gap-6 h-9/10 overflow-auto'>
        {
            result?.map((res,idx)=>{
                return (
                    <Card  key={idx} res={res} url={res.urls.full} name={res.user.name} download = {res.links.download} />
                )
            })
        }
      </div>
        )
        :
        <p className='text-white font-bold text-xl ml-10'>Searh Anything ...</p>
      }
    </div>
  )
}

export default Form
