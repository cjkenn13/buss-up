import { useState } from "react"; //brings in usestate, how react remembers information

function App() {
  const [stopID, setStopID] = useState('') //create memory called stopid starts as empty string
  //and will hold whatever stop number the user types, also has setter next o it
  const [arrivals, setArrivals] = useState([])//same thin gbut list of bus arrivals, starts as array
  const [loading, setLoading] = useState(false);//tracks whetherw we're waitin gfor api to responsd
  const [error, setError] = useState('')//error messages

  const searchArrivals = async () => {//create function, async wait for api calls
    if(!stopID) return//if input box empty, do nothing
    setLoading(true);//set lolading true to show loading on screen
    setError("")//clears errors
    setArrivals([])//clears arrivals

    try{
      //call fast api backend. fetch is JS way to make http request, await means finish before moving on
      const response = await fetch(`http://localhost:8000/arrivals/${stopID}`)
      const data = await response.json();//convert response to jason
      //saves arrivals array into our state
      setArrivals(data.arrivals)
    } catch(err){//if anything goes wrong use catch block
      setError('Count not get arrivals. Is the backend running?')
    } finally {
      setLoading(false);
  }
}

  return (
      <div>
        {/* app title */}
        <h1>Buss Up 🚌</h1>

        {/* text box where user types the stop number */}
        <input
            type="text"
            placeholder="Enter stop number..."
            value={stopID}
            onChange={(e) => setStopID(e.target.value)}
        />

        {/* button that triggers the search */}
        <button onClick={searchArrivals}>Search</button>

        {/* loading message*/}
        {loading && <p>Loading...</p>}

        {/*error*/}
        {error && <p>{error}</p>}

        {/*loop through arrivals and show eacl*/}
        {arrivals.map((arrival) => (
            <div key={arrival.id}>
              <p>Route {arrival.route} - {arrival.headsign}</p>
              <p>Arrives: {arrival.stopTime}</p>
            </div>
        ))}
      </div>
  )
}

export default App;//makes this usable by other files