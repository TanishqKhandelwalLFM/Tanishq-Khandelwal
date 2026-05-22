import axios from 'axios';
import React, { useEffect, useState } from 'react'
import Header from './components/Header';
import Card from './components/Card';

const App = () => {
  const [data, setData] = useState([]);

  useEffect(()=>{
    const fetchData = async () =>{
      const res = await axios.get("http://127.0.0.1:8000/posts")

      setData(res.data.data)


      
    }
    fetchData()
  },[])
  return (
    <div className='h-screen w-full bg-zinc-800'>
      <Header />

      <div className='flex flex-wrap gap-10 w-full h-87/100 p-10'>
        {data.map((elem,idx)=>{
        return (
          <Card key={idx} title={elem.title} body={elem.body}/>
        )
      })}
      </div>

      
    </div>
  )
}

export default App
