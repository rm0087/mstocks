import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
    return (
        <nav className="navbar">
            <ul className="navbar-nav">
                <li className="nav-item"><Link to="/financials" className="nav-link">Financials</Link></li>
                <li className="nav-item"><Link to="/keywords" className="nav-link">Keywords</Link></li>
                {/* <li className="nav-item"><Link to="/comments" className="nav-link">Notes</Link></li> */}
                <li className="nav-item"><Link to="/map" className="nav-link">Map</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;