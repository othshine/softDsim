import React, { useEffect } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Help from "./pages/Help";
import ScenarioOverview from "./pages/ScenarioOverview";
import SimulationAlternative from "./pages/SimulationAlternative";
import UserOverview from "./pages/UserOverview";
import { Flex } from "@chakra-ui/react";
import Simulation from "./pages/Simulation";
import Footer from "./components/Footer";
import GDPR from "./pages/GDPR";
import Imprint from "./pages/Imprint";

function App() {

    useEffect(() => {
        document.body.style.backgroundColor = "#EDF2F7";
    }, []);

    return (
        <Flex h="full" flexDir="column">
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
                    <Route path="/gdpr" element={<GDPR />} />
                    <Route path="/imprint" element={<Imprint />} />
                </Routes>
                <Footer />
            </BrowserRouter>
        </Flex>
    );
}

export default App;
