import React, { useState } from 'react'
import Form from './components/Form'
import Header from './components/Header'

const App = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState([]);
  return (
    <div className='h-screen w-full bg-zinc-900'>
      <Header />
      <Form query={query} setQuery = {setQuery} result={result} setResult = {setResult}  />
    </div>
  )
}

export default App
