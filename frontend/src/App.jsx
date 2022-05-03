import React, {useEffect} from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Navbar from "./components/Navbar";
import Landing from "./pages/Landing";
import ScenarioOverview from "./pages/ScenarioOverview";
import Simulation from "./pages/Simulation";

function App() {

    useEffect(() => {
        document.body.style.backgroundColor = "#EDF2F7";
    }, []);

    return (
        <>
        <BrowserRouter>
            <Navbar/>
            <Routes>
                <Route path="/" element={<Landing/>}/>
                <Route path="/scenarios" element={<ScenarioOverview/>}/>
                <Route path="/scenarios/:scn_id" element={<Simulation/>}/>
            </Routes>
        </BrowserRouter>
        </>
    );
}

export default App;
