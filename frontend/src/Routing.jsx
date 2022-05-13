import React, {useContext} from "react";
import {AuthContext} from "./AuthProvider";
import {Navigate, Route, Routes} from "react-router-dom";
import Landing from "./pages/Landing";
import ScenarioOverview from "./pages/ScenarioOverview";
import SimulationAlternative from "./pages/SimulationAlternative";
import UserOverview from "./pages/UserOverview";
import Simulation from "./pages/Simulation";
import Login from "./pages/Login";
import Help from "./pages/Help";
import GDPR from "./pages/GDPR";
import Imprint from "./pages/Imprint";

const Routing = () => {
    const {currentUser} = useContext(AuthContext)

    if (currentUser) {
        return (
            <Routes>
                <Route path="/" element={<Landing/>}/>
                <Route path="/scenarios" element={<ScenarioOverview/>}/>
                <Route path="/scenarios/:scn_id" element={<SimulationAlternative/>}/>
                <Route path="/users" element={<UserOverview/>}/>
                <Route path="/simulation" element={<Simulation/>}/>
                <Route path="/help" element={<Help/>}/>
                <Route path="/gdpr" element={<GDPR/>}/>
                <Route path="/imprint" element={<Imprint/>}/>
                <Route path="/login" element={<Navigate to="/" replace/>}/>
            </Routes>
        )
    } else {
        return (
            <Routes>
                <Route path="/login" element={<Login/>}/>
                <Route path="*" element={<Navigate to="/login" replace/>}/>
            </Routes>
        )
    }
};

export default Routing;