import React from "react";
import {BrowserRouter} from "react-router-dom";
import {Route, Routes} from "react-router";
import Navbar from "./components/Navbar";
import Landing from "./pages/Landing";

function App() {
    return (
        <BrowserRouter>
            <Navbar/>
            <Routes>
                <Route path="/" element={<Landing/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
