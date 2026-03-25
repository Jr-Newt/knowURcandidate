import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import CandidateList from './pages/CandidateList';
import CandidateDetail from './pages/CandidateDetail';
import ComparisonView from './pages/ComparisonView';
import RankingPanel from './pages/RankingPanel';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-neutral-50">
        {/* Navigation */}
        <nav className="bg-white border-b border-neutral-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-14">
              <a href="/" className="flex items-center gap-2 text-neutral-900 hover:text-accent-600 transition-colors">
                <svg className="w-6 h-6 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="font-semibold text-sm sm:text-base">Know Your Candidate</span>
              </a>
              <div className="flex items-center gap-1 sm:gap-4 text-xs sm:text-sm">
                <a href="/" className="px-2 py-1 sm:px-3 sm:py-2 rounded-lg text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 transition-all">
                  Home
                </a>
                <a href="/candidates" className="px-2 py-1 sm:px-3 sm:py-2 rounded-lg text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 transition-all">
                  Candidates
                </a>
                <a href="/compare" className="px-2 py-1 sm:px-3 sm:py-2 rounded-lg text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 transition-all">
                  Compare
                </a>
                <a href="/rank" className="px-2 py-1 sm:px-3 sm:py-2 rounded-lg bg-accent-600 text-white hover:bg-accent-700 transition-all">
                  Rank
                </a>
              </div>
            </div>
          </div>
        </nav>

        {/* Routes */}
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/candidates" element={<CandidateList />} />
            <Route path="/candidate/:id" element={<CandidateDetail />} />
            <Route path="/compare" element={<ComparisonView />} />
            <Route path="/rank" element={<RankingPanel />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-neutral-200 mt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center text-neutral-500 text-xs">
              <p className="mb-1">Know Your Candidate — Kerala Election Decision Support System</p>
              <p className="text-neutral-400">
                Data sourced from Election Commission affidavits. Rankings are based on user-selected preferences and do not represent any official position.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
