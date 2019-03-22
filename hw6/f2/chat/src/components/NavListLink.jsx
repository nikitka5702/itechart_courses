import React from 'react'
import { NavLink } from 'react-router-dom'
import PropTypes from 'prop-types'

 function NavListLink(props) {
    const {to, current, cls, activeCls, liCls, text} = props;
    return (
        <li className={`${liCls || ""} nav-item ${current === to ? "active": ""}`}>
            <NavLink className={cls} activeClassName={activeCls || ""} to={to}>{text}</NavLink>
        </li>
    )
}

//Prop Types
NavListLink.propTypes = {
    to: PropTypes.string.isRequired,
    current: PropTypes.string.isRequired,
    cls: PropTypes.string.isRequired,
    activeCls: PropTypes.string,
    liCls: PropTypes.string,
    text: PropTypes.string.isRequired
};

export default NavListLink;
