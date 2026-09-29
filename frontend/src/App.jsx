import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { MainLayout } from './components/layout/MainLayout'
import { HomeSection } from './components/sections/Home'
import { AboutSection } from './components/sections/About'
import { ProjectsSection } from './components/sections/Projects'
import { BlogSection } from './components/sections/Blog'
import { ConfigProvider } from './config/ConfigProvider'
import { useEffect } from 'react';

const App = () => {
  useEffect(() => {
  const wakeBackend = async () => {
    try {
      await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/health`
      );
    } catch (error) {
      console.log('Backend wake-up request failed:', error);
    }
  };

  wakeBackend();
}, []);
  return (
    <ConfigProvider>
      <BrowserRouter>
        <MainLayout>
          <Routes>
            <Route path="/" element={<HomeSection />} />
            <Route path="/about-me" element={<AboutSection />} />
            {/* <Route path="/projects" element={<ProjectsSection />} />
            <Route path="/blog" element={<BlogSection />} />
            <Route path="/blog/:postId" element={<BlogSection />} /> */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </MainLayout>
      </BrowserRouter>
    </ConfigProvider>
  )
}

export default App