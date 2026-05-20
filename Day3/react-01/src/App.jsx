import React from 'react'
import Header from './components/Header'
import Card from './components/Card'

const App = () => {
  const data = [
    {
      name : 'Sanjeev',
      role : 'Manager'
    },
    {
      name : 'chavvi gupta',
      role : "HR"
    },
    {
      name : 'palak gupta',
      role : 'HR'
    },
    {
      name : 'Tanishq Khandelwal',
      role : 'AI Engineer'
    },
    {
      name : 'sanjay kumawat',
      role : 'AI Engineer'
    },
    {
      name : 'Sudhanshu Agrawal',
      role : 'AI Engineer'
    },
    {
      name : 'Khushi Gehlot',
      role : 'AI Engineer'
    },
    {
      name : 'Daksh Dashora',
      role : 'AI Engineer'
    },
    {
      name : 'Tanmay Khatri',
      role : 'AI Engineer'
    },
    {
      name : 'rishu sharma',
      role : 'AI Engineer'
    },
    {
      name : 'kritika Dadech',
      role : 'AI Engineer'
    }
  ]
  return (
    <div className='h-screen w-full bg-zinc-800'>
      <Header />


      <div className='scroller w-full h-87/100  px-10 py-5 flex gap-10 flex-wrap overflow-auto'>
          {data.map((elem,idx)=>{
            return (
              <div key={idx}>
                <Card name={elem.name} role = {elem.role} />
              </div>
            )
          })}
      </div>
      

      
    </div>
  )
}

export default App
