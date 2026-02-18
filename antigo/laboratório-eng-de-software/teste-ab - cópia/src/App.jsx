import { Routes, Route } from 'react-router-dom';

import Layout from './components/Layout';
import FeedBackPage from './pages/FeedbackPage';
import HomePage from './pages/HomePage';
import QRCodeExamplesPage from './pages/QRCodeExamplesPage';
import QRCodeReaderPage from './pages/QRCodeReaderPage';
import StudentListPage from './pages/StudentListPage';

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/qr-code-exemples" element={<QRCodeExamplesPage />} />
        <Route path="/qr-code-reader" element={<QRCodeReaderPage />} />
        <Route path="/lista-alunos" element={<StudentListPage />} />
        <Route path="/feedback" element={<FeedBackPage />} />
      </Route>
    </Routes>
  );
}

export default App;
