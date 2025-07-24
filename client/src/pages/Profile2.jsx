import React from 'react'
import image from '../assets/Screenshot 2025-07-14 220659.png';

function Profile2() {
  return (
    <div className='bg-gradient-to-br from-green-300  to-green-400 min-h-screen flex justify-center items-center'>
        <div className='bg-slate-200 w-[80%] max-w-[600px] h-[600px] flex justify-center items-center rounded-xl shadow-2xl'>
          <div className='flex justifey-center items-center flex-col gap-4'>
            <h1 className='text-2xl font-semibold'>Your Profile</h1>
            <div className='bg-green-300 w-[150px] h-[150px] rounded-full'>
              <img src={image} alt="" className="rounded-full object-cover w-full h-full" />
            </div>
          </div>
        </div>
    </div>
  )
}

export default Profile2
