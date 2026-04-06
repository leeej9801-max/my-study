const Nav = () => {
  return (
    <nav className="navbar navbar-expand-sm bg-dark navbar-dark">
      <div className="container-fluid">
        <a className="navbar-brand" href="/">HOME</a>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="collapsibleNavbar">
          <ul className="navbar-nav">
            <li className="nav-item">
              <a className="nav-link" href="/new">Create</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/detail">Detail</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/404">404</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  )
}

export default Nav