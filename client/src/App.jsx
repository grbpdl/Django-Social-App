import React from 'react'
import { Route, Routes } from 'react-router-dom'
import Register from './pages/Register'
import Home from './pages/Home'
import Login from './pages/Login'
import Profile from './pages/Profile'
import Profile2 from './pages/Profile2'

export default function App() {
  return (
    <Routes>
      <Route path='/register' element={<Register />} />
      <Route path='/' element={<Home />} />
      <Route path='/login' element={<Login />} />
      <Route path='/Profile' element={<Profile />} />
    </Routes>
  )
}
