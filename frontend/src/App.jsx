import React, {useEffect} from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Navbar from "./components/Navbar";
import Landing from "./pages/Landing";
import ScenarioOverview from "./pages/ScenarioOverview";
import SimulationAlternative from "./pages/SimulationAlternative";
import UserOverview from "./pages/UserOverview";
import {Box} from "@chakra-ui/react";

function App() {

    useEffect(() => {
        document.body.style.backgroundColor = "#EDF2F7";
    }, []);

    return (
        <Box h="full">
        <BrowserRouter>
            <Navbar/>
            <Routes>
                <Route path="/" element={<Landing/>}/>
                <Route path="/scenarios" element={<ScenarioOverview/>}/>
                <Route path="/scenarios/:scn_id" element={<SimulationAlternative/>}/>
                <Route path="/users" element={<UserOverview/>}/>
            </Routes>
        </BrowserRouter>
        </Box>
    );
}

export default App;
