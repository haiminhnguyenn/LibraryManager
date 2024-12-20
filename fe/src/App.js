import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginRegister from './pages/auth/login_register';
import HomePage from './pages/home_page/home_page';
import Manage from './pages/home_page/home_page_component/manage/manage';
import User from './pages/home_page/home_page_component/user/user';
import Search from './pages/home_page/home_page_component/search/search';
import Contact from './pages/home_page/home_page_component/contact/contact';
import Home from './pages/home_page/home_page_component/home/home';
import Profile from './pages/home_page/home_page_component/profile/profile';

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<HomePage/>}>
          <Route path="/home" element={<Home />} />
          <Route path="/manage" element={<Manage />} />
          <Route path="/user" element={<User />} />
          <Route path="/search" element={<Search/>} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/profile" element={<Profile />} />
        </Route>

        <Route path="/login" element={<LoginRegister />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
