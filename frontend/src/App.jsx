import React, { useEffect } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Help from "./pages/Help";
import ScenarioOverview from "./pages/ScenarioOverview";
import SimulationAlternative from "./pages/SimulationAlternative";
import UserOverview from "./pages/UserOverview";
import { Box } from "@chakra-ui/react";
import Simulation from "./pages/Simulation";
import Footer from "./components/Footer";

function App() {

    useEffect(() => {
        document.body.style.backgroundColor = "#EDF2F7";
    }, []);

    return (
        <Box h="full">
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Landing />} />
                    <Route path="/scenarios" element={<ScenarioOverview />} />
                    <Route path="/scenarios/:scn_id" element={<SimulationAlternative />} />
                    <Route path="/users" element={<UserOverview />} />
                    <Route path="/simulation" element={<Simulation />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/help" element={<Help />} />
                </Routes>
                <Footer />
            </BrowserRouter>
        </Box>
    );
}

export default App;
