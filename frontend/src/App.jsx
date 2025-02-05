import { useState } from 'react'
import liveKitModal from './components/liveKitModal'
import './App.css'

function App() {

  const [showSupport, setShowSupport] = useState(false);
  const handleSupportClick = () =>{
    setShowSupport(true)
  }
  

  return (
   <div className='app'>
    <header className='header'>
      <div className='logo'>AutoZone</div>

    </header>
    <main>
      <section className='hero'>
        <h1>Get the Right Parts. Right Now</h1>
        <p>Free Next Day Delivery on Eligible Orders</p>
        <div className='seach-bar'>
          <input type="text" placeholder='Enter Vehicle part number'/>
          <button>Search</button>
        </div>
      </section>
      <button className='support-button'onClick={handleSupportClick}></button>
    </main>
    {showSupport && <liveKitModal setShowSupport={handleSupportClick}/>}
   </div>
    
 
  )
}

export default App
